#import "/config.typ": template, tufted, base
#show: template.with(title: "Posts")

= Posts

== 2026

- #link(base + "/posts/2026-11-22-pepmlm/")[PepMLM · PepPrCLIP]: 같은 연구실이 타깃 서열만으로 결합 펩타이드를 설계한 두 논문을 묶어 읽었다. 같은 베이스라인에 같은 지표인데 승패가 갈리길래 테스트셋을 직접 세어 봤더니, 한쪽은 테스트 결합 서열의 41%가 학습 파일에 그대로 들어 있었다.
- #link(base + "/posts/2026-11-22-boltzprot/")[BoltzProt-1 · BoltzPPI]: 공개 모델 Boltz-2 위에 올린 비공개 단백질 결합체 설계 모델의 기술 보고서를 읽었다. 모델이 닫혀 있어 코드 꼭짓점은 토대인 Boltz-2에서 이었고, 부록 표에서 확인한 결합체 수가 본문 그림과 달랐다.
- #link(base + "/posts/2026-11-22-iggm/")[IgGM]: 항원 구조와 항체 뼈대 서열만으로 CDR 서열과 복합체 구조를 한꺼번에 생성하는 ICLR 2025 논문을 읽었다. 코드에만 있고 본문에 없는 숫자가 둘 나왔다.
- #link(base + "/posts/2026-11-17-nanobind/")[NanoBind]: 나노바디-항원 결합을 서열만으로 예측하는 틀을 읽었다. 코드가 공개돼 있어 그림-본문-코드 삼각 대조를 세 꼭짓점 다 이었고, 친화도 모듈이 신경망이 아니라 49개 눈금에 끼워 넣는 절차라는 걸 코드에서 확인했다.
- #link(base + "/posts/2026-11-13-bonbon/")[Bonbon]: 단백질-리간드 쌍 서열만 먹인 1.6B 모델이 결합의 기능·위치·방식을 레이블 없이 배웠다는 NeurIPS 2026 구두 발표 논문을 읽었다. 코드도 가중치도 공개되지 않아 그림과 본문 두 꼭짓점만 이었다.
- #link(base + "/posts/2026-11-12-topk-sae/")[TopK SAE]: L1 벌점을 TopK로 바꿔 GPT-4에 1,600만 latent SAE를 학습한 OpenAI 논문을 그림·본문·코드로 대조해 읽었다.
- #link(base + "/posts/2026-11-12-esmc-sae/")[ESMC의 SAE 잠재 공간]: 희소 오토인코더로 ESMC 표현을 열어 보니 생물학의 계층이 나왔다는 부록 A.4를 읽었다.
- #link(base + "/posts/2026-11-12-esmc-esmfold2/")[ESMC & ESMFold2 통합 리뷰]: 언어 모델 표현 하나로 복합체 구조와 결합체 설계까지 간 Biohub 프리프린트를 읽었다.
- #link(base + "/posts/2026-11-12-esm2-esmfold/")[ESM-2 & ESMFold 통합 리뷰]: 단백질 언어 모델로 MSA 없이 구조를 예측한 논문을 그림·본문·코드로 대조해 읽었다.
