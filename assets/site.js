if ('scrollRestoration' in history) { history.scrollRestoration = 'auto'; }

(function () {
  // ===== GA4 event helper (no-ops safely until gtag exists) =====
  function track(name, params) { if (typeof window.gtag === 'function') { window.gtag('event', name, params || {}); } }
  document.querySelectorAll('a[data-call]').forEach(a => a.addEventListener('click', () => track('call_click', { location: 'site' })));

  // ===== Mobile drawer =====
  const hamburger = document.getElementById('hamburger');
  const drawer = document.getElementById('navDrawer');
  const overlay = document.getElementById('navOverlay');
  const drawerClose = document.getElementById('drawerClose');
  function openDrawer() {
    drawer.classList.add('open'); overlay.classList.add('open');
    document.body.classList.add('drawer-open');
    drawer.setAttribute('aria-hidden', 'false'); hamburger.setAttribute('aria-expanded', 'true');
  }
  function closeDrawer() {
    drawer.classList.remove('open'); overlay.classList.remove('open');
    document.body.classList.remove('drawer-open');
    drawer.setAttribute('aria-hidden', 'true'); hamburger.setAttribute('aria-expanded', 'false');
  }
  hamburger.addEventListener('click', openDrawer);
  drawerClose.addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeDrawer));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer(); });

  // ===== Anchor smooth-scroll, no hash persistence =====
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', window.location.pathname);
    });
  });
  if (window.location.hash) { history.replaceState(null, '', window.location.pathname); }

  // ===== FAQ accordion (single-open) =====
  document.querySelectorAll('.acc-header').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.parentElement;
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.acc-item').forEach(i => { i.classList.remove('open'); const b = i.querySelector('.acc-header'); if (b) b.setAttribute('aria-expanded', 'false'); });
      if (!isOpen) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  // ===== Lift ticket: 3 steps, auto-advance on tile tap, selection always changeable =====
  (function () {
    const form = document.getElementById('qq');
    if (!form) return;
    const steps = [...form.querySelectorAll('.qq-step')];
    const bars = [...form.querySelectorAll('.qq-bars i')];
    const count = document.getElementById('qqCount');
    const sel = document.getElementById('qqSel');
    const selVal = document.getElementById('qqSelVal');
    const done = document.getElementById('qqDone');
    let cur = 0;

    function picked() { const r = form.querySelector('input[name=load]:checked'); return r ? r.value : ''; }
    function paintSel() {
      const v = picked();
      // the chosen load shows on later steps and can always be changed
      if (v && cur > 0) { selVal.textContent = v; sel.classList.add('on'); }
      else sel.classList.remove('on');
    }
    function show(i) {
      cur = i;
      steps.forEach((s, n) => s.classList.toggle('on', n === i));
      bars.forEach((b, n) => b.classList.toggle('on', n <= i));
      if (count) count.textContent = 'Step ' + (i + 1) + ' / 3';
      form.querySelectorAll('.qq-err').forEach(e => e.classList.remove('show'));
      paintSel();
    }
    function valid(i) {
      const err = document.getElementById('qqE' + (i + 1));
      let ok = true;
      if (i === 0) ok = !!picked();
      if (i === 1) ok = form.where.value.trim().length > 1;
      if (i === 2) ok = form.name.value.trim().length > 0 && form.phone.value.trim().length > 0;
      if (!ok && err) err.classList.add('show');
      return ok;
    }
    // picking a tile advances straight to the next question
    form.querySelectorAll('input[name=load]').forEach(r => r.addEventListener('change', () => {
      document.getElementById('qqE1').classList.remove('show');
      if (cur === 0) setTimeout(() => show(1), 140);
      else paintSel();
    }));
    document.getElementById('qqChange').addEventListener('click', () => show(0));
    form.querySelectorAll('.qq-next').forEach(b => b.addEventListener('click', () => {
      if (valid(cur)) show(Math.min(cur + 1, steps.length - 1));
    }));
    form.querySelectorAll('.qq-back').forEach(b => b.addEventListener('click', () => show(Math.max(cur - 1, 0))));
    form.querySelectorAll('input').forEach(el => el.addEventListener('input', () => {
      const e = document.getElementById('qqE' + (cur + 1)); if (e) e.classList.remove('show');
    }));
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (form.company.value) return;               // honeypot
      if (!valid(2)) return;
      track('qualify_lead', { form_name: 'lift-ticket' });
      const subject = encodeURIComponent('Lift quote request: ' + form.name.value.trim());
      const body = encodeURIComponent(
        'What needs lifting: ' + (picked() || '(not given)') +
        '\nWhere: ' + form.where.value.trim() +
        '\nHeight / weight: ' + (form.reach.value.trim() || '(not given)') +
        '\n\nName/business: ' + form.name.value.trim() +
        '\nPhone: ' + form.phone.value.trim() +
        '\nEmail: ' + (form.email.value.trim() || '(not given)'));
      window.location.href = 'mailto:Coopercranefl@gmail.com?subject=' + subject + '&body=' + body;
      steps.forEach(s => s.classList.remove('on'));
      sel.classList.remove('on');
      done.classList.add('on');
      if (count) count.textContent = 'Done';
      bars.forEach(b => b.classList.add('on'));
    });

    // service pages preselect a load and open on question two; still changeable
    const pre = form.getAttribute('data-preselect');
    if (pre) {
      const hit = [...form.querySelectorAll('input[name=load]')].find(r => r.value === pre);
      if (hit) { hit.checked = true; show(1); }
    }
  })();

})();
