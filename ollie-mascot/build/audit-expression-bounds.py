import sys
from pathlib import Path
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
from build_data import read
issues=[];total=0
for scene in read('data/expressions.json')['expressions']:
    for p in sorted((root/'build/expressions').glob(scene['key']+'*.png')):
        if p.stem.endswith('-motion') or p.stem.endswith('-alpha'):continue
        im=Image.open(p).convert('RGB')
        if im.size!=(500,500):continue
        mask=ImageChops.difference(im,Image.new('RGB',im.size,(29,29,29))).point(lambda c:255 if c>24 else 0)
        bbox=mask.getbbox();total+=1
        if bbox is None or min(bbox[:2])<=0 or bbox[2]>=500 or bbox[3]>=500:issues.append((p.name,bbox))
print({'captures_checked':total,'edge_issues':issues})
