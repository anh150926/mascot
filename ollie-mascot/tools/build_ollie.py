"""Build Ollie's RML artwork on the proven NezFocus animation scaffold.

The reference project is read only. Stable component IDs keep its state machine,
timelines, data binding, and tap listener wired to the replacement owl artwork.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
from math import atan2, hypot
import xml.etree.ElementTree as ET
from build_data import generate as generate_data


HERE = Path(__file__).resolve().parent.parent
SOURCE = HERE / "tools" / "scaffold"
NEXT_ID = 3000
ART_SOURCE = ET.parse(HERE / "artwork" / "front.rml").getroot().find("Artboard")
sys.path.insert(0, str(HERE / "artwork"))
from build_artwork import vertices, SCALE


def new_id() -> str:
    global NEXT_ID
    NEXT_ID += 1
    return f"0:{NEXT_ID}"


def element(parent, tag, name, fixed_id=None, **attrs):
    values = {k: str(v) for k, v in attrs.items() if v is not None}
    values.update(name=name, id=fixed_id or new_id())
    return ET.SubElement(parent, tag, values)


def node(parent, name, fixed_id=None, **attrs):
    return element(parent, "Node", name, fixed_id, **attrs)


def art_group(parent, name, x, y):
    """Place editable Ollie vectors under an existing animated rig component."""
    source = next(
        item for item in ART_SOURCE.iter("Node") if item.get("name") == name
    )
    artwork = deepcopy(source)
    artwork.set("x", str(x))
    artwork.set("y", str(y))
    artwork.attrib.pop("opacity", None)
    for item in artwork.iter():
        if "id" in item.attrib:
            item.set("id", new_id())
    parent.append(artwork)
    return artwork


def bezier(parent, name, d, color=None, outline=None, thickness=2):
    """Cubic expression paths use the same master image coordinate system."""
    s = element(parent, "Shape", name)
    points, closed = vertices(d)
    p = element(s, "PointsPath", "Path", isClosed=str(closed).lower())
    for xy, inc, out in points:
        dx, dy = inc[0]-xy[0], inc[1]-xy[1]
        ox, oy = out[0]-xy[0], out[1]-xy[1]
        element(p, "CubicDetachedVertex", "V", x=xy[0], y=xy[1],
                inRotation=atan2(dy, dx), inDistance=hypot(dx, dy),
                outRotation=atan2(oy, ox), outDistance=hypot(ox, oy))
    if color:
        paint(s, color, outline, thickness)
    elif outline:
        st = element(s, "Stroke", "Lid", thickness=thickness, cap="round", join="round")
        element(st, "SolidColor", "Color", colorValue=outline)
    return s


def paint(shape, color, outline=None, thickness=3):
    fill = element(shape, "Fill", "Fill")
    element(fill, "SolidColor", "Color", colorValue=color)
    if outline:
        stroke = element(shape, "Stroke", "Outline", thickness=thickness, join="round")
        element(stroke, "SolidColor", "Color", colorValue=outline)


def ellipse(parent, name, x, y, width, height, color, outline=None, thickness=3, fixed_id=None, **attrs):
    s = element(parent, "Shape", name, fixed_id, x=x, y=y, **attrs)
    element(s, "Ellipse", "Path", width=width, height=height)
    paint(s, color, outline, thickness)
    return s


def polygon(parent, name, points, color, outline=None, thickness=3, fixed_id=None, **attrs):
    s = element(parent, "Shape", name, fixed_id, **attrs)
    p = element(s, "PointsPath", "Path", isClosed="true")
    for x, y, radius in points:
        element(p, "StraightVertex", "V", x=x, y=y, radius=radius)
    paint(s, color, outline, thickness)
    return s


def line(parent, name, points, color, thickness=4, fixed_id=None, **attrs):
    s = element(parent, "Shape", name, fixed_id, **attrs)
    p = element(s, "PointsPath", "Path", isClosed="false")
    for x, y in points:
        element(p, "StraightVertex", "V", x=x, y=y, radius=2)
    st = element(s, "Stroke", "Stroke", thickness=thickness, join="round", cap="round")
    element(st, "SolidColor", "Color", colorValue=color)
    return s


def curved(parent, name, points, color, outline=None, thickness=3):
    s = element(parent, "Shape", name)
    p = element(s, "PointsPath", "Path", isClosed="true")
    for x, y, rotation, distance in points:
        element(p, "CubicMirroredVertex", "V", x=x, y=y, rotation=rotation, distance=distance)
    paint(s, color, outline, thickness)
    return s


DARK = "FF14463A"
OUTLINE = "FF173D2B"
FOREST = "FF2E7040"
GREEN = "FF448C4D"
MID = "FF65AB57"
LIGHT = "FF8DCA8E"
PALE = "FFB5D7A4"
CREAM = "FFFAF2DB"
WHITE = "FFFFFBEF"
ORANGE = "FFFDC255"
BEAK_DARK = "FFE48921"
MINT = "FF74F5D0"


def add_eye(parent, name, x, y, expression="open", scale=1):
    e = node(parent, name, x=x, y=y, scaleX=scale, scaleY=scale)
    if expression in ("closed", "wink", "sleep"):
        path_data = "M -94 28 C -65 -25 39 -49 79 10" if expression != "sleep" else "M -94 -4 C -53 51 40 54 79 -6"
        bezier(e, "ClosedLid", path_data, outline="FF101D18", thickness=4.8)
        return e
    source_name = "LeftEye" if name == "EyeL" else "RightEye"
    source_x, source_y = (474 if name == "EyeL" else 780)*SCALE, 561*SCALE
    if expression == "half":
        bezier(e, "LidEdge", "M -119 -8 C -64 10 35 10 79 -8", outline="FF13251B", thickness=3.5)
        bezier(e, "UpperLid", "M -128 -130 L 99 -130 L 99 -12 C 40 13 -65 13 -128 -9 Z", color="FFFFF4DE")
    artwork = art_group(e, source_name, -source_x, -source_y)
    if expression == "surprised":
        e.set("scaleX", "1.06");e.set("scaleY", "1.06")
    return e


def add_eyes_variant(solo, name, fixed_id, left="open", right="open", left_y=0, right_y=0):
    group = node(solo, name, fixed_id)
    add_eye(group, "EyeL", 474*SCALE-250, left_y, left)
    add_eye(group, "EyeR", 780*SCALE-250, right_y, right)
    return group


def add_beak(parent, name, fixed_id, opened=False, small=False, slant=False):
    g = node(parent, name, fixed_id)
    art_group(g, "BeakClosed" if (small and not opened) or slant else "Beak", -250, -250)
    if small and opened:
        g.set("scaleX", "0.74")
    if slant:
        g.set("rotation", "-0.10")
    return g


def add_fx(face):
    fx = element(face, "Solo", "FxSet", "0:19", activeComponentId="0:51")
    node(fx, "FxNone", "0:51")
    shine = node(fx, "FxShine", "0:52")
    ellipse(shine, "ShineDot", 139, -102, 12, 12, ORANGE)
    ellipse(shine, "ShineDot2", 154, -119, 6, 6, ORANGE)
    low = node(fx, "FxSparkleLow", "0:53")
    ellipse(low, "Sparkle", -139, -25, 12, 12, MINT)
    node(fx, "FxGlasses", "0:54")
    ex = node(fx, "FxExclaim", "0:55")
    line(ex, "Exclamation", [(132, -153), (132, -128)], ORANGE, 7)
    ellipse(ex, "ExclamationDot", 132, -117, 7, 7, ORANGE)
    zzz = node(fx, "FxZzz", "0:56")
    for i, (xx, yy) in enumerate([(130, -142), (153, -169)]):
        line(zzz, f"Z{i}", [(xx-8, yy-7), (xx+6, yy-7), (xx-7, yy+7), (xx+8, yy+7)], GREEN, 4)
    q = node(fx, "FxQuestion", "0:57")
    line(q, "QuestionCurl", [(122, -149), (132, -158), (144, -155), (149, -145), (134, -129), (134, -123)], GREEN, 5)
    ellipse(q, "QuestionDot", 134, -111, 6, 6, GREEN)
    snore = node(fx, "FxSnore", "0:58")
    for idx, (xx, yy) in enumerate([(110, -125), (142, -157), (170, -185)], 1):
        z = node(snore, f"Z{idx}", f"0:{700+idx}", x=xx, y=yy, opacity=0)
        line(z, "ZLetter", [(-9, -8), (8, -8), (-8, 8), (9, 8)], GREEN, 4)
    bubble = node(snore, "SleepBubble", "0:704", x=29, y=12, opacity=0)
    ellipse(bubble, "Bubble", 0, 0, 23, 19, "99B5D7A4", GREEN, 2)


def build_head(character):
    head = node(character, "Head", "0:11", y=-186)
    sprout = node(head, "HeadSprout", "0:12", x=0, y=-178)
    art_group(sprout, "HeadLeaf", -250, -114)

    face = node(head, "Face", "0:15")
    add_fx(face)
    mouth = element(face, "Solo", "MouthSet", "0:18", activeComponentId="0:41", y=-42)
    add_beak(mouth, "MouthSmile", "0:41")
    add_beak(mouth, "MouthOpen", "0:42", opened=True)
    add_beak(mouth, "MouthO", "0:43", opened=True, small=True)
    add_beak(mouth, "MouthSmall", "0:44", small=True)
    add_beak(mouth, "MouthSlant", "0:45", slant=True)

    blink = node(face, "EyeBlink", "0:16", y=561*SCALE-292)
    eyes = element(blink, "Solo", "EyesSet", "0:17", activeComponentId="0:31")
    add_eyes_variant(eyes, "EyesNeutral", "0:31")
    add_eyes_variant(eyes, "EyesHappy", "0:32", "closed", "closed")
    add_eyes_variant(eyes, "EyesWink", "0:33", "open", "wink")
    focused = add_eyes_variant(eyes, "EyesFocus", "0:34", "open", "open")
    add_eyes_variant(eyes, "EyesSurprised", "0:35", "surprised", "surprised")
    add_eyes_variant(eyes, "EyesSleepy", "0:36", "half", "half")
    confused = node(eyes, "EyesConfused", "0:37")
    add_eye(confused, "EyeL", 474*SCALE-250, -2, "open")
    add_eye(confused, "EyeR", 780*SCALE-250, 2, "open", 0.92)
    add_eyes_variant(eyes, "EyesSleeping", "0:38", "sleep", "sleep")

    art_group(face, "FaceMask", -250, -292)

    tufts = node(head, "HeadTufts", "0:13")
    art_group(tufts, "CrownPlumage", -250, -292)
    art_group(tufts, "LeftHeadFeathers", -250, -292)
    art_group(tufts, "RightHeadFeathers", -250, -292)
    art_group(tufts, "CheekFeathers", -250, -292)
    art_group(head, "HeadBase", -250, -292)


def build_body(character):
    body = node(character, "Body", "0:23")
    core = node(body, "AICore", "0:900", x=0, y=917*SCALE-478)
    art_group(core, "AIBadge", -250, -917*SCALE)
    art_group(body, "ChestPatch", -250, -478)
    art_group(body, "Body", -250, -478)
    for x, name, fixed, source_x in [(-34,"FootL","0:1427",216),(38,"FootR","0:1447",288)]:
        foot = node(body, name, fixed, x=x, y=-30)
        art_group(foot, name, -source_x, -448)


def build_wing(character, name, fixed_id, x, mirror=False):
    wing = node(character, name, fixed_id, x=x, y=-160)
    source_name = "RightWing" if mirror else "LeftWing"
    art_group(wing, source_name, -250 - x, -318)


def make_artwork(old_character):
    ch = ET.Element("Node", {"name": "Character", "id": "0:10", "x": "250", "y": "478"})
    build_head(ch)
    build_wing(ch, "WingL", "0:20", -84)
    build_wing(ch, "WingR", "0:21", 84, True)
    build_body(ch)
    art_group(ch, "Tail", -250, -478)
    art_group(ch, "GroundShadow", -250, -478)
    old_hit = next(e for e in old_character if e.attrib.get("name") == "HitArea")
    ch.append(deepcopy(old_hit))
    return ch


def add_core_motion(artboard):
    machine = next(e for e in artboard if e.tag == "StateMachine")
    layer = ET.Element("StateMachineLayer", {"name": "Core", "id": "0:9000"})
    ET.SubElement(layer, "AnyState", {"x": "0", "y": "-150", "id": "0:9001"})
    ET.SubElement(layer, "ExitState", {"x": "400", "y": "-150", "id": "0:9002"})
    entry = ET.SubElement(layer, "EntryState", {"x": "-250", "y": "0", "id": "0:9003"})
    ET.SubElement(entry, "StateTransition", {"stateToId": "0:9005", "id": "0:9004"})
    ET.SubElement(layer, "AnimationState", {"x": "0", "y": "0", "animationId": "0:425", "id": "0:9005"})
    mood_index = next(i for i, e in enumerate(machine) if e.attrib.get("name") == "Mood")
    machine.insert(mood_index, layer)

    animation = ET.SubElement(artboard, "LinearAnimation", {"loopValue": "loop", "duration": "150", "name": "core_breathe", "id": "0:425"})
    keyed = ET.SubElement(animation, "KeyedObject", {"objectId": "0:900", "id": "0:9010"})
    prop = ET.SubElement(keyed, "KeyedProperty", {"propertyKey": "18", "id": "0:9011"})
    for frame, value, kid in [(0, "0.88", 9012), (75, "1", 9014), (150, "0.88", 9016)]:
        attrs = {"value": value, "frame": str(frame), "id": f"0:{kid}"}
        if frame != 150:
            attrs["interpolationType"] = "cubic"
        key = ET.SubElement(prop, "KeyFrameDouble", attrs)
        if frame != 150:
            ET.SubElement(key, "CubicEaseInterpolator", {"x1": "0.42", "y1": "0", "x2": "0.58", "y2": "1", "id": f"0:{kid+1}"})

    for sleep in artboard.findall("LinearAnimation"):
        if sleep.attrib.get("name") != "sleep_loop":
            continue
        keyed = ET.SubElement(sleep, "KeyedObject", {"objectId": "0:900", "id": "0:9020"})
        prop = ET.SubElement(keyed, "KeyedProperty", {"propertyKey": "18", "id": "0:9021"})
        for frame, value, kid in [(0, "0.48", 9022), (120, "0.56", 9024), (240, "0.48", 9026)]:
            attrs = {"value": value, "frame": str(frame), "id": f"0:{kid}"}
            if frame != 240:
                attrs["interpolationType"] = "cubic"
            key = ET.SubElement(prop, "KeyFrameDouble", attrs)
            if frame != 240:
                ET.SubElement(key, "CubicEaseInterpolator", {"x1": "0.42", "y1": "0", "x2": "0.58", "y2": "1", "id": f"0:{kid+1}"})


def main():
    HERE.mkdir(exist_ok=True)
    (HERE / "tools").mkdir(exist_ok=True)
    (HERE / "reference").mkdir(exist_ok=True)
    generate_data()
    tree = ET.parse(SOURCE / "runtime.rml")
    artboard = tree.getroot().find("Artboard")
    for animation in artboard.findall("LinearAnimation"):
        name = animation.attrib.get("name")
        # Nez's sleeves rest at +/-0.36 rad. Ollie's master wings are already
        # folded. Retarget that rest pose and soften motion for the larger head.
        for keyed in animation.findall("KeyedObject"):
            oid = keyed.get("objectId")
            for prop in keyed.findall("KeyedProperty"):
                pk = prop.get("propertyKey")
                for key in prop.findall("KeyFrameDouble"):
                    value = float(key.get("value"))
                    if oid in ("0:20", "0:21") and pk == "15":
                        value -= .36 if oid == "0:20" else -.36
                    if oid == "0:13" and pk == "15": value *= .12
                    if oid == "0:10" and pk == "14": value = 478+(value-478)*.45
                    if oid == "0:10" and pk == "17": value = 1+(value-1)*.30
                    key.set("value", str(round(value, 6)))
        if name == "sleep_loop":
            for key in animation.iter("KeyFrameId"):
                if key.attrib.get("value") == "0:36":
                    key.set("value", "0:38")
        if name == "mood_sleepy":
            for key in animation.iter("KeyFrameId"):
                if key.attrib.get("value") == "0:56":
                    key.set("value", "0:51")
    old = next(e for e in artboard if e.attrib.get("name") == "Character")
    position = list(artboard).index(old)
    artboard.remove(old)
    artboard.insert(position, make_artwork(old))
    add_core_motion(artboard)
    # Bundle the view model so runtime.rml and review snapshots are self-contained.
    # data/model.json is canonical; data.rml is its generated, excluded sidecar.
    tree.getroot().extend(list(ET.parse(HERE / "data.rml").getroot()))
    ET.indent(tree, space="    ")
    tree.write(HERE / "runtime.rml", encoding="utf-8", xml_declaration=False)
    (HERE / "rive.yaml").write_text(
        "name: ollie-mascot\nmain: Runtime\nexclude:\n  - data.rml\n  - data\n  - speech\n  - docs\n  - tools\n  - tests\n  - reference\n  - dist\n  - artwork\n  - playground\n  - web-pet\n  - visual-v2\n  - visual-v3\nlogs:\n  file: build/rive.log\n  problems: build/problems.log\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
