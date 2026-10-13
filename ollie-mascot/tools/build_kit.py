"""One command regenerates Ollie's artwork, rig, probes, review sheets and .riv."""

from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
from kit_common import ROOT, BUILD, run, render, clean, sheet
import check
import overlay
import trace
import build_data
import package_expo
import sync_cli_docs
from export_web_frames import main as export_frames
from build_expressions import main as export_expressions
from build_wing_review import main as export_wing_review

sys.path.insert(0, str(ROOT / "artwork"))
import build_artwork as art


def python(path):
    subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, check=True)


def stage(ident, names, review_only=False):
    if review_only:
        return clean(BUILD / f"probe-{ident}.png")
    project = BUILD / "rv/stages" / ident
    project.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(art.export(names)).write(project / "scene.rml", encoding="utf-8")
    (project / "rive.yaml").write_text(f"name: {ident}\nmain: Front\n", encoding="utf-8")
    target = BUILD / f"probe-{ident}.png"
    render(target, project=str(project))
    return clean(target)


def write_review(report):
    cards = "\n".join(
        "          <figure>\n"
        f'            <img loading="lazy" src="build/probe-{capture["id"]}.png" '
        f'alt="{capture["id"]}" />\n'
        f'            <figcaption>{capture["id"]}</figcaption>\n'
        "          </figure>"
        for capture in report["captures"]
    )
    template = (ROOT / "tools/templates/review.html").read_text(encoding="utf-8")
    html = template.replace("__PROBE_COUNT__", str(len(report["captures"])))
    html = html.replace("          <!-- PROBE_CARDS -->", cards)
    (ROOT / "review.html").write_text(html, encoding="utf-8")


def main(review_only=False):
    BUILD.mkdir(exist_ok=True)
    sync_cli_docs.sync()
    source = ROOT / "reference/ollie-front-master.png"
    im = Image.open(source).convert("RGBA")
    im.resize((500, 500), Image.Resampling.LANCZOS).save(ROOT / "reference/front-500.png")
    manifest = {
        "primary": {
            "file": source.name,
            "original_filename": "Cú lá xanh chibi đáng yêu.png",
            "size": list(im.size),
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "role": "front identity reference supplied by user",
            "status": "reference supplied; vector draft not approved",
        },
        "coordinate_system": {
            "source": [1254, 1254],
            "artboard": [500, 500],
            "fit": "contain",
            "crop": None,
        },
        "pending_views": ["left profile", "right profile", "back"],
        "incoming_folder": "reference/incoming",
        "secondary": "Earlier design board: expression/action direction only; latest front wins on conflicting anatomy.",
    }
    manifest_path = ROOT / "reference/manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        # Preserve added references, pending-view decisions and review notes.
        primary = {**manifest["primary"], **previous.get("primary", {})}
        if primary.get("sha256") != manifest["primary"]["sha256"]:
            primary["status"] = "reference changed; vector needs review"
        primary.update(file=source.name, size=list(im.size), sha256=manifest["primary"]["sha256"])
        manifest = {**manifest, **previous, "primary": primary}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if not review_only:
        print("Build artwork + rig", flush=True)
        python("artwork/build_artwork.py")
        python("tools/build_ollie.py")
        build_data.snapshot()
        python("tests/test_data.py")
        print(run([".", "--verify"]).strip())
        (BUILD / "inspect-summary.json").write_text(
            run(["inspect", ".", "--summary"]), encoding="utf-8"
        )
        render(BUILD / "front.png", project=str(ROOT / "artwork"))
    clean(BUILD / "front.png")
    # Keep a minimal executable runtime snapshot, analogous to Nez's rv folder.
    rv = BUILD / "rv"
    rv.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "runtime.rml", rv / "scene.rml")
    (rv / "rive.yaml").write_text(
        "name: ollie-rig-review\nmain: Runtime\nexclude:\n  - stages\n  - parts\n", encoding="utf-8"
    )
    head = {
        "HeadLeaf",
        "HeadBase",
        "LeftHeadFeathers",
        "RightHeadFeathers",
        "CrownPlumage",
        "CheekFeathers",
    }
    stages = [
        (
            "t1-silhouette",
            {"HeadBase", "Body", "FootL", "FootR", "LeftWing", "RightWing", "HeadLeaf"},
        ),
        ("t2-head", head),
        ("t3-face", head | {"FaceMask", "LeftEye", "RightEye", "Beak"}),
        ("t4-body", {"Body", "ChestPatch", "AIBadge", "LeftWing", "RightWing", "FootL", "FootR"}),
        ("t4-complete", None),
    ]
    images = []
    for ident, parts in stages:
        images.append((ident, stage(ident, parts, review_only)))
    sheet(images, BUILD / "construction.png", cols=5, size=215, title="OLLIE / CONSTRUCTION")
    parts = []
    labels = {
        "HeadLeaf": "01 Chồi lá",
        "CrownPlumage": "02 Chỏm sáng",
        "HeadBase": "03 Nền đầu",
        "FaceMask": "04 Mặt kem",
        "LeftEye": "05 Mắt trái",
        "RightEye": "06 Mắt phải",
        "Beak": "07 Mỏ cười",
        "CheekFeathers": "08 Má lá",
        "LeftWing": "09 Cánh trái",
        "RightWing": "10 Cánh phải",
        "Body": "11 Thân",
        "ChestPatch": "12 Ngực kem",
        "AIBadge": "13 Huy hiệu",
        "FootL": "14 Chân trái",
        "FootR": "15 Chân phải",
    }
    for name, label in labels.items():
        p = stage("part-" + name, {name}, review_only)
        bbox = p.getbbox()
        if bbox:
            p = p.crop(bbox)
        parts.append((label, p))
    sheet(parts, BUILD / "parts.png", cols=5, size=180, title="OLLIE / EDITABLE PARTS")
    if review_only:
        report = json.loads((BUILD / "check-report.json").read_text(encoding="utf-8"))
    else:
        print("Capture and test animation states", flush=True)
        report = check.main()
    moods = {
        "neutral": "t6-neutral",
        "happy": "t6-happy",
        "wink": "t6-wink",
        "focus": "t6-focus",
        "surprised": "t7-surprised",
        "sleepy": "t7-sleepy",
        "confused": "t7-confused",
        "thinking": "t7-thinking",
        "sleep": "t9-asleep",
    }
    (BUILD / "moods").mkdir(exist_ok=True)
    mood_images = []
    for mood, ident in moods.items():
        p = BUILD / f"probe-{ident}.png"
        shutil.copy2(p, BUILD / "moods" / f"{mood}.png")
        if mood != "sleep":
            shutil.copy2(p, BUILD / f"{mood}.png")
        mood_images.append((mood, clean(p)))
    sheet(
        mood_images,
        BUILD / "moods/contact-sheet.png",
        cols=3,
        title="OLLIE / 8 EXPRESSIONS + SLEEP",
    )
    shutil.copy2(BUILD / "moods/contact-sheet.png", BUILD / "mood-review.png")
    strips = {
        "idle-strip": ["t5-rest", "t5-inhale", "t5-seam", "t5-eyes-open", "t5-eyes-shut"],
        "wave-strip": ["t10-rest", "t10-wave", "t10-wave-mid", "t10-wave-end", "t10-after"],
        "sleep-strip": ["t9-awake", "t9-asleep", "t9-startle", "t9-awake-after"],
    }
    for filename, ids in strips.items():
        sheet(
            [(n, clean(BUILD / f"probe-{n}.png")) for n in ids],
            BUILD / f"{filename}.png",
            cols=len(ids),
            size=215,
            title="OLLIE / " + filename.upper(),
        )
    sheet(
        [
            (f"{percent/100*3:.2f}s", clean(BUILD / f"probe-thinking-{percent}.png"))
            for percent in (0, 25, 50, 75, 100)
        ],
        BUILD / "thinking-strip.png",
        cols=5,
        size=215,
        title="OLLIE / THINKING / 3s",
    )
    for size in [80, 120, 240, 500]:
        p = BUILD / f"size-{size}.png"
        if not review_only:
            render(p, viewport=f"{size}x{size}")
        clean(p)
    shutil.copy2(BUILD / "probe-t10-wave.png", BUILD / "wave-mid.png")
    shutil.copy2(BUILD / "probe-t9-asleep.png", BUILD / "sleep-late.png")
    export_frames()
    if not review_only:
        export_expressions()
    export_wing_review()
    overlay.main()
    trace.sync()
    if not review_only:
        run([BUILD / "trace", "--screenshot=" + str(BUILD / "trace.png"), "--fit=contain"])
    write_review(report)
    if not review_only:
        run([".", "--once"])
    (ROOT / "dist").mkdir(exist_ok=True)
    shutil.copy2(BUILD / "ollie-mascot.riv", ROOT / "dist/ollie.riv")
    shutil.copy2(ROOT / "artwork/ollie-front.svg", ROOT / "dist/ollie-front.svg")
    shutil.copy2(BUILD / "front-alpha.png", ROOT / "dist/ollie-front.png")
    build_data.package()
    package_expo.main()
    artifacts = [
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in BUILD.rglob("*")
        if p.is_file() and p.suffix in (".png", ".json", ".riv") and "visual-" not in str(p)
    ]
    (BUILD / "manifest.json").write_text(
        json.dumps(
            {
                "reference": manifest["primary"],
                "probe_count": len(report["captures"]),
                "passed": report["passed"],
                "artifacts": sorted(artifacts),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f'Kit ready: {len(report["captures"])} state probes; review.html; dist/ollie.riv',
        flush=True,
    )


if __name__ == "__main__":
    main(review_only="--review-only" in sys.argv)
