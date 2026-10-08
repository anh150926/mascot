import sharp from 'sharp';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const source = path.join(root, 'art-source/ollie-atlas.png');
const output = path.join(root, 'public/assets/parts');
await mkdir(output, { recursive: true });
// Measured cell boundaries of the AI source (not an assumed perfect grid).
// Only extraction/transparent padding: no redrawing, recoloring or synthetic art.
const boxes = {
  head: [0, 0, 344, 385], body: [345, 0, 303, 385],
  'wing-left': [655, 0, 280, 385], 'wing-right': [962, 0, 292, 385],
  'eye-left': [25, 395, 284, 258], 'eye-right': [340, 395, 284, 258],
  'lid-left': [650, 410, 267, 215], 'lid-right': [972, 410, 282, 215],
  'beak-closed': [40, 670, 248, 215], 'beak-open': [342, 670, 248, 215],
  'foot-left': [638, 672, 253, 218], 'foot-right': [986, 672, 257, 218],
  sprout: [0, 895, 321, 359], backpack: [323, 895, 313, 359],
  apple: [642, 905, 272, 349], tail: [925, 910, 329, 344],
};
const manifest = {};
for (const [name, [left, top, width, height]] of Object.entries(boxes)) {
  const buffer = await sharp(source).extract({ left, top, width, height }).png().toBuffer();
  const { data, info } = await sharp(buffer).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let x0 = info.width, y0 = info.height, x1 = 0, y1 = 0;
  for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
    if (data[(y * info.width + x) * 4 + 3] > 16) {
      x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
    }
  }
  if (x0 > x1) throw new Error(`Empty atlas cell: ${name}`);
  // Four transparent pixels protect texture filtering around each silhouette.
  const part = await sharp(buffer).extract({ left: x0, top: y0, width: x1 - x0 + 1, height: y1 - y0 + 1 })
    .extend({ top: 4, bottom: 4, left: 4, right: 4, background: '#00000000' }).png().toBuffer();
  await writeFile(path.join(output, `${name}.png`), part);
  const meta = await sharp(part).metadata();
  manifest[name] = { file: `${name}.png`, width: meta.width, height: meta.height, sourceRect: [left + x0, top + y0, x1 - x0 + 1, y1 - y0 + 1] };
}
await writeFile(path.join(output, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`Extracted ${Object.keys(manifest).length} transparent, editable parts.`);
