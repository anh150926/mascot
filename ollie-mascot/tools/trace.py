"""Regenerate a static Rive trace project with the supplied reference underneath."""
import argparse
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from kit_common import ROOT,BUILD,RIVE,run


def sync(opacity=.5):
    out=BUILD/'trace';out.mkdir(exist_ok=True,parents=True)
    tree=ET.parse(ROOT/'artwork/front.rml');root=tree.getroot();art=root.find('Artboard')
    for node in art.findall('Node'):
        if node.get('name')!='BeakClosed':node.set('opacity',str(opacity))
    ET.SubElement(art,'Image',x='250',y='250',assetId='0:99990',name='FrontReference',id='0:99991')
    ET.SubElement(root,'ImageAsset',file='front.png',name='FrontReferenceAsset',id='0:99990')
    shutil.copy2(ROOT/'reference/front-500.png',out/'front.png')
    ET.indent(tree,space='  ');tree.write(out/'scene.rml',encoding='utf-8')
    (out/'rive.yaml').write_text('name: ollie-trace\nmain: Front\n',encoding='utf-8')
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');parser.add_argument('--art-opacity',type=float,default=.5)
    args=parser.parse_args();out=sync(args.art_opacity)
    if not args.watch:
        print(run([out,'--screenshot='+str(BUILD/'trace.png'),'--fit=contain']))
        return
    preview=subprocess.Popen([RIVE,str(out),'--fit=contain'])
    last=None
    try:
        while preview.poll() is None:
            stamp=tuple((ROOT/p).stat().st_mtime_ns for p in ['artwork/front.rml','reference/front-500.png'])
            if stamp!=last:sync(args.art_opacity);last=stamp
            time.sleep(.6)
    except KeyboardInterrupt:preview.terminate()


if __name__=='__main__':main()
