"""Render actual state-machine probes and check visible behavior + bound data."""
import argparse
import glob
import json
from PIL import Image, ImageChops, ImageStat
from kit_common import ROOT,BUILD,run,render
from build_data import read,validate_sources,validate_runtime


def walk(item):
    if isinstance(item,dict):
        yield item
        for value in item.values():yield from walk(value)
    elif isinstance(item,list):
        for value in item:yield from walk(value)


def difference(a,b,box=None):
    a=Image.open(BUILD/f'probe-{a}.png').convert('RGB')
    b=Image.open(BUILD/f'probe-{b}.png').convert('RGB')
    if box:a,b=a.crop(box),b.crop(box)
    diff=ImageChops.difference(a,b)
    return sum(ImageStat.Stat(diff).mean)/3


def main(paths=None):
    validate_sources(*(read(p) for p in ['data/model.json','data/presets.json','speech/lines.vi.json','data/features.json']))
    validate_runtime()
    paths=paths or [str(ROOT/'tests/poses.json')]
    files=[p for pattern in paths for p in glob.glob(pattern)]
    if not files:raise RuntimeError('No probe files found')
    BUILD.mkdir(exist_ok=True)
    structure=json.loads(run(['inspect','.','--json']))
    (BUILD/'inspect.json').write_text(json.dumps(structure,indent=2),encoding='utf-8')
    names={x.get('name') for x in walk(structure)}
    errors=[];results=[]
    if structure.get('problems'):errors.append('Rive inspect reports problems')
    for file in files:
        spec=json.loads(open(file,encoding='utf-8').read())
        errors.extend('Missing component '+n for n in spec['names'] if n not in names)
        for cap in spec['captures']:
            ident=cap['id'];dump=BUILD/f'probe-{ident}.json'
            render(BUILD/f'probe-{ident}.png',steps=cap.get('steps') or [f'--advance={cap.get("advance",1)}'],data=cap.get('data',[]),viewport=cap.get('viewport'),dump=dump)
            actual=json.loads(dump.read_text(encoding='utf-8'))
            data={p['path']:p.get('value') for p in actual['viewModel']['properties']}
            for key,value in cap.get('expect',{}).items():
                if data.get(key)!=value:errors.append(f'{ident}: {key}={data.get(key)}, expected {value}')
            im=Image.open(BUILD/f'probe-{ident}.png').convert('RGB')
            background=Image.new('RGB',im.size,(29,29,29))
            diff=ImageChops.difference(im,background)
            bbox=diff.point(lambda p:255 if p>24 else 0).getbbox()
            if not bbox:errors.append(ident+': blank render')
            elif bbox[0]<=0 or bbox[1]<=0 or bbox[2]>=im.width or bbox[3]>=im.height:
                errors.append(ident+': artwork/effect touches viewport edge')
            results.append({'id':ident,'data':data,'bounds':bbox})
            print('Captured '+ident,flush=True)
    # Behavior checks compare equal-time controls, independent of exact colors.
    measures={
        'blink_eye_change':difference('t5-eyes-open','t5-eyes-shut',(132,164,364,272)),
        'wave_wing_change':difference('t10-rest','t10-wave',(12,242,177,459)),
        'wave_returns_to_rest':difference('t10-after','t10-baseline-after',(12,290,185,459)),
        'sleep_blocks_wave':difference('t9-asleep','t9-sleep-wave'),
        'sleep_closes_eyes':difference('t9-awake','t9-asleep',(130,170,365,274)),
        'breathing_visible':difference('t5-rest','t5-inhale'),
        'neutral_matches_front':0
    }
    for key in ('blink_eye_change','wave_wing_change','sleep_closes_eyes'):
        if measures[key]<3:errors.append(key+': visible behavior missing')
    if measures['breathing_visible']<.1:errors.append('No visible breathing')
    if measures['wave_returns_to_rest']>3:errors.append('Wave does not return to rest')
    if measures['sleep_blocks_wave']>1:errors.append('Wave changes sleeping pose')
    if (BUILD/'front.png').exists():
        a=Image.open(BUILD/'front.png').convert('RGB');b=Image.open(BUILD/'probe-t1-default.png').convert('RGB')
        measures['neutral_matches_front']=sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3
        if measures['neutral_matches_front']>2:errors.append('Neutral rig drifts from static master')
    report={'passed':not errors,'captures':results,'measurements':measures,'errors':errors}
    (BUILD/'check-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'passed':not errors,'captures':len(results),'measurements':measures,'errors':errors},indent=2))
    if errors:raise SystemExit(1)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('paths',nargs='*')
    main(parser.parse_args().paths)
