
    const root = document.documentElement;
    const canvas = document.getElementById('neutral');
    const fallback = document.getElementById('fallback');
    const zoom = document.getElementById('zoom');
    const zoomValue = document.getElementById('zoomValue');
    let player;
    function setSize(value) {
      root.style.setProperty('--size', value + 'px');
      zoom.value = value;
      zoomValue.value = value + ' px';
      document.querySelectorAll('[data-size]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.size === String(value))));
      requestAnimationFrame(() => player?.resizeDrawingSurfaceToCanvas());
    }
    document.querySelectorAll('[data-size]').forEach(button => button.addEventListener('click', () => setSize(button.dataset.size)));
    zoom.addEventListener('input', () => setSize(zoom.value));
    document.getElementById('background').addEventListener('click', event => {
      const light = event.currentTarget.getAttribute('aria-pressed') !== 'true';
      event.currentTarget.setAttribute('aria-pressed', String(light));
      event.currentTarget.textContent = light ? 'Nền tối' : 'Nền sáng';
      document.querySelectorAll('.stage').forEach(stage => stage.style.background = light ? '#eaf4e7' : '#1d1d1d');
    });
    const dialog = document.getElementById('partsDialog');
    document.getElementById('parts').addEventListener('click', () => dialog.showModal());
    document.getElementById('closeDialog').addEventListener('click', () => dialog.close());
    if (window.rive?.Rive) {
      player = new rive.Rive({
        src:'./build/ollie-neutral-v2.riv', canvas, artboard:'Neutral', autoplay:false,
        layout:new rive.Layout({fit:rive.Fit.Contain, alignment:rive.Alignment.Center}),
        onLoad:() => { player.resizeDrawingSurfaceToCanvas(); document.getElementById('riveStatus').textContent = 'Đã nạp artboard Rive neutral V2. Dùng thanh thu phóng để xem nét vector.'; },
        onLoadError:() => { canvas.style.display='none'; fallback.style.display='block'; document.getElementById('riveStatus').textContent = 'Đang xem ảnh PNG dự phòng.'; }
      });
    } else {
      canvas.style.display='none'; fallback.style.display='block';
      document.getElementById('riveStatus').textContent = 'Đang xem ảnh PNG dự phòng.';
    }
    window.addEventListener('resize', () => player?.resizeDrawingSurfaceToCanvas());
  