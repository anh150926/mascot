import { gsap } from 'gsap';

export const STATES = ['Idle', 'Blink', 'Happy', 'Sleep', 'Wake', 'Eat', 'Walk'];
export const NEUTRAL = Object.freeze({
  lift: 0, scaleX: 1, scaleY: 1, headAngle: 0, headY: 0,
  wingL: 0, wingR: 0, leaf: 0, close: 0, smile: 0,
  food: 0, foodY: 0, foodScale: 1, walk: 0, sleepy: 0,
});

// One interruptible timeline owns the action pose. Interruptions tween from the
// current values instead of snapping sprites back to their rest transforms.
export class PetAnimator {
  constructor(onState = () => {}) {
    this.pose = { ...NEUTRAL };
    this.state = 'Idle';
    this.onState = onState;
    this.paused = false;
    this.reduced = false;
    this.speed = 1;
    this.timeline = null;
  }
  play(state) {
    if (!STATES.includes(state)) throw new Error(`Unknown Ollie state: ${state}`);
    this.timeline?.kill();
    this.state = state;
    this.onState(state);
    const p = this.pose;
    const t = this.timeline = gsap.timeline({ paused: this.paused, defaults: { ease: 'sine.inOut' } });
    t.timeScale(this.speed);
    if (this.reduced) {
      t.to(p, { ...NEUTRAL, close: state === 'Sleep' ? 1 : 0, sleepy: state === 'Sleep' ? 1 : 0,
        smile: state === 'Happy' || state === 'Eat' ? 1 : 0, food: state === 'Eat' ? 1 : 0, duration: .18 });
      if (!['Idle', 'Sleep', 'Walk'].includes(state)) t.to({}, { duration: 1.4 }).call(() => this.play('Idle'));
      return t;
    }
    // Wake opens eyes as part of its stretch; preserve eyelid pose during reset.
    t.to(p, { ...NEUTRAL, close: ['Wake', 'Sleep'].includes(state) ? p.close : 0, duration: .3 });
    if (state === 'Idle') return t;
    if (state === 'Blink') {
      t.to(p, { close: 1, duration: .105 }).to(p, { close: 0, duration: .17 });
    } else if (state === 'Happy') {
      t.to(p, { wingL: .52, wingR: -.52, smile: 1, headAngle: -.07, scaleX: 1.025, scaleY: .98, duration: .3 })
        .to(p, { lift: -23, scaleX: .98, scaleY: 1.025, leaf: .12, duration: .32, ease: 'power2.out' })
        .to(p, { lift: 0, scaleX: 1.025, scaleY: .98, leaf: -.09, duration: .35, ease: 'power2.in' })
        .to(p, { lift: -11, scaleX: 1, scaleY: 1, headAngle: .05, duration: .28 })
        .to(p, { lift: 0, duration: .3 }).to({}, { duration: .6 });
    } else if (state === 'Sleep') {
      t.to(p, { close: 1, sleepy: 1, headAngle: .095, headY: 8, wingL: -.10, wingR: .10, scaleY: .965, leaf: .13, duration: 1.0 });
      return t;
    } else if (state === 'Wake') {
      t.to(p, { close: .35, headY: -5, scaleY: 1.03, wingL: .5, wingR: -.5, leaf: -.12, duration: .72 })
        .to(p, { close: 0, smile: .8, headAngle: -.04, duration: .45 }).to({}, { duration: .4 });
    } else if (state === 'Eat') {
      t.to(p, { food: 1, foodY: 0, foodScale: 1, wingL: -.35, wingR: .24, headAngle: -.07, duration: .45 })
        .to(p, { foodY: -80, smile: 1, headY: 5, duration: .6 })
        .to(p, { smile: 0, headY: 8, foodScale: .76, duration: .2 })
        .to(p, { smile: 1, headY: 2, duration: .22 })
        .to(p, { smile: 0, headY: 7, foodScale: .52, duration: .2 })
        .to(p, { smile: 1, headY: 1, duration: .22 })
        .to(p, { food: 0, foodScale: .15, headY: 4, duration: .25 })
        .to(p, { smile: 0, headY: 0, headAngle: .05, duration: .4 }).to({}, { duration: .4 });
    } else if (state === 'Walk') {
      t.to(p, { walk: 1, wingL: .06, wingR: -.06, duration: .5 });
      return t;
    }
    t.to(p, { ...NEUTRAL, duration: .45 }).call(() => this.play('Idle'));
    return t;
  }
  setPaused(value) { this.paused = value; this.timeline?.paused(value); }
  setSpeed(value) { this.speed = value; this.timeline?.timeScale(value); }
  setReduced(value) { this.reduced = value; this.play(this.state); }
  destroy() { this.timeline?.kill(); this.timeline = null; }
}
