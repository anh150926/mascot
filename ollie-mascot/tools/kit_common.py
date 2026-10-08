from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont
from export_web_frames import convert

ROOT=Path(__file__).resolve().parent.parent
BUILD=ROOT/'build'
RIVE=shutil.which('rive') or str(Path.home()/'.rive/bin/rive.exe')
PAPER='#F5F7EF'
INK='#164632'


def run(args,cwd=ROOT):
    result=subprocess.run([RIVE,*map(str,args)],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=75)
    if result.returncode:
        raise RuntimeError(result.stdout+'\n'+result.stderr)
    return result.stdout


def render(target,project='.',steps=None,data=(),viewport=None,dump=None):
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    args=[project,f'--screenshot={target}','--fit=contain']
    if viewport:args.append(f'--viewport={viewport}')
    args.extend(f'--data={d}' for d in data)
    args.extend(steps or ['--advance=1'])
    if dump:args.append(f'--data-dump={dump}')
    run(args)
    return target


def clean(path):
    """Only generated CLI screenshots have the known opaque preview background."""
    path=Path(path)
    dest=path.parent/(path.stem+'-alpha.png')
    convert(path,dest)
    return Image.open(dest).convert('RGBA')


def font(size=17):
    file=Path('C:/Windows/Fonts/segoeui.ttf')
    return ImageFont.truetype(str(file),size) if file.exists() else ImageFont.load_default()


def tile(source,size=300,bg=PAPER):
    image=Image.new('RGBA',(size,size),bg)
    source=source.copy();source.thumbnail((size,size),Image.Resampling.LANCZOS)
    image.alpha_composite(source,((size-source.width)//2,(size-source.height)//2))
    return image


def sheet(items,destination,cols=4,size=260,title=None):
    gap=16;top=64 if title else 12;rows=(len(items)+cols-1)//cols
    out=Image.new('RGB',(cols*(size+gap)+gap,top+rows*(size+50)+gap),PAPER)
    draw=ImageDraw.Draw(out)
    if title:draw.text((20,17),title,fill=INK,font=font(23))
    for i,(label,im) in enumerate(items):
        x=gap+(i%cols)*(size+gap);y=top+(i//cols)*(size+50)
        out.paste(tile(im,size).convert('RGB'),(x,y))
        draw.text((x+8,y+size+8),label,fill=INK,font=font(16))
    Path(destination).parent.mkdir(exist_ok=True,parents=True)
    out.save(destination)
    return out
