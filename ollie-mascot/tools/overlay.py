"""Reference + rendered master, same canvas, without auto-cropping either one."""
from PIL import Image,ImageDraw,ImageFont
from kit_common import ROOT,BUILD,clean,tile,sheet,font


def main():
    dest=BUILD/'trace';dest.mkdir(exist_ok=True,parents=True)
    ref=Image.open(ROOT/'reference/front-500.png').convert('RGBA')
    front=clean(BUILD/'front.png')
    a,b=tile(ref,500),tile(front,500)
    sheet([('Ảnh người dùng cung cấp',ref),('Vector Rive — bản dựng hiện tại',front)],dest/'front-compare.png',cols=2,size=500,title='OLLIE / FRONT REFERENCE')
    Image.blend(a,b,.5).convert('RGB').save(dest/'front-onion.png')
    grid=Image.blend(a,b,.5).convert('RGB');draw=ImageDraw.Draw(grid)
    for p in range(0,501,25):
        draw.line((p,0,p,500),fill='#739D8C',width=1);draw.line((0,p,500,p),fill='#739D8C',width=1)
    draw.line((250,0,250,500),fill='#D07B37',width=2)
    grid.save(dest/'front-grid.png')
    landmarks=tile(ref,500).convert('RGB');draw=ImageDraw.Draw(landmarks)
    points=[('01',(305,14)),('02',(250,106)),('03',(189,223)),('04',(311,223)),('05',(250,248)),('06',(250,324)),('07',(166,318)),('08',(334,318)),('09',(250,366)),('10',(200,474)),('11',(300,474))]
    for label,(x,y) in points:
        draw.ellipse((x-4,y-4,x+4,y+4),fill='#FFFDF0',outline='#D06F32',width=2)
        draw.text((x+7,y-11),label,font=font(13),fill='#A75424')
    landmarks.save(dest/'landmarks.png')
    return ref,front


if __name__=='__main__':main()
