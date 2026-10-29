/* HomeCore Construction lite YouTube facade.
   Thumbnail + play button first. Iframe from youtube-nocookie.com loads only on click. */
(function () {
  function activate(el) {
    if (!el || el.dataset.ytActive === '1') return;
    var id = el.getAttribute('data-yt-id');
    if (!id) return;
    var title = el.getAttribute('data-yt-title') || 'HomeCore Construction video';
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    iframe.title = title;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    iframe.loading = 'lazy';
    iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
    el.innerHTML = '';
    el.appendChild(iframe);
    el.dataset.ytActive = '1';
    el.classList.add('is-playing');
  }

  function onActivate(e) {
    var el = e.target.closest('[data-yt-id]');
    if (!el) return;
    e.preventDefault();
    activate(el);
  }

  document.addEventListener('click', onActivate);
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var el = e.target.closest('[data-yt-id]');
    if (!el) return;
    e.preventDefault();
    activate(el);
  });
})();
