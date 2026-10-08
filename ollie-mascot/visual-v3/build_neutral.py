"""Rebuild Ollie's front view as layered, editable Bézier artwork.

The separate rig generator imports these named parts into the animated mascot.
"""

from __future__ import annotations

from math import atan2, hypot
from pathlib import Path
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
ROOT = ET.Element("Rive", {"version": "1", "kind": "fragment"})
ART = ET.SubElement(ROOT, "Artboard", {"name": "Neutral", "width": "500", "height": "500", "styleId": "0:3", "id": "0:2"})
ET.SubElement(ART, "LayoutComponentStyle", {"name": "Neutral Style", "id": "0:3"})
SERIAL = 10


def ident():
    global SERIAL
    SERIAL += 1
    return f"0:{SERIAL}"


def group(name, parent=ART):
    return ET.SubElement(parent, "Node", {"name": name, "id": ident()})


def path(parent, name, anchors, color, outline=None, weight=3.0, closed=True, corners=(), gradient=None):
    """anchors are hand-placed. Catmull tangents become smooth Bézier handles."""
    shape = ET.SubElement(parent, "Shape", {"name": name, "id": ident()})
    geom = ET.SubElement(shape, "PointsPath", {"name": "Path", "isClosed": str(closed).lower(), "id": ident()})
    n = len(anchors)
    for i, point in enumerate(anchors):
        x, y = point[:2]
        if i in corners:
            ET.SubElement(geom, "StraightVertex", {"x": str(x), "y": str(y), "radius": "2", "id": ident()})
            continue
        before = anchors[(i - 1) % n] if closed or i else anchors[0]
        after = anchors[(i + 1) % n] if closed or i < n - 1 else anchors[-1]
        dx, dy = after[0] - before[0], after[1] - before[1]
        direction = atan2(dy, dx)
        distance = min(42, hypot(dx, dy) * 0.215)
        if len(point) > 2:
            distance = point[2]
        ET.SubElement(geom, "CubicMirroredVertex", {
            "x": str(x), "y": str(y), "rotation": f"{direction:.5f}",
            "distance": f"{distance:.3f}", "id": ident(),
        })
    if color:
        fill = ET.SubElement(shape, "Fill", {"name": "Fill", "id": ident()})
        if gradient:
            first, last, start, end = gradient
            paint = ET.SubElement(fill, "LinearGradient", {
                "name": "Gentle light", "startX": str(start[0]), "startY": str(start[1]),
                "endX": str(end[0]), "endY": str(end[1]), "id": ident(),
            })
            ET.SubElement(paint, "GradientStop", {"colorValue": first, "position": "0", "id": ident()})
            ET.SubElement(paint, "GradientStop", {"colorValue": last, "position": "1", "id": ident()})
        else:
            ET.SubElement(fill, "SolidColor", {"name": "Color", "colorValue": color, "id": ident()})
    if outline:
        stroke = ET.SubElement(shape, "Stroke", {
            "name": "Outline", "thickness": str(weight), "join": "round", "cap": "round", "id": ident(),
        })
        ET.SubElement(stroke, "SolidColor", {"name": "Color", "colorValue": outline, "id": ident()})
    return shape


def dot(parent, name, x, y, width, height, color):
    shape = ET.SubElement(parent, "Shape", {"name": name, "x": str(x), "y": str(y), "id": ident()})
    ET.SubElement(shape, "Ellipse", {"name": "Path", "width": str(width), "height": str(height), "id": ident()})
    fill = ET.SubElement(shape, "Fill", {"name": "Fill", "id": ident()})
    ET.SubElement(fill, "SolidColor", {"name": "Color", "colorValue": color, "id": ident()})
    return shape


def mirror(points, center=250, offset=0):
    return [(2 * center - p[0] + offset, p[1], *p[2:]) for p in reversed(points)]


def oval(cx, cy, rx, ry, drift=0):
    return [
        (cx - 2, cy - ry), (cx + rx * .66, cy - ry * .78),
        (cx + rx + drift, cy), (cx + rx * .72, cy + ry * .75),
        (cx, cy + ry), (cx - rx * .72, cy + ry * .74),
        (cx - rx, cy), (cx - rx * .68, cy - ry * .76),
    ]


C = {
    "outline": "FF173F2A", "deep": "FF286B3B", "green": "FF44924D",
    "fresh": "FF78B95B", "light": "FFA2D66D", "cream": "FFFFF2CF",
    "cream_shadow": "FFEEDFB9", "cream_light": "FFFFF9E9",
    "iris_deep": "FF123E28", "iris_mid": "FF2F8A45", "iris_light": "FF79CE69",
    "orange": "FFF6A62B", "orange_shadow": "FFD97A18", "mint": "FF67DFC1",
    "white": "FFFFFFFF",
}


def eye(name, cx, cy, asymmetric=0):
    e = group(name)
    # Front-to-back order. All major eye contours are custom editable paths.
    path(e, "UpperLashTip", [
        (cx-35,cy-22),(cx-43,cy-31),(cx-39,cy-20),(cx-32,cy-16),
    ], C["outline"])
    path(e, "PrimaryHighlight", [(cx-16,cy-24),(cx-9,cy-26),(cx-3,cy-21),(cx-3,cy-12),(cx-9,cy-7),(cx-16,cy-12)], C["white"])
    path(e, "SoftReflection", [
        (cx-19,cy-26),(cx-7,cy-31),(cx+2,cy-27),(cx-10,cy-24),
    ], "79FFFFFF")
    dot(e, "SecondaryHighlight", cx + 10, cy + 12, 4.5, 5.5, C["white"])
    path(e, "Pupil", [(cx+1,cy-21),(cx+14,cy-12),(cx+18,cy+4),(cx+12,cy+21),(cx+1,cy+26),(cx-15,cy+18),(cx-18,cy+1),(cx-13,cy-13)], C["iris_deep"])
    path(e, "IrisBottomLight", [(cx-19,cy+8),(cx-13,cy+22),(cx+1,cy+28),(cx+16,cy+20),(cx+20,cy+6),(cx+11,cy+15),(cx-7,cy+18)], C["iris_light"])
    path(e, "IrisInner", [(cx,cy-24),(cx+17,cy-18),(cx+23,cy-2),(cx+20,cy+16),(cx+4,cy+29),(cx-14,cy+24),(cx-22,cy+7),(cx-20,cy-12)], C["iris_mid"], gradient=("FF185C35", "FF55AF59", (cx,cy-28), (cx,cy+32)))
    path(e, "IrisLight", [(cx-18,cy-12),(cx-9,cy-23),(cx+5,cy-23),(cx+12,cy-13),(cx+3,cy-5)], "5579CE69")
    path(e, "IrisSideLight", [
        (cx+17,cy-18),(cx+25,cy-4),(cx+23,cy+12),(cx+17,cy+19),
        (cx+19,cy+1),
    ], "7779CE69")
    path(e, "IrisOuter", [(cx,cy-33),(cx+23,cy-25),(cx+30,cy-3),(cx+26,cy+20),(cx+5,cy+35),(cx-19,cy+28),(cx-29,cy+6),(cx-26,cy-18)], C["iris_deep"])
    path(e, "EyeWhite", [
        (cx-2,cy-41),(cx+21,cy-35),(cx+36+asymmetric,cy-17),
        (cx+36+asymmetric,cy+10),(cx+22,cy+35),(cx+1,cy+41),
        (cx-22,cy+36),(cx-37,cy+12),(cx-35,cy-17),(cx-20,cy-35),
    ], C["white"], "783B6244", 1.1)
    path(e, "UpperLid", [
        (cx-36,cy-8),(cx-32,cy-29),(cx-17,cy-40),(cx+2,cy-42),
        (cx+27,cy-32),(cx+36,cy-13),
    ], None, C["outline"], 5.4, closed=False)
    path(e, "LowerLid", [
        (cx-28,cy+25),(cx-11,cy+39),(cx+7,cy+40),(cx+27,cy+24),
    ], None, "55286B3B", 1.8, closed=False)


def add_neutral():
    # Leaf sprout, front-most brand feature.
    sprout = group("HeadLeaf")
    path(sprout, "LeafShine", [(257,84),(264,64),(278,51),(276,68),(266,84)], "8DA2D66D")
    path(sprout, "MainLeaf", [(249,104),(254,78),(263,59),(278,44),(284,43),(285,60),(276,79),(260,98)], C["fresh"], C["outline"], 2.8, corners=(4,))
    path(sprout, "MainLeafVein", [(250,101),(260,77),(279,50)], None, C["deep"], 1.7, closed=False)
    path(sprout, "SideLeafShine", [(242,90),(224,76),(221,66),(236,75)], C["light"])
    path(sprout, "SmallLeaf", [(248,98),(235,94),(221,84),(213,66),(214,62),(232,68),(246,83)], C["green"], C["outline"], 2.4, corners=(4,))
    path(sprout, "SmallLeafVein", [(244,92),(229,78),(216,67)], None, C["fresh"], 1.5, closed=False)
    path(sprout, "BentStem", [(248,116),(248,102),(250,91),(257,80)], None, C["outline"], 3.1, closed=False)

    # Eye and beak shapes sit above the facial disk.
    eye("LeftEye", 201, 228, -1.2)
    eye("RightEye", 300, 229, 1.0)
    beak = group("Beak")
    path(beak, "BeakSpecular", [(241,277),(248,272),(254,273),(248,279)], "B3FFF2CF")
    path(beak, "CalmSmile", [(245,292),(251,295),(258,290)], None, C["orange_shadow"], 1.4, closed=False)
    path(beak, "BeakLower", [(241,283),(249,292),(258,283),(255,294),(249,297),(244,292)], C["orange_shadow"])
    path(beak, "BeakUpper", [(237,277),(244,270),(252,268),(260,274),(263,281),(258,285),(251,290),(244,287)], C["orange"], C["orange_shadow"], 2.2)

    # Subtle cheeks and sculpted owl facial disk.
    face = group("FaceMask")
    path(face, "NeckDown", [(217,305),(227,321),(242,329),(250,328),(257,332),(270,327),(282,308),(273,337),(261,343),(252,336),(242,344),(228,336)], C["cream"])
    path(face, "CheekWarmthL", [(153,262),(169,271),(186,276),(174,282),(157,277)], "27F6A62B")
    path(face, "CheekWarmthR", [(345,265),(355,271),(345,282),(330,275),(339,269)], "1EF6A62B")
    path(face, "LeftFaceVolume", [(166,170),(187,156),(207,156),(186,176),(166,213),(157,248),(156,217)], "43FFFFFF")
    path(face, "RightFaceShade", [(322,164),(345,178),(357,216),(350,260),(331,292),(307,310),(320,276),(336,230)], "28A99963")
    path(face, "LeftLobeGlow", [(250,183),(224,160),(195,157),(171,177),(159,210),(166,242),(187,269),(213,285),(233,286),(219,259),(213,221),(229,191)], "26FFFFFF")
    path(face, "RightLobeShade", [(251,181),(278,159),(313,161),(339,187),(348,219),(337,253),(317,273),(299,280),(318,250),(323,214),(302,184)], "16B9946B")
    path(face, "MaskLight", [
        (250,178),(276,156),(308,151),(335,166),(352,193),(355,227),
        (344,264),(320,293),(288,313),(264,327),(252,335),(237,326),
        (209,316),(180,295),(159,266),(147,228),(152,194),(173,165),
        (204,154),(228,156),
    ], C["cream"], gradient=("FFFFF8E4", "FFF5E7C7", (175,168), (335,319)))
    path(face, "MaskShadow", [
        (250,182),(278,158),(309,153),(337,167),(356,194),(360,230),
        (349,270),(324,298),(289,317),(266,333),(252,341),(235,332),
        (207,323),(175,300),(154,268),(142,228),(148,189),(170,161),
        (202,149),(226,151),
    ], C["cream_shadow"])

    # The reference crown is a fan of narrow feathers, not a flat green band.
    crown = group("CrownPlumage")
    path(crown, "LeftFeatherVein", [(177,131),(199,129),(224,143),(244,165)], None, "8831643C", 1.4, closed=False)
    path(crown, "RightFeatherVein", [(324,132),(302,128),(278,141),(256,165)], None, "8831643C", 1.4, closed=False)
    path(crown, "LeftUpperPlume", [(149,153),(163,126),(176,113),(185,124),(194,128),(216,139),(238,161),(250,181),(224,162),(197,148),(175,146)], C["light"])
    path(crown, "LeftInnerPlume", [(172,149),(186,123),(205,121),(220,133),(240,154),(249,179),(222,154),(200,141),(183,140)], C["fresh"])
    path(crown, "RightUpperPlume", [(353,151),(340,127),(327,114),(315,125),(303,128),(281,141),(260,160),(251,180),(279,162),(305,149),(327,146)], C["light"])
    path(crown, "RightInnerPlume", [(331,149),(313,123),(295,122),(279,133),(262,154),(252,179),(278,155),(301,141),(319,140)], C["fresh"])
    path(crown, "RootShade", [(215,119),(237,120),(251,130),(266,119),(284,123),(273,143),(258,157),(250,181),(240,155),(224,138)], "57286B3B")

    # Several swept feathers make the ears read as owl plumage rather than horns.
    tuft_left = group("LeftHeadFeathers")
    path(tuft_left, "TipLight", [(177,151),(153,132),(131,111),(127,94),(148,116),(182,131)], C["light"])
    path(tuft_left, "OuterFeather", [(178,154),(152,139),(132,121),(123,101),(125,92),(147,113),(167,127),(189,134)], C["green"], C["outline"], 2.8, corners=(4,))
    path(tuft_left, "MiddleFeather", [(187,154),(164,147),(143,133),(136,116),(154,127),(174,131),(197,138)], C["fresh"], C["outline"], 2.1)
    path(tuft_left, "InnerFeather", [(189,146),(178,131),(165,112),(181,123),(198,138)], C["light"])
    tuft_right = group("RightHeadFeathers")
    path(tuft_right, "TipLight", mirror([(177,151),(153,132),(131,111),(127,94),(148,116),(182,131)], offset=2), C["light"])
    path(tuft_right, "OuterFeather", mirror([(178,154),(152,139),(132,121),(123,101),(125,92),(147,113),(167,127),(189,134)], offset=2), C["green"], C["outline"], 2.8)
    path(tuft_right, "MiddleFeather", mirror([(187,154),(164,147),(143,133),(136,116),(154,127),(174,131),(197,138)], offset=2), C["fresh"], C["outline"], 2.1)
    path(tuft_right, "InnerFeather", mirror([(189,146),(178,131),(165,112),(181,123),(198,138)], offset=2), C["light"])

    cheeks = group("CheekFeathers")
    path(cheeks, "CheekLightL", [(153,278),(136,270),(120,271),(131,279),(147,284)], C["light"])
    path(cheeks, "CheekFeatherL2", [(151,277),(134,267),(109,266),(120,280),(140,288),(159,289)], C["fresh"], C["outline"], 2.1, corners=(2,))
    path(cheeks, "CheekFeatherL1", [(156,293),(135,286),(111,293),(125,305),(147,309),(165,300)], C["green"], C["outline"], 2.1, corners=(2,))
    path(cheeks, "CheekLowL", [(160,301),(139,301),(124,315),(145,318),(168,308)], C["deep"])
    path(cheeks, "CheekLightR", mirror([(153,278),(136,270),(120,271),(131,279),(147,284)], offset=1), C["light"])
    path(cheeks, "CheekFeatherR2", mirror([(151,277),(134,267),(109,266),(120,280),(140,288),(159,289)], offset=1), C["fresh"], C["outline"], 2.1)
    path(cheeks, "CheekFeatherR1", mirror([(156,293),(135,286),(111,293),(125,305),(147,309),(165,300)], offset=1), C["green"], C["outline"], 2.1)
    path(cheeks, "CheekLowR", mirror([(160,301),(139,301),(124,315),(145,318),(168,308)], offset=1), C["deep"])

    head = group("HeadBase")
    path(head, "CrownFeatherLeft", [(165,137),(190,122),(211,119),(233,127),(213,135),(190,145),(175,157)], "96A2D66D")
    path(head, "CrownFeatherRight", [(339,138),(313,121),(291,120),(267,128),(286,136),(307,146),(326,157)], "5D78B95B")
    path(head, "HeadHighlight", [(162,145),(194,119),(238,114),(265,123),(227,138),(185,159),(153,206)], "6278B95B")
    path(head, "HeadSideShade", [(310,122),(355,148),(381,193),(388,243),(381,278),(360,301),(331,321),(316,330),(336,296),(351,246),(349,196)], "48286B3B")
    path(head, "HeadContour", [
        (249,119),(283,111),(315,112),(343,121),(363,118),(374,123),
        (370,144),(385,176),(394,211),(391,247),(384,269),
        (390,280),(377,291),(357,298),(341,309),(306,327),(250,341),
        (204,334),(169,319),(144,307),(122,300),(108,287),(111,270),
        (104,244),(107,209),(119,173),(135,148),(129,126),(128,111),
        (145,119),(165,121),(190,111),(221,110),
    ], C["green"], C["outline"], 4.6,
        gradient=("FF55A45D", "FF3D8547", (150,140), (355,325)))
    ART.remove(cheeks)
    ART.insert(list(ART).index(head) + 1, cheeks)

    # The AI badge is deliberately smaller than the eyes.
    core = group("AIBadge")
    path(core, "OuterRing", oval(250,387,25,25), None, "A067DFC1", 2.0)
    path(core, "InnerArc", [(237,382),(241,374),(252,371),(263,377)], None, "B0FFFFFF", 1.8, closed=False)
    path(core, "BadgeStem", [(250,395),(250,403)], None, C["cream_light"], 1.9, closed=False)
    path(core, "BadgeLeafL", [(249,392),(241,386),(240,379),(247,383),(250,390)], C["cream_light"])
    path(core, "BadgeLeafR", [(252,392),(260,385),(260,378),(253,382),(250,390)], C["cream_light"])
    path(core, "BadgeInner", oval(250,387,18,18), "FF69BB91")
    path(core, "BadgeBacking", oval(250,387,22,22), "7867DFC1")
    path(core, "SoftGlow", oval(250,387,30,30), "2867DFC1")

    # Leaf-like flight feathers overlap from one shoulder. Sharp tips and
    # stepped lengths avoid the laminated shoulder-pad look of V2.
    wing_shapes = [
        ("FeatherGlint", [(155,329),(141,341),(128,359),(141,351),(158,336)], "B0A2D66D", None, 0),
        ("ShoulderLight", [(165,323),(148,327),(136,340),(150,334),(169,330)], C["light"], None, 0),
        ("LowerFeatherLight", [(145,389),(134,406),(129,422),(140,414),(153,398)], "7FA2D66D", None, 0),
        ("WingVein", [(161,333),(140,353),(124,382)], None, "A067DFC1", 1.7),
        ("WingDotA", [(139,357),(142,355),(144,358),(141,361)], C["mint"], None, 0),
        ("WingDotB", [(126,382),(129,380),(131,383),(128,386)], "B267DFC1", None, 0),
        ("TopFeather", [(169,317),(145,319),(125,337),(111,365),(105,392,0.8),(119,390),(139,373),(160,342)], C["green"], None, 0),
        ("TopFeatherLight", [(159,326),(140,334),(123,352),(115,373),(133,357),(155,339)], C["fresh"], None, 0),
        ("MiddleFeather", [(172,332),(152,337),(130,355),(111,387),(106,414,0.8),(126,409),(149,387),(168,355)], C["fresh"], None, 0),
        ("LongFeather", [(177,347),(158,355),(141,378),(124,411),(123,438,0.8),(144,429),(164,404),(180,366)], C["deep"], None, 0),
        ("ShortFeather", [(160,374),(143,392),(133,416),(127,430,0.8),(145,424),(161,401),(169,376)], C["green"], None, 0),
        ("Shoulder", [(175,313),(152,317),(134,331),(127,352),(137,370),(157,361),(178,340),(182,326)], C["deep"], None, 0),
        ("WingSilhouette", [(178,312),(152,313),(130,332),(110,365),(104,398),(105,417),(123,440),(147,431),(170,401),(183,356),(184,328)], C["deep"], C["outline"], 3.5),
    ]
    left_wing = group("LeftWing")
    right_wing = group("RightWing")
    for name, points, fill, stroke, weight in wing_shapes:
        path(left_wing, name, points, fill, stroke, weight)
        right_points = mirror(points, offset=-8 if name == "TipHighlight" else 2)
        path(right_wing, name, right_points, fill, stroke, weight)

    chest = group("ChestPatch")
    path(chest, "ThroatFeathers", [(217,329),(226,339),(234,342),(241,338),(250,350),(259,338),(267,342),(277,329),(269,352),(255,357),(249,363),(242,356),(230,353)], C["cream_light"])
    path(chest, "BreastFeatherL", [(216,389),(218,405),(230,420),(236,416),(229,430),(217,420),(206,405)], "79EEDFB9")
    path(chest, "BreastFeatherR", mirror([(216,389),(218,405),(230,420),(236,416),(229,430),(217,420),(206,405)], offset=1), "69EEDFB9")
    path(chest, "LowerBreastTufts", [(224,417),(235,426),(245,424),(251,437),(258,424),(269,426),(282,416),(270,439),(252,446),(236,439)], C["cream"])
    path(chest, "ChestLightPlane", [(220,349),(236,337),(248,338),(237,353),(222,380),(212,394),(207,377)], "29FFFFFF")
    path(chest, "ChestFeatherShade", [(250,319),(274,329),(295,353),(311,387),(306,410),(288,427),(272,431),(263,429),(250,443),(236,429),(227,431),(210,424),(193,407),(191,383),(207,349),(227,327)], C["cream_shadow"])
    path(chest, "ChestFeather", [(250,320),(271,329),(291,352),(305,384),(300,405),(284,422),(269,426),(260,425),(250,439),(239,425),(230,427),(215,420),(199,403),(197,384),(212,351),(230,329)], C["cream"],
         gradient=("FFFFF7DE", "FFF4E4C2", (205,335), (295,435)))

    body = group("Body")
    path(body, "BodyHighlight", [(190,335),(221,318),(257,319),(230,331),(197,364),(180,385)], "4078B95B")
    path(body, "BodyShadow", [(299,321),(328,352),(338,400),(314,432),(279,445),(294,416),(308,376)], "36286B3B")
    path(body, "BodyContour", [
        (235,306),(269,307),(299,322),(326,348),(341,385),(336,409),
        (314,432),(292,441),(276,438),(251,448),(227,440),(211,443),
        (186,433),(164,408),(158,378),(169,344),(197,319),
    ], C["green"], C["outline"], 4.4)

    feet = group("Feet")
    for cx, suffix in [(216,"L"),(288,"R")]:
        f = group("Foot" + suffix, feet)
        path(f, "ToeBumpA", oval(cx-14,447,12,9), C["orange"], C["orange_shadow"], 2.0)
        path(f, "ToeBumpB", oval(cx+1,448,13,9), C["orange"], C["orange_shadow"], 2.0)
        path(f, "ToeBumpC", oval(cx+17,447,10,8), C["orange"], C["orange_shadow"], 2.0)
        path(f, "FootPad", [(cx-26,449),(cx-18,440),(cx-1,437),(cx+17,440),(cx+27,448),(cx+12,454),(cx-13,454)], C["orange"], C["orange_shadow"], 2.4)

    tail = group("Tail")
    path(tail, "TailLeft", [(189,388),(157,396),(130,424),(148,442),(181,433),(201,414)], C["deep"], C["outline"], 2.7)
    path(tail, "TailRight", mirror([(189,388),(157,396),(130,424),(148,442),(181,433),(201,414)], offset=2), C["deep"], C["outline"], 2.7)
    shadow = group("GroundShadow")
    path(shadow, "Shadow", oval(251,459,104,9), "2B173F2A")


def main():
    add_neutral()
    ET.indent(ROOT, space="    ")
    ET.ElementTree(ROOT).write(HERE / "neutral.rml", encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
