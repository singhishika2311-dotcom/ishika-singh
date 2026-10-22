// Runs inside a hidden Streamlit component iframe and animates the parent page:
// charts grow from zero and numbers count up every time they scroll into view.
(() => {
  const w = window.parent, doc = w.document;
  if (w.__chartAnim) return w.__chartAnim.scan();
  if (w.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const SLOW = 1.8;  // animation speed: 1 = fast, 2 = twice as slow — tweak to taste
  const EASE = "cubic-bezier(.22,1,.36,1)";
  const seen = new WeakSet();

  function countUp(el, dur = 1200 * SLOW) {
    if (el.__orig === undefined) el.__orig = el.textContent;  // remember the real value once
    const text = el.__orig, m = text.match(/-?\d[\d,]*\.?\d*/), id = (el.__countId = (el.__countId || 0) + 1);
    if (!m) return;
    const raw = m[0], target = parseFloat(raw.replace(/,/g, "")), dec = (raw.split(".")[1] || "").length;
    const pre = text.slice(0, m.index), post = text.slice(m.index + raw.length), t0 = w.performance.now();
    const fmt = v => v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const step = now => {
      if (id !== el.__countId) return;  // a newer count-up took over
      const p = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + fmt(target * e) + post;
      if (p < 1) w.requestAnimationFrame(step); else el.textContent = text;
    };
    w.requestAnimationFrame(step);
  }

  function grow(el, from, origin, delay = 0, dur = 900) {
    el.style.transformBox = "fill-box";
    el.style.transformOrigin = origin;
    el.animate([{ transform: from, opacity: 0 }, { transform: "none", opacity: 1 }],
               { duration: dur * SLOW, delay: delay * SLOW, easing: EASE, fill: "backwards" });
  }

  const fade = (el, delay = 0, dur = 700) =>
    el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: dur * SLOW, delay: delay * SLOW, easing: "ease-out", fill: "backwards" });

  function animateChart(gd) {
    gd.getAnimations({ subtree: true }).forEach(a => a.cancel());  // restart cleanly
    const horiz = (gd._fullData || []).some(t => t.orientation === "h" && (t.type === "bar" || t.type === "histogram"));

    // Bars and histograms: grow from the axis
    gd.querySelectorAll(".barlayer .point path").forEach((p, i) =>
      grow(p, horiz ? "scaleX(0)" : "scaleY(0)", horiz ? "left center" : "center bottom", Math.min(i * 35, 700)));

    // Pie / donut / sunburst: spin open from the centre
    gd.querySelectorAll(".pielayer, .sunburstlayer").forEach(l => grow(l, "scale(.2) rotate(-160deg)", "center", 0, 1100));

    // Radar charts spin open; gauges pop in
    gd.querySelectorAll(".polarlayer").forEach(l => grow(l, "scale(.3) rotate(-60deg)", "center", 0, 1100));
    gd.querySelectorAll(".indicatorlayer").forEach(l => grow(l, "scale(.7)", "center", 0, 900));

    // Box & violin plots: rise from the middle
    gd.querySelectorAll(".boxlayer .trace, .violinlayer .trace").forEach((t, i) =>
      grow(t, "scaleY(0)", "center", i * 80));

    // Scatter dots fade in, lines draw themselves, area fills fade in
    gd.querySelectorAll(".scatterlayer .points path").forEach(p => fade(p, Math.random() * 700, 500));
    gd.querySelectorAll(".scatterlayer .js-line").forEach(line => {
      const len = line.getTotalLength ? line.getTotalLength() : 0;
      if (!len) return;
      line.animate([{ strokeDasharray: `${len} ${len}`, strokeDashoffset: len },
                    { strokeDasharray: `${len} ${len}`, strokeDashoffset: 0 }], { duration: 1400 * SLOW, easing: EASE });
    });
    gd.querySelectorAll(".scatterlayer .js-fill, .heatmaplayer image").forEach(el => fade(el, 300, 1000));

    // Every number drawn inside the chart (bar labels, %, donut centre) counts up from 0
    gd.querySelectorAll(".barlayer text, .pielayer text, .sunburstlayer text, .annotation-text, .heatmaplayer text, .indicatorlayer text").forEach(t => {
      (t.querySelectorAll("tspan").length ? t.querySelectorAll("tspan") : [t]).forEach(el => countUp(el));
    });
  }

  function run(el) {
    if (el.classList.contains("js-plotly-plot")) {
      // Plotly may still be drawing; wait until it has
      if (!el._fullLayout || !el.querySelector(".main-svg")) return setTimeout(() => run(el), 200);
      animateChart(el);
    } else {
      countUp(el);
    }
  }

  // Play when at least 25% is visible; re-arm once it has fully left the screen
  const io = new w.IntersectionObserver(entries => entries.forEach(e => {
    const el = e.target;
    if (e.intersectionRatio >= 0.25 && !el.__played) { el.__played = true; run(el); }
    else if (!e.isIntersecting) el.__played = false;
  }), { threshold: [0, 0.25] });

  function scan() {
    doc.querySelectorAll(".js-plotly-plot, .kpi .value, .insight .big, .side-count .n").forEach(el => {
      if (seen.has(el)) return;
      seen.add(el);
      io.observe(el);
    });
  }

  let pending;
  new w.MutationObserver(() => { clearTimeout(pending); pending = setTimeout(scan, 150); })
    .observe(doc.body, { childList: true, subtree: true });
  w.__chartAnim = { scan };
  scan();
})();
