"""Guard integration boundaries: typoed app data must fail before export."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_data import ROOT,read,data_tree,validate_sources,validate_runtime,preset_args


class DataContractTests(unittest.TestCase):
    def setUp(self):
        self.sources=[read(p) for p in ['data/model.json','data/presets.json','speech/lines.vi.json','data/features.json']]

    def test_repository_sources_and_embedded_runtime_agree(self):
        counts=validate_sources(*self.sources)
        self.assertEqual(counts['properties'],3)
        validate_runtime(self.sources[0])

    def test_invalid_preset_and_unknown_trigger_fail(self):
        for change in [{'values':{'mood':'hapy'}},{'values':{'isAsleep':'false'}},{'values':{'wave':True}},{'triggers':['celebrate']}]:
            with self.subTest(change=change):
                model,presets,speech,features=deepcopy(self.sources)
                presets['presets'][0].update(change)
                with self.assertRaises(ValueError):validate_sources(model,presets,speech,features)

    def test_speech_and_feature_references_must_exist(self):
        model,presets,speech,features=deepcopy(self.sources)
        speech['categories']['greeting']['lines'][0]['text']='Chào {unknown}!'
        with self.assertRaisesRegex(ValueError,'placeholder'):validate_sources(model,presets,speech,features)
        model,presets,speech,features=deepcopy(self.sources)
        features['features'][0]['preset']='missing'
        with self.assertRaisesRegex(ValueError,'unknown preset'):validate_sources(model,presets,speech,features)

    def test_missing_default_machine_and_enum_order_drift_fail(self):
        root=ET.parse(ROOT/'runtime.rml').getroot()
        root.find('Artboard').attrib.pop('defaultStateMachineId')
        with self.assertRaisesRegex(ValueError,'defaultStateMachineId'):validate_runtime(self.sources[0],root)
        root=ET.parse(ROOT/'runtime.rml').getroot()
        enum=root.find('DataEnumCustom');a,b=list(enum)[:2];enum.remove(a);enum.insert(1,a)
        with self.assertRaisesRegex(ValueError,'Embedded data differs'):validate_runtime(self.sources[0],root)

    def test_wake_capture_preserves_pointer_sequence(self):
        wake=next(p for p in self.sources[1]['presets'] if p['id']=='wake')
        self.assertEqual(preset_args(wake,True)[-3:],['--advance=60','--pointer=click@250,350','--advance=12'])

    def test_expression_library_preserves_existing_integration(self):
        model=self.sources[0]
        values=model['enums'][0]['values']
        legacy=['neutral','happy','wink','focus','surprised','sleepy','confused']
        self.assertEqual([(v['key'],v['id']) for v in values[:7]],
                         [(key,f'0:{601+i}') for i,key in enumerate(legacy)])
        catalog=read('data/expressions.json')
        self.assertEqual([v['key'] for v in values[7:]], [s['key'] for s in catalog['expressions']])
        root=ET.parse(ROOT/'runtime.rml').getroot()
        animations={a.get('name'):a for a in root.iter('LinearAnimation')}
        presets={p['id']:p for p in self.sources[1]['presets']}
        for spec in catalog['expressions']:
            with self.subTest(scene=spec['key']):
                animation=animations['mood_'+spec['key']]
                self.assertEqual(int(animation.get('duration')),spec['frames'])
                self.assertEqual(animation.get('loopValue'),'loop')
                self.assertEqual(presets[spec['key']]['values']['mood'],spec['key'])
                self.assertEqual(presets[spec['key']]['values']['isAsleep'],False)

    def test_sleep_wave_and_legacy_moods_clear_new_props(self):
        root=ET.parse(ROOT/'runtime.rml').getroot()
        slots=[s for s in root.iter('Solo') if s.get('name','').startswith('Scene')]
        self.assertEqual(len(slots),3)
        animations={a.get('name'):a for a in root.iter('LinearAnimation')}
        for name in ['mood_'+s for s in ['neutral','happy','wink','focus','surprised','sleepy','confused']]+['sleep_loop','wake_startle','hello_wave']:
            for slot in slots:
                with self.subTest(animation=name,slot=slot.get('name')):
                    obj=animations[name].find(f"KeyedObject[@objectId='{slot.get('id')}']")
                    active=obj.find("KeyedProperty[@propertyKey='296']/KeyFrameId")
                    self.assertEqual(active.get('value'),slot.get('activeComponentId'))


if __name__=='__main__':unittest.main()
