#import "/config.typ": template, tufted, base
#import "/lib/review.typ": *
#show: template.with(title: "TopK SAE (Scaling and evaluating sparse autoencoders)")

= TopK SAE (Scaling and evaluating sparse autoencoders)

_Scaling and evaluating sparse autoencoders_

2026-11-12 작성. Gao, Dupré la Tour, Tillman, Goh, Troll, Radford, Sutskever, Leike, Wu (OpenAI), ICLR 2025 (oral), #link("https://arxiv.org/abs/2406.04093")[arXiv:2406.04093]

#callout("✏️", [
  _이 글은 내가 논문을 제대로 이해하려고 쓴 요약이라 틀린 곳이 있을 수 있다. 피드백은 언제든 환영한다._ 본문과 숫자는 #link("https://arxiv.org/html/2406.04093v1")[arXiv v1 HTML 전문]\(부록 포함)에서, 그림은 같은 v1의 PDF를 브라우저에서 250–450%로 확대해 패널별로 캡처했다(2026-11-12 열람). 논문은 CC BY 4.0이라 그림에 직접 손글씨 주석을 달았다. 코드는 #link("https://github.com/openai/sparse_autoencoder/tree/4965b941e9eb590b00b253a2c406db1e1b193942")[`openai/sparse_autoencoder@4965b94`]\(MIT)을 직접 읽었다.#footnote[arXiv에는 v1(2024-06-06) 하나뿐이다. ICLR 2025 학회판은 따로 대조하지 않았다.]
])

#versions(
  ("arXiv v1, 2024-06-06", "이 글의 모든 숫자와 그림의 출처"),
  ("코드 공개, 2024-06-30", "openai/sparse_autoencoder 마지막 커밋 4965b94"),
  ("ICLR 2025", "구두 발표(oral)"),
)

== 💡 Highlights

#callout("💡", kind: "highlight", [
  - GPT-4 활성값에 latent *1,600만* 개짜리 희소 오토인코더(SAE)를 *400억* 토큰 학습했다. 죽은 latent는 *7%* 뿐이다.
  - 아무 대책 없이 키우면 latent의 최대 *90%* 가 죽는다. 묶인 초기화와 보조 손실(AuxK) 두 가지로 막았다.
  - L1 벌점 대신 *TopK* 로 활성 개수 k를 직접 정한다. 같은 MSE를 내려면 ReLU SAE는 활성 개수가 약 *3배* 필요하다(Fig. 2a, 리뷰어 판독).
  - MSE가 latent 수 n과 k에 대해 매개변수 *6개* 짜리 식 하나로 맞는다. 수렴까지 드는 토큰은 n#super[0.6]–n#super[0.65]로 늘어난다.
  - 1,600만 latent SAE를 GPT-4에 끼우면 언어 모델 손실이 사전학습 계산량 *10%* 짜리 모델 수준으로 떨어진다.
])

== 1. Introduction

=== 1.1 뉴런 하나로는 모델을 읽을 수 없다

언어 모델은 차원 수보다 훨씬 많은 개념을 다룬다. 그래서 개념이 축 하나에 대응하지 않고 여러 축에 겹쳐 실린다(중첩, superposition). SAE는 이 벡터를 훨씬 넓은 공간으로 펼치되 *몇 칸만 켜서* 다시 접는 방식으로, 겹친 개념을 풀어 보려는 도구다.#footnote[✏️ latent: SAE의 넓은 중간층 한 칸. 잘 학습되면 한 칸이 해석 가능한 개념 하나(특징, feature)에 대응한다. L0는 한 토큰에서 0이 아닌 latent의 개수다.]

문제는 크기다. 모델이 아는 개념을 다 담으려면 사전이 수천만 칸이어야 하는데, 키울수록 한 번도 켜지지 않는 *죽은 latent* 가 늘어난다. Anthropic은 latent 3,400만 개짜리 SAE를 학습했는데 그중 살아 있는 것은 1,200만 개였다#super[\[4\]]. 계산의 3분의 2가 허공으로 간 셈이다.

사전을 수천만 칸으로 키우면서도 칸을 낭비하지 않을 수 있을까?

=== 1.2 L1 벌점 대 TopK

표준 SAE#super[\[2\]]는 복원 오차에 L1 벌점을 더해 희소성을 유도한다. 두 가지가 불편하다.

- *희소도를 간접적으로만 정한다.* 원하는 L0를 얻으려면 벌점 계수 λ를 스윕해야 하고, 그래서 SAE끼리 같은 L0에서 비교하기도 어렵다.
- *값을 줄인다(shrinkage).* L1은 켜진 latent의 크기까지 0 쪽으로 끌어당긴다. 그만큼 복원이 나빠진다.

k-sparse 오토인코더#super[\[3\]]는 상위 k개만 남기고 나머지를 0으로 만든다. 희소도가 손실이 아니라 *구조* 로 정해지니 벌점이 필요 없다. 이 논문은 이 오래된 아이디어를 언어 모델 SAE의 표준 레시피로 끌어올렸다.#footnote[이 블로그의 #link(base + "/posts/2026-11-12-esmc-sae/")[ESMC SAE 글]에서 본 단백질 언어 모델 SAE도 같은 TopK 계열(k = 64)이다.]

=== 1.3 Contributions

- 큰 SAE를 안정적으로 학습하는 레시피: TopK + 묶인 초기화 + AuxK
  - GPT-4 잔차 스트림에 latent *1,600만* 개, 토큰 *400억* 개
    - 죽은 latent *7%*
- 스케일링 법칙: 계산량 L(C), 수렴 시 L(N), n과 k를 함께 본 L(N, k), 주체 모델 크기 L#sub[s]\(N)
- MSE 말고 특징의 질을 재는 지표 넷: 다운스트림 손실, 프로브 손실, 설명 가능성(N2G), 제거 효과의 희소성
- GPT-2 small용 SAE 전체 세트, 학습 코드, 시각화 도구 공개

== 2. Method

=== 2.1 SAE는 무엇을 배우게 되나?

입력은 GPT-4 계열 모델의 *5/6 지점* 층, GPT-2 small의 *8층*(3/4 지점) 잔차 스트림이다. 마지막 층에 가까우면서 다음 토큰 예측에 특화되기 직전인 자리를 골랐다. 문맥 길이는 64 토큰이고, 입력은 평균을 빼고 단위 노름으로 맞춘다.

왜 이게 특징을 찾아 주는지는 사슬로 보면 된다.

+ 손실은 복원 오차 하나뿐이고, 통로는 토큰당 k칸으로 좁다.
+ 그러니 각 latent는 여러 토큰에서 *다시 쓸 수 있는* 방향을 맡아야 손해를 덜 본다.
+ 그렇게 자주 재사용되는 방향이 모델이 실제로 쓰는 개념일 것이라는 게 SAE의 가정이다.

=== 2.2 L1 대신 TopK를 쓰면 무엇이 달라지나?

논문에는 구조도가 없다. 그래서 2절과 부록 A, 코드로 직접 그렸다. 식은 두 줄인데 학습 레시피의 네 부분이 모두 이 식 안에 있다.

+ #mk(2) 입력에서 #hl(2)[$b_"pre"$를 빼고] 인코더 $W_"enc"$를 곱한다.
+ #mk(1) #hl(1)[TopK가 상위 k개만 남긴다.] L1 벌점은 없다.
+ #mk(3) 열마다 노름이 1인 디코더 $W_"dec"$로 복원하고 $b_"pre"$를 다시 더한다. #ev("fig-model")[모델 코드 보기]
+ #mk(4) 죽은 latent로 남은 오차를 한 번 더 복원해 보조 손실을 만든다. #ev("fig-train")[학습 코드 보기]

#wide-fig(
  "fig-arch",
  "imgs/arch_redraw.jpg",
  "리뷰어가 다시 그린 TopK SAE 구조: x에서 b_pre를 빼고 W_enc, TopK, W_dec, b_pre를 거쳐 x̂를 만들고, 죽은 latent로 오차를 복원하는 AuxK 가지가 있다",
  "x에서 b_pre를 빼고, 상위 k개만 켜서 복원한다. 죽은 칸은 남은 오차로 깨운다",
  [Gao et al. §2, 부록 A와 공식 코드를 바탕으로 리뷰어가 그린 그림(원 논문에는 구조도가 없다). 빌려온 부분은 "from …"으로 표시했다. Bricken et al.#super[\[2\]]은 라이선스 표시가 없고 Makhzani & Frey#super[\[3\]]는 arXiv 기본 라이선스라 원 그림을 싣지 않았다.],
)

위 그림의 상자 네 개가 식 두 줄의 항 네 개다. 같은 색끼리 대응한다.

#wide[
  #html.elem("div", attrs: (class: "decode"))[
    #set math.equation(numbering: none)
    $ z = #text(fill: rgb("#cf3f37"))[$"TopK"$] (#text(fill: rgb("#b9760c"))[$W_"enc"$] (x - #text(fill: rgb("#8b5a8f"))[$b_"pre"$])), quad hat(x) = #text(fill: rgb("#b9760c"))[$W_"dec"$] z + #text(fill: rgb("#8b5a8f"))[$b_"pre"$] $
    $ cal(L) = ||x - hat(x)||_2^2 + #text(fill: rgb("#2d6bb3"))[$alpha ||e - hat(e)||_2^2$] $
    #html.elem("div", attrs: (class: "chips"))[
      #html.elem("div", attrs: (class: "chip c-red"))[#html.elem("b")[#mk(1) TopK] 큰 값 k개만 두고 나머지를 0으로. 희소도가 손실이 아니라 구조로 정해진다. 코드는 뒤에 ReLU를 한 번 더 건다.]
      #html.elem("div", attrs: (class: "chip", style: "background:#f1e6f2;color:#6b3f6f"))[#html.elem("b")[#mk(2) b#sub[pre]] 들어갈 때 빼고 나올 때 더하는 공용 바이어스. 데이터의 기하 중앙값으로 시작한다.]
      #html.elem("div", attrs: (class: "chip c-amb"))[#html.elem("b")[#mk(3) W#sub[enc], W#sub[dec]] 시작할 때만 서로 전치로 맞춘다. 디코더 열은 매 스텝 노름 1로 되돌린다.]
      #html.elem("div", attrs: (class: "chip c-blu"))[#html.elem("b")[#mk(4) α · AuxK] e = x − x̂. 죽은 latent 중 상위 k#sub[aux]개로 e를 복원하게 한다. α = 1/32.]
    ]
    #hand[L1 항이 없으니 λ 스윕도 없다. k를 바꾸면 L0가 정확히 그만큼 바뀐다]
  ]
]

=== 2.3 죽은 latent는 어떻게 살리나?

처방은 둘이다.#footnote[부록 C.1의 절제 실험에서 이 두 가지가 죽은 latent 감소의 대부분을 설명한다. 인코더 크기 초기화나 $b_"enc"$ 같은 다른 선택은 효과가 없거나 미미했다.]

- #mk(3) *묶인 초기화*: 인코더를 디코더의 전치로 시작한다. 읽는 방향과 쓰는 방향이 처음부터 같으니, 처음부터 아무 입력에도 반응하지 않는 칸이 덜 생긴다. 파라미터를 계속 묶어 두지는 않는다.
#margin-img("imgs/fig15_annot.jpg", "Figure 15 축소판: 조건별 죽은 latent 비율", [Figure 15(CC BY 4.0, 주석: 리뷰어). 누르면 크게 보인다.])

- #mk(4) *AuxK*: 1천만 토큰 동안 한 번도 켜지지 않으면 죽었다고 표시한다. 죽은 칸 중 상위 k#sub[aux]개로 본 손실이 못 푼 오차 e를 복원하게 시켜서, 죽은 칸에도 그래디언트가 흐르게 한다. Anthropic의 ghost grads#super[\[5\]]를 단순화한 것이고, 계산량은 10% 정도 늘어난다. 두 처방의 효과는 #ev("fig-15")[3.3절의 Figure 15]에서 본다.

아래 보조 그림들은 이 구조도를 본문과 실제 구현에 연결한다. 번호 위에 마우스를 올리면 같은 구성요소의 본문 구절과 코드 줄이 함께 강조되고, 점선 화살표는 파일 사이의 대응이다.

#let src = "code/"
#gallery(
  links: "a-topk-train>a-topk-model,a-cfg-auxk>a-auxk-call,a-mask>a-auxk-call",
  cell(
    "fig-text",
    panel("본문과 부록", "arXiv v1", html.elem("div", attrs: (class: "textpanel"))[
      #mk(1) §2.3 · 식 (2): #hl(1)[상위 k개 latent만 남기고 나머지는 0으로 만든다.] 손실은 복원 MSE 하나다. 각주 3: 코드에서는 음수를 막으려고 ReLU를 한 번 더 건다.

      #mk(2) §2.1 · §2.2 · A.1: 입력은 #hl(2)[평균을 빼고 단위 노름으로 정규화]한다. $b_"pre"$는 인코더 앞에서 빼고 디코더 뒤에서 더하며, #hl(2)[데이터의 기하 중앙값으로 초기화]한다.

      #mk(3) A.1 · A.3 · C.4: #hl(3)[인코더 방향을 디코더 방향과 평행하게 초기화]하되 학습 중에는 묶지 않는다. #hl(3)[디코더 열은 매 스텝 단위 노름]으로 되돌리고, 그 방향의 그래디언트 성분은 빼 준다.

      #mk(4) §2.4 · A.2 · B.1: #hl(4)[1천만 토큰 동안 안 켜지면 죽은 latent]다. 보조 손실은 죽은 latent 상위 #hl(4)[k#sub[aux]개(보통 512)]로 오차를 복원하고, 계수는 1/32다.
    ]),
    "각 구성요소를 논문이 설명하는 방식",
    [arXiv v1 본문·부록의 리뷰어 요약(CC BY 4.0).],
  ),
  cell(
    "fig-model",
    panel("sparse_autoencoder/model.py", "@4965b94", code-panel(read(src + "model.py"),
      ((55, 66), (82, 91), (162, 174)),
      marks: ((62, 62, 2), (63, 65, 3), (87, 90, 2), (168, 174, 1)),
      badges: ("62": 2, "64": 3, "87": 2, "169": 1),
      anchors: ("169": "a-topk-model"),
    )),
    "추론용 모델: 식 (2)가 그대로 있다. 다만 latent_bias(b_enc)가 끼어 있다",
    [OpenAI #link("https://github.com/openai/sparse_autoencoder/blob/4965b941e9eb590b00b253a2c406db1e1b193942/sparse_autoencoder/model.py")[sparse_autoencoder] (MIT). 발췌·주석: 리뷰어.],
  ),
  cell(
    "fig-train",
    panel("sparse_autoencoder/train.py", "@4965b94", code-panel(read(src + "train.py"),
      ((315, 330), (340, 358), (361, 370), (438, 455)),
      marks: ((315, 318, 4), (325, 330, 3), (340, 340, 2), (341, 348, 1), (350, 358, 4), (361, 370, 4), (438, 455, 3)),
      badges: ("316": 4, "325": 3, "340": 2, "343": 1, "355": 4, "365": 4, "442": 3),
      anchors: ("316": "a-mask", "343": "a-topk-train", "365": "a-auxk-call"),
    )),
    "학습용 모델: 묶인 초기화, 분산 TopK, 죽은 칸 집계와 AuxK",
    [OpenAI #link("https://github.com/openai/sparse_autoencoder/blob/4965b941e9eb590b00b253a2c406db1e1b193942/sparse_autoencoder/train.py")[sparse_autoencoder] (MIT). 발췌·주석: 리뷰어.],
  ),
  cell(
    "fig-loss",
    panel("sparse_autoencoder/train.py", "@4965b94", code-panel(read(src + "train.py"),
      ((614, 620), (683, 698), (747, 761)),
      marks: ((617, 619, 2), (691, 691, 4), (696, 697, 4), (751, 761, 4)),
      badges: ("618": 2, "691": 4, "759": 4),
      anchors: ("691": "a-cfg-auxk"),
    )),
    "기하 중앙값 초기화, 설정값, 그리고 손실 = MSE + AuxK",
    [OpenAI #link("https://github.com/openai/sparse_autoencoder/blob/4965b941e9eb590b00b253a2c406db1e1b193942/sparse_autoencoder/train.py")[sparse_autoencoder] (MIT). 발췌·주석: 리뷰어.],
  ),
)

#wide[
  #table(
    columns: 7,
    [마커], [구성요소], [그림 위치], [본문·부록], [코드 (파일:라인)], [출처], [대조],
    mk(1), [TopK], [구조도 가운데 빨간 상자], [§2.3, 식 (2), 각주 3], [`model.py:L162–174`, `train.py:L340–348`, `L420`], [from Makhzani & Frey 2013], [식에 없는 $b_"enc"$가 코드에 있음],
    mk(2), [$b_"pre"$와 입력 정규화], [양 끝 보라 상자], [§2.1, §2.2, A.1], [`model.py:L8–13`, `L55–66`, `L82–91`, `train.py:L614–620`], [from Bricken 2023], [정규화 방식 표현이 다름],
    mk(3), [묶인 초기화, 디코더 노름], [인코더·디코더 상자와 위쪽 호], [A.1, A.3, C.2, C.4], [`train.py:L322–330`, `L438–455`, `L585–586`], [초기화는 신규, 노름은 Bricken 2023], [일치],
    mk(4), [AuxK], [아래쪽 파란 가지], [§2.4, A.2, B.1], [`train.py:L315–318`, `L350–370`, `L691–697`, `L747–761`], [ghost grads의 변형], [k#sub[aux] 기본값이 다름],
  )
]

*Training*: GPT-2 small과 GPT-4 계열 모델(GPT-4 포함). 배치는 13만 1,072 토큰, Adam에 학습률은 상수다.#footnote[학습률 감쇠는 일관된 이득이 없었다고 한다. 그 밖의 최적화 설정은 부록 A에 있다.] *Evaluation*: 정규화 MSE와 L0, 그리고 4절의 지표 넷.

==== 세 곳을 대조해서 찾은 것

- 🤔 *식 (2)에는 $b_"enc"$가 없는데 코드에는 있다.* 두 파일 모두 인코더에 `latent_bias`를 더한다(`model.py:L64`, `train.py:L341`). 부록 C.3이 그 이유를 준다. $b_"enc"$는 수렴 MSE를 바꾸지 않지만 없으면 수렴이 조금 느렸다. 본문 식은 단순화한 것이고, 실제로 돌린 건 코드 쪽이다.
- 🤔 *k#sub[aux] 기본값이 다르다.* 부록은 "보통 512", "d#sub[model]/2에 가까운 2의 거듭제곱, GPT-2 small이면 512"라고 하는데, 공개 설정은 `auxk = 256`이다(`train.py:L691`). 768/2 = 384라 둘 다 "가까운 2의 거듭제곱"이긴 하다.
- 🤔 *EMA가 꺼진 채 출하된다.* 부록 A.5는 모든 실험에 계수 0.999의 가중치 EMA를 썼다고 하지만, `Config`의 `ema_multiplier`는 `None`이다(`train.py:L698`). `training_loop_`의 기본값은 0.999다(`L555`).
- 🤔 *분산 TopK의 용량 계수.* 부록 D.1은 샤드당 2라고 하는데, 본 TopK는 4, AuxK만 2로 호출한다(`train.py:L347`, `L369`).
- 🤯 *"켜졌다"의 기준이 코드에만 있다.* 값이 10#super[−3]을 넘어야 켜진 것으로 센다(`train.py:L355`). 1천만 토큰은 스텝으로 바꿔 쓴다(1천만 ÷ 13만 1,072 ≈ 76스텝, `L720`).
- 정규화 표현도 조금 다르다. 본문은 "단위 노름"이라고 하지만 `model.py`의 `LN`은 표준편차로 나눈다(`L8–13`). 크기가 √d#sub[model]배 다를 뿐 MSE는 정규화해서 보니 결과는 같다. 이 정규화를 켤지는 활성화 함수 이름이 `TopK`인지로 정하는데, 주석에도 "hacky"라고 적혀 있다(`L120`).
- 데이터 로더는 "독자에게 맡긴다"며 비어 있다(`train.py:L708–710`). 그래서 이 저장소만으로 학습을 재현할 수는 없다.

== 3. Results

=== 3.1 TopK가 정말 더 나은가?

#wide-fig(
  "fig-2",
  "imgs/fig2_annot.jpg",
  "Figure 2: (a) n=32768에서 희소도별 정규화 MSE, (b) L0=128에서 latent 수별 정규화 MSE. ReLU, ProLU STE, Gated, TopK 비교",
  "같은 희소도에서 TopK가 가장 낮고, n을 키울수록 ReLU와의 간격이 벌어진다",
  [Figure 2, Gao et al. (2024), #link("https://arxiv.org/abs/2406.04093")[arXiv:2406.04093] v1 (CC BY 4.0). 손글씨 주석: 리뷰어.],
)

#lead[그러니까 Figure 2가 보여 주는 것은,]

- (a) L0 = 128에서 TopK의 정규화 MSE는 약 *0.40* 이다. ReLU가 같은 MSE에 닿으려면 L0가 약 350, 즉 *3배* 가까이 필요하다(로그 축에서 리뷰어가 읽은 값).
- Gated SAE#super[\[6\]]와는 거의 겹친다. 그러니 TopK의 이득은 "Gated보다 압도적"이 아니라 "*Gated만큼 좋으면서 튜닝이 쉽다*"에 가깝다.
- (b) L0 = 128에서 n을 키울 때 TopK 직선이 ReLU보다 가파르다. 규모가 커질수록 차이가 벌어진다.

복원만 보면 차이가 크지 않아 보이지만, 모델에 끼워 넣었을 때는 다르다.

#wide-fig(
  "fig-5",
  "imgs/fig5_annot.jpg",
  "Figure 5: (a) n=2^17에서 희소도별 다운스트림 cross-entropy 증가량, (b) L0=128에서 MSE와 다운스트림 손실의 관계",
  "MSE보다 다운스트림 손실에서 차이가 더 크다",
  [Figure 5, Gao et al. (2024) v1 (CC BY 4.0). 손글씨 주석: 리뷰어.],
)

- (a) L0 약 128에서 TopK의 Delta CE는 약 *0.04*, ReLU는 약 *0.09* 다. 절반 이하다.#footnote[✏️ Delta CE: 잔차 스트림을 SAE 복원값으로 바꿔 넣었을 때 언어 모델의 cross-entropy가 얼마나 오르는지. 완벽한 SAE라도 0이 아니어서 그 차이를 잰다.]
- (b) 같은 MSE에서도 TopK가 아래에 있다. *같은 크기의 오차라도 덜 중요한 방향으로 틀린다* 는 뜻이다.

#crit[
  🤔 Figure 2a에서는 방법마다 점이 찍힌 L0가 다르다. "L0 = 32, 128에서 각 방법의 MSE"를 표로 보간해 줬다면 3배라는 숫자를 눈대중 없이 읽을 수 있었을 것이다. 보간 오차가 생긴다는 단점은 있지만, 이 논문의 핵심 주장이 바로 이 간격이다.
]

=== 3.2 키우면 어디까지 좋아지나?

#wide-fig(
  "fig-1",
  "imgs/fig1_annot.jpg",
  "Figure 1: 왼쪽 계산량 대비 최적 MSE L(C), 오른쪽 latent 수와 k에 대한 수렴 MSE L(N,k)",
  "계산량에도, latent 수와 k에도 깔끔한 거듭제곱 법칙이 나온다",
  [Figure 1, Gao et al. (2024) v1 (CC BY 4.0). 손글씨 주석: 리뷰어.],
)

두 가지 방식으로 쟀다. *L(C)* 는 계산량이 주어졌을 때 수렴과 상관없이 얻을 수 있는 최적 MSE이고, *L(N)* 은 끝까지 수렴시켰을 때의 MSE다.#footnote[저자들은 L(C)가 SAE에는 원칙적이지 않다고 스스로 적는다. n이 크면 병목이 느슨해져 MSE가 쉽게 낮아지기 때문이다. 그래서 n이 다른 SAE를 MSE로만 비교하는 건 공정하지 않다.]

#lead[그러니까 Figure 1이 보여 주는 것은,]

- 왼쪽: MSE ≈ 0.09 + 0.056 · C#super[−0.084]. 계산량 C는 GPT-4 사전학습 대비 비율이다. 가장 작은 SAE들만 추세선 위로 뜬다.
- 오른쪽: 점(실측)이 식 (3)의 점선에 거의 그대로 올라앉는다. 수렴까지 드는 토큰은 GPT-2 small에서 n#super[0.6], GPT-4에서 n#super[0.65]로 늘어난다.
- 식 (3)의 교차항 계수 γ = −0.042가 음수다. *k가 클수록 n을 키우는 효과가 커진다* 는 뜻이다.

식 (3)의 계수 여섯 개가 논문에 다 있으니 직접 계산해 봤다.

#wide-fig(
  "fig-law",
  "imgs/chart-law.svg",
  "식 (3)으로 다시 계산한 L(n, k) 곡선. k=32, 128, 512. 피팅 범위는 실선, 1,680만까지의 외삽은 파선, 비가역 항은 점선",
  "1,600만 latent에서 남은 MSE의 3분의 2 이상이 '바닥'이다",
  [데이터: Gao et al. (2024) v1 식 (3)의 계수(α = −0.50, β#sub[k] = 0.26, β#sub[n] = −0.017, γ = −0.042, ζ = −1.32, η = −0.085). 계산과 차트: 리뷰어. 외삽 구간은 논문이 주장한 값이 아니다.],
)

- 2#super[11]–2#super[19]에서 식이 Figure 1 오른쪽과 맞는지 먼저 확인했다. k = 32에서 *0.631 → 0.375*, k = 512에서 0.523 → 0.235로 그림과 같다.
- 1,600만까지 외삽하면 k = 32에서 *0.30* 이다. 이 중 비가역 항(바닥)이 *0.20*, 비율로 *67%* 다. k = 512에서는 바닥이 84%를 차지한다.

#wow[
  🤯 latent를 무한히 늘려도 k = 32면 분산의 약 20%는 설명되지 않은 채 남는다는 것이 이 식의 함의다. 저자들도 바닥이 왜 있는지는 모른다고 적는다. 대신 768차원 순수 가우스 잡음으로 실험하면 L(N) 지수가 −0.04밖에 안 된다는 것을 보였다. GPT-2 small 활성값의 약 −0.26보다 훨씬 완만하다. 활성값 안에 SAE가 다루기 어려운 *구조 없는 성분* 이 섞여 있다는 가설이다.
]

#crit[
  🤔 다만 1,600만짜리 GPT-4 SAE는 계산 제약으로 수렴까지 학습하지 못해 L(N) 계열에 넣지 못했다(부록 B.1). 그러니 위 차트의 오른쪽 끝은 "그 SAE가 도달할 수 있었을 값"이지 실제 측정값이 아니다.
]

==== 주체 모델이 커지면?

#fig(
  "fig-4",
  "imgs/fig4_annot.jpg",
  "Figure 4: GPT-4 계열 모델 크기별 latent 수 대비 MSE (k=32)",
  "큰 모델일수록 같은 MSE에 latent가 훨씬 많이 든다",
  [Figure 4, Gao et al. (2024) v1 (CC BY 4.0). 주석: 리뷰어.],
)

k = 32로 고정하고 GPT-4 계열의 네 크기를 비교했다. 주석에 적었듯 MSE 0.40에 닿는 n은 가장 작은 모델에서 약 2천, GPT-4에서 약 *25만* 이다(눈대중). 게다가 큰 모델일수록 직선이 완만하다. 모델이 클수록 SAE 크기를 그보다 *더 빨리* 키워야 한다는 뜻이다.

=== 3.3 죽은 latent는 정말 사라졌나?

#wide-fig(
  "fig-15",
  "imgs/fig15_annot.jpg",
  "Figure 15: 학습 토큰에 따른 죽은 latent 비율. none, auxk, tied init, auxk + tied init 네 조건",
  "둘 중 하나만으로는 늦고, 둘을 합쳐야 빨리 0 근처로 간다",
  [Figure 15 (부록 C.1), Gao et al. (2024) v1 (CC BY 4.0). GPT-2 small, n = 2M, k = 32. 손글씨 주석: 리뷰어.],
)

#lead[그러니까 Figure 15가 보여 주는 것은,]

- 대책이 없으면 10억 토큰 근처에서 *95%* 가까이 죽고, 끝까지 회복하지 못한다.
- AuxK만 쓰면 한때 94%까지 치솟았다가 수백억 토큰을 지나서야 내려온다.
- 묶인 초기화만 쓰면 정점이 31%로 낮지만, 끝까지 4% 정도가 남는다.
- 둘을 합치면 정점이 28%이고, 끝에는 거의 0이다.

#fig(
  "fig-dead",
  "imgs/chart-dead.svg",
  "죽은 latent 비율 막대: Templeton 2024 34M 65%, 이 논문 대책 없음 최대 90%, 이 논문 16M 7%",
  "1,600만 latent에서 7%",
  [데이터: Gao et al. (2024) v1 §2.4. Templeton et al.의 값은 이 논문이 인용한 "34M 중 12M 생존"에서 계산했다. 차트: 리뷰어.],
)

#crit[
  🤔 이 막대들은 같은 조건의 비교가 아니다. Templeton et al.은 다른 모델, 다른 SAE 구성이었고, 90%는 GPT-2 small 절제 실험의 최대치다. "죽음"의 기준(1천만 토큰)만 같다. 그래도 *latent 1,600만 개 규모에서 93%가 살아 있다* 는 것 자체는 이 레시피의 가장 실용적인 결과다.
]

=== 3.4 MSE 말고 무엇으로 재나?

MSE는 SAE의 목적이 아니다. 저자들은 각주에서 극단적인 예를 든다. 무한히 넓고 k = 1인 SAE는 공간을 촘촘히 덮어 완벽하게 복원하지만 아무 구조도 없다. 그래서 지표 넷을 더 만들었다.

#callout("✏️", kind: "define", [
  *"사전학습 계산량 10%"는 무슨 뜻인가?* 흔히 쓰는 지표는 "잔차를 0으로 지웠을 때 대비 손실을 얼마나 회복했나"다. 1,600만 SAE는 이 지표로 *98.2%* 다. 하지만 잔차를 0으로 만들면 모델이 완전히 망가지니, 형편없는 복원도 높은 점수를 받는다. 저자들은 대신 "SAE를 끼운 GPT-4의 손실이 어떤 크기의 모델과 같은가"로 잰다. 답은 *GPT-4 사전학습 계산량의 10%로 학습한 모델* 이다.
])

#crit[
  🤔 이건 꽤 큰 손실이다. 98.2%라는 숫자만 보면 거의 다 설명한 것 같지만, 계산량으로 환산하면 GPT-4가 하는 일의 상당 부분이 SAE 복원 과정에서 사라진다. 이 논문이 둘 다 보고한 것은 정직하지만, "SAE로 모델을 해석한다"고 말할 때 그 모델이 사실상 10배 작은 모델이라는 점은 기억해 둘 만하다.
]

#wide-fig(
  "fig-6",
  "imgs/fig6_annot.jpg",
  "Figure 6: GPT-2 small SAE의 n과 L0별 (a) 프로브 손실, (b) 로짓 효과 희소성 히트맵",
  "n을 키우면 대체로 좋아지고, L0가 d_model에 가까워지면 다시 나빠진다",
  [Figure 6, Gao et al. (2024) v1 (CC BY 4.0). 주석: 리뷰어.],
)

- *프로브 손실*: 감정, 언어 식별 같은 이진 분류 *61* 개를 골라, latent 하나만으로 로지스틱 회귀를 했을 때 가장 좋은 손실을 본다. n = 524,288, L0 = 128에서 약 0.488로 가장 좋다. TopK가 ReLU보다, 둘 다 잔차 채널보다 낫다.
- *설명 가능성(N2G)*: 활성 패턴을 n-gram 규칙으로 설명하고 정밀도와 재현율을 잰다. 같은 n과 비슷한 L0에서 TopK는 ReLU보다 재현율이 *1.5배* 이상, 정밀도는 *0.9배* 이상이다.
- *제거 효과의 희소성*: latent 하나를 지웠을 때 로짓이 몇 개나 바뀌는지를 (L1/L2)#super[2]로 잰다. latent는 *10–14%*, 잔차 채널 하나는 *60%* 다. k = 512에서는 다시 나빠진다.

#crit[
  🤔 Figure 6a의 색 범위는 0.488에서 0.515까지다. 가장 좋은 칸과 나쁜 칸의 차이가 5%가 안 된다. 저자들도 이 지표가 "꽤 시끄럽다"고 인정한다. 히트맵의 노란 칸은 경향을 보는 데 쓰고, 칸 하나하나의 순위에는 의미를 두지 않는 편이 좋겠다.
]

=== 3.5 TopK는 왜 통하나?

L1이 값을 줄인다면, 켜진 latent의 값만 다시 맞췄을 때 값이 커져야 한다. 그대로 실험했다. 디코더와 켜진 칸은 고정하고 값만 최적화한다.

#wide-fig(
  "fig-9",
  "imgs/fig9_annot.jpg",
  "Figure 9: 값 재조정 전후 차이의 분포(왼쪽)와 재조정에 따른 MSE·Delta CE 변화(가운데, 오른쪽)",
  "ReLU만 +쪽으로 밀린다. L1이 값을 줄여 놓았다는 증거다",
  [Figure 9, Gao et al. (2024) v1 (CC BY 4.0). 손글씨 주석: 리뷰어.],
)

- ReLU의 분포는 0보다 오른쪽으로 치우친다. 재조정이 값을 *키운다*. TopK는 0을 중심으로 좁게 모인다.
- 재조정하면 둘 다 MSE와 Delta CE가 좋아진다. 하지만 ReLU의 재조정 점선은 TopK 실선에 가까워질 뿐이고, 특히 Delta CE에서는 여전히 한참 위에 있다. 값을 줄이는 문제(shrinkage)는 *차이의 일부만* 설명한다.

#wide-fig(
  "fig-10",
  "imgs/fig10_annot.jpg",
  "Figure 10: 테스트 때 k를 바꿨을 때의 MSE. 왼쪽 TopK로 학습, 오른쪽 Multi-TopK로 학습",
  "TopK는 학습한 k에 과적합한다. Multi-TopK로 풀린다",
  [Figure 10, Gao et al. (2024) v1 (CC BY 4.0). 손글씨 주석: 리뷰어.],
)

TopK에는 대가가 있다. 학습 때 쓴 k보다 많은 latent를 테스트 때 켜면 MSE가 *치솟는다*(왼쪽). 크기 순으로 latent를 더할수록 복원이 좋아지는 *점진적 코드* 가 아니라는 뜻이다. 손실을 L(k) + L(4k)/8로 바꾼 Multi-TopK로 학습하면 이 문제가 사라진다(오른쪽). 대신 원래 k에서는 TopK보다 조금 나쁘다.

=== 3.6 다른 SAE들과 비교하면?

#wide[
  #table(
    columns: 5,
    [방법], [희소도를 정하는 방식], [값 줄이기(shrinkage)], [죽은 latent 대책], [이 논문의 비교 (GPT-2 small)],
    [ReLU + L1#super[\[2\]]], [L1 계수 λ (간접)], [있음], [재샘플링], [가장 나쁨],
    [ProLU / JumpReLU], [문턱값 + L1], [완화], [재샘플링], [ReLU보다 낫고 TopK보다 나쁨],
    [Gated#super[\[6\]]], [게이트에만 L1], [해결], [재샘플링], [MSE에서 TopK와 비슷, Delta CE는 조금 나쁨],
    [*TopK (이 논문)*], [*k를 직접 지정*], [*없음*], [*묶인 초기화 + AuxK*], [*MSE·Delta CE 모두 가장 좋음*],
  )
]

- 마지막 열은 #ev("fig-2")[Figure 2a]\(n = 32,768)와 #ev("fig-5")[Figure 5a]\(n = 2#super[17])를 함께 읽은 것이다. MSE에서는 Gated와 TopK가 겹치지만, Delta CE에서는 TopK가 Gated보다도 아래에 있다.
- 기준선 설정은 부록 B.2에 있다. 기준선들도 죽은 latent가 TopK와 비슷하거나 더 적었다(Figure 14). 그러니 TopK의 이득은 죽은 latent 차이에서 오는 게 아니다.

== 4. Conclusion

L1 벌점을 TopK로 바꾸고 초기화와 보조 손실을 손보니, 1,600만 latent에서도 칸이 거의 죽지 않았고 MSE가 깔끔한 법칙을 따랐다. "SAE를 크게 키우는 일"을 공학 문제로 바꿔 놓은 논문이다.

남는 질문 셋.

+ *모든 토큰에 정확히 k개가 맞나?* 저자들도 한계로 꼽는다. 쉬운 토큰과 어려운 토큰에 같은 수의 latent를 쓰는 건 낭비다. 이후 나온 BatchTopK#super[\[7\]]가 배치 단위로 k를 풀어 이 문제를 다룬다.
+ *바닥은 무엇인가?* 비가역 항이 1,600만 latent에서 남은 MSE의 3분의 2를 차지한다면, 그 안에 잡음만 있는지 아니면 SAE라는 선형-희소 형식이 담지 못하는 구조가 있는지가 해석 가능성의 상한을 정한다.
+ *좋은 SAE의 기준은 무엇인가?* 지표 넷이 k에 대해 서로 다른 방향을 가리킨다. 키우면 대체로 좋아진다는 점은 일관되지만, 조종(steering)이나 회로 찾기 같은 실제 쓰임에 어떤 지표가 맞는지는 아직 열려 있다.

GPT-4 SAE의 특징들이 실제로 무엇을 담는지는 공개된 시각화 도구로 따로 들여다볼 생각이다. 읽어주셔서 감사하고, 다르게 읽은 부분이 있으면 알려주시면 좋겠다.

== References

+ #link("https://arxiv.org/abs/2406.04093")[Gao, Dupré la Tour, Tillman, Goh, Troll, Radford, Sutskever, Leike, Wu. _Scaling and evaluating sparse autoencoders_. arXiv:2406.04093 (2024); ICLR 2025.]
+ #link("https://transformer-circuits.pub/2023/monosemantic-features/index.html")[Bricken et al. _Towards Monosemanticity: Decomposing Language Models With Dictionary Learning_. Transformer Circuits Thread (2023).]
+ #link("https://arxiv.org/abs/1312.5663")[Makhzani, Frey. _k-Sparse Autoencoders_. arXiv:1312.5663 (2013).]
+ #link("https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html")[Templeton et al. _Scaling Monosemanticity_. Transformer Circuits Thread (2024).]
+ #link("https://transformer-circuits.pub/2024/jan-update/index.html#dict-learning-resampling")[Jermyn, Templeton. _Ghost grads: An improvement on resampling_. Transformer Circuits Thread (2024).]
+ #link("https://arxiv.org/abs/2404.16014")[Rajamanoharan et al. _Improving Dictionary Learning with Gated Sparse Autoencoders_. arXiv:2404.16014 (2024).]
+ #link("https://arxiv.org/abs/2412.06410")[Bussmann, Leask, Nanda. _BatchTopK Sparse Autoencoders_. arXiv:2412.06410 (2024).]
+ #link("https://github.com/openai/sparse_autoencoder/tree/4965b941e9eb590b00b253a2c406db1e1b193942")[openai/sparse_autoencoder, commit 4965b94 (MIT).]

#hand[형식은 Ramith Hettiarachchi의 ESM-2 리뷰를 본떴다. 논문 그림은 CC BY 4.0 원본에 직접 주석을 달았고, 구조도와 두 차트는 논문의 서술과 수치로 새로 그렸다.]

#review-scripts()
