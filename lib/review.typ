// Helpers for paper-review posts (paper-review-blog skill, tufted export).
// Every helper emits plain HTML elements styled by assets/review.css and wired by assets/review.js.

#import "/config.typ": base

// Load the review behaviour (lightbox, marker highlighting, cross-file arrows). Put once per post.
#let review-scripts() = html.elem("script", attrs: (src: base + "/assets/review.js", defer: ""))

// Component marker ①–④. The same number means the same component in figure, text and code.
#let mk(n) = html.elem("span", attrs: (class: "mk", "data-mk": str(n)))[#n]

// Highlight a phrase in the colour of component n.
#let hl(n, body) = html.elem("span", attrs: (class: "hl", "data-mk": str(n)), body)

// Boxed note, e.g. callout("💡", [...]) or callout("✏️", [...], kind: "define").
#let callout(icon, body, kind: "note") = html.elem("aside", attrs: (class: "callout callout--" + kind))[
  #html.elem("span", attrs: (class: "callout__icon", "aria-hidden": "true"))[#icon]
  #html.elem("div", attrs: (class: "callout__body"), body)
]

// Critique or reaction paragraph with a coloured rule.
#let crit(body) = html.elem("div", attrs: (class: "crit"), body)
#let wow(body) = html.elem("div", attrs: (class: "wow"), body)

// Bold lead sentence before the bullets that read a figure.
#let lead(body) = html.elem("p", attrs: (class: "lead"), strong(body))

// Phrase that opens the element with the given id in the lightbox.
#let ev(target, body) = html.elem("a", attrs: (class: "ev", href: "#" + target, "data-lb-target": target), body)

// Plain image (opens full size on click).
#let img(src, alt, width: none) = {
  let attrs = (src: src, alt: alt, "data-lb": "")
  if width != none { attrs.insert("width", str(width)) }
  html.elem("img", attrs: attrs)
}

// Thumbnail with a short caption in the margin (opens full size on click).
// Wrap the image in box() so Typst keeps it inline; otherwise it opens a <p> inside the note.
#let margin-img(src, alt, caption) = html.span(class: "marginnote rv-thumb", box(img(src, alt)) + html.span(class: "rv-thumb__cap", caption))

// Figure in the main column with the caption in the margin (Tufte style).
#let fig(id, src, alt, take, credit) = html.elem("figure", attrs: (id: id, class: "rv-fig"))[
  #html.elem("span", attrs: (class: "marginnote"))[#strong(take) #credit]
  #img(src, alt)
]

// Wide figure spanning text and margin, caption underneath.
#let wide-fig(id, src, alt, take, credit) = html.elem("figure", attrs: (id: id, class: "rv-fig fullwidth"))[
  #img(src, alt)
  #html.elem("figcaption")[#html.elem("span", attrs: (class: "take"))[#take] #credit]
]

// Two panels side by side (e.g. unmodified original + reviewer's redraw), caption underneath.
#let pair(id, left, right, take, credit, left-label: none, right-label: none) = html.elem("figure", attrs: (id: id, class: "rv-pair fullwidth"))[
  #html.elem("div", attrs: (class: "pair"))[
    #html.elem("div", attrs: (class: "pair__cell"))[
      #if left-label != none { html.elem("p", attrs: (class: "tag"))[#left-label] }
      #left
    ]
    #html.elem("div", attrs: (class: "pair__cell pair__cell--note"))[
      #if right-label != none { html.elem("p", attrs: (class: "tag"))[#right-label] }
      #right
    ]
  ]
  #html.elem("figcaption")[#html.elem("span", attrs: (class: "take"))[#take] #credit]
]

// Handwritten memo text.
#let hand(body, color: "#9f231c") = html.elem("p", attrs: (class: "hand", style: "color:" + color), body)

// Code excerpt. Pass the file text from the post: code-panel(read("code/trunk.py"), ...)
// (read() resolves paths relative to the file that calls it, so the post must do the reading).
//   segments: ((from, to), ...) line ranges to show
//   marks:    ((from, to, n), ...) background colour of component n
//   badges:   (line: n, ...) marker badge at the end of a line
//   anchors:  (line: "id", ...) element ids used by the cross-file arrows
#let code-panel(source, segments, marks: (), badges: (:), anchors: (:)) = {
  let lines = source.split("\n")
  html.elem("div", attrs: (class: "code"))[
    #let prev = none
    #for (a, b) in segments {
      if prev != none and a > prev + 1 {
        html.elem("div", attrs: (class: "gap"))[⋯ L#(prev + 1)–#(a - 1) 생략]
      }
      for n in range(a, b + 1) {
        let mkn = none
        for (x, y, m) in marks { if x <= n and n <= y { mkn = m } }
        let attrs = (class: "cl")
        if mkn != none { attrs.insert("data-mk", str(mkn)) }
        if str(n) in anchors { attrs.insert("id", anchors.at(str(n))) }
        html.elem("div", attrs: attrs)[
          #html.elem("span", attrs: (class: "ln"))[#n]
          #html.elem("span", attrs: (class: "tx"))[#lines.at(n - 1)]
          #html.elem("span", attrs: (class: "bd"))[#if str(n) in badges { mk(badges.at(str(n))) }]
        ]
      }
      prev = b
    }
  ]
}

// Panel with a file-name header around any content (code panel or text).
#let panel(head, note, body) = html.elem("div", attrs: (class: "panel"))[
  #html.elem("div", attrs: (class: "panel__head"))[#html.elem("b")[#head] #html.elem("span")[#note]]
  #body
]

// Gallery of panels; arrows between anchors are drawn by review.js from data-links ("from>to,from>to").
#let gallery(links: "", ..items) = html.elem("div", attrs: (class: "gallery-wrap fullwidth", "data-links": links))[
  #html.elem("div", attrs: (class: "gallery"))[#for it in items.pos() { it }]
]

// One gallery cell: panel plus two-part caption.
#let cell(id, body, take, credit) = html.elem("figure", attrs: (id: id, class: "cell"))[
  #body
  #html.elem("figcaption")[#html.elem("span", attrs: (class: "take"))[#take] #credit]
]

// Row in the version timeline at the top of a post.
#let versions(..items) = html.elem("ol", attrs: (class: "versions"))[
  #for (title, note) in items.pos() {
    html.elem("li")[#html.elem("b")[#title] #html.elem("span")[#note]]
  }
]

// Wide block (tables, charts) that may use the margin.
#let wide(body) = html.elem("div", attrs: (class: "fullwidth rv-wide"), body)
