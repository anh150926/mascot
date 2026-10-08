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


if __name__=='__main__':unittest.main()
