# Eden

논문 리뷰 블로그. [tufted](https://github.com/vsheg/tufted) 템플릿(Typst HTML 내보내기)으로 빌드하고 GitHub Pages로 배포한다.

- 주소: https://hongyubinbin.github.io/Eden/
- 글 작성 방식: paper-review-blog 스킬 (그림·본문·코드 삼각 연결, 곁주, 손글씨 주석)

## 빌드

Typst 0.14 이상과 `make`가 필요하다.

```sh
make html          # _site/ 에 사이트 생성
python3 -m http.server -d _site 8000   # 미리보기 (경로 /Eden/ 확인은 아래 참고)
```

사이트가 `/Eden/` 아래에서 서비스되므로 로컬에서 경로까지 똑같이 보려면 상위 폴더에 `Eden` 링크를 만든다.

```sh
mkdir -p /tmp/serve && ln -sfn "$PWD/_site" /tmp/serve/Eden && python3 -m http.server -d /tmp/serve 8000
# http://localhost:8000/Eden/
```

## 구조

```
config.typ            사이트 설정 (base = "/Eden", 메뉴, CSS)
lib/review.typ        리뷰용 도우미 (마커, 곁주 썸네일, 그림 쌍, 코드 패널, 갤러리)
assets/               tufted.css, custom.css(글꼴), review.css, review.js(확대 보기, 마커 강조, 파일 간 화살표)
content/index.typ     홈
content/posts/        글 목록과 글 폴더
  YYYY-MM-DD-slug/
    index.typ         글 본문
    imgs/             그림 (원본 캡처, 주석판, 차트)
    code/             코드 발췌 원본 (라이선스 파일 포함)
```

## 새 글 쓰기

1. `content/posts/YYYY-MM-DD-slug/index.typ`를 만들고 맨 위에 다음을 둔다.
   ```typst
   #import "/config.typ": template, tufted, base
   #import "/lib/review.typ": *
   #show: template.with(title: "글 제목")
   ```
2. 곁주는 `#footnote[...]`, 여백 썸네일은 `#margin-img(...)`, 넓은 그림은 `#wide-fig(...)`, 원본과 주석판 나란히는 `#pair(...)`, 코드 패널은 `#code-panel(read("code/파일.py"), ...)`.
3. 글 끝에 `#review-scripts()`를 넣는다.
4. `content/posts/index.typ`와 `content/index.typ`의 목록에 링크를 추가한다.
5. `make html`로 빌드해 확인한다.

Typst 마크업 주의: `@`는 참조라서 `P\@L`처럼 쓴다. `~`는 줄바꿈 없는 공백이다. 링크 뒤에 바로 `(`가 오면 `\(`로 쓴다.

## 배포

`main`에 푸시하면 `.github/workflows/deploy.yml`이 빌드해 GitHub Pages에 올린다. 처음 한 번 저장소 Settings → Pages → Build and deployment에서 Source를 **GitHub Actions**로 바꿔야 한다.

## 라이선스

- 템플릿: tufted (MIT, `template/`은 MIT-0)
- 글에 실린 논문 그림은 각 그림 캡션에 적힌 원 라이선스를 따른다. 코드 발췌는 원 저장소 라이선스(`code/LICENSE-*.txt`)를 따른다.
