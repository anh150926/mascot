"""Make transparent browser fallback frames from Rive CLI screenshots.

The CLI screenshot has a uniform #1d1d1d preview background. The live .riv
artboard itself is transparent; this removes only the screenshot background.
"""

from pathlib import Path
from collections import deque
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
DEST = ROOT / "playground" / "frames"
FRAMES = ["neutral", "happy", "wink", "focus", "surprised", "sleepy", "confused", "wave-mid"]
BACKGROUND = (29, 29, 29)


def convert(source: Path, destination: Path):
    image = Image.open(source).convert("RGBA")
    out = image.copy()
    input_pixels = image.load()
    output_pixels = out.load()
    # The eyes also contain near-black colors. Color-keying every pixel erased
    # their lashes and pupils. Remove only background connected to the border.
    mask = Image.new("L", image.size)
    background_pixels = mask.load()
    queue = deque()
    for x in range(image.width):
        queue.append((x, 0)); queue.append((x, image.height-1))
    for y in range(image.height):
        queue.append((0, y)); queue.append((image.width-1, y))
    visited = set()
    while queue:
        x, y = queue.popleft()
        if (x,y) in visited or not (0 <= x < image.width and 0 <= y < image.height):
            continue
        visited.add((x,y))
        rgb = input_pixels[x,y][:3]
        if max(abs(rgb[i]-BACKGROUND[i]) for i in range(3)) > 12:
            continue
        background_pixels[x,y] = 255
        queue.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
    edge = mask.filter(ImageFilter.MaxFilter(3)).load()
    for y in range(image.height):
        for x in range(image.width):
            rgb = input_pixels[x, y][:3]
            difference = max(abs(rgb[i] - BACKGROUND[i]) for i in range(3))
            alpha = min(255, difference * 8)
            if background_pixels[x,y] or (edge[x,y] and difference <= 2):
                output_pixels[x, y] = (0, 0, 0, 0)
            elif not edge[x,y] or alpha == 255:
                output_pixels[x, y] = (*rgb, 255)
            else:
                a = alpha / 255
                clean = tuple(max(0, min(255, round((rgb[i] - (1-a) * BACKGROUND[i]) / a))) for i in range(3))
                output_pixels[x, y] = (*clean, alpha)
    out.save(destination)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for frame in FRAMES:
        convert(BUILD / f"{frame}.png", DEST / f"{frame}.png")
    convert(BUILD / "sleep-late.png", DEST / "sleep.png")


if __name__ == "__main__":
    main()
