"""One command regenerates Ollie's artwork, rig, probes, review sheets and .riv."""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
from kit_common import ROOT,BUILD,run,render,clean,sheet
import check
import overlay
import trace
import build_data
import sync_cli_docs
from export_web_frames import main as export_frames

sys.path.insert(0,str(ROOT/'artwork'))
import build_artwork as art


def python(path):
    subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,check=True)


def stage(ident,names,review_only=False):
    if review_only:return clean(BUILD/f'probe-{ident}.png')
    project=BUILD/'rv/stages'/ident;project.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(art.export(names)).write(project/'scene.rml',encoding='utf-8')
    (project/'rive.yaml').write_text(f'name: {ident}\nmain: Front\n',encoding='utf-8')
    target=BUILD/f'probe-{ident}.png'
    render(target,project=str(project))
    return clean(target)


def write_review(report):
    probes=''.join(f'<figure><img loading="lazy" src="build/probe-{cap["id"]}.png" alt="{cap["id"]}"><figcaption>{cap["id"]}</figcaption></figure>' for cap in report['captures'])
    html='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ollie — bộ mẫu & đối chiếu</title><style>
:root{font:16px/1.6 system-ui;color:#173e2d;background:#f3f5ed}*{box-sizing:border-box}body{margin:0}main{max-width:1180px;margin:auto;padding:32px 24px 70px}header{border-bottom:1px solid #c5d4c0;padding-bottom:24px;margin-bottom:28px}h1{font-size:42px;line-height:1.1;margin:12px 0}h2{margin:36px 0 14px;font-size:24px}p{max-width:850px}a{color:#276b40}nav{display:flex;gap:12px;flex-wrap:wrap}nav a{padding:9px 14px;background:white;border:1px solid #c5d4c0;border-radius:10px;text-decoration:none}.tag{font-size:12px;letter-spacing:.12em;color:#557859}.compare{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:#fbfcf6;border:1px solid #dae3d3;border-radius:16px;padding:14px;overflow:hidden}figure img{display:block;max-width:100%;height:auto;margin:auto}figcaption{padding:8px;font-size:14px}.overlay{position:relative;aspect-ratio:1}.overlay img{position:absolute;inset:0;width:100%;height:100%}label{display:block;padding:10px}input{width:100%}.wide{width:100%;border-radius:14px}.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.gallery figure{padding:7px}.gallery figcaption{font-size:12px}details{margin-top:30px}summary{cursor:pointer;font-weight:600}.status{background:#e6efdf;border-left:4px solid #70a657;padding:14px 20px}.small{font-size:14px;color:#577161}@media(max-width:720px){.compare{grid-template-columns:1fr}.gallery{grid-template-columns:repeat(2,1fr)}h1{font-size:32px}}
</style><main><header><span class="tag">OLLIE / FRONT MASTER / 08.10.2026</span><h1>Bộ mẫu Ollie</h1><p>Dựng theo ảnh “Cú lá xanh chibi đáng yêu”. Nguồn vector chia theo bộ phận, rig Rive và các frame kiểm tra đều có thể tái tạo bằng một lệnh.</p><nav><a href="playground/index.html">Thử biểu cảm & chuyển động</a><a href="artwork/ollie-front.svg">Vector SVG</a><a href="dist/ollie.riv">Tệp Rive</a><a href="build/check-report.json">Kết quả kiểm tra</a></nav></header>
<div class="status">Bản dựng để đối chiếu và tiếp tục chỉnh sửa. Front là mẫu chính hiện có; góc nghiêng, sau lưng và các đạo cụ đang chờ ảnh bổ sung.</div>
<h2>01 / Kiểm tra đúng nhân vật</h2><div class="compare"><figure><img src="reference/front-500.png" alt="Ảnh front gốc người dùng cung cấp"><figcaption>Ảnh chuẩn — giữ nguyên tỉ lệ và vị trí</figcaption></figure><figure><img src="build/front-alpha.png" alt="Ollie vector render bằng Rive"><figcaption>Bản vector — 77 đường, 18 nhóm có hình</figcaption></figure></div>
<h2>02 / Chồng nét</h2><div class="compare"><figure><div class="overlay"><img src="reference/front-500.png" alt="Ảnh chuẩn"><img id="overlay" style="opacity:.5" src="build/front-alpha.png" alt="Bản vector chồng lên ảnh chuẩn"></div><label>Độ đậm vector <span id="opacity">50%</span><input id="mix" type="range" min="0" max="100" value="50" aria-label="Độ đậm vector"></label></figure><figure><img src="build/trace/landmarks.png" alt="Các điểm neo hình dáng"><figcaption>Mốc đầu lá, tâm mắt, mỏ, cổ, vai, huy hiệu và chân. Chi tiết trong docs/MODEL_BRIEF.md.</figcaption></figure></div>
<h2>03 / Cấu tạo & từng bộ phận</h2><img class="wide" src="build/construction.png" alt="Các bước dựng Ollie"><img class="wide" src="build/parts.png" alt="Các bộ phận tách riêng">
<h2>04 / Biểu cảm</h2><img class="wide" src="build/moods/contact-sheet.png" alt="Bảy biểu cảm và tư thế ngủ">
<h2>05 / Chuyển động</h2><img class="wide" src="build/idle-strip.png" alt="Thở và chớp mắt"><img class="wide" src="build/wave-strip.png" alt="Chuỗi vẫy cánh"><img class="wide" src="build/sleep-strip.png" alt="Ngủ và chạm để thức">
<h2>06 / Kích thước ứng dụng</h2><div style="display:flex;gap:20px;align-items:end;flex-wrap:wrap"><figure><img width="80" src="build/size-80-alpha.png" alt="80 pixel"><figcaption>80 px</figcaption></figure><figure><img width="120" src="build/size-120-alpha.png" alt="120 pixel"><figcaption>120 px</figcaption></figure><figure><img width="240" src="build/size-240-alpha.png" alt="240 pixel"><figcaption>240 px</figcaption></figure></div>
<details><summary>Tất cả frame probe (28)</summary><div class="gallery">PROBES</div></details><p class="small">Biểu cảm ngoài front là bản phát triển từ ảnh chuẩn, chưa phải mẫu đã được bạn duyệt. Xem README.md để thêm ảnh và dựng lại.</p></main><script>document.getElementById('mix').addEventListener('input',e=>{document.getElementById('overlay').style.opacity=e.target.value/100;document.getElementById('opacity').textContent=e.target.value+'%'});</script></html>'''
    (ROOT/'review.html').write_text(html.replace('PROBES',probes),encoding='utf-8')


def main(review_only=False):
    BUILD.mkdir(exist_ok=True)
    sync_cli_docs.sync()
    source=ROOT/'reference/ollie-front-master.png'
    im=Image.open(source).convert('RGBA')
    im.resize((500,500),Image.Resampling.LANCZOS).save(ROOT/'reference/front-500.png')
    manifest={'primary':{'file':source.name,'original_filename':'Cú lá xanh chibi đáng yêu.png','size':list(im.size),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'role':'front identity reference supplied by user','status':'reference supplied; vector draft not approved'},'coordinate_system':{'source':[1254,1254],'artboard':[500,500],'fit':'contain','crop':None},'pending_views':['left profile','right profile','back'],'incoming_folder':'reference/incoming','secondary':'Earlier design board: expression/action direction only; latest front wins on conflicting anatomy.'}
    manifest_path=ROOT/'reference/manifest.json'
    if manifest_path.exists():
        previous=json.loads(manifest_path.read_text(encoding='utf-8'))
        # Preserve added references, pending-view decisions and review notes.
        primary={**manifest['primary'],**previous.get('primary',{})}
        if primary.get('sha256')!=manifest['primary']['sha256']:
            primary['status']='reference changed; vector needs review'
        primary.update(file=source.name,size=list(im.size),sha256=manifest['primary']['sha256'])
        manifest={**manifest,**previous,'primary':primary}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    if not review_only:
        print('Build artwork + rig',flush=True)
        python('artwork/build_artwork.py');python('tools/build_ollie.py')
        build_data.snapshot()
        python('tests/test_data.py')
        print(run(['.','--verify']).strip())
        (BUILD/'inspect-summary.json').write_text(run(['inspect','.','--summary']),encoding='utf-8')
        render(BUILD/'front.png',project=str(ROOT/'artwork'))
    clean(BUILD/'front.png')
    # Keep a minimal executable runtime snapshot, analogous to Nez's rv folder.
    rv=BUILD/'rv';rv.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'runtime.rml',rv/'scene.rml')
    (rv/'rive.yaml').write_text('name: ollie-rig-review\nmain: Runtime\nexclude:\n  - stages\n  - parts\n',encoding='utf-8')
    head={'HeadLeaf','HeadBase','LeftHeadFeathers','RightHeadFeathers','CrownPlumage','CheekFeathers'}
    stages=[('t1-silhouette',{'HeadBase','Body','FootL','FootR','LeftWing','RightWing','HeadLeaf'}),('t2-head',head),('t3-face',head|{'FaceMask','LeftEye','RightEye','Beak'}),('t4-body',{'Body','ChestPatch','AIBadge','LeftWing','RightWing','FootL','FootR'}),('t4-complete',None)]
    images=[]
    for ident,parts in stages:
        images.append((ident,stage(ident,parts,review_only)))
    sheet(images,BUILD/'construction.png',cols=5,size=215,title='OLLIE / CONSTRUCTION')
    parts=[]
    labels={'HeadLeaf':'01 Chồi lá','CrownPlumage':'02 Chỏm sáng','HeadBase':'03 Nền đầu','FaceMask':'04 Mặt kem','LeftEye':'05 Mắt trái','RightEye':'06 Mắt phải','Beak':'07 Mỏ cười','CheekFeathers':'08 Má lá','LeftWing':'09 Cánh trái','RightWing':'10 Cánh phải','Body':'11 Thân','ChestPatch':'12 Ngực kem','AIBadge':'13 Huy hiệu','FootL':'14 Chân trái','FootR':'15 Chân phải'}
    for name,label in labels.items():
        p=stage('part-'+name,{name},review_only);bbox=p.getbbox()
        if bbox:p=p.crop(bbox)
        parts.append((label,p))
    sheet(parts,BUILD/'parts.png',cols=5,size=180,title='OLLIE / EDITABLE PARTS')
    if review_only:
        report=json.loads((BUILD/'check-report.json').read_text(encoding='utf-8'))
    else:
        print('Capture and test animation states',flush=True)
        report=check.main()
    moods={'neutral':'t6-neutral','happy':'t6-happy','wink':'t6-wink','focus':'t6-focus','surprised':'t7-surprised','sleepy':'t7-sleepy','confused':'t7-confused','sleep':'t9-asleep'}
    (BUILD/'moods').mkdir(exist_ok=True)
    mood_images=[]
    for mood,ident in moods.items():
        p=BUILD/f'probe-{ident}.png';shutil.copy2(p,BUILD/'moods'/f'{mood}.png')
        if mood!='sleep':shutil.copy2(p,BUILD/f'{mood}.png')
        mood_images.append((mood,clean(p)))
    sheet(mood_images,BUILD/'moods/contact-sheet.png',title='OLLIE / EXPRESSIONS')
    shutil.copy2(BUILD/'moods/contact-sheet.png',BUILD/'mood-review.png')
    strips={'idle-strip':['t5-rest','t5-inhale','t5-seam','t5-eyes-open','t5-eyes-shut'],'wave-strip':['t10-rest','t10-wave','t10-wave-mid','t10-wave-end','t10-after'],'sleep-strip':['t9-awake','t9-asleep','t9-startle','t9-awake-after']}
    for filename,ids in strips.items():sheet([(n,clean(BUILD/f'probe-{n}.png')) for n in ids],BUILD/f'{filename}.png',cols=len(ids),size=215,title='OLLIE / '+filename.upper())
    for size in [80,120,240,500]:
        p=BUILD/f'size-{size}.png'
        if not review_only:render(p,viewport=f'{size}x{size}')
        clean(p)
    shutil.copy2(BUILD/'probe-t10-wave.png',BUILD/'wave-mid.png')
    shutil.copy2(BUILD/'probe-t9-asleep.png',BUILD/'sleep-late.png')
    export_frames();overlay.main();trace.sync()
    if not review_only:run([BUILD/'trace','--screenshot='+str(BUILD/'trace.png'),'--fit=contain'])
    write_review(report)
    if not review_only:run(['.','--once'])
    (ROOT/'dist').mkdir(exist_ok=True)
    shutil.copy2(BUILD/'ollie-mascot.riv',ROOT/'dist/ollie.riv')
    shutil.copy2(ROOT/'artwork/ollie-front.svg',ROOT/'dist/ollie-front.svg')
    shutil.copy2(BUILD/'front-alpha.png',ROOT/'dist/ollie-front.png')
    build_data.package()
    artifacts=[str(p.relative_to(ROOT)).replace('\\','/') for p in BUILD.rglob('*') if p.is_file() and p.suffix in ('.png','.json','.riv') and 'visual-' not in str(p)]
    (BUILD/'manifest.json').write_text(json.dumps({'reference':manifest['primary'],'probe_count':len(report['captures']),'passed':report['passed'],'artifacts':sorted(artifacts)},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Kit ready: {len(report["captures"])} state probes; review.html; dist/ollie.riv',flush=True)


if __name__=='__main__':main(review_only='--review-only' in sys.argv)
