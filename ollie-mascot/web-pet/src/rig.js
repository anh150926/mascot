import { Application, Assets, Container, Sprite, Graphics, Text } from 'pixi.js';
import { PetAnimator } from './animation.js';

const PARTS = ['head', 'body', 'wing-left', 'wing-right', 'eye-left', 'eye-right',
  'lid-left', 'lid-right', 'beak-closed', 'beak-open', 'foot-left', 'foot-right', 'sprout', 'backpack', 'apple', 'tail'];
const asset = (name) => `${import.meta.env.BASE_URL}assets/parts/${name}.png`;

export async function createPet(host, onState, onReady) {
  const app = new Application();
  await app.init({ width: host.clientWidth || 600, height: host.clientHeight || 540,
    backgroundAlpha: 0, antialias: true, resolution: Math.min(window.devicePixelRatio || 1, 2),
    autoDensity: true, preference: 'webgl', powerPreference: 'low-power' });
  let textures;
  try { textures = await Promise.all(PARTS.map(name => Assets.load(asset(name)))); }
  catch (error) { app.destroy(true, { children: true, texture: false }); throw error; }
  const tex = Object.fromEntries(PARTS.map((name, i) => [name, textures[i]]));
  host.appendChild(app.canvas);
  app.canvas.setAttribute('aria-hidden', 'true');
  const world = new Container();
  app.stage.addChild(world);
  const shadow = new Graphics().ellipse(0, 0, 94, 13).fill({ color: 0x315e39, alpha: .10 });
  shadow.y = 432;
  world.addChild(shadow);
  const character = new Container();
  character.position.set(0, 421);
  world.addChild(character);
  const torso = new Container();
  torso.position.set(0, -119);
  character.addChild(torso);
  const make = (parent, name, x, y, width, ax = .5, ay = .5) => {
    const s = new Sprite(tex[name]);
    s.label = name; s.anchor.set(ax, ay); s.position.set(x, y);
    s.scale.set(width / s.texture.width); parent.addChild(s); return s;
  };
  const tail = make(torso, 'tail', 0, 82, 128);
  const backpack = make(torso, 'backpack', 15, -17, 227);
  const footL = make(character, 'foot-left', -45, -2, 48, .5, .25);
  const footR = make(character, 'foot-right', 45, -2, 48, .5, .25);
  const body = make(torso, 'body', 0, 1, 213);
  const wingL = make(torso, 'wing-left', -79, -67, 91, .79, .13);
  const wingR = make(torso, 'wing-right', 79, -67, 91, .21, .13);
  const head = new Container();
  head.position.set(0, -82);
  torso.addChild(head);
  make(head, 'head', 0, 0, 320, .5, .90);
  const eyeL = new Container(); eyeL.position.set(-65, -122); head.addChild(eyeL);
  const eyeR = new Container(); eyeR.position.set(65, -122); head.addChild(eyeR);
  make(eyeL, 'eye-left', 0, 0, 95);
  make(eyeR, 'eye-right', 0, 0, 95);
  const lidL = make(head, 'lid-left', -65, -115, 93);
  const lidR = make(head, 'lid-right', 65, -115, 93);
  const beak = make(head, 'beak-closed', 0, -67, 41);
  const mouth = make(head, 'beak-open', 0, -65, 41);
  const sprout = make(head, 'sprout', 7, -244, 81, .54, .96);
  const apple = make(torso, 'apple', -39, 5, 52);
  const zzz = new Text({ text: 'z  z  Z', style: { fontFamily: 'Georgia', fontSize: 23, fontStyle: 'italic', fill: 0x65816a } });
  zzz.position.set(115, -370); character.addChild(zzz);
  const animator = new PetAnimator(onState);
  let clock = 0, walkClock = 0, blinkClock = 0, nextBlink = 3.1, blinkAge = -1;
  let pausedByUser = false, reduced = false, zoom = 1, destroyed = false;
  let targetX = 0, targetY = 0, gazeX = 0, gazeY = 0;
  let showBackpack = true;
  const wingBaseL = wingL.rotation, wingBaseR = wingR.rotation;
  const resize = () => {
    if (destroyed) return;
    const w = host.clientWidth, h = host.clientHeight;
    if (!w || !h) return;
    app.renderer.resize(w, h);
    const scale = Math.min(w / 640, h / 535) * zoom;
    world.scale.set(scale); world.position.set(w / 2, (h - 475 * scale) / 2 + 10 * scale);
  };
  const observer = new ResizeObserver(resize); observer.observe(host); resize();
  function render(ticker) {
    const dt = Math.min(ticker.deltaMS / 1000, .04) * animator.speed;
    if (!pausedByUser && !document.hidden) {
      clock += dt; walkClock += dt * 8; blinkClock += dt;
    }
    const p = animator.pose;
    if (!reduced && !pausedByUser && animator.state === 'Idle') {
      if (blinkClock > nextBlink && blinkAge < 0) { blinkAge = 0; nextBlink = blinkClock + 3 + Math.random() * 3; }
      if (blinkAge >= 0) { blinkAge += dt; if (blinkAge > .26) blinkAge = -1; }
    } else blinkAge = -1;
    const blink = blinkAge < 0 ? 0 : Math.sin(Math.PI * blinkAge / .26);
    const eyeClose = Math.max(p.close, blink);
    const breathing = reduced ? 0 : Math.sin(clock * (p.sleepy > .5 ? 1.55 : 2.05));
    const walking = reduced ? 0 : p.walk;
    const step = Math.sin(walkClock);
    const travel = Math.sin(walkClock / 7) * 55 * walking;
    character.x = travel;
    character.y = 421 + p.lift - Math.abs(step) * 5 * walking;
    character.scale.set(p.scaleX, p.scaleY);
    torso.y = -119 - breathing * 1.5;
    torso.scale.set(1 + breathing * .003, 1 + breathing * .005);
    head.rotation = p.headAngle + (reduced ? 0 : Math.sin(clock * .95) * .013) + step * .018 * walking;
    head.y = -82 + p.headY;
    wingL.rotation = wingBaseL + p.wingL + breathing * .012 + step * .12 * walking;
    wingR.rotation = wingBaseR + p.wingR - breathing * .012 - step * .12 * walking;
    sprout.rotation = p.leaf + (reduced ? 0 : Math.sin(clock * 1.65 - .6) * .045) + step * .04 * walking;
    footL.y = -2 - Math.max(0, step) * 9 * walking;
    footR.y = -2 - Math.max(0, -step) * 9 * walking;
    footL.rotation = step * .15 * walking; footR.rotation = -step * .15 * walking;
    backpack.visible = showBackpack; backpack.rotation = -step * .025 * walking;
    tail.rotation = step * .035 * walking;
    const follow = reduced || p.sleepy > .1 || pausedByUser ? 0 : 1;
    gazeX += ((targetX * follow) - gazeX) * Math.min(1, dt * 7);
    gazeY += ((targetY * follow) - gazeY) * Math.min(1, dt * 7);
    eyeL.x = -65 + gazeX; eyeR.x = 65 + gazeX;
    eyeL.y = eyeR.y = -122 + gazeY;
    eyeL.scale.y = eyeR.scale.y = Math.max(.025, 1 - eyeClose);
    eyeL.alpha = eyeR.alpha = eyeClose > .88 ? Math.max(0, (1 - eyeClose) / .12) : 1;
    lidL.alpha = lidR.alpha = Math.max(0, (eyeClose - .70) / .3);
    mouth.alpha = p.smile; beak.alpha = 1 - p.smile;
    apple.alpha = p.food; apple.y = 5 + p.foodY; apple.scale.set(52 / apple.texture.width * p.foodScale);
    zzz.alpha = p.sleepy * .65; zzz.y = -370 - (reduced ? 0 : Math.sin(clock * 1.1) * 5);
    shadow.x = travel; shadow.scale.x = 1 + p.lift * .006;
  }
  app.ticker.add(render);
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const applyPause = () => {
    animator.setPaused(pausedByUser || document.hidden);
    if (pausedByUser || document.hidden) app.stop(); else app.start();
  };
  const visibility = () => applyPause();
  document.addEventListener('visibilitychange', visibility);
  const controller = {
    play: state => { blinkAge = -1; animator.play(state); render({ deltaMS: 0 }); app.render(); },
    pause: value => { pausedByUser = value; applyPause(); },
    speed: value => animator.setSpeed(value),
    zoom: value => { zoom = value; resize(); },
    backpack: value => { showBackpack = value; render({ deltaMS: 0 }); app.render(); },
    reduced: value => { reduced = value; animator.setReduced(value); },
    look: (x, y) => { targetX = Math.max(-3, Math.min(3, x * 3)); targetY = Math.max(-2, Math.min(2, y * 2)); },
    destroy: () => {
      destroyed = true; observer.disconnect(); animator.destroy();
      document.removeEventListener('visibilitychange', visibility);
      app.destroy(true, { children: true, texture: false });
    },
  };
  controller.reduced(motion.matches);
  applyPause(); render({ deltaMS: 0 }); onReady?.();
  return controller;
}
