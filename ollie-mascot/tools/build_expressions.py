"""Render scene stills, motion strips and transparent browser fallback frames."""

from __future__ import annotations
import argparse
import json
import shutil
from PIL import Image, ImageChops, ImageStat
from build_data import read, validate_runtime
from kit_common import ROOT, BUILD, render, clean, sheet
from export_web_frames import convert


def check_bounds(path):
    image = Image.open(path).convert("RGB")
    mask = ImageChops.difference(image, Image.new("RGB", image.size, (29, 29, 29))).point(
        lambda c: 255 if c > 24 else 0
    )
    bbox = mask.getbbox()
    if not bbox or min(bbox[:2]) <= 0 or bbox[2] >= image.width or bbox[3] >= image.height:
        raise RuntimeError(f"{path.name}: empty or clipped artwork: {bbox}")
    return bbox


def main(stills_only=False, scene_keys=None):
    validate_runtime()
    catalog = read("data/expressions.json")
    destination = ROOT / "playground/frames"
    destination.mkdir(exist_ok=True)
    out = BUILD / "expressions"
    out.mkdir(exist_ok=True)
    images = []
    report = []
    selected = set(scene_keys or (s["key"] for s in catalog["expressions"]))
    unknown = selected - {s["key"] for s in catalog["expressions"]}
    if unknown:
        raise ValueError("Unknown scenes: " + ", ".join(sorted(unknown)))
    previous = (
        {r["key"]: r for r in json.loads((out / "report.json").read_text(encoding="utf-8"))}
        if scene_keys and (out / "report.json").exists()
        else {}
    )
    presets = {p["id"]: p for p in read("data/presets.json")["presets"]}
    for spec in catalog["expressions"]:
        key = spec["key"]
        frame = presets[key]["capture_steps"][0]["advance"]
        if key not in selected:
            images.append((spec["label"], Image.open(destination / f"{key}.png").convert("RGBA")))
            if not stills_only:
                report.append(previous[key])
            continue
        target = out / f"{key}.png"
        dump = out / f"{key}.json"
        render(target, data=[f"mood={key}"], steps=[f"--advance={frame}"], dump=dump)
        actual = json.loads(dump.read_text(encoding="utf-8"))
        values = {p["path"]: p.get("value") for p in actual["viewModel"]["properties"]}
        if values.get("mood") != key:
            raise RuntimeError(key + ": View Model mood mismatch")
        bounds = [check_bounds(target)]
        convert(target, destination / f"{key}.png")
        still = Image.open(destination / f"{key}.png").convert("RGBA")
        images.append((spec["label"], still))
        if not stills_only:
            # Warm up beyond the 220ms neutral transition, then sample a loop.
            strip = []
            for fraction in (0, 0.25, 0.5, 0.75, 1):
                t = spec["frames"] + int(spec["frames"] * fraction)
                p = out / f"{key}-{int(fraction*100)}.png"
                render(p, data=[f"mood={key}"], steps=[f"--advance={t}"])
                bounds.append(check_bounds(p))
                strip.append((f'{fraction*spec["frames"]/60:.2f}s', clean(p)))
            sheet(strip, out / f"{key}-motion.png", cols=5, size=180, title=spec["label"])
            delta = (
                sum(
                    ImageStat.Stat(
                        ImageChops.difference(
                            strip[0][1].convert("RGB"), strip[2][1].convert("RGB")
                        )
                    ).mean
                )
                / 3
            )
            report.append(
                {
                    "key": key,
                    "duration_seconds": spec["frames"] / 60,
                    "visible_motion_delta": delta,
                    "bounds": bounds,
                }
            )
            if delta < 0.08:
                raise RuntimeError(key + ": no visible motion")
        print("Rendered " + key, flush=True)
    sheet(images, out / "contact-sheet.png", cols=5, size=260, title="OLLIE / 19 NEW EXPRESSIONS")
    # Track the contact sheet alongside the runtime for a portable review page.
    shutil.copy2(out / "contact-sheet.png", destination / "expressions-contact.png")
    if not stills_only:
        (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Expression library rendered.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stills-only", action="store_true")
    parser.add_argument(
        "--scenes", nargs="+", help="Re-render selected scenes; retain the other existing frames."
    )
    args = parser.parse_args()
    main(args.stills_only, args.scenes)
