// Site-wide settings for the Eden blog (tufted template).
// The site is served from https://hongyubinbin.github.io/Eden/, so every absolute path starts with `base`.
#import "@preview/tufted:0.1.1"

#let base = "/Eden"

#let template = tufted.tufted-web.with(
  header-links: (
    base + "/": "Home",
    base + "/posts/": "Posts",
  ),
  title: "Eden",
  lang: "ko",
  css: (
    "https://cdnjs.cloudflare.com/ajax/libs/tufte-css/1.8.0/tufte.min.css",
    base + "/assets/tufted.css",
    base + "/assets/custom.css",
    base + "/assets/review.css",
  ),
)
