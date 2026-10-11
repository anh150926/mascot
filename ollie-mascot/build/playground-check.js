
    const SRC = '../dist/ollie.riv';
    const FRAME = name => './frames/' + name + '.png';
    const MOODS = [
      ['neutral','Mặc định'],['happy','Vui vẻ'],['wink','Nháy mắt'],
      ['focus','Tập trung'],['surprised','Bất ngờ'],['sleepy','Buồn ngủ'],['confused','Thắc mắc']
    ];
    const canvas = document.getElementById('rive');
    const statusEl = document.getElementById('status');
    const moodBox = document.getElementById('moods');
    const sleepBtn = document.getElementById('sleep');
    const bubble = document.getElementById('bubble');
    const fallback = document.getElementById('fallback');
    let animation = null, moodProp = null, sleepProp = null, waveProp = null, playing = true, bubbleTimer = null;
    let fallbackMode = false, fallbackMood = 'neutral', fallbackSleep = false, gestureTimer = null;

    function showFrame(name) { fallback.src = FRAME(name); }
    function useFrames(reason) {
      if (animation) { animation.cleanup(); animation = null; }
      fallbackMode = true; fallback.style.display = 'block'; canvas.style.display = 'none';
      showFrame(fallbackSleep ? 'sleep' : fallbackMood);
      status(reason || 'Đang xem các frame render từ Rive. Mood, wave và sleep có thể thử ở chế độ này.');
    }

    function status(message, error=false) {
      statusEl.textContent = message;
      statusEl.classList.toggle('error', error);
    }
    function selectButton(container, current) {
      container.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === current)));
    }
    function setMood(key) {
      if (fallbackMode) {
        fallbackMood = key;
        if (!fallbackSleep) showFrame(key);
        selectButton(moodBox, moodBox.querySelector(`[data-mood="${key}"]`));
        return status(`mood = ${key} · frame preview`);
      }
      if (!moodProp) return status('Chưa tìm thấy Mascot.mood.', true);
      moodProp.value = key;
      selectButton(moodBox, moodBox.querySelector(`[data-mood="${key}"]`));
      status(`mood = ${key}`);
    }
    MOODS.forEach(([key,label],index) => {
      const b = document.createElement('button');
      b.dataset.mood = key;
      b.textContent = `${index+1}. ${label}`;
      b.setAttribute('aria-pressed', String(key === 'neutral'));
      b.onclick = () => setMood(key);
      moodBox.appendChild(b);
    });
    [['120px','120 px'],['240px','240 px'],['400px','400 px']].forEach(([size,label]) => {
      const b = document.createElement('button');
      b.textContent = label;
      b.setAttribute('aria-pressed', String(size === '400px'));
      b.onclick = () => {
        document.documentElement.style.setProperty('--size', size);
        selectButton(document.getElementById('sizes'), b);
        requestAnimationFrame(() => animation?.resizeDrawingSurfaceToCanvas());
      };
      document.getElementById('sizes').appendChild(b);
    });
    document.querySelectorAll('[data-stage]').forEach(b => b.onclick = () => {
      document.documentElement.dataset.stage = b.dataset.stage;
      selectButton(b.parentElement, b);
    });
    document.querySelectorAll('[data-say]').forEach(b => b.onclick = () => {
      if (fallbackMode ? fallbackSleep : sleepProp?.value) return status('Ollie đang ngủ. Chạm vào nhân vật để đánh thức.');
      bubble.textContent = b.dataset.say;
      bubble.classList.add('show');
      clearTimeout(bubbleTimer);
      bubbleTimer = setTimeout(() => bubble.classList.remove('show'), 3600);
    });
    function syncSleep() {
      const asleep = fallbackMode ? fallbackSleep : !!sleepProp?.value;
      sleepBtn.textContent = asleep ? 'Đang ngủ…' : 'Cho ngủ';
      sleepBtn.setAttribute('aria-pressed', String(asleep));
      if (asleep) bubble.classList.remove('show');
    }
    function load() {
      if (animation) animation.cleanup();
      animation = null; moodProp = null; sleepProp = null; waveProp = null;
      fallbackMode = false; fallback.style.display = 'none'; canvas.style.display = 'block';
      status('Đang nạp Ollie…');
      if (!window.rive) return useFrames('Web runtime chưa tải được. Đang dùng frame do Rive CLI render.');
      animation = new rive.Rive({
        src: SRC + '?t=' + Date.now(), canvas, artboard:'Runtime', stateMachine:'Main',
        autoplay:true, autoBind:true,
        layout:new rive.Layout({fit:rive.Fit.Contain,alignment:rive.Alignment.Center}),
        onLoad:() => {
          animation.resizeDrawingSurfaceToCanvas();
          const model = animation.viewModelInstance;
          moodProp = model?.enum('mood');
          sleepProp = model?.boolean('isAsleep');
          waveProp = model?.trigger('wave');
          if (sleepProp) sleepProp.on(() => { syncSleep(); status(`isAsleep = ${sleepProp.value}`); });
          syncSleep();
          playing = true;
          document.getElementById('toggle').textContent = 'Dừng';
          status(moodProp && sleepProp && waveProp
            ? `Đã nạp Ollie · mood = ${moodProp.value}\nChạm nhân vật khi ngủ để tỉnh.`
            : 'File đã nạp nhưng thiếu mood, isAsleep hoặc wave.', !(moodProp && sleepProp && waveProp));
        },
        onLoadError:e => useFrames('Web runtime không nạp được file .riv cục bộ: ' + (e?.data || e) + '\nĐang dùng frame do Rive CLI render.')
      });
    }
    sleepBtn.onclick = () => {
      if (fallbackMode) {
        fallbackSleep = !fallbackSleep;
        showFrame(fallbackSleep ? 'sleep' : fallbackMood);
        syncSleep();
        return status(`isAsleep = ${fallbackSleep} · frame preview`);
      }
      if (!sleepProp) return status('Không tìm thấy isAsleep.', true);
      sleepProp.value = !sleepProp.value;
      syncSleep();
    };
    document.getElementById('wave').onclick = () => {
      if (fallbackMode) {
        if (fallbackSleep) return status('Ollie đang ngủ, chưa vẫy cánh.');
        clearTimeout(gestureTimer);
        showFrame('wave-mid');
        gestureTimer = setTimeout(() => showFrame(fallbackMood), 900);
        return status('wave() · các frame Rive đã render');
      }
      if (!waveProp) return status('Không tìm thấy wave.', true);
      if (sleepProp?.value) return status('Ollie đang ngủ, chưa vẫy cánh.');
      waveProp.trigger(); status('wave() · Ollie vẫy cánh');
    };
    document.getElementById('toggle').onclick = e => {
      if (fallbackMode) {
        fallback.style.animationPlayState = playing ? 'paused' : 'running';
        playing = !playing;
        e.target.textContent = playing ? 'Dừng' : 'Chạy';
        return;
      }
      if (!animation) return;
      playing ? animation.pause() : animation.play();
      playing = !playing;
      e.target.textContent = playing ? 'Dừng' : 'Chạy';
    };
    document.getElementById('reload').onclick = load;
    document.getElementById('useFrames').onclick = () => useFrames();
    fallback.onclick = () => {
      if (!fallbackSleep) return;
      fallbackSleep = false;
      showFrame('surprised');
      syncSleep();
      setTimeout(() => showFrame(fallbackMood), 650);
      status('Ollie đã tỉnh · frame preview');
    };
    window.addEventListener('resize', () => animation?.resizeDrawingSurfaceToCanvas());
    window.addEventListener('keydown', e => {
      if (e.key >= '1' && e.key <= '7') setMood(MOODS[Number(e.key)-1][0]);
      if (e.key.toLowerCase() === 'w') document.getElementById('wave').click();
      if (e.key.toLowerCase() === 's') sleepBtn.click();
      if (e.code === 'Space') { e.preventDefault(); document.getElementById('toggle').click(); }
    });
    load();
  