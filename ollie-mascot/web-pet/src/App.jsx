import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Leaf, Sun, Moon, Apple, Footprints, Heart, Eye, Play, Pause, RotateCcw, ArrowUpRight, SlidersHorizontal, Backpack, Sparkles, X, ChevronRight } from 'lucide-react';
import { createPet } from './rig.js';

const actions = [
  { state: 'Idle', label: 'Thư giãn', sub: 'Hít thở một chút', icon: Leaf },
  { state: 'Blink', label: 'Chớp mắt', sub: 'Nhìn nhau nào', icon: Eye },
  { state: 'Happy', label: 'Vui chơi', sub: 'Một niềm vui nhỏ', icon: Heart },
  { state: 'Sleep', label: 'Đi ngủ', sub: 'Nạp lại năng lượng', icon: Moon },
  { state: 'Wake', label: 'Thức dậy', sub: 'Chào ngày mới', icon: Sun },
  { state: 'Eat', label: 'Cho ăn', sub: 'Một miếng táo ngon', icon: Apple },
  { state: 'Walk', label: 'Đi dạo', sub: 'Cùng vận động nhé', icon: Footprints },
];
const messages = {
  Idle: 'Một ngày thật xanh, cùng bạn.', Blink: 'Mình đang nghe bạn nè!',
  Happy: 'Có bạn ở đây, vui thật đó!', Sleep: 'Một giấc mơ xanh…',
  Wake: 'Chào bạn! Mình tỉnh rồi.', Eat: 'Mmm… cảm ơn bạn nhé!', Walk: 'Một bước nhỏ, một ngày vui.',
};
const initialReduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
export default function App() {
  const host = useRef(null), pet = useRef(null);
  const [status, setStatus] = useState('loading');
  const [state, setState] = useState('Idle');
  const [paused, setPaused] = useState(false);
  const [night, setNight] = useState(false);
  const [settings, setSettings] = useState(false);
  const [gallery, setGallery] = useState(false);
  const [reduced, setReduced] = useState(initialReduced);
  const [bag, setBag] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [zoom, setZoom] = useState(1);
  const [retries, setRetries] = useState(0);
  const [visits, setVisits] = useState(0);
  const prefs = useRef({ paused, reduced, bag, speed, zoom });
  prefs.current = { paused, reduced, bag, speed, zoom };

  useEffect(() => {
    let cancelled = false, local;
    setStatus('loading');
    createPet(host.current, setState).then(controller => {
      if (cancelled) { controller.destroy(); return; }
      local = controller; pet.current = controller;
      const p = prefs.current;
      controller.pause(p.paused); controller.reduced(p.reduced); controller.backpack(p.bag);
      controller.speed(p.speed); controller.zoom(p.zoom); setStatus('ready');
    }).catch(error => {
      if (!cancelled) { console.error('Ollie could not start:', error); setStatus('error'); }
    });
    return () => { cancelled = true; local?.destroy(); if (pet.current === local) pet.current = null; };
  }, [retries]);
  useEffect(() => { pet.current?.pause(paused); }, [paused]);
  useEffect(() => { pet.current?.reduced(reduced); }, [reduced]);
  useEffect(() => { pet.current?.backpack(bag); }, [bag]);
  useEffect(() => { pet.current?.speed(speed); }, [speed]);
  useEffect(() => { pet.current?.zoom(zoom); }, [zoom]);
  useEffect(() => {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    const change = e => setReduced(e.matches);
    media.addEventListener('change', change); return () => media.removeEventListener('change', change);
  }, []);
  const act = useCallback(next => {
    if (!pet.current) return;
    setPaused(false); pet.current.pause(false); pet.current.play(next);
    if (next === 'Happy' || next === 'Eat') setVisits(n => n + 1);
  }, []);
  useEffect(() => {
    const key = e => {
      if (/INPUT|BUTTON|SELECT|TEXTAREA/.test(e.target.tagName) || e.ctrlKey || e.metaKey || e.altKey) return;
      if (gallery || settings) return;
      if (/^[1-7]$/.test(e.key)) act(actions[Number(e.key) - 1].state);
      if (e.code === 'Space') { e.preventDefault(); setPaused(p => !p); }
    };
    window.addEventListener('keydown', key); return () => window.removeEventListener('keydown', key);
  }, [act, gallery, settings]);
  return <div className={`app ${night ? 'night' : ''}`}>
    <header className="topbar">
      <a href="#" className="brand" aria-label="Ollie, trang chủ"><span className="brand-icon"><Leaf size={24} /></span>ollie<span className="brand-dot">.</span></a>
      <div className="topbar-note"><span className="live-dot" /> Người bạn nhỏ, luôn bên bạn</div>
      <button className="text-button" onClick={() => setGallery(true)}>Góc của Ollie <ArrowUpRight size={16} /></button>
    </header>
    <main>
      <div className="page-heading"><div><div className="eyebrow"><span /> YOUR LITTLE GREEN COMPANION</div><h1>Một chút xanh.<br className="mobile-break" /> Một ngày vui.</h1><p>Chậm lại một nhịp. Dành chút thời gian cho người bạn nhỏ.</p></div><div className="day-note"><Sun size={19}/><span>Hôm nay là một ngày đẹp<br /><strong>để bắt đầu từ điều nhỏ.</strong></span></div></div>
      <div className="experience">
        <section className="habitat" aria-label="Khu vườn của Ollie">
          <div className="stage-top"><span className="garden-tag"><span className="live-dot" /> Khu vườn nhỏ</span><button className="icon-button theme-button" onClick={() => setNight(!night)} aria-label={night ? 'Chuyển sang ban ngày' : 'Chuyển sang ban đêm'}>{night ? <Sun size={19}/> : <Moon size={18}/>}</button></div>
          <div className="garden-orb"/><div className="garden-orb secondary"/>
          <div className="garden-leaf leaf-one"><Leaf /></div><div className="garden-leaf leaf-two"><Leaf /></div><div className="garden-leaf leaf-three"><Leaf /></div>
          <span className="spark spark-one">✦</span><span className="spark spark-two">✧</span><span className="spark spark-three">·</span>
          <div className="speech" role="status" aria-live="polite">{messages[state]}<span>♡</span></div>
          <div ref={host} className="pet-canvas" role="button" tabIndex={status === 'ready' ? 0 : -1}
            aria-label={state === 'Sleep' ? 'Đánh thức Ollie' : 'Vuốt ve Ollie'}
            onClick={() => act(state === 'Sleep' ? 'Wake' : 'Happy')}
            onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); act(state === 'Sleep' ? 'Wake' : 'Happy'); } }}
            onPointerMove={e => { const b = e.currentTarget.getBoundingClientRect(); pet.current?.look((e.clientX - b.left) / b.width * 2 - 1, (e.clientY - b.top) / b.height * 2 - 1); }}
            onPointerLeave={() => pet.current?.look(0, 0)} />
          {status !== 'ready' && <div className="loading-scene"><img src={`${import.meta.env.BASE_URL}assets/ollie-master.png`} alt="Ollie, chú cú xanh với mắt long lanh và mầm lá trên đầu"/><p>{status === 'loading' ? 'Ollie đang ghé khu vườn…' : 'Chưa mở được khu vườn tương tác.'}</p>{status === 'error' && <button onClick={() => setRetries(n => n + 1)}>Thử lại</button>}</div>}
          <div className="stage-bottom"><span><span className="touch-dot" /> Chạm vào Ollie để làm quen</span><div className="stage-tools"><button className="icon-button" disabled={status !== 'ready'} onClick={() => setPaused(!paused)} aria-label={paused ? 'Tiếp tục chuyển động' : 'Tạm dừng chuyển động'} aria-pressed={paused}>{paused ? <Play size={17}/> : <Pause size={17}/>}</button><button className="icon-button" onClick={() => { act('Idle'); setZoom(1); }} aria-label="Đưa Ollie về tư thế nghỉ"><RotateCcw size={17}/></button><button className="icon-button" onClick={() => setSettings(!settings)} aria-label="Tùy chỉnh chuyển động" aria-expanded={settings}><SlidersHorizontal size={17}/></button></div></div>
          {settings && <div className="settings-panel"><div className="settings-title"><strong>Một chút tùy chỉnh</strong><button className="icon-button" onClick={() => setSettings(false)} aria-label="Đóng tùy chỉnh"><X size={16}/></button></div><label>Tốc độ <output>{speed.toFixed(1)}×</output><input aria-label="Tốc độ chuyển động" type="range" min="0.5" max="1.5" step="0.1" value={speed} onChange={e => setSpeed(+e.target.value)}/></label><label>Kích thước <output>{Math.round(zoom * 100)}%</output><input aria-label="Kích thước Ollie" type="range" min="0.7" max="1.1" step="0.05" value={zoom} onChange={e => setZoom(+e.target.value)}/></label><label className="check"><Backpack size={16}/> Mang balo<input type="checkbox" checked={bag} onChange={e => setBag(e.target.checked)}/></label><label className="check">Chuyển động nhẹ<input type="checkbox" checked={reduced} onChange={e => setReduced(e.target.checked)}/></label></div>}
        </section>
        <aside className="companion-panel"><div className="profile-heading"><div className="tiny-label">LÀM QUEN VỚI BẠN NHỎ</div><div className="name-row"><h2>Ollie</h2><span className="nature-badge"><Leaf size={12}/> Một tâm hồn xanh</span></div><p>Một chú cú tò mò, thích những chiếc lá<br className="desktop-break"/> và những khoảnh khắc bên bạn.</p></div>
          <div className="mood-card"><div className="mood-icon">{state === 'Sleep' ? <Moon size={22}/> : <Heart size={22}/>}</div><div><span>{state === 'Sleep' ? 'Đang mơ những giấc mơ đẹp' : state === 'Walk' ? 'Sẵn sàng khám phá cùng bạn' : 'Thật vui vì có bạn ở đây'}</span><div className="bond-dots" aria-label={`${Math.min(5, 3 + Math.floor(visits / 3))} trên 5 nhịp gắn kết`}>{Array.from({length:5}, (_, i) => <i key={i} className={i < Math.min(5, 3 + Math.floor(visits / 3)) ? 'filled' : ''}/>)}</div></div><span className="little-heart">♡</span></div>
          <div className="action-heading"><h3>Mình làm gì cùng nhau?</h3><span>01 — 07</span></div>
          <div className="actions">{actions.map(({state: s,label,sub,icon:Icon}, i) => <button key={s} className={`action ${state === s ? 'selected' : ''} ${s === 'Walk' ? 'wide' : ''}`} disabled={status !== 'ready'} onClick={() => act(s)} aria-pressed={state === s} data-state={s}><span className="action-icon"><Icon size={20}/></span><span><strong>{label}</strong><small>{sub}</small></span>{s === 'Walk' ? <ArrowUpRight size={17} className="action-arrow"/> : <span className="key-hint">{i+1}</span>}</button>)}</div>
          <div className="gentle-note"><Sparkles size={18}/><p>Không cần vội đâu.<br/><strong>Mỗi bước nhỏ đều đáng trân trọng.</strong></p></div>
        </aside>
      </div>
      <footer><span><Leaf size={14}/> Nhỏ thôi, nhưng luôn ở đây.</span><span className="keyboard-note">Phím <kbd>1</kbd>–<kbd>7</kbd> để khám phá <i>·</i> <kbd>Space</kbd> để nghỉ một nhịp</span><button className="text-button" onClick={() => setGallery(true)}>Từ một chiếc lá nhỏ <ChevronRight size={14}/></button></footer>
    </main>
    {gallery && <Gallery onClose={() => setGallery(false)}/>}
  </div>;
}

function Gallery({ onClose }) {
  const dialog = useRef(null);
  useEffect(() => { const el = dialog.current; el.showModal(); return () => el.close(); }, []);
  return <dialog ref={dialog} className="gallery-dialog" onCancel={onClose} onClick={e => { if (e.target === e.currentTarget) onClose(); }}><div className="gallery-header"><div><div className="eyebrow">A LITTLE FRIEND, A LOT OF HEART</div><h2>Ollie, từ một chiếc lá nhỏ.</h2></div><button autoFocus className="icon-button" onClick={onClose} aria-label="Đóng góc của Ollie"><X/></button></div><div className="gallery-body"><img className="master-image" src={`${import.meta.env.BASE_URL}assets/ollie-master.png`} alt="Thiết kế minh họa gốc của Ollie"/><div><p>Mắt xanh long lanh. Một mầm lá luôn hướng lên. Và chiếc balo cho những chuyến đi cùng bạn.</p><p>Ollie được tạo từ tranh minh họa AI, tách thành từng bộ phận để có thể thở, chớp mắt, vẫy cánh và bước đi.</p><div className="parts-preview">{['head','body','wing-left','eye-left','sprout','backpack'].map(name => <img key={name} src={`${import.meta.env.BASE_URL}assets/parts/${name}.png`} alt={`Bộ phận ${name}`}/>)}</div><span className="gallery-caption">Cùng một nhân vật. Từng chi tiết được giữ lại.</span></div></div></dialog>;
}
