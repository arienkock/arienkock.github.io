(function () {
  var root = document.documentElement;
  var themeToggle = document.getElementById('theme-toggle');
  var navToggle = document.getElementById('nav-toggle');
  var siteHeader = document.querySelector('.site-header');

  if (!themeToggle && !navToggle) return;

  function currentTheme() {
    if (root.classList.contains('dark')) return 'dark';
    if (root.classList.contains('light')) return 'light';
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.classList.remove('light', 'dark');
      root.classList.add(next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  if (navToggle && siteHeader) {
    var nav = document.getElementById('primary-nav');
    var navMq = window.matchMedia('(min-width: 769px)');

    function setNavOpen(open) {
      siteHeader.classList.toggle('nav-open', open);
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    navToggle.addEventListener('click', function () {
      setNavOpen(!siteHeader.classList.contains('nav-open'));
    });

    if (nav) {
      nav.addEventListener('click', function (event) {
        if (event.target.closest('a')) setNavOpen(false);
      });
    }

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') setNavOpen(false);
    });

    function onBreakpointChange(event) {
      if (event.matches) setNavOpen(false);
    }

    if (typeof navMq.addEventListener === 'function') navMq.addEventListener('change', onBreakpointChange);
    else if (typeof navMq.addListener === 'function') navMq.addListener(onBreakpointChange);
  }
})();
