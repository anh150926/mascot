"""Preview a validated preset: python tools/preview.py sleep [--capture]."""
import argparse
import subprocess
from build_data import read,validate_sources,preset_args
from kit_common import ROOT,BUILD,RIVE,run


def main():
    p=argparse.ArgumentParser();p.add_argument('preset',nargs='?',default='neutral');p.add_argument('--list',action='store_true');p.add_argument('--capture',action='store_true')
    args=p.parse_args()
    model,presets,speech,features=(read(n) for n in ['data/model.json','data/presets.json','speech/lines.vi.json','data/features.json'])
    validate_sources(model,presets,speech,features)
    if args.list:
        print('\n'.join(item['id']+' - '+item['label'] for item in presets['presets']));return
    preset=next((item for item in presets['presets'] if item['id']==args.preset),None)
    if preset is None:p.error('Unknown preset; use --list')
    if not args.capture and any('click' in step for step in preset['capture_steps']):
        print('This preset starts asleep. Click Ollie to wake it; --capture replays the recorded click.')
    flags=preset_args(preset,args.capture)
    if args.capture:
        dest=BUILD/'presets';dest.mkdir(exist_ok=True)
        flags.extend([f'--screenshot={dest/(args.preset+".png")}',f'--data-dump={dest/(args.preset+".json")}'])
        print(run(['.',*flags]))
    else:subprocess.run([RIVE,'.',*flags],cwd=ROOT,check=True)


if __name__=='__main__':main()
