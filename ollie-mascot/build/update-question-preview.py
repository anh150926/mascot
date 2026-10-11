from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from kit_common import BUILD, run, render, clean, sheet
from export_web_frames import convert
import build_data
from PIL import Image

build_data.validate_sources(*(build_data.read(p) for p in [
    'data/model.json', 'data/presets.json', 'speech/lines.vi.json', 'data/features.json'
]))
build_data.validate_runtime()
sequence = []
for frame in (12, 24, 60, 120):
    target = BUILD / f'question-frame-{frame}.png'
    render(target, data=['mood=confused'], steps=[f'--advance={frame}'])
    sequence.append((f'Frame {frame}', clean(target)))
sheet(sequence, BUILD / 'question-motion-review.png', cols=4, size=300)

target = BUILD / 'question-frame-24.png'
for dest in ['probe-t7-confused.png', 'confused.png', 'moods/confused.png']:
    shutil.copy2(target, BUILD / dest)
clean(BUILD / 'probe-t7-confused.png')
convert(target, ROOT / 'playground/frames/confused.png')

samples = []
for size in (120, 240, 400):
    target = BUILD / f'question-size-{size}.png'
    render(target, data=['mood=confused'], steps=['--advance=60'], viewport=f'{size}x{size}')
    art = clean(target)
    for label, background in [('Light', '#e8f2e7'), ('Dark', '#1b2520')]:
        preview = Image.new('RGBA', art.size, background)
        preview.alpha_composite(art)
        samples.append((f'{size}px / {label}', preview))
sheet(samples, BUILD / 'question-size-review.png', cols=2, size=400)

moods = [('neutral', 't6-neutral'), ('happy', 't6-happy'), ('wink', 't6-wink'),
         ('focus', 't6-focus'), ('surprised', 't7-surprised'), ('sleepy', 't7-sleepy'),
         ('confused', 't7-confused'), ('sleep', 't9-asleep')]
sheet([(name, clean(BUILD / f'probe-{ident}.png')) for name, ident in moods],
      BUILD / 'moods/contact-sheet.png', title='OLLIE / EXPRESSIONS')
shutil.copy2(BUILD / 'moods/contact-sheet.png', BUILD / 'mood-review.png')
shutil.copy2(ROOT / 'runtime.rml', BUILD / 'rv/scene.rml')
(BUILD / 'inspect-summary.json').write_text(run(['inspect', '.', '--summary']), encoding='utf-8')
print(run(['.', '--once']).strip())
shutil.copy2(BUILD / 'ollie-mascot.riv', ROOT / 'dist/ollie.riv')
build_data.package()
print('Updated Rive export, confused fallback, review sheets and runtime validation.')
