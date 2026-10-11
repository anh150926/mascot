"""Publish the source-layer breakdown and five-frame review for all posed wings."""
from __future__ import annotations
import json
import shutil
import sys
from html import escape
from pathlib import Path
from PIL import Image
from kit_common import ROOT, sheet
from build_data import read

sys.path.insert(0,str(ROOT/'artwork'))
from build_artwork import PARTS,vertices
from wing_poses import HOLD_SOURCE


def svg_path(source):
    points,closed=vertices(source['d'])
    def xy(p):return f'{p[0]:.3f} {p[1]:.3f}'
    d='M '+xy(points[0][0])
    for i in range(1,len(points)):
        d+=' C '+xy(points[i-1][2])+' '+xy(points[i][1])+' '+xy(points[i][0])
    if closed:d+=' C '+xy(points[-1][2])+' '+xy(points[0][1])+' '+xy(points[0][0])+' Z'
    return d


def anatomy(destination):
    sources=next(p for p in PARTS if p['name']=='LeftWing')['shapes']
    names=['01 · Khối cánh tối','02 · Lông dài phía sau','03 · Lông giữa','04 · Lông bên',
           '05 · Mảng cánh trên','06 · Lông phủ xanh non','07 · Lá sáng trên cánh','08 · Ghép đủ bảy lớp']
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" role="img" aria-label="Bảy lớp cánh gốc Ollie"><rect width="960" height="560" fill="#f5f7ef"/>']
    for i,label in enumerate(names):
        x=12+(i%4)*240;y=12+(i//4)*280
        parts.append(f'<rect x="{x}" y="{y}" width="228" height="256" rx="16" fill="#fffdf5" stroke="#d2dfce"/><g transform="translate({x-61} {y-365}) scale(1.25)">')
        for j,source in enumerate(sources if i==7 else [sources[i]]):
            fill='#'+source['fill'];gradient=source['gradient']
            if gradient:
                c1,c2,x1,y1,x2,y2=gradient;gid=f'g{i}_{j}'
                parts.append(f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1*500/1254}" y1="{y1*500/1254}" x2="{x2*500/1254}" y2="{y2*500/1254}"><stop stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}"/></linearGradient></defs>')
                fill=f'url(#{gid})'
            stroke='#'+source['stroke'] if source['stroke'] else 'none'
            parts.append(f'<path d="{svg_path(source)}" fill="{fill}" stroke="{stroke}" stroke-width="{source["weight"]*500/1254}" stroke-linejoin="round" stroke-linecap="round"/>')
        parts.append(f'</g><text x="{x+12}" y="{y+240}" fill="#164632" font-family="Segoe UI,sans-serif" font-size="15">{label}</text>')
    parts.append('</svg>')
    destination.write_text(''.join(parts),encoding='utf-8')


def soft_anatomy(destination):
    """Show both original wing contours used by every posed expression."""
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 370" role="img" aria-label="Hai cánh gốc Ollie dùng cho cử chỉ và cầm đồ">',
           '<rect width="840" height="370" rx="18" fill="#f5f7ef"/>']
    for x,title,side in [(12,'Cánh trái: bảy lớp lông gốc', 'L'),
                         (426,'Cánh phải: phản chiếu từ mẫu gốc', 'R')]:
        parts.append(f'<rect x="{x}" y="10" width="402" height="350" rx="16" fill="#fffdf5" stroke="#d2dfce"/>')
        view_x=69 if side=='L' else 271
        parts.append(f'<svg x="{x+30}" y="24" width="340" height="290" viewBox="{view_x} 305 160 169">')
        if side=='R':parts.append('<g transform="translate(500 0) scale(-1 1)">')
        for item in HOLD_SOURCE:
            fill='#'+item['fill']
            if item.get('gradient'):
                c1,c2,x1,y1,x2,y2=item['gradient'];gid=item['name']
                parts.append(f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}"/></linearGradient></defs>')
                fill=f'url(#{gid})'
            stroke='#'+item['stroke'] if item['stroke'] else 'none'
            d=svg_path(item) if item.get('master') else item['d']
            parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{item["weight"]}" stroke-linejoin="round" stroke-linecap="round"/>')
        if side=='R':parts.append('</g>')
        parts.append(f'</svg><text x="{x+17}" y="340" fill="#164632" font-family="Segoe UI,sans-serif" font-size="17">{escape(title)}</text>')
    parts.append('</svg>')
    destination.write_text(''.join(parts),encoding='utf-8')


def main():
    out=ROOT/'playground/frames/wings';out.mkdir(parents=True,exist_ok=True)
    anatomy(out/'anatomy.svg')
    soft_anatomy(out/'soft-anatomy.svg')
    scenes=read('data/expressions.json')['expressions']
    # Full-resolution stills make the contact edges easy to inspect in build/.
    detail=ROOT/'build/wing-redesign';detail.mkdir(parents=True,exist_ok=True)
    focus=('meditate','worried','idea','bedtime','love','nutrition','sad','wallet','saving','checklist','alarm','letter','pomodoro','workout','celebrate')
    labels={spec['key']:spec['label'] for spec in scenes}
    for key in focus:
        for suffix in ('','-alpha'):
            shutil.copy2(ROOT/f'build/expressions/{key}-50{suffix}.png',detail/f'{key}{suffix}.png')
        phases=[('Đầu',0),('¼',25),('Giữa',50),('¾',75),('Cuối',100)]
        frames=[(label,Image.open(ROOT/f'build/expressions/{key}-{frame}-alpha.png').convert('RGBA'))
                for label,frame in phases]
        sheet(frames,detail/f'{key}-motion.png',cols=5,size=260,title=labels[key])
    cards=''.join(f'<figure><img loading="lazy" src="{key}-motion.png" alt="{escape(labels[key])}: năm mốc chuyển động"><figcaption><a href="{key}-alpha.png">Xem khung giữa ở 500 px · {escape(labels[key])}</a></figcaption></figure>' for key in focus)
    (detail/'index.html').write_text('''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ollie · Khung chuyển động cánh gốc</title><style>
body{margin:0;background:#f5f7ef;color:#164632;font:16px/1.6 system-ui}main{max-width:1420px;margin:auto;padding:28px 20px}h1{line-height:1.2}a{color:#276b40}figure{margin:24px 0;border:1px solid #cadcc5;border-radius:14px;overflow:hidden;background:#fffdf5}img{display:block;width:100%;height:auto}figcaption{padding:12px 20px}p{max-width:850px}
</style><main><a href="../../playground/index.html">Mở playground</a> · <a href="../../playground/wing-review.html">Xem từng khung</a>
<h1>Ollie · Cánh gốc trong 15 cảnh tạo dáng</h1><p>Bản 08 dùng bảy lớp lông của mẫu gốc cho cả cử chỉ và động tác cầm, nâng đồ. Cánh dùng màu phẳng và giữ hai lớp lông dài. Ở cảnh ăn mừng, mặt cúp hiện trước cánh giữ. Mỗi dải thể hiện năm mốc trong vòng chuyển động.</p>'''+cards+'</main></html>',encoding='utf-8')
    for spec in scenes:
        for frame in (0,25,50,75,100):
            source=ROOT/f'build/expressions/{spec["key"]}-{frame}-alpha.png'
            Image.open(source).save(out/f'{spec["key"]}-{frame}.webp',lossless=True)
    options=''.join(f'<option value="{s["key"]}"'+(' selected' if s['key']=='letter' else '')+f'>{escape(s["label"])}</option>' for s in scenes)
    html='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ollie · Cánh lá / bản dựng 08</title><style>
:root{font:16px/1.6 system-ui;color:#164632;background:#f5f7ef}*{box-sizing:border-box}body{margin:0}main{max-width:1120px;margin:auto;padding:32px 24px 70px}a{color:#327c47}h1{font-size:clamp(30px,4vw,48px);line-height:1.1;max-width:720px;margin:16px 0}h2{margin:36px 0 12px}p{max-width:760px}.tag{font-size:12px;letter-spacing:.16em;color:#557e61}.layout{display:grid;grid-template-columns:1fr 1fr;gap:20px}.card{background:#fffdf5;border:1px solid #cadcc5;border-radius:20px;overflow:hidden;padding:20px}img{display:block;width:100%;height:auto}.stage{background:#e6efe1;border-radius:16px}.stage.dark{background:#17382d}.crop{position:relative;aspect-ratio:2.1;overflow:hidden;background:#e6efe1;border-radius:14px}.crop img{position:absolute;width:140%;max-width:none;left:-20%;top:-165%}select,button{font:inherit;padding:9px 13px;border:1px solid #9cbe9b;background:#fffdf5;color:#164632;border-radius:9px}select{width:100%}button{cursor:pointer}input[type=range]{width:100%;accent-color:#408d4a}label{display:block;margin:14px 0 5px}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.phases{display:flex;justify-content:space-between;font-size:12px;color:#598264}.note{padding:15px 18px;border-left:4px solid #72a34c;background:#e7efdf}.anatomy{margin-top:18px}.small{font-size:14px;color:#53765b}@media(max-width:700px){.layout{grid-template-columns:1fr}main{padding:24px 16px}.card{padding:14px}}
</style><main><a href="index.html">← Chạy thư viện chuyển động</a><p class="tag">OLLIE / CÁNH LÁ / BUILD 08</p><h1>Cánh gốc của Ollie trong mọi tư thế.</h1><p>Cả tư thế cử chỉ và động tác cầm, nâng đồ đều dùng bảy lớp lông của mẫu front gốc. Hai bên cánh có màu phẳng, đầu lông nhọn và có hai lớp dài phía dưới. Cúp ăn mừng hiện trước cánh giữ. Xem đủ 19 cảnh và năm mốc mỗi vòng.</p>
<div class="layout"><div class="card"><div class="stage" id="stage"><img id="full" width="500" height="500" alt="Toàn thân Ollie tại khung đang chọn"></div><div class="controls"><button id="theme">Đổi nền</button><a href="../dist/ollie.riv">Tải bản Rive</a></div></div><div class="card"><label for="scene">Tư thế cánh</label><select id="scene">OPTIONS</select><label for="frame">Khung hình <output id="time"></output></label><input id="frame" type="range" min="0" max="4" value="0" step="1"><div class="phases"><span>Đầu</span><span>¼</span><span>Giữa</span><span>¾</span><span>Cuối</span></div><div class="controls"><button id="previous" aria-label="Khung trước">← Trước</button><button id="next" aria-label="Khung sau">Sau →</button></div><p class="small">Năm khung xuất từ vòng lặp Rive sau khi hoàn tất chuyển trạng thái. Kéo để xem vai, nếp gập và điểm tiếp xúc qua từng pha.</p><div class="crop"><img id="detail" alt="Chi tiết cánh và đạo cụ"></div><p id="motion"></p></div></div>
<h2>Cấu trúc hai cánh</h2><p>Cánh trái lấy trực tiếp đường Bézier từ mẫu gốc; cánh phải phản chiếu các đường đó. Tư thế thay góc và tỷ lệ đồng đều để chạm vật hoặc biểu lộ cảm xúc. Các lớp lông xanh non và đầu lông nhọn luôn giữ vị trí tương đối.</p><img class="anatomy" src="frames/wings/soft-anatomy.svg" alt="Cánh trái và cánh phải lấy từ mẫu gốc" width="840" height="370"><h2>Cánh front gốc</h2><p>Bốn cảnh chạy, mệt, reo vui và tràn năng lượng dùng cánh front gốc vì đường lông dang và hạ của chúng vẫn rõ. Sơ đồ này giữ để so tỷ lệ và bảng màu.</p><img class="anatomy" src="frames/wings/anatomy.svg" alt="Tách bảy lớp cánh front gốc" width="960" height="560">
<h2>Ba điểm cần kiểm tra khi chỉnh tiếp</h2><p class="note">Vai nối liền thân · Đầu lông cong mềm, không gãy góc · Cánh chạm đúng đạo cụ ở cả đầu, giữa và cuối vòng.</p><p>Các tư thế chống cằm và ngáp chỉ thay cánh tham gia động tác. Cánh bên kia vẫn dùng mẫu đứng gốc. Khi ngủ thật, vẫy hoặc trở về biểu cảm cơ bản, rig tự trả lại cánh tương ứng.</p><p><a href="../docs/WING_STUDY.md">Đọc phân tích tạo hình và thông số dựng ↗</a></p></main><script>
const scenes=SCENES, picker=document.getElementById('scene'), slider=document.getElementById('frame');
function show(){const spec=scenes.find(s=>s.key===picker.value),index=Number(slider.value),src=`frames/wings/${spec.key}-${index*25}.webp?v=8`;document.getElementById('full').src=src;document.getElementById('detail').src=src;document.getElementById('time').textContent=`${index+1}/5 · ${(spec.frames*index/240).toFixed(2)} s`;document.getElementById('motion').textContent=spec.motion;}
picker.addEventListener('change',show);slider.addEventListener('input',show);document.getElementById('previous').onclick=()=>{slider.value=Math.max(0,Number(slider.value)-1);show()};document.getElementById('next').onclick=()=>{slider.value=Math.min(4,Number(slider.value)+1);show()};document.getElementById('theme').onclick=()=>document.getElementById('stage').classList.toggle('dark');show();
</script></html>'''
    (ROOT/'playground/wing-review.html').write_text(html.replace('OPTIONS',options).replace('SCENES',json.dumps(scenes,ensure_ascii=False)),encoding='utf-8')
    print(f'Wing review ready: original feathers in every posed scene; {len(scenes)} scenes x 5 frames.',flush=True)


if __name__=='__main__':main()
