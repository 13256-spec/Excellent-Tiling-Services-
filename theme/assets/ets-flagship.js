(() => {
  if (window.etsRetailInstalled) return;
  window.etsRetailInstalled = true;
  // Original Shopify adaptations of React Bits Split Text and Animated Content.
  // No React/GSAP runtime. Content is always visible before enhancement.
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const seen = new WeakSet();
  const animations = new Map();
  const splits = new Map();
  const selector = '.ets-section-head h2,.ets-support-intro h2,.ets-footer-intro h2,.ets-category-tile,.ets-department-feature';
  function play(element, frames, options = {}) {
    const animation = element.animate(frames, {duration: 620, easing: 'cubic-bezier(.16,1,.3,1)', ...options});
    animations.set(animation, element);
    animation.finished.then(() => animations.delete(animation), () => animations.delete(animation));
    return animation;
  }
  function restore(heading) {
    const original = splits.get(heading);
    if (!original) return;
    heading.replaceChildren(...original.nodes);
    if (original.label === null) heading.removeAttribute('aria-label');
    else heading.setAttribute('aria-label', original.label);
    splits.delete(heading);
  }
  function revealHeading(heading) {
    if (heading.children.length) return;
    const text = heading.textContent;
    const original = {nodes: [...heading.childNodes], label: heading.getAttribute('aria-label')};
    const fragment = document.createDocumentFragment();
    const words = [];
    text.split(/(\s+)/).forEach(part => {
      if (!part.trim()) fragment.append(document.createTextNode(part));
      else {
        const word = document.createElement('span');
        word.className = 'ets-motion-word';
        word.textContent = part;
        word.setAttribute('aria-hidden', 'true');
        fragment.append(word);
        words.push(word);
      }
    });
    splits.set(heading, original);
    heading.setAttribute('aria-label', text);
    heading.replaceChildren(fragment);
    const running = words.map((word, index) => play(word,
      [{opacity: .3, transform: 'translateY(.45em)'}, {opacity: 1, transform: 'none'}],
      {delay: Math.min(index * 42, 250), fill: 'backwards'}));
    Promise.allSettled(running.map(a => a.finished)).then(() => restore(heading));
  }
  const observer = new IntersectionObserver(entries => entries.forEach(({target, isIntersecting}) => {
    if (!isIntersecting) return;
    observer.unobserve(target);
    if (reduced.matches || window.Shopify?.designMode) return;
    if (target.tagName === 'H2') revealHeading(target);
    else {
      const index = [...target.parentElement.children].indexOf(target);
      play(target, [{opacity: .55, transform: 'translateY(20px)'}, {opacity: 1, transform: 'none'}],
        {delay: Math.min(index % 6 * 55, 220), fill: 'backwards'});
    }
  }), {threshold: .12});
  function mount(root) {
    root.querySelectorAll(selector).forEach(el => {
      if (!seen.has(el)) {seen.add(el); observer.observe(el);}
    });
    root.querySelectorAll('[data-ets-store-header]').forEach(header => {
      if (header.etsCleanup) return;
      const controller = new AbortController();
      const opts = {signal: controller.signal};
      const menu = header.querySelector('.ets-mobile-nav');
      const mega = header.querySelector('.ets-mega');
      document.addEventListener('click', event => {if (mega && !mega.contains(event.target)) mega.open = false;}, opts);
      header.addEventListener('focusout', event => {if (mega && !mega.contains(event.relatedTarget)) mega.open = false;}, opts);
      header.addEventListener('keydown', event => {
        if (event.key !== 'Escape') return;
        const open = [mega, menu].find(el => el?.open);
        if (open) {open.open = false; open.querySelector('summary').focus(); event.preventDefault();}
      }, opts);
      window.addEventListener('resize', () => {if (innerWidth >= 990 && menu) menu.open = false; if (innerWidth < 990 && mega) mega.open = false;}, opts);
      header.etsCleanup = () => controller.abort();
    });
  }
  mount(document);
  reduced.addEventListener('change', () => {
    if (!reduced.matches) return;
    animations.forEach((_, animation) => animation.cancel());
    [...splits.keys()].forEach(restore);
  });
  document.addEventListener('shopify:section:load', event => mount(event.target));
  document.addEventListener('shopify:section:unload', event => {
    const root = event.target;
    root.querySelectorAll('[data-ets-store-header]').forEach(el => {el.etsCleanup?.(); delete el.etsCleanup;});
    root.querySelectorAll(selector).forEach(el => {observer.unobserve(el); seen.delete(el);});
    animations.forEach((el, animation) => {if (root.contains(el)) animation.cancel();});
    [...splits.keys()].forEach(el => {if (root.contains(el)) restore(el);});
  });
})();
