"""Keep local, versioned Rive CLI docs and Nez-compatible build/doc_*.txt files."""
import argparse
import hashlib
import json
import re
from datetime import datetime,timezone
from kit_common import ROOT,BUILD,run

TOPICS={'data':'doc_data.txt','drawing':'doc_draw.txt','easing':'doc_ease.txt',
        'rigging':'doc_rig.txt','state-machines':'doc_sm.txt','workflow':'doc_workflow.txt','format':'doc_format.txt'}
TYPES=['Artboard','ViewModel','ViewModelInstance','DataEnumCustom','DataEnumValue',
       'ViewModelPropertyEnumCustom','ViewModelPropertyBoolean','ViewModelPropertyTrigger',
       'ViewModelInstanceEnum','ViewModelInstanceBoolean','ViewModelInstanceTrigger',
       'DataBindContext','TransitionViewModelCondition','TransitionValueEnumComparator']


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def sync(refresh=False):
    dest=ROOT/'docs/rive-cli';dest.mkdir(parents=True,exist_ok=True)
    schemas=dest/'schema';schemas.mkdir(exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    version=run(['--version']).strip()
    index_path=dest/'index.json'
    old=json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {}
    expected=[dest/(t+'.md') for t in TOPICS]+[schemas/(t+'.json') for t in TYPES]
    cached=not refresh and old.get('cli_version')==version and all(p.exists() and old.get('hashes',{}).get(str(p.relative_to(dest)).replace('\\','/'))==sha(p) for p in expected)
    if not cached:
        for topic in TOPICS:
            content=re.sub(r'\n{3,}','\n\n',run(['docs',topic]).replace('\r','')).strip()+'\n'
            if not content.startswith('#'):raise ValueError('Invalid CLI document: '+topic)
            (dest/(topic+'.md')).write_text(content,encoding='utf-8')
        for name in TYPES:
            content=json.loads(run(['schema',name,'--all','--json']))
            if content.get('type')!=name:raise ValueError('Invalid CLI schema: '+name)
            (schemas/(name+'.json')).write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        old={'cli_version':version,'captured_at_utc':datetime.now(timezone.utc).isoformat(),
             'source':'Bundled documentation and schema from installed Rive CLI; no Nez project content copied.',
             'commands':['rive docs '+t for t in TOPICS]+['rive schema '+t+' --all --json' for t in TYPES],
             'hashes':{str(p.relative_to(dest)).replace('\\','/'):sha(p) for p in expected}}
        index_path.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for topic,alias in TOPICS.items():
        (BUILD/alias).write_text((dest/(topic+'.md')).read_text(encoding='utf-8'),encoding='utf-8')
    (BUILD/'cli-docs-manifest.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'CLI docs: {version}; {len(TOPICS)} topics, {len(TYPES)} schemas; '+('cached' if cached else 'refreshed'),flush=True)
    return old


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true')
    sync(p.parse_args().refresh)
