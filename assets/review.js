/* Paper-review behaviour: lightbox for images and evidence links, marker cross-highlighting, cross-file arrows. */
(function () {
  const ready = (fn) => (document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", fn) : fn());
  ready(function () {
    /* Lightbox */
    const dlg = document.createElement("dialog");
    dlg.className = "rv-lightbox";
    dlg.innerHTML = '<div class="rv-lightbox__bar"><span></span><button type="button">닫기</button></div><div class="rv-lightbox__body"></div>';
    document.body.appendChild(dlg);
    const title = dlg.querySelector("span"), body = dlg.querySelector(".rv-lightbox__body");
    dlg.querySelector("button").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    function open(node, label) {
      body.innerHTML = ""; body.appendChild(node); title.textContent = label || "";
      if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    }
    document.querySelectorAll("img[data-lb]").forEach((im) => im.addEventListener("click", () => {
      const c = new Image(); c.src = im.src; c.alt = im.alt; open(c, im.alt);
    }));
    document.querySelectorAll("a.ev").forEach((a) => a.addEventListener("click", (e) => {
      const t = document.getElementById(a.dataset.lbTarget); if (!t) return;
      e.preventDefault();
      const panel = t.querySelector(".panel");
      if (panel) { const c = panel.cloneNode(true); c.querySelectorAll("[id]").forEach((n) => n.removeAttribute("id")); open(c, a.textContent); return; }
      const im = t.querySelector("img"); if (im) { const c = new Image(); c.src = im.src; c.alt = im.alt; open(c, im.alt); }
    }));

    /* Marker cross-highlighting */
    const lit = (mk, on) => document.querySelectorAll('.hl[data-mk="' + mk + '"], .cl[data-mk="' + mk + '"]').forEach((n) => n.classList.toggle("lit", on));
    document.querySelectorAll(".mk").forEach((n) => {
      const mk = n.dataset.mk;
      n.tabIndex = 0; n.setAttribute("role", "button"); n.setAttribute("aria-label", "구성요소 " + mk + " 강조");
      n.addEventListener("mouseenter", () => lit(mk, true));
      n.addEventListener("mouseleave", () => { if (!n.classList.contains("sticky")) lit(mk, false); });
      n.addEventListener("focus", () => lit(mk, true));
      n.addEventListener("blur", () => { if (!n.classList.contains("sticky")) lit(mk, false); });
      n.addEventListener("click", () => {
        const on = !n.classList.contains("sticky");
        document.querySelectorAll(".mk.sticky").forEach((s) => { s.classList.remove("sticky"); lit(s.dataset.mk, false); });
        if (on) { n.classList.add("sticky"); lit(mk, true); }
      });
    });

    /* Cross-file arrows inside galleries: data-links="fromId>toId,fromId>toId" */
    const NS = "http://www.w3.org/2000/svg";
    function draw(wrap) {
      let svg = wrap.querySelector("svg.rv-arrows");
      if (!svg) { svg = document.createElementNS(NS, "svg"); svg.setAttribute("class", "rv-arrows"); svg.setAttribute("aria-hidden", "true"); wrap.prepend(svg); }
      svg.innerHTML = '<defs><marker id="rv-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8b5a8f"/></marker></defs>';
      const box = wrap.getBoundingClientRect();
      const stacked = window.matchMedia("(max-width: 900px)").matches;
      (wrap.dataset.links || "").split(",").filter(Boolean).forEach((pair) => {
        const [f, t] = pair.split(">");
        const a = document.getElementById(f), b = document.getElementById(t); if (!a || !b) return;
        const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
        const y1 = ra.top + ra.height / 2 - box.top, y2 = rb.top + rb.height / 2 - box.top;
        let x1, x2, d;
        if (stacked || Math.abs(ra.left - rb.left) < 40) {
          x1 = ra.right - box.left - 4; x2 = rb.right - box.left - 4;
          const bg = Math.min(box.width + 14, Math.max(x1, x2) + 30);
          d = `M${x1},${y1} C${bg},${y1} ${bg},${y2} ${x2},${y2}`;
        } else if (rb.left < ra.left) {
          x1 = ra.left - box.left - 2; x2 = rb.right - box.left + 2; const m = (x1 + x2) / 2;
          d = `M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}`;
        } else {
          x1 = ra.right - box.left - 2; x2 = rb.left - box.left + 2; const m = (x1 + x2) / 2;
          d = `M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}`;
        }
        const p = document.createElementNS(NS, "path");
        p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", "#8b5a8f");
        p.setAttribute("stroke-width", "2"); p.setAttribute("stroke-dasharray", "5 4"); p.setAttribute("marker-end", "url(#rv-ah)");
        svg.appendChild(p);
      });
    }
    const wraps = document.querySelectorAll(".gallery-wrap[data-links]");
    const redraw = () => wraps.forEach(draw);
    redraw(); window.addEventListener("resize", redraw); window.addEventListener("load", redraw);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(redraw);
  });
})();
