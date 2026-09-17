/* Full screen photo viewer for the gallery pages: tap a photo to open it,
   swipe or use the arrows to move, Escape or the X to close. */
(function () {
  var photos = [].slice.call(document.querySelectorAll('.masonry img'));
  if (!photos.length) return;

  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.innerHTML =
    '<button class="lightbox-close" aria-label="Close photo">&times;</button>' +
    '<button class="lightbox-prev" aria-label="Previous photo">&#8249;</button>' +
    '<img alt="">' +
    '<button class="lightbox-next" aria-label="Next photo">&#8250;</button>' +
    '<p class="lightbox-caption"></p>';
  document.body.appendChild(box);

  var full = box.querySelector('img');
  var caption = box.querySelector('.lightbox-caption');
  var current = 0;

  function show(n) {
    current = (n + photos.length) % photos.length;
    full.src = photos[current].currentSrc || photos[current].src;
    full.alt = photos[current].alt || '';
    caption.textContent = photos[current].alt || '';
  }
  function open(n) {
    show(n);
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    box.querySelector('.lightbox-close').focus();
  }
  function close() {
    box.classList.remove('open');
    document.body.style.overflow = '';
  }

  photos.forEach(function (photo, n) {
    photo.tabIndex = 0;
    photo.addEventListener('click', function () { open(n); });
    photo.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(n); }
    });
  });

  box.querySelector('.lightbox-close').addEventListener('click', close);
  box.querySelector('.lightbox-prev').addEventListener('click', function (e) { e.stopPropagation(); show(current - 1); });
  box.querySelector('.lightbox-next').addEventListener('click', function (e) { e.stopPropagation(); show(current + 1); });
  box.addEventListener('click', function (e) { if (e.target === box || e.target === caption) close(); });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });

  var startX = null;
  box.addEventListener('touchstart', function (e) { startX = e.changedTouches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 40) show(current + (dx < 0 ? 1 : -1));
    startX = null;
  }, { passive: true });
})();
