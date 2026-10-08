"""Editable front master. Coordinates follow ollie-front-master.png (1254 square).

Explicit cubic handles preserve leaf tips and contour joins. This single source
exports both SVG for inspection and vector RML for the animated rig. Layers below
are authored back-to-front, then reversed for Rive's draw order.
"""
from __future__ import annotations
import json
import math
import re
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SIZE = 1254
SCALE = 500 / SIZE
PARTS = []
DARK = "06442B"
CREAM = "FFF4DE"


def group(name):
    part = {"name": name, "shapes": []}
    PARTS.append(part)
    return part


def path(part, name, d, fill, stroke=None, weight=8, gradient=None):
    part["shapes"].append(dict(name=name, d=d, fill=fill, stroke=stroke,
                               weight=weight, gradient=gradient))


def oval(part, name, cx, cy, rx, ry, fill, stroke=None, weight=8, gradient=None):
    k = .5522847498
    path(part, name, f"M {cx+rx} {cy} C {cx+rx} {cy+k*ry} {cx+k*rx} {cy+ry} {cx} {cy+ry} C {cx-k*rx} {cy+ry} {cx-rx} {cy+k*ry} {cx-rx} {cy} C {cx-rx} {cy-k*ry} {cx-k*rx} {cy-ry} {cx} {cy-ry} C {cx+k*rx} {cy-ry} {cx+rx} {cy-k*ry} {cx+rx} {cy} Z", fill, stroke, weight, gradient)


def mirrored(source, name):
    target = group(name)
    for shape in source["shapes"]:
        copy = dict(shape)
        copy["mirror"] = True
        target["shapes"].append(copy)
    return target


group("GroundShadow")
group("Tail")
foot = group("FootL")
path(foot,"ToeSilhouette", "M 480 1121 C 486 1134 480 1142 463 1148 C 426 1160 410 1183 413 1200 C 415 1217 444 1220 469 1208 C 483 1234 526 1222 540 1204 C 563 1217 591 1200 586 1178 C 582 1160 567 1150 553 1146 L 548 1121 Z", "F49A13", "A6530A", 8)
path(foot,"ToeLight", "M 481 1144 C 448 1151 418 1178 421 1192 C 429 1208 452 1191 477 1178 C 487 1171 497 1167 505 1163 C 482 1181 467 1199 477 1207 C 495 1222 530 1200 540 1175 C 538 1198 563 1202 574 1191 C 592 1175 571 1151 546 1148 Z", "FFC337", gradient=("FFD044","FFAE19",440,1140,527,1220))
mirrored(foot,"FootR")
body=group("Body")
path(body,"BodySilhouette", "M 489 730 C 427 756 397 835 392 939 C 381 1012 405 1090 461 1124 C 510 1154 553 1149 585 1124 L 626 1092 L 669 1124 C 700 1152 748 1153 793 1124 C 847 1094 873 1016 862 937 C 858 834 829 756 765 730 Z", "71B04B", DARK, 10, ("A9CD62","529D47",480,780,760,1140))
path(body,"LeftThighLeaf", "M 483 1042 C 500 1083 531 1082 556 1066 C 577 1083 576 1101 558 1108 C 523 1121 500 1095 483 1042 Z", "A9D462")
path(body,"RightThighLeaf", "M 771 1042 C 754 1083 723 1082 698 1066 C 677 1083 678 1101 696 1108 C 731 1121 754 1095 771 1042 Z", "A9D462")
chest=group("ChestPatch")
path(chest,"CreamUnderfeathers", "M 548 797 C 566 791 579 789 593 795 C 609 771 642 771 660 795 C 675 789 696 792 710 800 C 744 812 766 839 750 850 C 741 856 727 849 718 846 C 754 873 779 910 769 930 C 764 944 748 935 740 929 C 761 960 777 1005 761 1018 C 750 1028 735 1008 728 999 C 741 1062 687 1090 627 1120 C 566 1090 512 1062 525 999 C 518 1008 503 1028 492 1018 C 476 1005 492 960 513 929 C 505 935 489 944 484 930 C 474 910 499 873 535 846 C 526 849 512 856 503 850 C 487 839 509 811 548 797 Z", "EEDFC1")
path(chest,"CreamFeatherLight", "M 548 804 C 571 798 585 802 600 814 C 615 794 640 794 654 814 C 684 795 719 805 738 824 C 763 849 749 860 718 846 C 754 875 775 908 767 925 C 761 940 746 931 735 923 C 758 958 769 1001 756 1015 C 744 1026 729 998 723 989 C 727 1038 710 1067 692 1061 C 680 1057 674 1042 670 1027 C 659 1058 642 1071 626 1070 C 607 1069 590 1055 584 1027 C 577 1050 570 1062 558 1061 C 532 1063 514 1019 528 989 C 516 1009 501 1025 492 1014 C 480 999 492 956 514 923 C 501 934 488 940 484 926 C 477 907 500 874 535 846 C 502 862 489 850 503 831 C 516 813 535 807 548 804 Z", CREAM, gradient=("FFF8E9","FBF0D9",530,822,700,1060))
badge=group("AIBadge")
oval(badge,"CoreRim",627,917,91,91,"FFFBED")
oval(badge,"CoreMint",627,917,80,80,"57C68F",gradient=("50BB88","62CEA0",570,860,694,980))
path(badge,"LeafEmblem", "M 622 977 L 622 957 C 594 950 574 930 577 891 C 598 891 615 904 622 919 C 631 889 650 871 675 867 C 684 905 666 940 632 952 L 632 977 C 632 985 622 985 622 977 Z", "FFFFFF")
path(badge,"EmblemLeftCut", "M 620 947 C 611 933 599 922 590 915 C 604 920 615 927 620 947 Z", "59C894")
path(badge,"EmblemRightCut", "M 630 947 C 634 928 644 907 656 896 C 642 919 637 932 630 947 Z", "59C894")
wing=group("LeftWing")
path(wing,"LowerWingOutline", "M 414 814 C 460 837 463 921 434 1005 C 416 1051 372 1125 329 1143 C 310 1150 307 1126 308 1090 C 291 1100 272 1107 271 1083 C 266 1066 270 1046 273 1027 C 251 1041 238 1040 241 1012 C 246 937 306 813 371 784 C 389 776 405 781 414 814 Z", "075338", DARK, 10)
path(wing,"LongLowerFeather", "M 402 931 C 402 1021 373 1104 325 1129 C 310 1136 317 1080 324 1054 C 340 1009 370 964 402 931 Z", "085638")
path(wing,"MiddleLowerFeather", "M 404 909 C 421 956 401 1037 369 1068 C 346 1091 338 1056 345 1035 C 359 984 381 940 404 909 Z", "064F34", DARK, 9)
path(wing,"LongSideFeather", "M 369 901 C 368 972 333 1060 289 1090 C 271 1102 274 1049 282 1023 C 300 968 335 923 369 901 Z", "69AF47")
path(wing,"FoldedUpperWing", "M 381 782 C 412 765 439 784 454 821 C 470 861 465 903 445 950 C 429 985 408 1012 389 1011 C 367 1011 367 977 369 953 C 354 993 335 1010 317 1006 L 313 970 C 290 1006 261 1036 248 1033 C 226 1028 246 960 261 924 C 286 859 334 802 381 782 Z", "287D43", DARK, 10, ("4A9C47","196C3E",416,804,289,1018))
path(wing,"LongLimeCovert", "M 446 873 C 461 910 443 967 406 995 C 374 1021 363 993 370 961 C 373 940 382 923 387 913 C 385 930 390 940 395 946 C 419 926 438 900 446 873 Z", "A4D156")
path(wing,"UpperLeafCovert", "M 384 844 C 382 889 350 941 300 951 C 294 915 333 862 384 844 Z", "A9D75F", gradient=("B1DB65","8EC94D",342,850,343,950))
mirrored(wing,"RightWing")
head=group("HeadBase")
path(head,"HeadSilhouette", "M 471 265 C 510 239 570 225 626 227 C 687 225 745 239 783 265 C 888 286 965 388 996 505 C 1023 607 1004 704 930 762 C 882 797 813 791 758 779 C 694 795 560 795 496 779 C 436 799 368 795 322 759 C 246 700 232 607 258 506 C 288 389 368 286 471 265 Z", "49994B", DARK, 11, ("68AE50","297D43",373,330,861,783))
path(head,"LeftHeadLight", "M 367 366 C 291 440 257 509 260 578 C 263 650 292 704 335 732 C 293 650 291 506 367 366 Z", "6AAD50")
cheek=group("CheekFeathers")
for mirror in [False,True]:
    temp={"shapes":[]}
    path(temp,"CheekLower", "M 255 671 C 285 698 315 704 351 720 C 370 734 396 747 423 762 C 387 775 372 789 353 794 C 331 799 314 793 304 784 L 333 763 C 286 772 230 740 219 700 C 228 693 245 696 263 697 Z", "277D44", DARK, 9)
    path(temp,"CheekMidLight", "M 230 703 C 262 690 300 701 322 722 C 292 750 256 750 230 703 Z", "58A34B")
    path(temp,"CheekLeaf", "M 196 562 C 253 589 301 636 296 686 C 250 714 177 651 196 562 Z", "A6D35A", DARK, 10)
    path(temp,"CheekLeafShade", "M 246 634 C 270 647 287 664 289 690 C 266 693 251 666 246 634 Z", "71B54B")
    for item in temp['shapes']:
        item['name'] += "R" if mirror else "L"
        item['mirror']=mirror
        cheek['shapes'].append(item)
tuft=group("LeftHeadFeathers")
path(tuft,"CrownOuterTufts", "M 450 277 C 399 253 358 235 331 189 C 312 203 315 236 327 259 C 313 258 298 249 290 243 C 275 272 278 310 296 332 L 271 337 C 265 365 285 395 315 397 C 353 366 405 337 457 333 Z", "408F48", DARK, 11)
path(tuft,"CrownOuterLight", "M 278 344 C 303 348 331 343 353 331 C 340 354 314 370 290 370 C 281 362 278 352 278 344 Z", "6EB14E")
mirrored(tuft,"RightHeadFeathers")
crown=group("CrownPlumage")
path(crown,"LimeCrown", "M 331 198 C 373 246 445 265 507 280 C 531 285 551 304 561 323 C 549 300 534 286 520 280 C 570 280 611 318 627 362 C 643 318 684 280 734 280 C 720 286 705 300 693 323 C 703 304 723 285 747 280 C 809 265 881 246 923 198 C 928 224 913 263 882 286 C 901 284 917 280 930 270 C 922 302 901 321 866 317 C 880 324 890 335 896 347 C 841 324 794 332 748 351 C 681 380 645 433 627 523 C 609 433 573 380 506 351 C 460 332 413 324 358 347 C 364 335 374 324 388 317 C 353 321 332 302 324 270 C 337 280 353 284 372 286 C 341 263 326 224 331 198 Z", "AED66A", gradient=("B5D974","9FCC5D",500,243,665,499))
face=group("FaceMask")
path(face,"FacialDiscShadow", "M 626 522 C 613 435 557 354 478 354 C 371 342 301 443 301 570 C 294 679 364 767 499 770 C 521 772 541 769 554 765 C 530 785 540 805 580 791 C 590 812 609 827 627 829 C 645 827 664 812 674 791 C 714 805 724 785 700 765 C 713 769 733 772 755 770 C 890 767 960 679 953 570 C 953 443 883 342 776 354 C 697 354 640 435 626 522 Z", "E9DCBF")
path(face,"FacialDisc", "M 626 522 C 613 435 557 354 478 354 C 371 342 301 443 301 570 C 294 679 364 767 499 767 C 521 769 541 766 554 763 C 530 783 544 802 582 785 C 591 806 610 816 627 816 C 644 816 663 806 672 785 C 710 802 724 783 700 763 C 713 766 733 769 755 767 C 890 767 960 679 953 570 C 953 443 883 342 776 354 C 697 354 640 435 626 522 Z", CREAM, gradient=("FFFAE9","FCF0D9",400,400,820,760))
path(face,"BrowL", "M 462 411 C 486 379 523 393 538 436 C 513 417 486 406 462 411 Z", "CDDA9C")
path(face,"BrowR", "M 792 411 C 768 379 731 393 716 436 C 741 417 768 406 792 411 Z", "CDDA9C")


def eye(name, cx, mirrored_lash=False):
    e=group(name)
    # Center at (474,560); the right eye mirrors only its contour, not highlights.
    path(e,"UpperLash", "M 552 552 C 549 488 510 441 457 442 C 421 440 397 460 378 480 C 366 486 352 486 343 481 C 344 494 351 507 363 509 C 346 543 347 591 366 621 C 391 653 514 668 542 616 C 551 598 555 578 552 552 Z", "101313")
    path(e,"EyeWhite", "M 551 556 C 548 500 510 460 466 462 C 417 462 379 494 366 544 C 350 601 377 647 433 651 C 494 658 548 623 551 556 Z", "FEFEFB")
    oval(e,"IrisOutline",474,561,77,87,"073A23","052E1C",5)
    oval(e,"IrisGreen",474,561,73,82,"257D40",gradient=("0A5330","67B956",463,487,490,642))
    path(e,"LowerIrisLight", "M 411 574 C 421 600 446 620 475 622 C 502 623 523 602 535 573 C 554 612 515 644 476 642 C 435 644 401 616 411 574 Z", "65B958")
    oval(e,"Pupil",476,561,54,62,"062318",gradient=("041A15","072B1A",454,518,491,621))
    if mirrored_lash:
        for item in e['shapes']: item['mirror']=True
    # Glints remain upper-right for a single consistent light direction.
    oval(e,"MainCatchlight",cx+21,519,21,21,"FFFFFF")
    oval(e,"SmallCatchlight",cx-38,555,8,8,"FFFFFF")
    return e


eye("LeftEye",474)
eye("RightEye",780,True)
beak=group("Beak")
path(beak,"SmileRim", "M 574 614 C 574 649 596 700 626 706 C 656 700 678 649 678 614 Z", "FFB324","F39515",5)
path(beak,"SmileInterior", "M 584 626 C 590 660 608 689 626 692 C 644 689 662 660 668 626 C 640 617 612 617 584 626 Z", "3F100A")
path(beak,"Tongue", "M 600 668 C 611 652 638 651 653 667 C 644 682 635 690 626 691 C 616 689 607 680 600 668 Z", "E03920")
path(beak,"TongueLight", "M 603 673 C 618 660 638 661 649 674 C 640 686 631 690 626 690 C 618 688 610 682 603 673 Z", "F54B29")
path(beak,"UpperBeak", "M 570 612 C 585 603 598 571 622 568 C 648 563 665 601 682 612 C 693 624 672 626 658 631 C 643 634 637 644 627 645 C 616 645 610 635 596 632 C 580 628 561 625 570 612 Z", "FFBC32","B9510A",5,("FFD04B","FFAE24",621,577,627,645))
oval(beak,"BeakGlint",626,585,10,8,"FFD56A")
closed=group("BeakClosed")
path(closed,"ClosedBeak", "M 570 612 C 585 603 598 571 622 568 C 648 563 665 601 682 612 C 676 639 646 664 627 670 C 607 664 578 639 570 612 Z", "FFBA2E","B9510A",5)
path(closed,"ClosedSeam", "M 575 618 C 596 621 616 634 627 638 C 640 630 659 622 679 618",None,"D88113",4)
sprout=group("HeadLeaf")
path(sprout,"SmallLeafOutline", "M 631 216 C 578 228 533 187 525 138 C 578 128 620 147 640 186 Z", "68AB49",DARK,11)
path(sprout,"SmallLeafLight", "M 535 142 C 581 140 614 159 628 192 C 592 166 557 178 535 142 Z", "A8D35B")
path(sprout,"TallLeafOutline", "M 634 213 C 605 172 634 91 680 66 C 710 50 743 47 765 36 C 778 87 779 135 748 171 C 718 208 674 216 634 213 Z", "70B548",DARK,12)
path(sprout,"TallLeafLight", "M 638 195 C 626 153 648 98 684 78 C 709 63 745 60 760 48 C 765 71 768 93 764 116 C 738 148 683 153 657 186 C 672 157 699 119 724 92 C 683 120 651 159 638 195 Z", "A6D054",gradient=("B2D861","9FCC52",684,62,706,185))
path(sprout,"StemDark", "M 625 268 C 619 245 622 222 632 199 C 641 177 655 158 670 145 C 654 174 642 208 643 236 L 641 268 Z", DARK)
path(sprout,"StemLight", "M 625 267 C 620 241 624 219 635 200 C 643 184 654 169 670 145 C 651 181 638 218 638 267 Z", "69AF4B")


def vertices(d, mirror=False):
    tokens=re.findall(r"[MLCZ]|-?(?:\d*\.)?\d+(?:e[-+]?\d+)?",d)
    pts=[]; cursor=0; closed=False
    def point():
        nonlocal cursor
        x,y=map(float,tokens[cursor:cursor+2]);cursor+=2
        return ((SIZE-x if mirror else x)*SCALE,y*SCALE)
    while cursor<len(tokens):
        command=tokens[cursor];cursor+=1
        if command=='M':
            p=point();pts.append([p,p,p])
        elif command=='L':
            p=point();pts.append([p,p,p])
        elif command=='C':
            c1,c2,p=point(),point(),point();pts[-1][2]=c1;pts.append([p,c2,p])
        elif command=='Z':closed=True
        else:raise ValueError(command)
    if closed and pts[0][0]==pts[-1][0]:
        pts[0][1]=pts[-1][1];pts.pop()
    return pts,closed


def export(selected=None,name="Front"):
    root=ET.Element('Rive',version='1',kind='fragment')
    art=ET.SubElement(root,'Artboard',name=name,width='500',height='500',styleId='0:3',id='0:2')
    ET.SubElement(art,'LayoutComponentStyle',name='Style',id='0:3')
    serial=10
    def el(parent,tag,**attrs):
        nonlocal serial
        serial+=1
        return ET.SubElement(parent,tag,{**{k:str(v) for k,v in attrs.items()},'id':f'0:{serial}'})
    for part in reversed(PARTS):
        if selected is not None and part['name'] not in selected:continue
        g=el(art,'Node',name=part['name'])
        if part['name']=='BeakClosed' and selected is None:g.set('opacity','0')
        for shape in reversed(part['shapes']):
            s=el(g,'Shape',name=shape['name'])
            points,closed=vertices(shape['d'],shape.get('mirror',False))
            winding=sum(a[0][0]*b[0][1]-b[0][0]*a[0][1] for a,b in zip(points,points[1:]+points[:1]))>=0
            p=el(s,'PointsPath',name='Path',isClosed=str(closed).lower(),isClockwise=str(winding).lower())
            for xy,inc,out in points:
                dx,dy=inc[0]-xy[0],inc[1]-xy[1]
                ox,oy=out[0]-xy[0],out[1]-xy[1]
                el(p,'CubicDetachedVertex',x=xy[0],y=xy[1],inRotation=math.atan2(dy,dx),inDistance=math.hypot(dx,dy),outRotation=math.atan2(oy,ox),outDistance=math.hypot(ox,oy))
            if shape['fill']:
                f=el(s,'Fill',name='Fill')
                if shape['gradient']:
                    c1,c2,x1,y1,x2,y2=shape['gradient']
                    if shape.get('mirror'):x1,x2=SIZE-x1,SIZE-x2
                    gr=el(f,'LinearGradient',name='Soft light',startX=x1*SCALE,startY=y1*SCALE,endX=x2*SCALE,endY=y2*SCALE)
                    el(gr,'GradientStop',position=0,colorValue='FF'+c1);el(gr,'GradientStop',position=1,colorValue='FF'+c2)
                else:el(f,'SolidColor',name='Color',colorValue='FF'+shape['fill'])
            if shape['stroke']:
                st=el(s,'Stroke',name='Outline',thickness=shape['weight']*SCALE,join='round',cap='round')
                el(st,'SolidColor',name='Color',colorValue='FF'+shape['stroke'])
    ET.indent(root,space='  ')
    return root


def main():
    HERE.mkdir(exist_ok=True)
    ET.ElementTree(export()).write(HERE/'front.rml',encoding='utf-8')
    (HERE/'rive.yaml').write_text('name: ollie-front\nmain: Front\nexclude:\n  - build\n',encoding='utf-8')
    (HERE/'parts.json').write_text(json.dumps(PARTS,indent=2),encoding='utf-8')
    svg=ET.Element('svg',xmlns='http://www.w3.org/2000/svg',viewBox=f'0 0 {SIZE} {SIZE}',width='500',height='500')
    defs=ET.SubElement(svg,'defs')
    serial=0
    for part in PARTS:
        if part['name']=='BeakClosed':continue
        g=ET.SubElement(svg,'g',id=part['name'])
        for s in part['shapes']:
            serial+=1
            attrs={'d':s['d'],'fill':'#'+s['fill'] if s['fill'] else 'none','stroke-linecap':'round','stroke-linejoin':'round'}
            if s.get('mirror'):attrs['transform']=f'translate({SIZE},0) scale(-1,1)'
            if s['gradient']:
                c1,c2,x1,y1,x2,y2=s['gradient'];gid=f'g{serial}'
                gr=ET.SubElement(defs,'linearGradient',id=gid,gradientUnits='userSpaceOnUse',x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2))
                ET.SubElement(gr,'stop',offset='0',attrib={'stop-color':'#'+c1});ET.SubElement(gr,'stop',offset='1',attrib={'stop-color':'#'+c2})
                attrs['fill']=f'url(#{gid})'
            if s['stroke']:attrs.update(stroke='#'+s['stroke'],**{'stroke-width':str(s['weight'])})
            ET.SubElement(g,'path',attrs)
    ET.indent(svg,space='  ')
    ET.ElementTree(svg).write(HERE/'ollie-front.svg',encoding='utf-8')
    print(f'Front master: {len(PARTS)} named parts, {sum(len(p["shapes"]) for p in PARTS)} paths')


if __name__=='__main__':main()
