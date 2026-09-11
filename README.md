# 수하물 신호등

항공 수하물 250개 품목을 기내 · 위탁 · 반입금지로 판별해 주는 정적 웹사이트입니다.
빌드 도구 없이 그대로 GitHub Pages에 올릴 수 있습니다.

---

## 1. 올리기 전에 반드시 바꿀 것

전체 파일에서 아래 문자열을 찾아 본인 정보로 바꿔 주세요. (VS Code 기준 `Ctrl+Shift+F` → `Ctrl+Shift+H`)

| 찾을 문자열 | 바꿀 내용 | 나오는 곳 |
|---|---|---|
| `YOUR-DOMAIN` | 실제 도메인 (예: `baggage.example.com`) | 모든 HTML의 canonical, `sitemap.xml`, `robots.txt` |
| `[운영자명]` | 이름 또는 닉네임 | about / contact / privacy |
| `[이메일 주소]` | 연락받을 이메일 | about / contact / privacy |
| `[시행일]` | 공개하는 날짜 (예: `2026년 9월 15일`) | privacy / terms |

`[사이트명]`을 다른 이름으로 바꾸고 싶다면 `_build.py`의 `SITE_NAME`을 고친 뒤 `python3 _build.py`를 다시 실행하세요.

---

## 2. GitHub Pages에 올리기

```bash
git init
git add .
git commit -m "수하물 신호등 최초 배포"
git branch -M main
git remote add origin https://github.com/<사용자명>/<저장소명>.git
git push -u origin main
```

저장소 → **Settings → Pages** → Source를 **Deploy from a branch**, 브랜치를 **main / (root)** 로 지정하면 1~2분 뒤 공개됩니다.

`.nojekyll` 파일이 들어 있어 Jekyll 처리를 건너뜁니다. 지우지 마세요.

### 커스텀 도메인 (애드센스에는 사실상 필수)

1. 도메인을 구입합니다 (가비아 · 후이즈 · Cloudflare 등, `.com` 기준 연 1~2만 원)
2. DNS에 아래 레코드를 추가합니다
   - `A` 레코드 → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 또는 `www` 서브도메인이면 `CNAME` → `<사용자명>.github.io`
3. Settings → Pages → Custom domain에 도메인을 입력하고 **Enforce HTTPS** 체크
4. 저장소 루트에 `CNAME` 파일이 자동 생성됩니다

---

## 3. 애드센스 붙이기 (승인 후)

1. **게시자 코드** — 모든 HTML `<head>`에 주석 처리된 한 줄이 있습니다. 주석을 풀고 `ca-pub-0000000000000000`을 본인 게시자 ID로 교체
2. **ads.txt** — 루트의 `ads.txt`에서 `#`을 지우고 게시자 ID 교체
3. **광고 단위** — 본문의 `<div class="adslot">` 안에 애드센스에서 발급받은 광고 코드를 붙여 넣기

승인 심사 중에는 코드를 넣어 둔 상태여야 합니다. 광고가 나오지 않는 건 정상이에요.

---

## 4. 검색엔진 등록

| 서비스 | 주소 | 할 일 |
|---|---|---|
| Google Search Console | search.google.com/search-console | 소유권 확인 → `sitemap.xml` 제출 |
| 네이버 서치어드바이저 | searchadvisor.naver.com | 사이트 등록 → 사이트맵 제출 |
| 빙 웹마스터 | bing.com/webmasters | Search Console에서 가져오기 가능 |

---

## 5. 글 추가하는 법

1. `_posts1.py` ~ `_posts4.py` 중 아무 파일이나 열어 `POSTS["키"] = dict(...)` 형식으로 새 글을 추가
2. `_build.py`의 `ORDER` 리스트에 그 키를 넣기 (목록에 보이는 순서입니다)
3. `python3 _build.py` 실행 → `posts/` 아래에 HTML이 생성되고 사이트맵·목록·홈이 함께 갱신됩니다

본문에는 `<h2>` `<h3>` `<p>` `<ul>` 과 `.callout` `.tablewrap` 같은 클래스를 그대로 쓸 수 있습니다.
기존 글을 열어 형식을 참고하세요.

---

## 6. 파일 구조

```
index.html          홈
tool.html           수하물 판별기 (품목 250개)
about.html          소개 · 자료 출처 · 업데이트 원칙
contact.html        문의
privacy.html        개인정보처리방침 (쿠키 · 광고 조항 포함)
terms.html          이용약관 · 면책조항
404.html            없는 페이지
robots.txt          크롤러 안내
sitemap.xml         사이트맵
ads.txt             애드센스 게시자 확인
.nojekyll           Jekyll 비활성화
assets/style.css    공통 스타일
posts/              여행 가이드 글
_build.py           빌드 스크립트
_posts*.py          글 원고
```

`_build.py`와 `_posts*.py`, `__pycache__`는 사이트 동작에 필요 없습니다.
저장소에 두어도 무방하지만, 숨기고 싶다면 별도 폴더로 옮기거나 `.gitignore`에 넣으세요.
