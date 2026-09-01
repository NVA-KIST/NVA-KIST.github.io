/* Mobile navigation toggle.
 *
 * Listeners are delegated from `document` rather than bound to the button,
 * because the DC runtime re-renders the header on state changes and would
 * otherwise throw away anything bound directly to those nodes.
 */
(function () {
  'use strict';

  function nav() { return document.getElementById('site-nav'); }
  function toggle() { return document.querySelector('.nav-toggle'); }

  function setOpen(open) {
    var n = nav(), t = toggle();
    if (!n || !t) return;
    n.classList.toggle('is-open', open);
    t.setAttribute('aria-expanded', open ? 'true' : 'false');
    t.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
  }

  function isOpen() {
    var n = nav();
    return !!n && n.classList.contains('is-open');
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.nav-toggle')) {
      e.preventDefault();
      setOpen(!isOpen());
      return;
    }
    if (!isOpen()) return;
    // A link inside the menu navigates; anything outside it just closes.
    if (e.target.closest && e.target.closest('#site-nav a')) {
      setOpen(false);
    } else if (!(e.target.closest && e.target.closest('#site-nav'))) {
      setOpen(false);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) {
      setOpen(false);
      var t = toggle();
      if (t) t.focus();
    }
  });

  // Leaving the mobile breakpoint must not strand the panel in the open state.
  var mq = window.matchMedia('(max-width:768px)');
  var onChange = function (ev) { if (!ev.matches) setOpen(false); };
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else if (mq.addListener) mq.addListener(onChange);
})();
