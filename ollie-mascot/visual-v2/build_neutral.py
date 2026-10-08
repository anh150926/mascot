"""Author the neutral Ollie illustration as editable Rive Bézier artwork.

This visual checkpoint has no rig or animation. The existing functional mascot
stays in ../runtime.rml until this illustration is approved.
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
    path(e, "PrimaryHighlight", [(cx-14,cy-22),(cx-8,cy-24),(cx-3,cy-19),(cx-3,cy-11),(cx-8,cy-7),(cx-14,cy-11)], C["white"])
    path(e, "SoftReflection", [
        (cx-19,cy-26),(cx-7,cy-31),(cx+2,cy-27),(cx-10,cy-24),
    ], "79FFFFFF")
    dot(e, "SecondaryHighlight", cx + 10, cy + 12, 4.5, 5.5, C["white"])
    path(e, "Pupil", [(cx+1,cy-19),(cx+13,cy-11),(cx+17,cy+4),(cx+12,cy+19),(cx+1,cy+24),(cx-13,cy+17),(cx-16,cy+1),(cx-12,cy-12)], C["iris_deep"])
    path(e, "IrisBottomLight", [(cx-19,cy+8),(cx-13,cy+22),(cx+1,cy+28),(cx+16,cy+20),(cx+20,cy+6),(cx+11,cy+15),(cx-7,cy+18)], C["iris_light"])
    path(e, "IrisInner", [(cx,cy-24),(cx+17,cy-18),(cx+23,cy-2),(cx+20,cy+16),(cx+4,cy+29),(cx-14,cy+24),(cx-22,cy+7),(cx-20,cy-12)], C["iris_mid"])
    path(e, "IrisLight", [(cx-18,cy-12),(cx-9,cy-23),(cx+5,cy-23),(cx+12,cy-13),(cx+3,cy-5)], "5579CE69")
    path(e, "IrisSideLight", [
        (cx+17,cy-18),(cx+25,cy-4),(cx+23,cy+12),(cx+17,cy+19),
        (cx+19,cy+1),
    ], "7779CE69")
    path(e, "IrisOuter", [(cx,cy-31),(cx+21,cy-23),(cx+28,cy-3),(cx+25,cy+18),(cx+5,cy+33),(cx-18,cy+26),(cx-27,cy+6),(cx-24,cy-17)], C["iris_deep"])
    path(e, "EyeWhite", [
        (cx-2,cy-41),(cx+21,cy-35),(cx+36+asymmetric,cy-17),
        (cx+36+asymmetric,cy+10),(cx+22,cy+35),(cx+1,cy+41),
        (cx-22,cy+36),(cx-37,cy+12),(cx-35,cy-17),(cx-20,cy-35),
    ], C["cream_light"], C["outline"], 2.6)
    path(e, "UpperLid", [
        (cx-36,cy-8),(cx-32,cy-29),(cx-17,cy-40),(cx+2,cy-42),
        (cx+27,cy-32),(cx+36,cy-13),
    ], None, C["outline"], 4.4, closed=False)
    path(e, "LowerLid", [
        (cx-28,cy+25),(cx-11,cy+39),(cx+7,cy+40),(cx+27,cy+24),
    ], None, "55286B3B", 1.8, closed=False)


def add_neutral():
    # Leaf sprout, front-most brand feature.
    sprout = group("HeadLeaf")
    path(sprout, "MainLeafLight", [(257,78),(260,61),(273,51),(280,55),(276,70),(263,87)], C["light"])
    path(sprout, "MainLeaf", [(250,102),(252,78),(260,61),(271,51),(281,49),(281,63),(275,79),(261,96)], C["fresh"], C["outline"], 2.7)
    path(sprout, "MainLeafVein", [(251,99),(259,78),(274,58)], None, C["deep"], 1.7, closed=False)
    path(sprout, "SmallLeafLight", [(239,88),(225,79),(220,68),(235,72)], C["light"])
    path(sprout, "SmallLeaf", [(248,98),(232,95),(219,82),(217,68),(221,65),(238,71),(250,88)], C["fresh"], C["outline"], 2.4)
    path(sprout, "SmallLeafVein", [(244,93),(229,80),(221,72)], None, C["deep"], 1.5, closed=False)
    path(sprout, "BentStem", [(250,110),(249,98),(248,88),(251,77)], None, C["outline"], 2.9, closed=False)

    # Eye and beak shapes sit above the facial disk.
    eye("LeftEye", 201, 228, -1.2)
    eye("RightEye", 300, 229, 1.0)
    beak = group("Beak")
    path(beak, "BeakSpecular", [(244,274),(250,271),(255,273),(249,277)], "A7FFF2CF")
    path(beak, "CalmSmile", [(245,289),(250,294),(257,289)], None, C["orange_shadow"], 1.6, closed=False)
    path(beak, "BeakLower", [(241,281),(249,290),(261,280),(256,291),(250,295),(245,290)], C["orange_shadow"])
    path(beak, "BeakUpper", [(238,276),(245,269),(252,267),(260,272),(263,278),(257,284),(251,290),(244,284)], C["orange"], C["orange_shadow"], 2.3)

    # Subtle cheeks and sculpted owl facial disk.
    face = group("FaceMask")
    path(face, "NeckDown", [(224,316),(237,326),(249,331),(260,327),(278,315),(270,334),(260,339),(251,335),(244,341),(233,335)], C["cream"])
    path(face, "CheekWarmthL", [(156,264),(166,270),(178,273),(169,277),(157,273)], "20F6A62B")
    path(face, "CheekWarmthR", [(345,263),(355,270),(345,277),(332,274),(341,269)], "20F6A62B")
    path(face, "MaskLight", [
        (250,183),(276,156),(317,153),(345,182),(351,224),(339,268),
        (308,300),(270,316),(252,329),(232,318),(198,304),(166,270),
        (151,227),(157,186),(184,157),(219,154),
    ], C["cream"], gradient=("FFFFF8E3", "FFFFEBCB", (165,165), (335,320)))
    path(face, "MaskShadow", [
        (250,188),(279,159),(320,156),(349,184),(356,229),(344,275),
        (310,309),(271,324),(252,334),(230,324),(196,312),(162,277),
        (146,232),(153,183),(183,154),(218,156),
    ], C["cream_shadow"])

    # Forehead plumage sits beneath the facial disk. Curved overlapping lobes
    # break the plain green crown without crossing the eyes.
    crown = group("CrownPlumage")
    path(crown, "CrestLightLeft", [
        (139,147),(154,128),(173,116),(183,118),(177,126),
        (196,124),(216,136),(238,158),(249,180),(225,160),
        (201,147),(177,145),(155,153),
    ], C["fresh"])
    path(crown, "CrestLightRight", [
        (360,149),(345,130),(324,118),(315,121),(324,130),
        (304,127),(286,139),(265,159),(250,181),(276,164),
        (300,150),(326,149),(345,156),
    ], C["light"])
    path(crown, "CrestCenterShade", [
        (211,120),(231,119),(250,128),(269,118),(292,121),
        (276,140),(260,154),(250,174),(239,154),(225,138),
    ], "7331643C")
    path(crown, "CrestFeatherLeft", [
        (177,130),(194,128),(211,136),(225,148),
    ], None, "8B286B3B", 1.5, closed=False)
    path(crown, "CrestFeatherRight", [
        (324,131),(306,128),(289,138),(275,150),
    ], None, "8B286B3B", 1.5, closed=False)

    # Feather tufts are layered leaf forms rather than cat-ear triangles.
    tuft_left = group("LeftHeadFeathers")
    path(tuft_left, "InnerTuft", [(181,148),(160,138),(145,125),(140,113),(159,123),(188,136)], C["light"])
    path(tuft_left, "MiddleTuft", [(180,151),(156,138),(140,122),(131,108),(131,104),(147,116),(165,125),(189,133)], C["fresh"], C["outline"], 2.8)
    path(tuft_left, "LowerTuft", [(188,151),(164,149),(146,139),(135,123),(149,130),(171,132),(197,140)], C["green"], C["outline"], 2.5)
    path(tuft_left, "TuftShadow", [(162,151),(140,140),(130,122),(146,137)], C["deep"])
    path(tuft_left, "SmallFeather", [
        (163,145),(151,141),(140,133),(149,137),(163,137),(177,143),
    ], C["light"])
    tuft_right = group("RightHeadFeathers")
    path(tuft_right, "InnerTuft", mirror([(181,148),(160,138),(145,125),(140,113),(159,123),(188,136)], offset=3), C["light"])
    path(tuft_right, "MiddleTuft", mirror([(180,151),(156,138),(140,122),(131,108),(131,104),(147,116),(165,125),(189,133)], offset=4), C["fresh"], C["outline"], 2.8)
    path(tuft_right, "LowerTuft", mirror([(188,151),(164,149),(146,139),(135,123),(149,130),(171,132),(197,140)], offset=3), C["green"], C["outline"], 2.5)
    path(tuft_right, "TuftShadow", mirror([(162,151),(140,140),(130,122),(146,137)], offset=3), C["deep"])
    path(tuft_right, "SmallFeather", mirror([
        (163,145),(151,141),(140,133),(149,137),(163,137),(177,143),
    ], offset=3), C["light"])

    cheeks = group("CheekFeathers")
    path(cheeks, "CheekFeatherL2", [(146,282),(123,271),(98,279),(103,294),(127,302),(157,296)], C["fresh"], C["outline"], 2.5)
    path(cheeks, "CheekFeatherL1", [(151,296),(129,294),(105,305),(116,317),(145,321),(165,305)], C["green"], C["outline"], 2.5)
    path(cheeks, "CheekFeatherR2", mirror([(146,282),(123,271),(98,279),(103,294),(127,302),(157,296)], offset=1), C["fresh"], C["outline"], 2.5)
    path(cheeks, "CheekFeatherR1", mirror([(151,296),(129,294),(105,305),(116,317),(145,321),(165,305)], offset=1), C["green"], C["outline"], 2.5)
    path(cheeks, "CheekAccentL", [(130,289),(115,286),(106,290),(122,295),(140,297)], C["light"])
    path(cheeks, "CheekAccentR", mirror([(130,289),(115,286),(106,290),(122,295),(140,297)], offset=1), C["light"])

    head = group("HeadBase")
    path(head, "CrownFeatherLeft", [(165,136),(187,119),(211,116),(235,124),(217,130),(195,139),(178,153)], "A0A2D66D")
    path(head, "CrownFeatherRight", [(337,137),(311,119),(289,118),(266,126),(283,132),(308,141),(326,155)], "5778B95B")
    path(head, "HeadHighlight", [(166,139),(195,113),(248,108),(265,117),(231,129),(193,153),(165,184),(144,203)], "5478B95B")
    path(head, "HeadSideShade", [(314,119),(351,150),(378,194),(384,247),(368,291),(340,322),(314,336),(330,296),(346,251),(347,197)], "40286B3B")
    path(head, "HeadContour", [
        (250,119),(283,111),(316,109),(345,116),(365,116),(373,119),
        (371,137),(386,169),(398,207),(397,240),(388,267),
        (389,284),(373,294),(351,302),(340,310),(307,326),(252,340),
        (199,330),(162,313),(139,299),(116,294),(106,284),(110,268),
        (102,241),(102,209),(114,172),(130,146),(129,128),(130,119),
        (147,117),(166,120),(189,109),(221,109),
    ], C["green"], C["outline"], 4.6,
        gradient=("FF55A45D", "FF3D8547", (150,140), (355,325)))
    ART.remove(cheeks)
    ART.insert(list(ART).index(head) + 1, cheeks)

    # The AI badge is deliberately smaller than the eyes.
    core = group("AIBadge")
    path(core, "BadgeStem", [(250,395),(250,403)], None, C["cream_light"], 1.9, closed=False)
    path(core, "BadgeLeafL", [(249,392),(241,386),(240,379),(247,383),(250,390)], C["cream_light"])
    path(core, "BadgeLeafR", [(252,392),(260,385),(260,378),(253,382),(250,390)], C["cream_light"])
    path(core, "BadgeInner", oval(250,387,18,18), "FF69BB91")
    path(core, "BadgeBacking", oval(250,387,22,22), "7867DFC1")

    # Small shoulder plus four independently tapering feathers. Their tips form
    # a stepped wing edge instead of one enclosing armor/glove contour.
    wing_shapes = [
        ("TipHighlight", [(148,331),(135,340),(121,355),(137,350),(158,338)], C["light"], None, 0),
        ("FeatherGlint", [(146,349),(137,362),(127,380),(140,366),(154,352)], "8BA2D66D", None, 0),
        ("FeatherVein", [(153,340),(139,358),(130,377)], None, "A067DFC1", 1.6),
        ("PrimaryFeatherA", [(164,324),(144,325),(127,338),(115,354),(108,374),(111,392),(118,399),(134,384),(153,360),(170,336)], C["fresh"], C["outline"], 2.4),
        ("PrimaryFeatherB", [(169,333),(149,338),(133,354),(119,379),(112,401),(116,414),(125,419),(142,402),(158,377),(174,346)], C["green"], C["outline"], 2.4),
        ("PrimaryFeatherC", [(175,346),(157,356),(143,378),(132,403),(129,421),(135,430),(145,432),(161,410),(175,379),(182,356)], C["deep"], C["outline"], 2.4),
        ("SecondaryFeather", [(154,365),(138,384),(126,402),(121,418),(126,425),(138,421),(148,405),(160,378)], C["green"], C["outline"], 2.2),
        ("WingBase", [(164,316),(146,320),(131,333),(127,353),(139,370),(159,363),(178,341),(177,324)], C["deep"], C["outline"], 3.5),
    ]
    left_wing = group("LeftWing")
    right_wing = group("RightWing")
    for name, points, fill, stroke, weight in wing_shapes:
        path(left_wing, name, points, fill, stroke, weight)
        right_points = mirror(points, offset=-8 if name == "TipHighlight" else 2)
        path(right_wing, name, right_points, fill, stroke, weight)

    chest = group("ChestPatch")
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
