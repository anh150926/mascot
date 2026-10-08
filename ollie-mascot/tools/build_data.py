"""Build and validate Ollie's data, presets, speech and app-facing contract.

data/model.json is the source; data.rml is generated and embedded by build_ollie.
No Nez files are read by this pipeline.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
from kit_common import ROOT,BUILD


def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def require(ok,message):
    if not ok:raise ValueError(message)


def validate_model(model):
    require(model.get('schema_version')==1,'Unsupported data/model.json schema_version')
    ids=[model['artboard']['id'],model['state_machine']['id'],model['view_model']['id'],model['view_model']['instance']['id']]
    enum_names=[]
    enums={}
    for enum in model['enums']:
        enum_names.append(enum['name']);ids.append(enum['id'])
        keys=[item['key'] for item in enum['values']]
        require(keys and len(set(keys))==len(keys),'Duplicate/empty enum values: '+enum['name'])
        enums[enum['name']]=keys
        ids.extend(v['id'] for v in enum['values'])
    require(len(set(enum_names))==len(enum_names),'Duplicate enum names')
    names=[]
    for prop in model['properties']:
        names.append(prop['name']);ids.extend([prop['id'],prop['instance_value_id']])
        kind=prop['type'];require(kind in ('enum','boolean','trigger'),'Unsupported property type '+kind)
        if kind=='enum':require(prop.get('default') in enums.get(prop.get('enum'),[]),'Invalid enum default: '+prop['name'])
        if kind=='boolean':require(type(prop.get('default')) is bool,'Boolean default must be true/false: '+prop['name'])
        if kind=='trigger':require('default' not in prop,'Trigger must not have a persistent default: '+prop['name'])
    require(names and len(set(names))==len(names),'Duplicate/empty property names')
    require(all(re.fullmatch(r'\d+:\d+',i) for i in ids),'Malformed RML ID in data model')
    require(len(ids)==len(set(ids)),'Duplicate RML ID in data model')
    require(all(type(model['artboard'][k]) is int and model['artboard'][k]>0 for k in ('width','height')),'Invalid artboard dimensions')
    require(model['artboard']['fit']=='contain','Ollie requires fit=contain')
    return {p['name']:p for p in model['properties']},enums


def validate_values(values,props,enums,where):
    for name,value in values.items():
        require(name in props,f'{where}: unknown property {name}')
        prop=props[name]
        require(prop['type']!='trigger',f'{where}: triggers belong in triggers[], not values')
        if prop['type']=='enum':require(value in enums[prop['enum']],f'{where}: invalid {name}={value}')
        if prop['type']=='boolean':require(type(value) is bool,f'{where}: {name} must be a boolean')


def validate_sources(model,presets,speech,features):
    props,enums=validate_model(model)
    preset_ids=[]
    for preset in presets['presets']:
        pid=preset['id'];preset_ids.append(pid)
        require(re.fullmatch(r'[a-z][a-z0-9_-]*',pid),'Invalid preset ID '+pid)
        validate_values(preset.get('values',{}),props,enums,pid)
        for trigger in preset.get('triggers',[]):require(trigger in props and props[trigger]['type']=='trigger',pid+': unknown trigger '+trigger)
        require(preset.get('capture_steps'),pid+': missing capture steps')
        for step in preset['capture_steps']:
            require(len(step)==1 and next(iter(step)) in ('advance','click'),pid+': unsupported capture step')
            if 'advance' in step:require(type(step['advance']) is int and step['advance']>=0,pid+': advance must be non-negative frames')
            if 'click' in step:
                xy=step['click'];require(isinstance(xy,list) and len(xy)==2 and all(type(v) in (int,float) for v in xy),pid+': click needs x,y')
                require(0<=xy[0]<=model['artboard']['width'] and 0<=xy[1]<=model['artboard']['height'],pid+': click is outside artboard')
    require(len(preset_ids)==len(set(preset_ids)),'Duplicate preset IDs')
    for axis,dimension in [('artboardX','width'),('artboardY','height')]:
        require(0<=speech['anchor'][axis]<=model['artboard'][dimension],'Speech anchor outside artboard')
    line_ids=[]
    for category,record in speech['categories'].items():
        require(record['lines'],'Empty speech category '+category)
        for line in record['lines']:
            line_ids.append(line['id']);validate_values({'mood':line['mood']},props,enums,line['id'])
            require(line['text'].strip(),line['id']+': empty text')
            placeholders=set(re.findall(r'\{([^{}]+)\}',line['text']))
            require(placeholders<=set(speech['placeholders']),line['id']+': undeclared placeholder')
            if 'gesture' in line:require(line['gesture'] in props and props[line['gesture']]['type']=='trigger',line['id']+': unknown gesture')
    require(len(line_ids)==len(set(line_ids)),'Duplicate speech line IDs')
    feature_ids=[]
    for item in features['features']:
        feature_ids.append(item['id'])
        require(item['preset'] in preset_ids,item['id']+': unknown preset')
        require(item['speech_category'] in speech['categories'],item['id']+': unknown speech category')
        require(item['artwork_status'] in ('available','mood_only'),item['id']+': invalid artwork status')
        if item['artwork_status']=='mood_only':require(item.get('pending_prop'),item['id']+': missing pending prop')
    require(len(feature_ids)==len(set(feature_ids)),'Duplicate feature IDs')
    return {'properties':len(props),'enum_values':sum(map(len,enums.values())),'presets':len(preset_ids),
            'speech_categories':len(speech['categories']),'speech_lines':len(line_ids),'feature_mappings':len(feature_ids)}


def data_tree(model):
    validate_model(model)
    root=ET.Element('Rive',version='1',kind='fragment')
    enums={e['name']:e for e in model['enums']}
    for enum in model['enums']:
        out=ET.SubElement(root,'DataEnumCustom',name=enum['name'],id=enum['id'])
        for item in enum['values']:ET.SubElement(out,'DataEnumValue',key=item['key'],value=item['label'],id=item['id'])
    vm=model['view_model'];instance=vm['instance']
    out=ET.SubElement(root,'ViewModel',name=vm['name'],id=vm['id'],defaultInstanceId=instance['id'])
    tags={'enum':'EnumCustom','boolean':'Boolean','trigger':'Trigger'}
    for prop in model['properties']:
        attrs={'name':prop['name'],'id':prop['id']}
        if prop['type']=='enum':attrs['enumId']=enums[prop['enum']]['id']
        ET.SubElement(out,'ViewModelProperty'+tags[prop['type']],attrs)
    values=ET.SubElement(out,'ViewModelInstance',name=instance['name'],id=instance['id'],exports='true')
    for prop in model['properties']:
        attrs={'viewModelPropertyId':prop['id'],'id':prop['instance_value_id']}
        if prop['type']=='enum':attrs['propertyValue']=next(v['id'] for v in enums[prop['enum']]['values'] if v['key']==prop['default'])
        if prop['type']=='boolean':attrs['propertyValue']=str(prop['default']).lower()
        ET.SubElement(values,'ViewModelInstance'+{'enum':'Enum','boolean':'Boolean','trigger':'Trigger'}[prop['type']],attrs)
    ET.indent(root,space='    ')
    return root


def preset_args(preset,capture=False):
    args=['--fit=contain']
    for key,value in preset.get('values',{}).items():
        value=str(value).lower() if type(value) is bool else value
        args.append(f'--data={key}={value}')
    args.extend('--data='+name+'=1' for name in preset.get('triggers',[]))
    if capture:
        for step in preset['capture_steps']:
            if 'advance' in step:args.append('--advance='+str(step['advance']))
            else:args.append('--pointer=click@'+','.join(map(str,step['click'])))
    return args


def public_contract(model):
    enums={e['name']:[v['key'] for v in e['values']] for e in model['enums']}
    properties=[]
    for p in model['properties']:
        item={k:p[k] for k in ('name','type','default','description') if k in p}
        if p['type']=='enum':item['values']=enums[p['enum']]
        properties.append(item)
    return {'schema_version':1,'runtime_file':Path(model['runtime_file']).name,
            'artboard':model['artboard']['name'],'size':[model['artboard']['width'],model['artboard']['height']],
            'fit':model['artboard']['fit'],'state_machine':model['state_machine']['name'],
            'view_model':model['view_model']['name'],'instance':model['view_model']['instance']['name'],
            'properties':properties,'layers':model['state_machine']['layers']}


def generate():
    model,presets,speech,features=(read(p) for p in ['data/model.json','data/presets.json','speech/lines.vi.json','data/features.json'])
    counts=validate_sources(model,presets,speech,features)
    ET.ElementTree(data_tree(model)).write(ROOT/'data.rml',encoding='utf-8')
    out=BUILD/'data'
    write(out/'contract.json',public_contract(model))
    write(out/'presets.json',{'schema_version':1,'presets':[{**p,'preview_args':preset_args(p),'capture_args':preset_args(p,True)} for p in presets['presets']]})
    write(out/'source-validation.json',{'passed':True,'counts':counts,'errors':[]})
    print('Data sources valid: '+', '.join(f'{v} {k}' for k,v in counts.items()),flush=True)
    return model


def signature(element):
    return element.tag,sorted(element.attrib.items()),[signature(child) for child in element]


def validate_runtime(model=None,root=None):
    model=model or read('data/model.json');root=root if root is not None else ET.parse(ROOT/'runtime.rml').getroot()
    validate_model(model)
    ids=[e.get('id') for e in root.iter() if e.get('id')]
    require(len(ids)==len(set(ids)),'Runtime has duplicate IDs')
    byid={e.get('id'):e for e in root.iter() if e.get('id')}
    art=byid.get(model['artboard']['id']);require(art is not None and art.tag=='Artboard','Runtime artboard missing')
    for key in ('name','width','height'):require(art.get(key)==str(model['artboard'][key]),'Artboard mismatch: '+key)
    vm=model['view_model'];sm=model['state_machine']
    for key,value in {'defaultStateMachineId':sm['id'],'viewModelId':vm['id'],'viewModelInstanceId':vm['instance']['id']}.items():
        require(art.get(key)==value,'Runtime binding mismatch: '+key)
    machine=art.find('StateMachine');require(machine is not None and machine.get('id')==sm['id'] and machine.get('name')==sm['name'],'State machine mismatch')
    require([layer.get('name') for layer in machine.findall('StateMachineLayer')]==sm['layers'],'State machine layer order mismatch')
    for expected in data_tree(model):
        actual=byid.get(expected.get('id'))
        require(actual is not None and signature(actual)==signature(expected),'Embedded data differs from model: '+expected.get('name',''))
    binds={bind.get('sourcePathIds') for bind in root.iter('DataBindContext')}
    for prop in model['properties']:require(vm['id']+'-'+prop['id'] in binds,'Property has no runtime binding: '+prop['name'])
    animations={a.get('name') for a in art.findall('LinearAnimation')}
    for enum in model['enums']:
        if enum['name']=='Mood':
            for value in enum['values']:
                require('mood_'+value['key'] in animations,'Mood animation missing: '+value['key'])
                require(any(e.get('value')==value['id'] for e in machine.iter('TransitionValueEnumComparator')),'Mood transition missing: '+value['key'])
    require(art.find('Fill') is None,'Artboard must remain transparent')
    require(not list(root.iter('ImageAsset')) and not list(root.iter('Image')),'Reference bitmap must not enter the production rig')
    return art


def snapshot():
    model=read('data/model.json');art=validate_runtime(model)
    parents={child:parent for parent in art.iter() for child in parent}
    rig_ids={'0:10','0:11','0:12','0:13','0:15','0:16','0:17','0:18','0:19','0:20','0:21','0:23','0:900','0:1427','0:1447'}
    nodes=[{'type':e.tag,'name':e.get('name'),'id':e.get('id'),'parent':parents[e].get('name'),
            'local_transform':{k:float(e.get(k,default)) for k,default in [('x','0'),('y','0'),('rotation','0'),('scaleX','1'),('scaleY','1')]}}
           for e in art.iter() if e.get('id') in rig_ids]
    animations=[{'name':a.get('name'),'id':a.get('id'),'frames':int(a.get('duration','0')),'fps':60,'loop':a.get('loopValue','oneShot')}
                for a in art.findall('LinearAnimation')]
    write(BUILD/'data/rig-map.json',{'coordinate_space':'Local transforms in 500x500 artboard; parent transforms compose at runtime.','nodes':nodes,'animations':animations})
    paths=['data/model.json','data/presets.json','data/features.json','speech/lines.vi.json','data.rml','runtime.rml']
    write(BUILD/'data/validation.json',{'passed':True,'checks':['unique IDs','artboard and default state machine','exported View Model defaults','embedded model equality','bindings for every property','enum animations and transitions','ordered layers','transparent vector-only rig'],
          'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'errors':[]})
    print(f'Runtime data valid: {len(nodes)} rig nodes, {len(animations)} animations',flush=True)


def package():
    snapshot()
    dest=ROOT/'dist/data';dest.mkdir(parents=True,exist_ok=True)
    for name in ['contract.json','presets.json','rig-map.json','validation.json']:
        shutil.copy2(BUILD/'data'/name,dest/name)
    shutil.copy2(ROOT/'data/features.json',dest/'features.json')
    speech=ROOT/'dist/speech';speech.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'speech/lines.vi.json',speech/'lines.vi.json')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--package',action='store_true')
    args=parser.parse_args()
    if args.check:
        counts=validate_sources(*(read(p) for p in ['data/model.json','data/presets.json','speech/lines.vi.json','data/features.json']))
        snapshot();print(json.dumps(counts))
    else:generate()
    if args.package:package()
