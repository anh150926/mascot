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

sys.path.insert(0, str(ROOT / "artwork"))
from build_artwork import PARTS, vertices
from wing_poses import HOLD_SOURCE


def svg_path(source):
    points, closed = vertices(source["d"])

    def xy(p):
        return f"{p[0]:.3f} {p[1]:.3f}"

    d = "M " + xy(points[0][0])
    for i in range(1, len(points)):
        d += " C " + xy(points[i - 1][2]) + " " + xy(points[i][1]) + " " + xy(points[i][0])
    if closed:
        d += " C " + xy(points[-1][2]) + " " + xy(points[0][1]) + " " + xy(points[0][0]) + " Z"
    return d


def anatomy(destination):
    sources = next(p for p in PARTS if p["name"] == "LeftWing")["shapes"]
    names = [
        "01 · Khối cánh tối",
        "02 · Lông dài phía sau",
        "03 · Lông giữa",
        "04 · Lông bên",
        "05 · Mảng cánh trên",
        "06 · Lông phủ xanh non",
        "07 · Lá sáng trên cánh",
        "08 · Ghép đủ bảy lớp",
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" role="img" aria-label="Bảy lớp cánh gốc Ollie"><rect width="960" height="560" fill="#f5f7ef"/>'
    ]
    for i, label in enumerate(names):
        x = 12 + (i % 4) * 240
        y = 12 + (i // 4) * 280
        parts.append(
            f'<rect x="{x}" y="{y}" width="228" height="256" rx="16" fill="#fffdf5" stroke="#d2dfce"/><g transform="translate({x-61} {y-365}) scale(1.25)">'
        )
        for j, source in enumerate(sources if i == 7 else [sources[i]]):
            fill = "#" + source["fill"]
            gradient = source["gradient"]
            if gradient:
                c1, c2, x1, y1, x2, y2 = gradient
                gid = f"g{i}_{j}"
                parts.append(
                    f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1*500/1254}" y1="{y1*500/1254}" x2="{x2*500/1254}" y2="{y2*500/1254}"><stop stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}"/></linearGradient></defs>'
                )
                fill = f"url(#{gid})"
            stroke = "#" + source["stroke"] if source["stroke"] else "none"
            parts.append(
                f'<path d="{svg_path(source)}" fill="{fill}" stroke="{stroke}" stroke-width="{source["weight"]*500/1254}" stroke-linejoin="round" stroke-linecap="round"/>'
            )
        parts.append(
            f'</g><text x="{x+12}" y="{y+240}" fill="#164632" font-family="Segoe UI,sans-serif" font-size="15">{label}</text>'
        )
    parts.append("</svg>")
    destination.write_text("".join(parts), encoding="utf-8")


def soft_anatomy(destination):
    """Show both original wing contours used by every posed expression."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 370" role="img" aria-label="Hai cánh gốc Ollie dùng cho cử chỉ và cầm đồ">',
        '<rect width="840" height="370" rx="18" fill="#f5f7ef"/>',
    ]
    for x, title, side in [
        (12, "Cánh trái: bảy lớp lông gốc", "L"),
        (426, "Cánh phải: phản chiếu từ mẫu gốc", "R"),
    ]:
        parts.append(
            f'<rect x="{x}" y="10" width="402" height="350" rx="16" fill="#fffdf5" stroke="#d2dfce"/>'
        )
        view_x = 69 if side == "L" else 271
        parts.append(
            f'<svg x="{x+30}" y="24" width="340" height="290" viewBox="{view_x} 305 160 169">'
        )
        if side == "R":
            parts.append('<g transform="translate(500 0) scale(-1 1)">')
        for item in HOLD_SOURCE:
            fill = "#" + item["fill"]
            if item.get("gradient"):
                c1, c2, x1, y1, x2, y2 = item["gradient"]
                gid = item["name"]
                parts.append(
                    f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}"/></linearGradient></defs>'
                )
                fill = f"url(#{gid})"
            stroke = "#" + item["stroke"] if item["stroke"] else "none"
            d = svg_path(item) if item.get("master") else item["d"]
            parts.append(
                f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{item["weight"]}" stroke-linejoin="round" stroke-linecap="round"/>'
            )
        if side == "R":
            parts.append("</g>")
        parts.append(
            f'</svg><text x="{x+17}" y="340" fill="#164632" font-family="Segoe UI,sans-serif" font-size="17">{escape(title)}</text>'
        )
    parts.append("</svg>")
    destination.write_text("".join(parts), encoding="utf-8")


def main():
    out = ROOT / "playground/frames/wings"
    out.mkdir(parents=True, exist_ok=True)
    anatomy(out / "anatomy.svg")
    soft_anatomy(out / "soft-anatomy.svg")
    scenes = read("data/expressions.json")["expressions"]
    # Full-resolution stills make the contact edges easy to inspect in build/.
    detail = ROOT / "build/wing-redesign"
    detail.mkdir(parents=True, exist_ok=True)
    focus = (
        "meditate",
        "worried",
        "idea",
        "bedtime",
        "love",
        "nutrition",
        "sad",
        "wallet",
        "saving",
        "checklist",
        "alarm",
        "letter",
        "pomodoro",
        "workout",
        "celebrate",
    )
    labels = {spec["key"]: spec["label"] for spec in scenes}
    for key in focus:
        for suffix in ("", "-alpha"):
            shutil.copy2(
                ROOT / f"build/expressions/{key}-50{suffix}.png", detail / f"{key}{suffix}.png"
            )
        phases = [("Đầu", 0), ("¼", 25), ("Giữa", 50), ("¾", 75), ("Cuối", 100)]
        frames = [
            (label, Image.open(ROOT / f"build/expressions/{key}-{frame}-alpha.png").convert("RGBA"))
            for label, frame in phases
        ]
        sheet(frames, detail / f"{key}-motion.png", cols=5, size=260, title=labels[key])
    cards = "\n".join(
        "      <figure>\n"
        f'        <img loading="lazy" src="{key}-motion.png" '
        f'alt="{escape(labels[key])}: năm mốc chuyển động" />\n'
        "        <figcaption>\n"
        f'          <a href="{key}-alpha.png">'
        f"Xem khung giữa ở 500 px · {escape(labels[key])}</a>\n"
        "        </figcaption>\n"
        "      </figure>"
        for key in focus
    )
    template = (ROOT / "tools/templates/wing-redesign.html").read_text(encoding="utf-8")
    (detail / "index.html").write_text(
        template.replace("      <!-- MOTION_CARDS -->", cards), encoding="utf-8"
    )
    for spec in scenes:
        for frame in (0, 25, 50, 75, 100):
            source = ROOT / f'build/expressions/{spec["key"]}-{frame}-alpha.png'
            Image.open(source).save(out / f'{spec["key"]}-{frame}.webp', lossless=True)
    options = "\n".join(
        f'            <option value="{spec["key"]}"'
        + (" selected" if spec["key"] == "letter" else "")
        + f'>{escape(spec["label"])}</option>'
        for spec in scenes
    )
    template = (ROOT / "tools/templates/wing-review.html").read_text(encoding="utf-8")
    html = template.replace("            <!-- SCENE_OPTIONS -->", options)
    scene_data = json.dumps(scenes, ensure_ascii=False, indent=2).replace("\n", "\n      ")
    html = html.replace("__SCENES__", scene_data)
    (ROOT / "playground/wing-review.html").write_text(html, encoding="utf-8")
    print(
        f"Wing review ready: original feathers in every posed scene; {len(scenes)} scenes x 5 frames.",
        flush=True,
    )


if __name__ == "__main__":
    main()
