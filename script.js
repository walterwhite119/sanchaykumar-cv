(function () {
  const C = window.PORTFOLIO;
  const $ = (s, el = document) => el.querySelector(s);

  // Image with graceful placeholder if the file doesn't exist yet
  function img(src, alt) {
    const i = document.createElement("img");
    i.loading = "lazy";
    i.alt = alt || "";
    i.src = src;
    i.onerror = () => i.parentElement && i.parentElement.classList.add("missing");
    return i;
  }

  // Text fields
  document.querySelectorAll("[data-field]").forEach((el) => {
    const v = C[el.dataset.field];
    if (v) el.textContent = v;
  });
  document.title = `${C.name} — Model`;
  $("#year").textContent = new Date().getFullYear();

  // Hero image
  const hero = $(".hero-img img");
  hero.onerror = () => hero.parentElement.classList.add("missing");
  hero.src = hero.dataset.src;

  // Stats
  $("#stats").innerHTML = C.stats
    .filter(([, v]) => v)
    .map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`)
    .join("");

  // Comp card
  const cc = $("#compcard-link");
  if (C.compCard) cc.href = C.compCard; else cc.remove();

  // Book + filters
  const grid = $("#grid");
  const items = C.book.map((p, idx) => {
    const fig = document.createElement("figure");
    fig.className = "tile";
    fig.dataset.category = p.category;
    fig.tabIndex = 0;
    fig.appendChild(img(p.src, p.credit));
    fig.addEventListener("click", () => openLB(idx));
    fig.addEventListener("keydown", (e) => e.key === "Enter" && openLB(idx));
    grid.appendChild(fig);
    return fig;
  });

  const filters = $("#filters");
  C.categories.forEach((cat, i) => {
    const b = document.createElement("button");
    b.textContent = cat;
    b.setAttribute("role", "tab");
    b.setAttribute("aria-selected", i === 0);
    b.onclick = () => {
      filters.querySelectorAll("button").forEach((x) => x.setAttribute("aria-selected", x === b));
      items.forEach((f) => (f.hidden = cat !== "All" && f.dataset.category !== cat));
    };
    filters.appendChild(b);
  });

  // Digitals
  const dg = $("#digitals-grid");
  C.digitals.forEach((d) => {
    const fig = document.createElement("figure");
    fig.appendChild(img(d.src, `Digital — ${d.label}`));
    const cap = document.createElement("figcaption");
    cap.textContent = d.label;
    fig.appendChild(cap);
    dg.appendChild(fig);
  });

  // Lists
  const li = (arr) => arr.filter(Boolean).map((x) => `<li>${x}</li>`).join("");
  $("#experience").innerHTML = li(C.experience);
  $("#skills").innerHTML = li(C.skills);

  // Contact
  $("#contact-list").innerHTML = C.contact
    .filter((c) => c.value)
    .map((c) => `<div><span>${c.label}</span>${c.href ? `<a href="${c.href}" target="_blank" rel="noopener">${c.value}</a>` : c.value}</div>`)
    .join("");

  // Lightbox (only cycles through currently visible tiles)
  const lb = $("#lightbox");
  const lbImg = $("img", lb);
  const lbCap = $("figcaption", lb);
  let visible = [], pos = 0;

  function show() {
    const p = C.book[visible[pos]];
    lbImg.src = p.src;
    lbCap.textContent = p.credit || "";
  }
  function openLB(idx) {
    visible = C.book.map((_, i) => i).filter((i) => !items[i].hidden);
    pos = visible.indexOf(idx);
    show();
    lb.hidden = false;
    document.body.style.overflow = "hidden";
  }
  function close() { lb.hidden = true; document.body.style.overflow = ""; }
  const step = (d) => { pos = (pos + d + visible.length) % visible.length; show(); };

  $(".lb-close", lb).onclick = close;
  $(".lb-prev", lb).onclick = () => step(-1);
  $(".lb-next", lb).onclick = () => step(1);
  lb.addEventListener("click", (e) => e.target === lb && close());
  document.addEventListener("keydown", (e) => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
})();
