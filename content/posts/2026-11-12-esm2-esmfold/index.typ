#import "/config.typ": template, tufted, base
#import "/lib/review.typ": *
#show: template.with(title: "ESM-2 & ESMFold 통합 리뷰")

= ESM-2 & ESMFold 통합 리뷰

_Evolutionary-scale prediction of atomic-level protein structure with a language model_

2026-11-12 작성. Lin et al., _Science_ 379:1123–1130 (2023), #link("https://doi.org/10.1126/science.ade2574")[doi:10.1126/science.ade2574]

#callout("✏️", [
  _이 글은 내가 논문을 제대로 이해하려고 쓴 요약이라 틀린 곳이 있을 수 있다. 피드백은 언제든 환영한다._ 본문과 그림은 #link("https://www.biorxiv.org/content/10.1101/2022.07.20.500902v3.full")[bioRxiv v3]\(부록 포함)를 브라우저로 직접 열어 읽고 v1과 대조했다. 코드는 #link("https://github.com/facebookresearch/esm/tree/2b369911bb5b4b0dda914521b9475cad1656b2ac")[`facebookresearch/esm@2b36991`]을 직접 읽었다.#footnote[Science 최종판은 로그인이 필요하고 재사용이 허용되지 않는 기본 라이선스다. bioRxiv판은 CC BY-NC-ND 4.0이라 그림을 원본 그대로 싣고, 주석은 옆에 다시 그린 판에 달았다. AlphaFold2 논문 그림(CC BY 4.0)에는 직접 손글씨 주석을 그렸다.]
])

#versions(
  ("bioRxiv v1, 2022-07-21", "원제 \"Language models of protein sequences at the scale of evolution enable accurate structure prediction\""),
  ("bioRxiv v3, 2022-12-21", "현재 제목, 메타게놈 아틀라스와 부록 Algorithm 1·2"),
  ("Science, 2023-03-17", "최종 출판본"),
)

== 💡 Highlights

#callout("💡", kind: "highlight", [
  - 단백질 언어 모델을 *15B* 파라미터까지 키웠다.#footnote[발표 당시 가장 큰 단백질 언어 모델이다.] perplexity는 10.45 → 6.37로 떨어졌다.
  - MSA 없이 서열 하나에서 원자 수준 구조를 바로 예측한다(ESMFold). CAMEO TM-score *0.83*, CASP14 *0.68*.
  - 언어 모델이 서열을 잘 이해할수록 구조도 정확하다. 모델 크기별 perplexity와 TM-score의 상관이 *−0.99*, *−1.00*이다.
  - 384잔기 단백질 하나에 V100에서 *14.2초*, 단일 AlphaFold2 모델보다 6배 빠르다.
  - 메타게놈 단백질 *6억 1,700만* 개를 접어 ESM Metagenomic Atlas를 만들었다.#footnote[메타게놈학(metagenomics)은 환경 시료에서 미생물 DNA를 통째로 시퀀싱하는 방법과 그 연구 분야를 말한다. 배양하지 못하는 미생물의 단백질이 대부분이라 구조가 거의 알려지지 않았다.] 그중 2억 2,500만 개가 고신뢰 예측이다.
])

== 1. Introduction

=== 1.1 구조와 기능은 서열 안에 숨어 있다

단백질의 생물학적 성질은 서열의 어느 위치가 돌연변이를 견딜 수 있는지를 정한다. 그래서 진화를 거친 서열에는 공진화(coevolution)와 보존(conservation) 같은 패턴이 남고, 이 패턴으로 구조와 기능을 거꾸로 추론할 수 있다.#footnote[요컨대 구조와 기능에 대한 정보는 서열 안에 숨어 있다.]

보통은 비슷한 서열을 찾아 한 줄로 맞춘 *다중 서열 정렬(multiple sequence alignment, MSA)*을 먼저 만든다. 관련 서열을 검색하고 정렬하는 이 중간 단계가 느리다.#footnote[AlphaFold2와 RoseTTAFold의 고민감도 검색은 단백질 하나에 10분이 넘게 걸릴 수 있다. 민감도를 낮추면 1분 안쪽까지 줄일 수 있다(§3).]

이 중간 단계를 아예 없앨 수는 없을까? 이 논문이 해낸 일 중 하나가 바로 그것이다.

=== 1.2 대규모 언어 모델 (LLM)

언어 모델은 원래 다음 단어를 예측하도록 사전학습했다. BERT#super[\[4\]]는 입력 일부를 가리고 맞히게 하는 *마스크 언어 모델링(MLM)*이 효과적인 사전학습 방식임을 보였다.#footnote[왼쪽에서 오른쪽으로만 읽는 사전학습과 달리, MLM은 양쪽 문맥을 함께 쓰는 깊은 양방향 표현을 만든다. 단백질에는 읽는 방향이 없으니 잘 맞는다.]

=== 1.3 Contributions

저자들은 "빠진 아미노산 채우기"만으로도 구조를 추론할 만큼 풍부한 표현이 생길 거라 가정하고, 모델을 8M에서 15B 파라미터까지 키웠다. 그 결과는 다음과 같다.

- 서열에서 원자 수준 구조를 바로 예측한다.
- perplexity와 구조 예측 정확도 사이에 강한 상관이 있다.
- 추론이 최대 60배 빠르고, 관련 서열 검색이 필요 없다.

빠르고 MSA가 필요 없으니, 훨씬 크고 다양한 메타게놈 단백질 공간으로 구조 예측을 넓혔다.

- MGnify90의 서열 *6억 1,700만* 개를 접었다.#footnote[GPU 약 2,000개로 2주가 걸렸다. 🤯 V100만으로 계산하면 약 28,000 GPU-일이다(부록 A.4.1).]
  - 그중 *2억 2,500만* 개(36%)가 고신뢰 예측이다.
    - 고신뢰 표본의 76.8%는 UniRef90과 서열 일치도 90% 미만이다.
    - 12.6%는 PDB에 비슷한 실험 구조가 없다.

== 2. Method

=== 2.1 서열만 배운 언어 모델에서 어떻게 구조가 떠오를까?

ESM-2는 약 6,500만 개의 고유 서열로 학습한다.#footnote[UniRef50의 약 4,300만 개 클러스터에서 균등하게 뽑고, 클러스터 안의 UniRef90 서열로 바꿔 넣는다. 그래서 같은 가족만 반복해서 보지 않는다.] MLM은 주변 문맥으로 빠진 아미노산을 맞히게 하므로, 모델은 아미노산 사이의 의존성을 배울 수밖에 없다. 앞선 연구#super[\[7\]]는 이렇게 학습한 트랜스포머의 어텐션 패턴이 잔기 간 접촉 지도(contact map)와 닮는다는 것을 보였다.#footnote[어텐션 헤드마다 무엇을 보는지는 따로 글로 정리할 생각이다.]

저자들은 Rao et al.#super[\[7\]]의 방법 그대로, 어텐션 맵에서 로지스틱 회귀로 접촉을 뽑는다. 식 하나가 이 과정을 전부 담고 있어서, 항마다 풀어 봤다.

#pair(
  "fig-contact",
  [
    #img("imgs/rao_fig1.jpg", "Rao et al. 2020 Figure 1: 마스크 토큰 예측 사전학습, 어텐션 맵 대칭화와 APC 보정, 회귀로 접촉 지도 예측")
    #hand[위쪽 줄의 "Symmetrize + APC → Regression"이 오른쪽 식이다 →]
  ],
  html.elem("div", attrs: (class: "decode"))[
    $ p(#text(fill: rgb("#9f231c"))[$c_(i j)$]) = (1 + exp(- #text(fill: rgb("#85540a"))[$beta_0$] - sum_(l=1)^#text(fill: rgb("#85540a"))[$L$] sum_(k=1)^#text(fill: rgb("#85540a"))[$K$] #text(fill: rgb("#1e6b37"))[$beta_(k l)$] #text(fill: rgb("#1f4f8a"))[$a_(i j)^(k l)$]))^(-1) $
    #html.elem("div", attrs: (class: "chips"))[
      #html.elem("div", attrs: (class: "chip c-red"))[#html.elem("b")[p(c#sub[ij])] 잔기 i, j가 접촉할(Cα 거리 8Å 미만) 확률. c#sub[ij]는 참/거짓.]
      #html.elem("div", attrs: (class: "chip c-blu"))[#html.elem("b")[a#sub[ij]#super[kl]] l번째 층, k번째 헤드의 어텐션 맵에서 (i, j) 값. 대칭화와 APC 보정을 거친다.]
      #html.elem("div", attrs: (class: "chip c-grn"))[#html.elem("b")[β#sub[kl]] 헤드마다 하나씩인 가중치. L1 정규화(λ = 0.15) 때문에 대부분 0이 되고, 접촉을 보는 소수 헤드만 남는다.]
      #html.elem("div", attrs: (class: "chip c-amb"))[#html.elem("b")[β#sub[0], L, K] β#sub[0]는 절편, L은 층 수, K는 층당 헤드 수. 합은 모든 층·헤드에 걸친다.]
    ]
    #hand[학습엔 단백질 20개면 충분했다! 20개씩 20번 다시 뽑아도 P\@L이 0.4287 ± 0.0028]
  ],
  "어텐션 맵 → 대칭화 + APC → 로지스틱 회귀 → 접촉 확률",
  [왼쪽: Rao et al. (2020) Figure 1, bioRxiv (CC BY-NC-ND 4.0), 원본 그대로. 오른쪽: Lin et al. 부록 A.2.1을 바탕으로 한 리뷰어 해설. #link("https://doi.org/10.1101/2020.12.15.422761")[원문]],
  left-label: "원본: Rao et al. (2020) Figure 1",
  right-label: "리뷰어 해설: 회귀 식을 항별로 풀기",
)

평가 지표는 *장거리 접촉 정밀도(P\@L)*다.#footnote[✏️ P\@L: 모델이 가장 확신하는 상위 L개(L = 서열 길이) 접촉 예측 중 실제 접촉의 비율. "장거리"는 서열상 멀리 떨어진 쌍만 센다는 뜻이다.] 본문은 이 단계를 "선형 투영"이라고만 부르지만, 부록을 열어 보면 위의 로지스틱 회귀다.

=== 2.2 원자 수준 구조는? (Enter ESMFold)

접촉 지도는 누가 누구 옆에 있는지까지만 알려준다. 원자 좌표를 내려면 회전·이동에 대해 등변인(equivariant) 트랜스포머가 필요하다. 저자들은 AlphaFold2가 도입한 #ev("fig-af2")[구조 모듈]을 그대로 가져와, 언어 모델 표현에서 원자 좌표를 뽑는다. 이 전체가 ESMFold다.

#margin-img("imgs/af2_fig3_annot.jpg", "AlphaFold2 Figure 3 축소판(리뷰어 손글씨 주석)", [AlphaFold2의 구조 모듈과 IPA. 누르면 크게 보인다.])

_ESMFold의 단계_

+ #mk(1) 서열을 ESM-2에 통과시킨다.
+ #mk(2) ESM-2의 표현을 폴딩 블록 48개에 넣는다. 블록마다 서열 표현과 쌍 표현을 #ev("fig-tri")[번갈아 갱신한다].
+ #mk(3) 결과를 구조 모듈로 넘긴다.
+ #mk(4) 세 번의 recycling을 반복한다. #ev("fig-trunk")[주석 단 코드 보기]

#wide-fig(
  "fig-af2",
  "imgs/af2_fig3_annot.jpg",
  "AlphaFold2 Figure 3에 리뷰어가 손글씨 주석을 단 그림: MSA 행·열 어텐션에 X, 외적 평균은 외적+외차로 교체, 삼각 갱신은 유지, 48블록과 구조 모듈 8블록, Single repr와 Pair repr의 ESMFold 대응 코드 라인",
  "AlphaFold2에서 무엇을 지우고 무엇을 남겼나",
  [Jumper et al. (2021) _Nature_ Figure 3 (#link("https://doi.org/10.1038/s41586-021-03819-2")[원문], CC BY 4.0). 손글씨 주석: 리뷰어. 번호 ②③은 본문의 구성요소 번호와 같다.],
)

#lead[즉, 이 그림에 표시한 것은,]

- *지운 것*: Evoformer에서 MSA를 도는 행·열 어텐션. 언어 모델 특징은 1차원이라, 쌍 표현에서 온 bias를 얹은 일반 셀프 어텐션으로 바꿨다(부록 A.3.1).
- *바꾼 것*: 서열에서 쌍으로 정보를 보내는 외적 평균(outer product mean)을 외적과 외차(outer difference)의 결합으로 바꿨다.
- *남긴 것*: 삼각 갱신과 삼각 어텐션 네 개, 그리고 블록 수 48. ESMFold 트렁크도 AlphaFold2 Evoformer와 똑같이 48블록이다.#footnote[🤯 블록 수까지 같다는 건 그림 두 장을 나란히 놓고서야 보였다. 구조 모듈 8블록도 AlphaFold2와 같다.]
- *입력이 바뀐 것*: 구조 모듈의 single representation이 AlphaFold2에서는 MSA의 첫 행이고, ESMFold에서는 언어 모델에서 온 서열 표현이다(`trunk.py:L204`).

#pair(
  "fig-arch",
  img("imgs/fig2.jpg", "Lin et al. Figure 2 원본: ESMFold 구조, 정확도 막대와 산점도, pLDDT 보정, 예측 예시"),
  img("imgs/esmfold_redraw.png", "리뷰어가 다시 그린 ESMFold 패널 A: ESM-2(고정), 층별 가중합, 48블록 트렁크, 8블록 구조 모듈, recycling 3회, 손글씨 메모"),
  "ESM-2 표현이 폴딩 트렁크와 AlphaFold2 구조 모듈을 거치고, recycling으로 되돌아온다",
  [왼쪽: Lin et al., bioRxiv v3 Figure 2 (#link("https://www.biorxiv.org/content/10.1101/2022.07.20.500902v3.full")[원문], 2026-11-12 열람, CC BY-NC-ND 4.0), 원본 그대로. 오른쪽: 패널 A를 리뷰어가 다시 그리고 주석을 달았다. 블록 수, LM 크기, recycling 횟수는 부록과 코드에서 확인한 값이다.],
  left-label: "원본: Lin et al. Figure 2",
  right-label: "리뷰어가 다시 그린 패널 A",
)

아래 보조 그림들은 이 구조도를 본문과 실제 구현에 연결한다. 번호 위에 마우스를 올리면 같은 구성요소의 본문 구절과 코드 줄이 함께 강조되고, 점선 화살표는 파일 사이의 호출이다.

#let src = "code/"
#gallery(
  links: "a-esm-call>a-trunk-fwd,a-trunk-block>a-tri-fwd",
  cell(
    "fig-text",
    panel("본문과 부록", "bioRxiv v3 · v1", html.elem("div", attrs: (class: "textpanel"))[
      #mk(1) §3 · A.3.1: #hl(1)[언어 모델의 내부 표현을 폴딩 헤드로 넘긴다.] #hl(1)[3B ESM-2를 쓰고 파라미터는 고정하며, 층별 표현을 학습된 가중합으로 합친다.] 3B는 단일 GPU에서 추론할 수 있는 가장 큰 모델이라서 골랐다.

      #mk(2) §3 · A.3.1 · v1: #hl(2)[폴딩 블록은 서열 표현과 쌍 표현을 번갈아 갱신한다.] Evoformer를 단순화했고, #hl(2)[최종 모델은 48블록]이다. 쌍 표현의 초기값은 v1이 어텐션 맵, v3가 상대 위치 인코딩이다.

      #mk(3) §3 · A.3.1: 트렁크 출력은 #hl(3)[AlphaFold2의 IPA 구조 모듈]로 간다. 템플릿은 쓰지 않는다.

      #mk(4) §3 · Fig. S3: 본문 표현은 #hl(4)["three steps of recycling are performed"]. 끄면 LDDT가 0.01–0.04 떨어진다.
    ]),
    "각 구성요소를 논문이 설명하는 방식",
    [bioRxiv v3·v1의 리뷰어 요약. 직접 인용은 ④의 한 구절뿐이다.],
  ),
  cell(
    "fig-esmfold",
    panel("esm/esmfold/v1/esmfold.py", "@2b36991", code-panel(read(src + "esmfold.py"),
      ((59, 67), (78, 84), (196, 214)),
      marks: ((59, 67, 1), (78, 84, 2), (200, 202, 1), (203, 208, 2), (212, 214, 2)),
      badges: ("61": 1, "64": 1, "67": 1, "78": 2, "200": 1, "208": 2, "212": 2),
      anchors: ("212": "a-esm-call"),
    )),
    "언어 모델을 고정하고 층을 가중합한 뒤 트렁크를 호출한다",
    [Meta #link("https://github.com/facebookresearch/esm/blob/2b369911bb5b4b0dda914521b9475cad1656b2ac/esm/esmfold/v1/esmfold.py")[facebookresearch/esm] (MIT). 발췌·주석: 리뷰어.],
  ),
  cell(
    "fig-trunk",
    panel("esm/esmfold/v1/trunk.py", "@2b36991", code-panel(read(src + "trunk.py"),
      ((11, 11), (26, 26), (36, 40), (48, 48), (157, 157), (173, 184), (192, 210)),
      marks: ((11, 11, 3), (26, 26, 3), (38, 40, 2), (48, 48, 4), (157, 157, 2), (173, 177, 4), (179, 184, 2), (193, 200, 4), (203, 207, 3)),
      badges: ("11": 3, "26": 3, "38": 2, "48": 4, "157": 2, "177": 4, "183": 2, "194": 4, "203": 3),
      anchors: ("157": "a-trunk-fwd", "183": "a-trunk-block"),
    )),
    "폴딩 블록 반복, 구조 모듈 호출, recycling",
    [Meta #link("https://github.com/facebookresearch/esm/blob/2b369911bb5b4b0dda914521b9475cad1656b2ac/esm/esmfold/v1/trunk.py")[facebookresearch/esm] (MIT). 발췌·주석: 리뷰어.],
  ),
  cell(
    "fig-tri",
    panel("esm/esmfold/v1/tri_self_attn_block.py", "@2b36991", code-panel(read(src + "tri_self_attn_block.py"),
      ((6, 13), (106, 106), (130, 158)),
      marks: ((6, 13, 2), (106, 106, 2), (131, 137, 2), (140, 140, 2), (144, 155, 2), (158, 158, 2)),
      badges: ("6": 2, "106": 2, "131": 2, "140": 2, "144": 2),
      anchors: ("106": "a-tri-fwd"),
    )),
    "폴딩 트렁크와 삼각 셀프 어텐션 블록의 대응",
    [Meta #link("https://github.com/facebookresearch/esm/blob/2b369911bb5b4b0dda914521b9475cad1656b2ac/esm/esmfold/v1/tri_self_attn_block.py")[facebookresearch/esm] (MIT). 삼각 연산은 OpenFold에서 import한다. 발췌·주석: 리뷰어.],
  ),
)

#wide[
  #table(
    columns: 7,
    [마커], [구성요소], [그림], [본문·부록], [코드 (파일:라인)], [출처], [대조],
    mk(1), [ESM-2], [Fig. 2A 왼쪽 빨간 블록], [§3, A.3.1: 3B, 고정, 층별 가중합], [`esmfold.py:L59–67`, `L200–202`], [신규], [Alg. 2와 어긋남],
    mk(2), [폴딩 트렁크], [가운데 48 blocks, Folding Block], [§3, A.3.1, Alg. 1·2], [`trunk.py:L38–40`, `L179–184`, `tri_self_attn_block.py:L130–158`], [Evoformer 단순화], [일치],
    mk(3), [구조 모듈], [가운데 오른쪽 8 blocks], [§3, A.3.1: AlphaFold2 IPA], [`trunk.py:L11`, `L26`, `L203–207`], [from AlphaFold2 (OpenFold)], [일치],
    mk(4), [Recycling], [위쪽 화살표], [§3: 3회], [`trunk.py:L48`, `L173–177`, `L193–200`], [AlphaFold2], [이름 주의],
  )
]

*Training*: 2020-05-01 이전 PDB의 약 2만 5천 개 클러스터, 약 32만 5천 개 구조로 학습한다. 여기에 AlphaFold2가 예측한 약 1,200만 개 구조를 더한다.#footnote[학습 중에는 예측 구조를 75%, 실험 구조를 25% 비율로 뽑는다. 예측 구조는 pLDDT 70 초과인 것만 쓰고, 70 미만인 잔기는 손실에서 뺀다.] *Evaluation*: CAMEO 194개와 CASP14 51개 단백질.

이 방식은 기존 최고 성능 파이프라인에서 다음을 통째로 없앤다. AlphaFold2는 셋 다 필요하다.

- 외부 진화 데이터베이스
- 다중 서열 정렬(MSA)
- 템플릿

==== 세 곳을 대조해서 찾은 것

부록의 Algorithm 1(폴딩 블록)은 `tri_self_attn_block.py`의 `forward`와 줄 단위로 일치한다. 블록 안의 순서도, 서열 차원 1024와 쌍 차원 128도 같다(`trunk.py:L39–40`).#footnote[Algorithm 1 원본은 아래 여백 그림이다(CC BY-NC-ND 4.0).]
#margin-img("imgs/alg1.jpg", "Algorithm 1 원본: FoldingBlock 의사코드", [Algorithm 1 원본. 누르면 크게 보인다.])
반면 Algorithm 2(ESMFold 전체)에서는 세 가지가 어긋났다.

- 🤔 *언어 모델 차원이 1280으로 적혀 있다.* 1280은 650M 모델의 차원이고, 부록이 쓴다고 한 3B 모델은 2560이다(저장소 README `L478–479`). 코드는 차원을 모델에서 읽어 오므로(`esmfold.py:L64`) 동작에는 문제가 없다.#footnote[Algorithm 2 첫 줄의 C#sub[esm] = 1280을 보면 된다. 원본은 여백 그림.]
- 🤔 *recycling 루프가 없다.* 본문과 그림에는 있는데, 의사코드는 블록을 한 번 통과하고 끝난다. 아미노산 임베딩을 더하는 줄(`esmfold.py:L210`)도 빠져 있다.
- 🤯 *판본이 바뀐 흔적이 코드에 남아 있다.* v1은 언어 모델 어텐션 맵으로 쌍 표현을 시작했다. v3 부록은 그 효과가 학습 중에 사라진다며 상대 위치 인코딩만 쓴다. 코드에는 두 방식이 `use_esm_attn_map` 플래그(`esmfold.py:L78–84`, `L203–208`)로 모두 있다.

#margin-img("imgs/alg2.jpg", "Algorithm 2 원본: ESMFold 의사코드, C_esm = 1280", [Algorithm 2 원본.])

코드에서만 보이는 것도 둘 있다. 설정값 `max_recycles = 4`는 첫 패스를 포함한 전체 패스 수라서 본문의 "3회"와 같은 뜻이다(`trunk.py:L173–177`). 또 그래디언트는 마지막 패스에서만 흐른다(`trunk.py:L194`). 그래서 recycling을 학습해도 메모리는 한 패스 분량만 든다.

== 3. Results

=== 3.1 구조를 얼마나 잘 예측할까?

CAMEO와 CASP14 단백질에서 *TM-score*로 평가한다.#footnote[✏️ TM-score: 예측 구조와 실제 구조의 전체 접힘이 얼마나 겹치는지를 0–1로 잰다. 0.5를 넘으면 같은 접힘으로 본다.] 서열 하나만 줄 때 ESMFold는 AlphaFold2와 RoseTTAFold보다 훨씬 잘한다. #ev("fig-arch")[Figure 2B]의 막대를 숫자로 옮기면 다음과 같다.

#wide-fig(
  "fig-gap",
  "imgs/chart-gap.svg",
  "ESMFold TM-score에서 AlphaFold2를 뺀 값. CAMEO: MSA 대비 −0.05, 단일 서열 대비 +0.42. CASP14: −0.17, +0.30",
  "MSA가 있는 AlphaFold2에는 조금 못 미치고, 서열 하나만 준 AlphaFold2보다는 크게 앞선다",
  [데이터: Lin et al., bioRxiv v3 §3과 Figure 2B. 차트: 리뷰어.],
)

#lead[즉, 이 차트가 보여주는 것은,]

- CAMEO에서 ESMFold *0.83*은 AlphaFold2 0.88에 0.05 뒤지고, RoseTTAFold 0.82와 비슷하다.
- CASP14에서는 *0.68* 대 0.85로 0.17까지 벌어진다.#footnote[🤔 초록은 CAMEO를 앞세우지만 차이가 나는 곳은 어려운 표적이다. 부록 Table S4가 CAMEO를 난이도별로 나누는데, 중간·어려운 표적은 MSA 깊이가 낮고 AlphaFold2가 앞선다. 이게 본문 그림에 있었다면 "언제 ESMFold로 충분한가"가 바로 보였을 것이다.]
- 서열 하나만 주면 AlphaFold2는 0.41 / 0.38, RoseTTAFold는 0.47 / 0.37로 무너진다.

=== 3.2 이 파이프라인에서 언어 모델은 얼마나 중요할까?

소거 실험부터 보면 답이 분명하다. 8블록 기준 모델의 CAMEO LDDT는 0.74다. 언어 모델을 빼면 *0.58*로 가장 크게 떨어지고, 폴딩 블록을 빼면 0.66이다.#footnote[🤔 CASP14에서 작은 소거들(recycling, 삼각 갱신 등)의 오차 막대는 모두 0을 지난다. 51개 표적으로는 이들의 효과를 가를 수 없다. 원본은 여백 그림(Figure S3).]
#margin-img("imgs/figS3.jpg", "Figure S3 원본: ESMFold 소거 실험", [Figure S3 원본(CC BY-NC-ND 4.0).])

그럼 언어 모델이 서열을 얼마나 이해하는지는 어떻게 잴까? 여기서 perplexity가 나온다. 구조가 얼마나 맞는지는 이미 TM-score로 잰다.

#callout("✏️", kind: "define", [
  *What's perplexity?* 언어 모델이 단백질 서열을 얼마나 잘 예측하는지를 나타낸다. 완벽한 모델은 1, 무작위로 찍는 모델은 20이다. 직관적으로는 모델이 매 위치에서 몇 개의 아미노산 사이에서 고민하는지다.
])

#ev("fig-arch")[Figure 2B] 오른쪽 산점도는 TM-score가 높은 단백질일수록 perplexity가 낮다는 것을 보여준다. 수치로 말하면 피어슨 상관이 CAMEO *−0.55*, CASP14 *−0.67*이다.

==== 어떻게 하면 perplexity를 더 낮출 수 있을까?

더 좋은 표현이 더 좋은 구조를 만든다는 건 알았다. 그럼 더 좋은 표현은 어떻게 얻을까? 🤔 스케일만 키우면 될까? 부록 Table S1의 숫자로 모델 크기별 perplexity와 TM-score를 직접 그려 봤다.

#wide-fig(
  "fig-scale",
  "imgs/chart-scale.svg",
  "ESM-2 크기별 검증 perplexity와 구조 투영 TM-score. 8M: 10.45, CAMEO 0.48, CASP14 0.37. 15B: 6.37, 0.72, 0.55",
  "perplexity가 낮아질수록 TM-score가 거의 일직선으로 오른다",
  [데이터: Lin et al., bioRxiv v3 Table S1(270K 스텝 행, 고정된 언어 모델 위에 구조 모듈만 얹은 투영 실험). 차트: 리뷰어.],
)

#lead[즉, 이 차트가 보여주는 것은,]

- 8M에서 15B로 가며 perplexity가 10.45 → 6.37, CAMEO TM-score가 0.48 → 0.72로 함께 움직인다. 모델 크기별 상관은 *−1.00*(CAMEO), *−0.99*(CASP14)다.
- 점들이 일직선에 가깝다. 단백질 단위로도, perplexity가 크게 좋아진 단백질이 접촉 정확도도 크게 좋아진다(NDCG 0.87).

#fig(
  "fig-1",
  "imgs/fig1.jpg",
  "Lin et al. Figure 1 원본: 접촉 예측 정밀도의 규모 효과, MMseqs 히트 수별 곡선, 크기 간 단백질별 비교, TM-score 비교, 7QQA와 T1056 예시",
  "모델을 키울 때 단백질마다 무슨 일이 일어나나.",
  [Lin et al., bioRxiv v3 Figure 1 (CC BY-NC-ND 4.0), 원본 그대로.],
)

패널 D는 작은 모델(x축)과 바로 위 크기 모델(y축)의 P\@L을 단백질마다 비교한다. 대각선 위의 점은 키웠더니 좋아진 단백질이다. 점의 색은 perplexity 변화량인데, 파랄수록 많이 좋아졌다.#footnote[🤔 색 체계를 바꿨으면 더 잘 읽혔을 것 같다. 좋아진 단백질의 비율을 패널마다 숫자로 적어 주면 좋겠다. 그림이 복잡해질 수는 있다. 그리고 패널 D의 축 이름은 "700M"인데 Table S1과 패널 F는 "650M"이다.] 패널 F의 7QQA는 35M → 150M에서 RMSD가 7.0Å에서 3.2Å로 뚝 떨어진다. 개별 단백질은 서서히가 아니라 어떤 규모에서 갑자기 좋아진다.

==== 스케일링이 답일까?

그렇게 간단하지는 않다. 패널 B와 C를 보면 학습 세트에 관련 서열이 많은 단백질은 작은 모델에서 이미 포화되고, 적은 단백질은 15B까지 계속 오른다. 언어 모델은 질의와 관련된 학습 데이터가 적을수록 힘들어한다. 많이 공부할수록 잘한다는 건 직관적이지만, 그게 이해일까 암기일까?

#wide-fig(
  "fig-s8",
  "imgs/figS8.jpg",
  "Lin et al. Figure S8 원본: 고아 단백질에서 ESMFold와 AlphaFold2의 TM-score 비교",
  "관련 서열이 거의 없는 고아 단백질에서도 AlphaFold2가 조금 앞선다",
  [Lin et al., bioRxiv v3 Figure S8 (CC BY-NC-ND 4.0), 원본 그대로.],
)

MSA 깊이가 1인 단백질 22개에서 평균 TM-score는 AlphaFold2 약 0.70, ESMFold 약 0.65로 보인다.#footnote[그림에서 눈으로 읽은 근삿값이다. 오차 막대는 크게 겹친다.] 결론부는 깊이가 낮은 단백질의 개선을 근거로 스케일링에 낙관하지만, 이 조건에서도 ESMFold가 앞서지는 못한다.#footnote[🤔 이 데이터셋은 TM-score 0.5 미만의 템플릿을 허용했다. AlphaFold2가 약한 템플릿 신호를 쓰고 있을 수 있으니, 언어 모델 대 MSA의 순수 비교로 읽기는 어렵다.]

=== 3.3 예측 속도는?

- 384잔기 단백질 하나를 NVIDIA V100 한 장에서 *14.2초*에 예측한다.#footnote[단일 AlphaFold2 모델보다 6배 빠르다. Apple M1 CPU에서도 5분 남짓이다.]
- 짧은 서열에서는 최대 60배 빠르다고 한다.

#pair(
  "fig-s2",
  img("imgs/figS2.jpg", "Lin et al. Figure S2 원본: 서열 길이별 추론 시간(로그 축)"),
  [
    #hand(color: "#1f4f8a")[짧은 서열에서는 언어 모델 순전파가, 긴 서열에서는 쌍 표현의 O(N#super[3]) 계산이 시간을 잡아먹는다.]
    #hand[이 비교에서 빠진 것 (부록 A.3.4) - MSA·템플릿 검색 (CPU) - AlphaFold2 기본 5모델 앙상블 (5배) - JAX 컴파일 시간]
    #hand(color: "#85540a")["60배"는 어디서? 가장 짧은 길이에서 눈으로 읽으면 ESMFold 약 0.8초, AF2 약 6초, 앙상블 약 28초. 약 7배, 약 35배다.]
  ],
  "서열 길이별 추론 시간(로그 축)과 비교 조건",
  [왼쪽: Lin et al., bioRxiv v3 Figure S2 (CC BY-NC-ND 4.0), 원본 그대로. 오른쪽: 리뷰어 메모(그림에서 읽은 값은 근삿값).],
  left-label: "원본: Figure S2",
  right-label: "리뷰어 메모",
)

=== 3.4 다른 단백질 언어 모델과 비교하면?

부록 Table S1은 ESM-2를 크기와 학습 스텝별로, 다른 단백질 언어 모델과 나란히 놓는다. 일부 행을 옮기면 다음과 같다.#footnote[CASP14·CAMEO 열은 구조 모듈 투영의 TM-score다. 다른 모델의 perplexity는 학습 데이터가 달라 비교하지 않는다.]

#wide[
  #table(
    columns: 7,
    [모델], [파라미터], [스텝], [검증 PPL], [P\@L], [CASP14], [CAMEO],
    [ESM-2], [8M], [270K], [10.45], [0.16], [0.37], [0.48],
    [ESM-2], [150M], [270K], [8.00], [0.42], [0.47], [0.63],
    [ESM-2], [650M], [270K], [7.23], [0.50], [0.51], [0.68],
    [ESM-2], [3B], [270K], [6.73], [0.53], [0.51], [0.71],
    [*ESM-2*], [*3B*], [*500K*], [*6.49*], [*0.54*], [*0.52*], [*0.72*],
    [*ESM-2*], [*15B*], [*270K*], [*6.37*], [*0.54*], [*0.55*], [*0.72*],
    [ESM-1b], [650M], [–], [–], [0.41], [0.42], [0.64],
    [Prot-T5-XL (UR50)], [3B], [–], [–], [0.48], [0.50], [0.69],
    [Prot-T5-XL (BFD)], [3B], [–], [–], [0.36], [0.46], [0.63],
    [CARP], [640M], [–], [–], [–], [0.42], [0.59],
  )
]

- 🤯 *3B를 500K 스텝 학습하면 15B(270K 스텝)와 CAMEO가 같다*(0.72). P\@L도 0.54로 같다. ESMFold가 단일 GPU에 들어가는 3B를 고른 대가가 생각보다 작다는 뜻이다.#footnote[CASP14에서는 15B가 0.55로 3B(500K)의 0.52보다 여전히 높다. 어려운 표적일수록 규모가 효과를 낸다는 3.2의 관찰과 맞는다.]
- 같은 3B 크기에서 ESM-2는 Prot-T5-XL보다 P\@L이 0.05–0.06 높다. 150M ESM-2가 650M ESM-1b와 비슷하다(P\@L 0.42 대 0.41).

=== 3.5 예측 신뢰도는 믿을 만할까?

ESMFold의 pLDDT(*예측 LDDT*, 모델이 스스로 매긴 잔기별 신뢰도)는 실제 정확도와 잘 맞는다.#footnote[✏️ LDDT: 원자 간 거리가 국소적으로 얼마나 보존됐는지를 재는 점수.] CAMEO에서 실제 LDDT와의 상관은 0.86이고, 메타게놈 서열 약 4천 개에서 AlphaFold2 예측과의 상관은 r = 0.79다. pLDDT가 0.9를 넘으면 전원자 RMSD95 중앙값이 *1.42Å*로 실험 구조 수준에 가깝다. 그래서 신뢰도로 걸러 아틀라스를 만들 수 있었다.

#pair(
  "fig-atlas",
  img("imgs/fig3.jpg", "Lin et al. Figure 3 원본: 메타게놈 구조의 pLDDT 보정, 평균 pLDDT 분포, 가장 가까운 PDB 구조와의 TM-score 분포, UMAP 지도"),
  img("imgs/chart-atlas.svg", "ESM Metagenomic Atlas 신뢰도 단계별 구조 수: 전체 6억 1,700만, 좋은 신뢰도 3억 6,500만, 고신뢰 2억 2,500만, 매우 높은 신뢰도 1억 1,300만"),
  "메타게놈 구조 공간의 지도와 신뢰도 깔때기",
  [왼쪽: Lin et al., bioRxiv v3 Figure 3 (CC BY-NC-ND 4.0), 원본 그대로. 오른쪽: §4의 수치로 리뷰어가 그렸다.],
  left-label: "원본: Figure 3",
  right-label: "리뷰어 차트: 신뢰도 단계별 구조 수",
)

패널 C의 가장 왼쪽 막대(0.5 미만)가 솟아 있다. 고신뢰 구조 표본의 12.6%가 PDB에 비슷한 접힘이 없다는 뜻이다.#footnote[🤯 복합체로 학습하지 않았는데도, 최근 PDB 다량체 2,978개에서 체인 쌍의 53.2%를 AlphaFold-Multimer와 같은 DockQ 등급으로 맞혔다. 체인 사이에 25잔기 글리신 링커를 끼우는 간단한 방법이다.]

== 4. Conclusion

단백질 언어 모델을 키웠더니 서열 데이터베이스 속에 숨어 있던 구조를 배웠고, 그래서 MSA에 기대지 않아도 된다. 놀라운 결과다.

그래도 묻고 싶은 게 남는다. 모델은 예전에 MSA로 얻던 공진화 신호를 스스로 배운 걸까, 아니면 많이 본 단백질 가족을 기억해 꺼내 쓰는 걸까? 학습 데이터에 관련 서열이 적은 단백질은 왜 여전히 고전할까? 15B를 넘어 키우면 좁혀질까, 아니면 다른 신호가 필요할까? 학습 세트와의 서열 유사도를 통제해서 이 방향을 분석해 보면 아주 흥미로울 것 같다.#footnote[지난 판에서 바로잡은 것: 48블록·3B·고정·층별 가중합은 본문이 아니라 부록 A.3.1에 있다. 속도 비교의 제외 조건도 부록 A.3.4가 밝힌다. 15B 투영 TM-score는 v1 71.3/53.9, v2 0.71/0.54, v3 0.72/0.55로 판본마다 조금씩 다르다.]

읽어줘서 고맙고, 도움이 됐으면 좋겠다. 의견이나 고칠 곳이 있으면 언제든 알려주면 좋겠다.

== References

+ #link("https://doi.org/10.1126/science.ade2574")[Lin, Z. et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. _Science_ 379, 1123–1130 (2023).]
+ #link("https://www.biorxiv.org/content/10.1101/2022.07.20.500902v3.full")[Lin, Z. et al. bioRxiv 2022.07.20.500902, v3 (2022).]
+ #link("https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1.full")[Lin, Z. et al. Language models of protein sequences at the scale of evolution enable accurate structure prediction. bioRxiv, v1 (2022).]
+ #link("https://arxiv.org/abs/1810.04805")[Devlin, J. et al. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. arXiv:1810.04805 (2018).]
+ #link("https://doi.org/10.1038/s41586-021-03819-2")[Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. _Nature_ 596, 583–589 (2021).]
+ #link("https://doi.org/10.1126/science.abj8754")[Baek, M. et al. Accurate prediction of protein structures and interactions using a three-track neural network. _Science_ 373, 871–876 (2021).]
+ #link("https://doi.org/10.1101/2020.12.15.422761")[Rao, R. et al. Transformer protein language models are unsupervised structure learners. bioRxiv 2020.12.15.422761 (2020).]
+ #link("https://github.com/facebookresearch/esm/tree/2b369911bb5b4b0dda914521b9475cad1656b2ac")[facebookresearch/esm, commit 2b36991 (MIT License).]
+ #link("https://github.com/aqlaboratory/openfold")[aqlaboratory/openfold.]

_리뷰 형식은 Ramith Hettiarachchi의 #link("https://ramith.fyi/posts/2023-02-10-esm-2-evolutionary-scale-prediction-of-atomic-level-protein-structure-with-a-language-model/")[ESM-2 리뷰]를 참고했다. Lin et al.·Rao et al. 그림은 CC BY-NC-ND 4.0으로 원본 그대로, Jumper et al. 그림은 CC BY 4.0으로 주석을 달아, 코드는 MIT License로 실었다._

#review-scripts()
