// DRAFT SKELETON — not built (any path containing "_" is skipped by the Makefile).
// Move to content/posts/2026-11-__-esmc-esmfold2/ when the body is written.
// Prep notes: _sources.md, _numbers.md, _triangulation.md, _outline.md, _figures.md

#import "/config.typ": template, tufted, base
#import "/lib/review.typ": *
#show: template.with(title: "ESMC & ESMFold2 통합 리뷰")

= ESMC & ESMFold2 통합 리뷰

_Language Modeling Materializes a World Model of Protein Biology_

2026-11-__ 작성. Candido, Hayes, Derry, Rao, Lin, Verkuil, … Sercu, Rives (저자 123명), bioRxiv 프리프린트 (2026-06-04), #link("https://doi.org/10.64898/2026.06.03.729735")[doi:10.64898/2026.06.03.729735]

#callout("✏️", [
  _이 글은 내가 논문을 제대로 이해하려고 쓴 요약이라 틀린 곳이 있을 수 있다. 피드백은 언제든 환영한다._ 본문과 그림은 #link("https://www.biorxiv.org/content/10.64898/2026.06.03.729735v1.full")[bioRxiv v1 전문]\(부록 A.1–A.6 포함)을 브라우저로 직접 열어 읽었다. 코드는 #link("https://github.com/Biohub/esm/tree/fddac936fc921445da2d099a3e4f7ae928717292")[`Biohub/esm@fddac93`]\(MIT)을 직접 읽었다.#footnote[프리프린트는 CC BY 4.0이라 원본 그림에 직접 주석을 달 수 있다. 지난 ESM-2 글에서는 bioRxiv판이 CC BY-NC-ND였던 탓에 원본 옆에 다시 그린 판을 놓아야 했다.]
])

#versions(
  ("bioRxiv v1, 2026-06-04", "프리프린트 공개 (심사 전)"),
  ("릴리스, 2026-05-27", "ESMC·ESMFold2·ESM Atlas 공개 (MIT)"),
  ("모델 카드, 2026-05", "esmfold2-2026-05 / esmfold2-fast-2026-05"),
)

== 💡 Highlights

#callout("💡", kind: "highlight", [
  - TODO 5 bullets, numbers first — see _outline.md
])

== 1. Introduction

=== 1.1 TODO 주장형 제목 (서열만으로 복합체까지 갈 수 있나?)

=== 1.2 TODO ESM-2/ESMFold에서 남은 문제

=== 1.3 Contributions

== 2. Method

=== 2.1 ESMC는 ESM-2에서 무엇을 바꿨나?

=== 2.2 표현 안에서 구조와 기능은 어디에 있나?

=== 2.3 ESMFold2는 그 표현을 어떻게 원자로 바꾸나?

// 앵커 그림: Fig 2A + ①–⑤ 주석 → #wide-fig("fig-arch", "imgs/fig2a_annot.jpg", ...)
// 갤러리: LanguageModelShim / parcae 루프 / A.2.5 문장 / ESMFold 선행 패널
// 매핑 표: _triangulation.md

== 3. Results

=== 3.1 서열 하나로 복합체를 맞출 수 있나?

=== 3.2 추론 때 계산을 더 쓰면 정말 좋아지나?

=== 3.3 언어모델 compute가 구조 정확도를 결정하나?

=== 3.4 얼마나 빠른가?

=== 3.5 설계까지 되나?

== 4. Conclusion

== References

#review-scripts()
