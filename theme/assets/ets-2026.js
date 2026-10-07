/* Excellent Tiling Services — 2026 storefront behaviour.
   Header mega menu + mobile drawer, cart count, scroll reveal, product rails/tabs,
   tile quantity calculator. No dependencies. Content is usable before this runs. */
(() => {
  if (window.etsInstalled) return;
  window.etsInstalled = true;

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const mq = window.matchMedia('(min-width: 990px)');

  /* ---------- Mega menu ---------- */
  // Desktop behaviour: the label is a link, the chevron toggles. With a mouse the panel opens once
  // the pointer rests on an item (so sweeping across the bar doesn't flash panels), stays open while
  // the pointer is anywhere over the item or its panel, and closes shortly after it leaves.
  const OPEN_DELAY = 140;   // first panel
  const SWITCH_DELAY = 90;  // moving between items while a panel is already open
  const CLOSE_DELAY = 280;
  function initMega(root) {
    const items = $$('[data-ets-mega-item]', root).filter((i) => $('[data-ets-mega-trigger]', i));
    if (!items.length) return;
    const hdr = $('[data-ets-hdr]', root);
    const scrim = $('[data-ets-scrim]', root);
    let openTimer;
    let closeTimer;
    let hoverOpenedAt = 0;
    const current = () => items.find((i) => i.classList.contains('is-open'));
    const trigger = (item) => $('[data-ets-mega-trigger]', item);
    const fit = (item) => {
      // Keep the whole panel on screen below the (sticky) header; anything taller scrolls inside it.
      const bottom = hdr ? hdr.getBoundingClientRect().bottom : 0;
      item.style.setProperty('--ets-mega-max', `${Math.max(240, window.innerHeight - bottom - 48)}px`);
    };
    const close = (item) => {
      if (!item || !item.classList.contains('is-open')) return;
      item.classList.remove('is-open');
      trigger(item).setAttribute('aria-expanded', 'false');
      if (!current() && scrim) scrim.classList.remove('is-on');
    };
    const closeAll = () => { clearTimeout(openTimer); clearTimeout(closeTimer); items.forEach(close); };
    const open = (item) => {
      clearTimeout(openTimer);
      clearTimeout(closeTimer);
      items.forEach((i) => i !== item && close(i));
      if (item.classList.contains('is-open')) return;
      fit(item);
      item.classList.add('is-open');
      trigger(item).setAttribute('aria-expanded', 'true');
      if (scrim) scrim.classList.add('is-on');
    };
    const isMouse = (e) => e.pointerType === 'mouse' && mq.matches;

    items.forEach((item) => {
      trigger(item).addEventListener('click', () => {
        // A click just after the hover opened it means "open", not "close again".
        if (item.classList.contains('is-open') && Date.now() - hoverOpenedAt > 500) close(item); else open(item);
      });
      item.addEventListener('pointerenter', (e) => {
        if (!isMouse(e)) return;
        clearTimeout(closeTimer);
        if (item.classList.contains('is-open')) return;
        clearTimeout(openTimer);
        openTimer = setTimeout(() => { hoverOpenedAt = Date.now(); open(item); }, current() ? SWITCH_DELAY : OPEN_DELAY);
      });
      item.addEventListener('pointerleave', (e) => {
        if (!isMouse(e)) return;
        clearTimeout(openTimer);
        if (item.classList.contains('is-open')) closeTimer = setTimeout(() => close(item), CLOSE_DELAY);
      });
      item.addEventListener('focusout', (e) => { if (!item.contains(e.relatedTarget)) close(item); });
    });
    // Non-panel items (e.g. Renovations): hovering them closes an open panel promptly.
    $$('[data-ets-mega-item]', root).filter((i) => !items.includes(i)).forEach((i) => {
      i.addEventListener('pointerenter', (e) => {
        if (!isMouse(e) || !current()) return;
        clearTimeout(closeTimer);
        closeTimer = setTimeout(closeAll, SWITCH_DELAY);
      });
    });
    if (scrim) scrim.addEventListener('click', closeAll);
    document.addEventListener('click', (e) => { if (current() && !current().contains(e.target)) closeAll(); });
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const openItem = current();
      if (openItem) { close(openItem); trigger(openItem).focus(); }
    });
    window.addEventListener('resize', () => { const o = current(); if (o) fit(o); });
    mq.addEventListener('change', closeAll);
  }

  /* ---------- Mobile drawer ---------- */
  function initDrawer(root) {
    const drawer = $('[data-ets-drawer]', root);
    if (!drawer) return;
    const openers = $$('[data-ets-drawer-open]', root);
    let last;
    const setOpen = (on) => {
      drawer.classList.toggle('is-open', on);
      drawer.setAttribute('aria-hidden', on ? 'false' : 'true');
      openers.forEach((b) => b.setAttribute('aria-expanded', on ? 'true' : 'false'));
      document.documentElement.style.overflow = on ? 'hidden' : '';
      if (on) { last = document.activeElement; setTimeout(() => { const f = $('[data-ets-drawer-close].ets-burger', drawer); if (f) f.focus(); }, 60); }
      else if (last) last.focus();
    };
    openers.forEach((b) => b.addEventListener('click', () => setOpen(true)));
    $$('[data-ets-drawer-close]', drawer).forEach((b) => b.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && drawer.classList.contains('is-open')) setOpen(false); });
    mq.addEventListener('change', (e) => { if (e.matches) setOpen(false); });
  }

  /* ---------- Cart count + drawer ---------- */
  function setCount(n) {
    $$('[data-ets-cart-count]').forEach((el) => { el.textContent = n; el.hidden = !n; });
  }
  function refreshCount() {
    fetch(`${window.Shopify && Shopify.routes ? Shopify.routes.root : '/'}cart.js`, { headers: { Accept: 'application/json' } })
      .then((r) => r.json()).then((c) => setCount(c.item_count)).catch(() => {});
  }
  document.addEventListener('cart:update', (e) => {
    const d = e.detail || {};
    const n = d.resource && typeof d.resource.item_count === 'number' ? d.resource.item_count
      : d.data && typeof d.data.itemCount === 'number' ? d.data.itemCount : null;
    if (n === null) refreshCount(); else setCount(n);
  });
  document.addEventListener('click', (e) => {
    const link = e.target.closest('[data-ets-cart]');
    if (!link) return;
    const drawer = document.getElementById('cart-drawer');
    if (drawer && typeof drawer.open === 'function') { e.preventDefault(); drawer.open(); }
  });
  window.addEventListener('pageshow', (e) => { if (e.persisted) refreshCount(); });

  /* ---------- Reveal on scroll ---------- */
  function initReveal(root) {
    const els = $$('[data-reveal]:not(.is-in)', root);
    if (!('IntersectionObserver' in window)) { els.forEach((el) => el.classList.add('is-in')); return; }
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach((el) => io.observe(el));
  }

  /* ---------- Product rails + tabs ---------- */
  function initRails(root) {
    $$('[data-ets-tabs]', root).forEach((wrap) => {
      const tabs = $$('[role="tab"]', wrap);
      const panels = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
      const select = (i) => tabs.forEach((t, j) => {
        t.setAttribute('aria-selected', i === j ? 'true' : 'false');
        t.tabIndex = i === j ? 0 : -1;
        if (panels[j]) panels[j].hidden = i !== j;
      });
      tabs.forEach((t, i) => {
        t.addEventListener('click', () => select(i));
        t.addEventListener('keydown', (e) => {
          if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
          const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
          select(n); tabs[n].focus();
        });
      });
    });
    $$('[data-ets-rail-nav]', root).forEach((nav) => {
      const scope = nav.closest('[data-ets-rail-scope]') || document;
      const step = (dir) => {
        const rail = $$('[data-ets-rail]', scope).find((r) => !r.hidden);
        if (rail) rail.scrollBy({ left: dir * rail.clientWidth * 0.9, behavior: 'smooth' });
      };
      $('.is-prev', nav).addEventListener('click', () => step(-1));
      $('.is-next', nav).addEventListener('click', () => step(1));
    });
  }

  /* ---------- Tile calculator (product page, delegated so re-renders keep working) ---------- */
  function calcState(calc) {
    const len = $('[data-len]', calc), wid = $('[data-wid]', calc), area = $('[data-area]', calc);
    const waste = $('[data-waste]', calc), out = $('[data-out]', calc), apply = $('[data-apply]', calc);
    return { len, wid, area, waste, out, apply };
  }
  function calcUpdate(calc, fromDims) {
    const c = calcState(calc);
    if (fromDims && c.len && c.wid) {
      const l = parseFloat(c.len.value), w = parseFloat(c.wid.value);
      if (l > 0 && w > 0) c.area.value = (l * w).toFixed(2);
    }
    const a = parseFloat(c.area.value);
    if (a > 0) {
      const qty = Math.ceil(a * (1 + parseFloat(c.waste.value) / 100));
      calc.dataset.qty = qty;
      c.out.textContent = `${qty} m²`;
      c.apply.disabled = false;
      c.apply.textContent = `Set quantity to ${qty} m²`;
    } else {
      calc.dataset.qty = '';
      c.out.textContent = '—';
      c.apply.disabled = true;
    }
  }
  document.addEventListener('input', (e) => {
    const calc = e.target.closest('[data-ets-calc]');
    if (calc) calcUpdate(calc, e.target.matches('[data-len],[data-wid]'));
  });
  document.addEventListener('change', (e) => {
    const calc = e.target.closest('[data-ets-calc]');
    if (calc && e.target.matches('[data-waste]')) calcUpdate(calc, false);
  });
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-ets-calc] [data-apply]');
    if (!btn) return;
    const calc = btn.closest('[data-ets-calc]');
    const qty = parseInt(calc.dataset.qty, 10);
    if (!qty) return;
    const scope = calc.closest('.shopify-section') || document;
    const input = $('input[name="quantity"]', scope) || $('input[name="quantity"]');
    if (!input) return;
    input.value = qty;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    btn.textContent = `Quantity set to ${qty} m² ✓`;
    const submit = $('[name="add"], button[type="submit"].add-to-cart-button, form[action*="/cart/add"] [type="submit"]', scope);
    if (submit) submit.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  /* ---------- Hero image slideshow ---------- */
  function initSlides(root) {
    $$('[data-ets-slides]', root).forEach((wrap) => {
      if (wrap.dataset.ready) return;
      wrap.dataset.ready = '1';
      const slides = $$('[data-slide]', wrap);
      const dots = $$('[data-dot]', wrap);
      if (slides.length < 2) return;
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const interval = (parseInt(wrap.dataset.interval, 10) || 6) * 1000;
      let index = 0;
      let timer;
      let paused = false;
      let visible = true;

      const show = (n) => {
        index = (n + slides.length) % slides.length;
        slides.forEach((s, i) => {
          const on = i === index;
          s.classList.toggle('is-active', on);
          if (on) s.removeAttribute('aria-hidden'); else s.setAttribute('aria-hidden', 'true');
          $$('a', s).forEach((a) => { if (on) a.removeAttribute('tabindex'); else a.setAttribute('tabindex', '-1'); });
        });
        dots.forEach((d, i) => { if (i === index) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
        preload(index + 1);
      };
      // Load the next image ahead of time so it's ready when it fades in.
      const preload = (n) => {
        const img = $('img', slides[(n + slides.length) % slides.length]);
        if (img && img.loading === 'lazy') img.loading = 'eager';
      };
      const stop = () => { clearInterval(timer); timer = null; };
      const start = () => {
        stop();
        if (reduced || paused || !visible || document.hidden) return;
        timer = setInterval(() => show(index + 1), interval);
      };

      dots.forEach((d) => d.addEventListener('click', () => { show(parseInt(d.dataset.dot, 10)); start(); }));
      wrap.addEventListener('mouseenter', () => { paused = true; stop(); });
      wrap.addEventListener('mouseleave', () => { paused = false; start(); });
      wrap.addEventListener('focusin', () => { paused = true; stop(); });
      wrap.addEventListener('focusout', () => { paused = false; start(); });
      document.addEventListener('visibilitychange', start);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(([e]) => { visible = e.isIntersecting; start(); }).observe(wrap);
      }
      document.addEventListener('shopify:block:select', (e) => {
        const i = slides.indexOf(e.target);
        if (i > -1) { show(i); paused = true; stop(); }
      });
      document.addEventListener('shopify:block:deselect', () => { paused = false; start(); });
      if (document.readyState === 'complete') preload(index + 1);
      else window.addEventListener('load', () => preload(index + 1), { once: true });
      start();
    });
  }

  /* ---------- Email sign-up pop-up ---------- */
  const POP_KEY = 'ets-news-popup';
  const store = {
    get() { try { return parseInt(localStorage.getItem(POP_KEY), 10) || 0; } catch (e) { return 0; } },
    set(v) { try { localStorage.setItem(POP_KEY, String(v)); } catch (e) { /* storage blocked */ } }
  };
  const FOREVER = 4102444800000; // 2100-01-01: never show again after subscribing

  function initPopup() {
    const pop = $('[data-ets-pop]');
    if (!pop || pop.dataset.ready || typeof pop.showModal !== 'function') return;
    pop.dataset.ready = '1';
    const formId = pop.dataset.form;
    const hash = location.hash.slice(1);
    const open = () => {
      if (pop.open || $('dialog[open]')) return;
      pop.showModal();
      const title = $('h2', pop);
      if (title) title.focus({ preventScroll: true });
    };

    // Shopify returns to #FormId after a sign-up. Only the form that was sent keeps its message.
    $$('[data-ets-news]').forEach((f) => {
      const msg = $('[data-ets-news-msg]', f);
      if (msg && f.id !== hash) msg.remove();
      else if (msg && msg.classList.contains('ets-alert--ok')) store.set(FOREVER);
    });

    pop.addEventListener('click', (e) => {
      if (e.target === pop || e.target.closest('[data-ets-pop-close]')) pop.close();
    });
    pop.addEventListener('close', () => {
      if (store.get() < Date.now()) store.set(Date.now() + (parseInt(pop.dataset.days, 10) || 30) * 864e5);
    });

    if (window.Shopify && Shopify.designMode) {
      document.addEventListener('shopify:section:select', (e) => { if (e.detail.sectionId === pop.dataset.section) open(); });
      document.addEventListener('shopify:section:deselect', (e) => { if (e.detail.sectionId === pop.dataset.section && pop.open) pop.close(); });
      return;
    }
    if (hash === formId) { open(); return; }
    if (store.get() > Date.now()) return;

    const delay = (parseInt(pop.dataset.delay, 10) || 12) * 1000;
    let armed = false;
    // Don't cover a Shopify Inbox chat the visitor has open.
    const fire = () => { cleanup(); if (!$('shopify-chat[open]')) open(); };
    const timer = setTimeout(fire, delay);
    const exit = (e) => { if (armed && !e.relatedTarget && e.clientY <= 0) fire(); };
    const armTimer = setTimeout(() => { armed = true; }, 4000);
    const cleanup = () => { clearTimeout(timer); clearTimeout(armTimer); document.removeEventListener('mouseout', exit); };
    if (mq.matches) document.addEventListener('mouseout', exit);
  }

  function init(root = document) {
    const header = $('[data-ets-header]', root) || (root.matches && root.matches('[data-ets-header]') ? root : null);
    if (header && !header.dataset.ready) { header.dataset.ready = '1'; initMega(header); initDrawer(header); }
    initReveal(root);
    initRails(root);
    initSlides(root);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { init(); initPopup(); });
  else { init(); initPopup(); }
  document.addEventListener('shopify:section:load', (e) => { init(e.target); initPopup(); });
})();
