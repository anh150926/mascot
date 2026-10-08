"""Lay out exact neutral RML components on a diagnostic artboard."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SOURCE = ET.parse(HERE / "neutral.rml").getroot()
NEUTRAL = SOURCE.find("Artboard")

PARTS = [
    ("HeadBase", "Đầu"), ("FaceMask", "Mặt kem"),
    ("LeftEye", "Mắt trái · nhiều lớp"), ("RightEye", "Mắt phải · nhiều lớp"),
    ("Beak", "Mỏ"), ("LeftWing", "Cánh trái · nhiều lớp"),
    ("RightWing", "Cánh phải · nhiều lớp"), ("Body", "Thân"),
    ("ChestPatch", "Ngực"), ("FootL", "Chân trái"),
    ("FootR", "Chân phải"), ("HeadLeaf", "Mầm lá"),
    ("Tail", "Đuôi"), ("AIBadge", "Huy hiệu AI"),
    ("LeftHeadFeathers", "Lông đầu trái"),
    ("RightHeadFeathers", "Lông đầu phải"),
    ("CheekFeathers", "Lông má"),
]


def find_group(name: str) -> ET.Element:
    for element in NEUTRAL.iter("Node"):
        if element.get("name") == name:
            return element
    raise ValueError(name)


def bounds(element: ET.Element) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for vertex in element.iter():
        if vertex.tag in {"CubicMirroredVertex", "StraightVertex"}:
            xs.append(float(vertex.get("x", 0)))
            ys.append(float(vertex.get("y", 0)))
        elif vertex.tag == "Shape":
            ellipse = vertex.find("Ellipse")
            if ellipse is not None:
                x = float(vertex.get("x", 0))
                y = float(vertex.get("y", 0))
                w = float(ellipse.get("width", 0))
                h = float(ellipse.get("height", 0))
                xs.extend((x - w / 2, x + w / 2))
                ys.extend((y - h / 2, y + h / 2))
    return min(xs), min(ys), max(xs), max(ys)


def main() -> None:
    root = ET.Element("Rive", {"version": "1", "kind": "fragment"})
    art = ET.SubElement(root, "Artboard", {
        "name": "Parts", "width": "1500", "height": "1200",
        "x": "560", "y": "0",
        "styleId": "0:20001", "id": "0:20000",
    })
    ET.SubElement(art, "LayoutComponentStyle", {"name": "Parts Style", "id": "0:20001"})
    next_id = 20010
    for index, (name, _) in enumerate(PARTS):
        source = find_group(name)
        x0, y0, x1, y1 = bounds(source)
        scale = min(220 / max(1, x1-x0), 195 / max(1, y1-y0), 3.2)
        col, row = index % 5, index // 5
        center_x, center_y = col * 300 + 150, row * 300 + 143
        copy = deepcopy(source)
        copy.set("x", f"{center_x - scale * (x0+x1)/2:.3f}")
        copy.set("y", f"{center_y - scale * (y0+y1)/2:.3f}")
        copy.set("scaleX", f"{scale:.4f}")
        copy.set("scaleY", f"{scale:.4f}")
        for item in copy.iter():
            if "id" in item.attrib:
                next_id += 1
                item.set("id", f"0:{next_id}")
        art.append(copy)
    ET.indent(root, space="    ")
    ET.ElementTree(root).write(HERE / "parts.rml", encoding="utf-8", xml_declaration=False)


def label_screenshot() -> None:
    image_path = HERE / "build" / "ollie_parts.png"
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 21)
    except OSError:
        font = ImageFont.load_default()
    for index, (name, label) in enumerate(PARTS):
        col, row = index % 5, index // 5
        x, y = col * 300, row * 300
        draw.rounded_rectangle((x + 6, y + 5, x + 294, y + 292), radius=18,
                               outline=(82, 119, 101), width=2)
        draw.text((x + 18, y + 251), label, fill=(236, 247, 230), font=font)
        draw.text((x + 18, y + 275), name, fill=(154, 190, 165))
    image.save(image_path)


if __name__ == "__main__":
    main()
