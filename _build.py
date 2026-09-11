# -*- coding: utf-8 -*-
"""수하물 신호등 정적 사이트 빌더 — python3 _build.py"""
import os, json, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
SITE_NAME = "수하물 신호등"
SITE_DESC = "항공 수하물 250개 품목을 기내·위탁·반입금지로 바로 알려주는 여행 준비 사이트"
TODAY = "2026-09-11"

CLOUDS = ('<svg viewBox="0 0 1000 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
 '<g fill="var(--surface)" opacity=".5">'
 '<ellipse cx="120" cy="48" rx="62" ry="23"/><ellipse cx="168" cy="41" rx="40" ry="19"/>'
 '<ellipse cx="860" cy="136" rx="78" ry="26"/><ellipse cx="806" cy="129" rx="44" ry="19"/>'
 '<ellipse cx="560" cy="24" rx="52" ry="17"/></g>'
 '<g fill="var(--accent)" opacity=".13">'
 '<ellipse cx="300" cy="152" rx="95" ry="25"/><ellipse cx="700" cy="56" rx="60" ry="17"/></g>'
 '<path d="M188 106 q56 -32 118 -28 q62 4 108 30" fill="none" stroke="var(--accent)" '
 'stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round" opacity=".45"/>'
 '<path d="M418 104 l16 4 l-16 4 l4 -4 z" fill="var(--accent)" opacity=".6"/></svg>')

NAV = [("index.html","홈"), ("tool.html","수하물 판별기"), ("posts/index.html","여행 가이드"),
       ("about.html","소개"), ("contact.html","문의")]

def nav_html(cur, depth):
    up = "../" * depth
    out = []
    for href, label in NAV:
        a = 'aria-current="page" ' if href == cur else ""
        out.append(f'<a {a}href="{up}{href}">{label}</a>')
    return "\n        ".join(out)

def page(*, path, title, desc, body, cur=None, depth=0, head_extra="", body_class=""):
    up = "../" * depth
    cur = cur or path
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://YOUR-DOMAIN/{path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&family=Outfit:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧳</text></svg>">
<!-- 애드센스 승인 후 아래 한 줄의 주석을 풀고 ca-pub-000... 를 본인 게시자 ID로 바꾸세요 -->
<!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0000000000000000" crossorigin="anonymous"></script> -->
{head_extra}</head>
<body{(' class="'+body_class+'"') if body_class else ''}>

<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="{up}index.html"><span class="mark">🧳</span>{SITE_NAME}</a>
    <nav class="nav" aria-label="주 메뉴">
        {nav_html(cur, depth)}
    </nav>
  </div>
</header>

{body}

<footer class="sitefoot">
  <div class="wrap foot-in">
    <span class="foot-name">{SITE_NAME}</span>
    <nav class="foot-links" aria-label="사이트 문서">
      <a href="{up}about.html">소개</a>
      <a href="{up}privacy.html">개인정보처리방침</a>
      <a href="{up}terms.html">이용약관 · 면책</a>
      <a href="{up}contact.html">문의</a>
    </nav>
    <p class="foot-copy">본 사이트의 정보는 참고용입니다. 실제 반입 여부는 항공사와 공항 보안검색의 판단에 따릅니다. © 2026 {SITE_NAME}</p>
  </div>
</footer>

</body>
</html>
"""
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return path

def hero(eyebrow, h1, lede):
    return f"""<section class="hero-band">
  {CLOUDS}
  <div class="wrap hero-in">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""

AD = """<div class="adslot">
  <span class="adslot--label">광고</span>
  <!-- 애드센스 승인 후 이 자리에 광고 단위 코드를 붙여 넣으세요 -->
</div>"""

# ── 글 모으기 ────────────────────────────────
import _posts1, _posts2, _posts3, _posts4
ALL_POSTS = {}
for mod in (_posts1, _posts2, _posts3, _posts4):
    ALL_POSTS.update(mod.POSTS)
ORDER = ["battery", "liquid", "banned", "checked", "airlines", "packing"]
POSTS = [ALL_POSTS[k] for k in ORDER]

def post_page(p):
    schema = json.dumps({
        "@context":"https://schema.org","@type":"Article",
        "headline":p["title"],"description":p["desc"],
        "datePublished":p["date"],"dateModified":p["date"],
        "author":{"@type":"Person","name":"[운영자명]"},
        "publisher":{"@type":"Organization","name":SITE_NAME}
    }, ensure_ascii=False)
    others = [q for q in POSTS if q["slug"] != p["slug"]][:3]
    more = "".join(
        f'<a class="card" href="{os.path.basename(q["slug"])}"><h3>{q["title"]}</h3>'
        f'<p>{q["desc"][:70]}…</p></a>' for q in others)
    body = f"""{hero("여행 가이드", p["title"], p["lede"])}

<main class="wrap">
  <article class="post">
    <p class="meta"><span class="tag">{p["tag"]}</span> <span>{p["date"]}</span> <span>읽는 데 {p["read"]}</span></p>
    {AD}
    {p["body"]}
    {AD}
    <div class="toolcta">
      <p><strong>내 짐은 어느 쪽일까?</strong><br>품목 250개를 기내·위탁·반입금지로 바로 알려드립니다.</p>
      <a class="btn" href="../tool.html">수하물 판별기 열기</a>
    </div>
    <h2>함께 읽으면 좋은 글</h2>
    <div class="cards">{more}</div>
  </article>
</main>"""
    return page(path=p["slug"], title=f'{p["title"]} | {SITE_NAME}', desc=p["desc"],
                body=body, cur="posts/index.html", depth=1,
                head_extra=f'<script type="application/ld+json">{schema}</script>\n')

for p in POSTS:
    post_page(p)

# ── 글 목록 ──────────────────────────────────
cards = "".join(
    f'<a class="card" href="{os.path.basename(p["slug"])}">'
    f'<span class="tag" style="align-self:flex-start">{p["tag"]}</span>'
    f'<h3>{p["title"]}</h3><p>{p["desc"]}</p>'
    f'<p class="meta">{p["date"]} · {p["read"]}</p></a>' for p in POSTS)
page(path="posts/index.html", cur="posts/index.html", depth=1,
     title=f"여행 가이드 | {SITE_NAME}",
     desc="항공 수하물 규정을 주제별로 정리한 글 모음. 보조배터리, 액체류 100ml, 반입 금지 물품, 항공사별 비교까지.",
     body=f"""{hero("Travel Guides", "여행 가이드",
       "공식 규정을 직접 확인하고 실제로 쓸 수 있게 정리한 글들입니다. 짐 싸기 전에 한 번씩 읽어 보세요.")}
<main class="wrap"><div class="cards">{cards}</div>{AD}</main>""")

# ── 홈 ──────────────────────────────────────
home_cards = "".join(
    f'<a class="card" href="posts/{os.path.basename(p["slug"])}">'
    f'<span class="tag" style="align-self:flex-start">{p["tag"]}</span>'
    f'<h3>{p["title"]}</h3><p>{p["desc"][:80]}…</p></a>' for p in POSTS)
page(path="index.html", cur="index.html", depth=0,
     title=f"{SITE_NAME} — 기내 반입? 위탁 수하물? 바로 확인",
     desc=SITE_DESC,
     body=f"""{hero("Cabin · Checked · Prohibited", "이 짐, 들고 탈까 부칠까",
       "항공사와 노선을 고르고 물건 이름을 치면 기내·위탁·반입금지를 신호등처럼 알려드려요. 품목 250개를 담았습니다.")}
<main class="wrap">
  <div class="toolcta">
    <p><strong>수하물 판별기</strong><br>항공사 14곳 규정 + 품목 250개. 보조배터리 용량과 액체 용기 크기는 숫자를 넣으면 바로 계산됩니다.</p>
    <a class="btn" href="tool.html">판별기 열기</a>
  </div>

  <article class="post" style="max-width:none">
    <h2>이 사이트는 무엇을 합니다</h2>
    <p>공항 보안검색에서 물건을 버리는 일은 대부분 규정을 어겨서가 아니라, <strong>어느 쪽에 넣어야 하는지를 몰라서</strong> 생깁니다. 보조배터리는 부치면 안 되고, 액체는 남은 양이 아니라 용기 크기가 기준이고, 가위는 날 길이 6cm가 경계선이죠. 이런 기준들이 항공사 홈페이지 곳곳에 흩어져 있어서 출발 전에 다 찾아보기가 어렵습니다.</p>
    <p>그래서 국토교통부 고시와 국내외 항공사 9곳의 공식 규정을 직접 확인해 <strong>품목 250개를 한 곳에 모았습니다.</strong> 물건 이름만 치면 기내와 위탁을 각각 ○ △ ✕로 보여 주고, 국내선과 국제선의 차이도 토글 하나로 바뀝니다.</p>

    <h2>최근 글</h2>
  </article>
  <div class="cards">{home_cards}</div>
  {AD}
</main>""")

# ── 소개 ────────────────────────────────────
page(path="about.html", cur="about.html", depth=0,
     title=f"소개 | {SITE_NAME}", desc="수하물 신호등을 누가, 왜, 어떤 자료로 만들었는지 밝힙니다.",
     body=f"""{hero("About", "이 사이트를 만든 이유",
       "규정을 찾느라 출발 전날 밤을 보내지 않아도 되게 만들고 싶었습니다.")}
<main class="wrap"><article class="post">
  <h2>왜 만들었나</h2>
  <p>여행 전날 짐을 싸다 보면 꼭 애매한 물건이 하나씩 나옵니다. 고데기는 되나, 김치는 부쳐야 하나, 보조배터리는 몇 개까지인가. 검색하면 블로그 글이 수십 개 나오는데 서로 말이 다르고, 언제 쓴 글인지도 알기 어렵습니다. 규정이 몇 년 사이에 여러 번 바뀌었기 때문이에요.</p>
  <p>그래서 <strong>공식 출처만 직접 확인해서 한곳에 모으기로</strong> 했습니다. 물건 이름만 치면 답이 나오고, 항공사와 노선에 따라 달라지는 부분은 선택으로 바뀌도록요.</p>

  <h2>자료의 출처</h2>
  <p>이 사이트의 정보는 아래 출처를 직접 확인해 작성했습니다. 2차 가공된 블로그 글이 아니라 원문을 기준으로 삼았습니다.</p>
  <ul>
    <li>국토교통부 및 정책브리핑의 항공 보안 고시 · 보도자료</li>
    <li>대한항공, 아시아나항공, 제주항공, 진에어, 트리니티항공(구 티웨이), 에어부산, 에어서울, 이스타항공, 에어프레미아의 공식 수하물 안내</li>
    <li>ANA, JAL, 피치항공, 에어아시아, 세부퍼시픽의 공식 수하물 안내</li>
    <li>국제민간항공기구(ICAO)의 위험물 운송 기준</li>
  </ul>

  <h2>업데이트 원칙</h2>
  <ul>
    <li>규정 변경 소식이 확인되면 해당 품목과 항공사 정보를 수정합니다</li>
    <li>글에는 작성일을 표시하고, 내용이 크게 바뀌면 본문에 변경 사실을 적습니다</li>
    <li>출처가 확인되지 않은 내용은 싣지 않습니다</li>
  </ul>

  <div class="callout warn">
    <span class="label">한계</span>
    <p>같은 물건이라도 항공사·노선·기종·운임 등급에 따라 결과가 달라질 수 있고, 최종 판단은 공항 보안검색 담당자가 합니다. 이 사이트는 <strong>참고용</strong>이며 공식 규정을 대체하지 않습니다. 출발 전 이용하시는 항공사의 공식 안내를 한 번 더 확인해 주세요.</p>
  </div>

  <h2>운영자</h2>
  <ul>
    <li>사이트명: {SITE_NAME}</li>
    <li>운영자: [운영자명]</li>
    <li>이메일: [이메일 주소]</li>
    <li>개설: 2026년 9월</li>
  </ul>
  <p>오류를 발견하시거나 추가했으면 하는 품목이 있다면 <a href="contact.html">문의 페이지</a>를 통해 알려 주세요. 확인 후 반영하겠습니다.</p>
</article></main>""")

# ── 문의 ────────────────────────────────────
page(path="contact.html", cur="contact.html", depth=0,
     title=f"문의 | {SITE_NAME}", desc="오류 제보, 품목 추가 요청, 개인정보 관련 문의를 받습니다.",
     body=f"""{hero("Contact", "문의하기", "규정 오류 제보와 품목 추가 요청을 환영합니다.")}
<main class="wrap"><article class="post">
  <h2>연락처</h2>
  <ul>
    <li>사이트명: {SITE_NAME}</li>
    <li>운영자: [운영자명]</li>
    <li>이메일: <a href="mailto:[이메일 주소]">[이메일 주소]</a></li>
  </ul>

  <h2>이런 내용을 보내 주세요</h2>
  <ul>
    <li>규정 정보의 오류 제보 및 수정 요청</li>
    <li>추가했으면 하는 품목 제안</li>
    <li>개인정보 열람 · 정정 · 삭제 · 처리정지 요청</li>
    <li>제휴 및 기타 문의</li>
  </ul>

  <h2>답변 기한</h2>
  <p>영업일 기준 3일 이내에 답변드리는 것을 원칙으로 합니다. 오류 제보의 경우 공식 출처를 함께 보내 주시면 확인이 훨씬 빠릅니다.</p>

  <div class="callout">
    <p>긴급한 수하물 문의는 이 사이트가 아니라 <strong>이용하시는 항공사 고객센터</strong>로 연락하시는 편이 확실합니다. 출발 당일이라면 공항 카운터에서 직접 확인해 주세요.</p>
  </div>
</article></main>""")

# ── 개인정보처리방침 ─────────────────────────
page(path="privacy.html", cur="privacy.html", depth=0,
     title=f"개인정보처리방침 | {SITE_NAME}",
     desc="수하물 신호등의 개인정보 수집·이용·보관에 관한 방침과 쿠키 및 광고 관련 안내입니다.",
     body=f"""{hero("Privacy", "개인정보처리방침", "시행일 [시행일] · 최종 수정 [시행일]")}
<main class="wrap"><article class="post">
  <h2>1. 총칙</h2>
  <p>{SITE_NAME}(이하 '본 사이트')은 이용자의 개인정보를 소중히 여기며 「개인정보 보호법」 등 관련 법령을 준수합니다. 본 방침은 본 사이트가 어떤 정보를 어떻게 다루고 보호하는지를 안내합니다.</p>

  <h2>2. 수집하는 개인정보 항목</h2>
  <p>본 사이트는 회원가입 절차가 없으며, 이름·연락처·주소 등 개인을 식별할 수 있는 정보를 직접 수집하지 않습니다.</p>
  <ul>
    <li>이용자가 입력한 검색어와 선택 값은 이용자의 브라우저 안에서만 처리되며 서버로 전송되거나 저장되지 않습니다.</li>
    <li>문의를 위해 이메일을 보내주신 경우, 답변 목적에 한해 해당 이메일 주소와 문의 내용을 이용합니다.</li>
  </ul>

  <h2>3. 자동으로 수집되는 정보와 쿠키</h2>
  <p>서비스 운영 과정에서 접속 일시, 브라우저 종류, 기기 정보, 유입 경로 등이 자동으로 기록될 수 있습니다.</p>
  <ul>
    <li>쿠키는 이용자의 브라우저에 저장되는 작은 텍스트 파일로, 방문 분석과 광고 게재에 사용됩니다.</li>
    <li>이용자는 브라우저 설정에서 쿠키 저장을 거부할 수 있으며, 거부하더라도 본 사이트 이용에는 지장이 없습니다.</li>
  </ul>

  <h2>4. 제3자 광고 및 분석 도구</h2>
  <p>본 사이트는 광고 게재를 위해 Google을 포함한 제3자 광고 사업자를 이용할 수 있습니다.</p>
  <ul>
    <li>Google을 포함한 제3자 공급업체는 쿠키를 사용하여 이용자의 이전 방문 기록에 기반한 광고를 게재합니다.</li>
    <li>Google이 광고 쿠키를 사용함으로써, 이용자는 본 사이트 및 인터넷의 다른 사이트 방문에 기반한 맞춤 광고를 받을 수 있습니다.</li>
    <li>이용자는 <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google 광고 설정</a>에서 맞춤 광고를 비활성화할 수 있습니다.</li>
    <li>제3자 공급업체의 쿠키 사용을 거부하려면 <a href="https://www.aboutads.info" target="_blank" rel="noopener">www.aboutads.info</a>를 방문하시기 바랍니다.</li>
    <li>방문 분석을 위해 Google Analytics 등의 도구를 사용할 수 있으며, 수집된 정보는 통계 목적으로만 이용됩니다.</li>
  </ul>

  <h2>5. 개인정보의 이용 목적</h2>
  <ul>
    <li>문의에 대한 답변 및 민원 처리</li>
    <li>서비스 개선과 오류 수정을 위한 통계 분석</li>
    <li>광고 게재 및 서비스 운영 유지</li>
  </ul>

  <h2>6. 보유 및 이용 기간</h2>
  <p>문의 응대를 위해 수집한 정보는 처리가 완료된 즉시 파기합니다. 관련 법령에 따라 보존이 필요한 경우에는 해당 기간 동안 보관합니다.</p>

  <h2>7. 개인정보의 제3자 제공</h2>
  <p>본 사이트는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 근거하거나 수사기관의 적법한 요청이 있는 경우에는 예외로 합니다.</p>

  <h2>8. 이용자의 권리</h2>
  <p>이용자는 언제든지 본인의 개인정보에 대한 열람·정정·삭제·처리정지를 요청할 수 있습니다. 아래 연락처로 요청하시면 지체 없이 처리하겠습니다.</p>

  <h2>9. 개인정보 보호책임자</h2>
  <ul>
    <li>성명: [운영자명]</li>
    <li>이메일: [이메일 주소]</li>
  </ul>
  <p>개인정보 침해에 관한 상담이 필요하신 경우 개인정보침해신고센터(privacy.kisa.or.kr, 국번없이 118)에 문의하실 수 있습니다.</p>

  <h2>10. 고지의 의무</h2>
  <p>본 개인정보처리방침은 [시행일]부터 시행됩니다. 내용의 추가·삭제·수정이 있을 경우 시행 7일 전부터 본 페이지를 통해 공지합니다.</p>
</article></main>""")

# ── 이용약관 ────────────────────────────────
page(path="terms.html", cur="terms.html", depth=0,
     title=f"이용약관 · 면책조항 | {SITE_NAME}",
     desc="수하물 신호등이 제공하는 정보의 성격과 책임 범위, 저작권에 관한 안내입니다.",
     body=f"""{hero("Terms", "이용약관 · 면책조항", "시행일 [시행일]")}
<main class="wrap"><article class="post">
  <h2>1. 정보의 성격</h2>
  <p>본 사이트가 제공하는 수하물 규정 정보는 이용자의 이해를 돕기 위한 참고용 자료입니다. 공식 규정을 대체하지 않습니다.</p>

  <h2>2. 최종 판단의 주체</h2>
  <p>실제 반입 가능 여부는 항공사의 운송약관과 공항 보안검색 담당자의 현장 판단에 따릅니다. 같은 물건이라도 항공사·노선·기종·운임 등급에 따라 결과가 달라질 수 있습니다.</p>

  <h2>3. 책임의 한계</h2>
  <p>본 사이트는 정보를 정확하게 유지하기 위해 노력하지만, 규정 변경이나 표기 오류로 인해 발생한 손해에 대해서는 책임을 지지 않습니다. 출발 전 반드시 이용하시는 항공사의 공식 안내를 확인해 주세요.</p>

  <h2>4. 저작권</h2>
  <p>본 사이트에 게시된 문서와 디자인의 저작권은 운영자에게 있습니다. 상업적 목적의 무단 복제·배포를 금합니다. 각 항공사 규정의 저작권은 해당 항공사에 있습니다.</p>

  <h2>5. 링크된 사이트</h2>
  <p>본 사이트는 항공사 공식 페이지로 연결되는 링크를 제공합니다. 링크된 사이트의 내용과 운영에 대해서는 책임지지 않습니다.</p>

  <h2>6. 광고</h2>
  <p>본 사이트는 운영 유지를 위해 광고를 게재할 수 있습니다. 광고주의 상품이나 서비스에 대해서는 본 사이트가 보증하지 않으며, 거래에 따른 책임은 이용자와 광고주에게 있습니다.</p>

  <h2>7. 약관의 변경</h2>
  <p>본 약관은 [시행일]부터 적용되며, 변경 시 본 페이지를 통해 공지합니다.</p>
</article></main>""")

# ── 404 ─────────────────────────────────────
page(path="404.html", cur="index.html", depth=0,
     title=f"페이지를 찾을 수 없습니다 | {SITE_NAME}", desc="요청하신 페이지가 없습니다.",
     body=f"""{hero("404", "페이지를 찾을 수 없어요", "주소가 바뀌었거나 삭제된 페이지입니다.")}
<main class="wrap"><article class="post">
  <p>찾으시는 내용이 아래에 있을 수 있습니다.</p>
  <div class="toolcta">
    <p><strong>수하물 판별기</strong><br>물건 이름으로 기내·위탁 여부를 바로 확인하세요.</p>
    <a class="btn" href="tool.html">판별기 열기</a>
  </div>
  <p><a href="index.html">홈으로 돌아가기</a> · <a href="posts/index.html">여행 가이드 보기</a></p>
</article></main>""")

# ── 수하물 판별기 ────────────────────────────
TOOL_STYLE  = pathlib.Path("/tmp/claude-0/tool_style.html").read_text(encoding="utf-8")
TOOL_BODY   = pathlib.Path("/tmp/claude-0/tool_body.html").read_text(encoding="utf-8")
TOOL_SCRIPT = pathlib.Path("/tmp/claude-0/tool_script.html").read_text(encoding="utf-8")

page(path="tool.html", cur="tool.html", depth=0,
     title=f"수하물 판별기 — 기내? 위탁? | {SITE_NAME}",
     desc="항공사와 노선을 고르고 물건 이름을 검색하면 기내·위탁·반입금지를 바로 알려줍니다. 품목 250개, 보조배터리 Wh 계산기 포함.",
     head_extra=TOOL_STYLE + "\n<style>.controls{top:52px; z-index:25}</style>\n",
     body=f"""{hero("Cabin · Checked · Prohibited", "이 짐, 들고 탈까 부칠까",
       "항공사와 노선을 고르고 물건 이름을 치면 기내·위탁·반입금지를 신호등처럼 알려드려요. 품목 250개를 담았고, 초성으로도 찾을 수 있어요.")}

{TOOL_BODY}

{TOOL_SCRIPT}""")

# ── robots · sitemap · ads.txt ───────────────
PAGES_FOR_SITEMAP = ["index.html", "tool.html", "posts/index.html", "about.html",
                     "contact.html", "privacy.html", "terms.html"] + [p["slug"] for p in POSTS]

(ROOT / "robots.txt").write_text(
"""User-agent: *
Allow: /

Sitemap: https://YOUR-DOMAIN/sitemap.xml
""", encoding="utf-8")

urls = "\n".join(
    f"  <url>\n    <loc>https://YOUR-DOMAIN/{u}</loc>\n"
    f"    <lastmod>{TODAY}</lastmod>\n"
    f"    <priority>{'1.0' if u=='index.html' else '0.9' if u=='tool.html' else '0.7'}</priority>\n  </url>"
    for u in PAGES_FOR_SITEMAP)
(ROOT / "sitemap.xml").write_text(
f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""", encoding="utf-8")

(ROOT / "ads.txt").write_text(
"""# 애드센스 승인 후 아래 줄의 pub-0000000000000000 을 본인 게시자 ID로 바꾸고 # 을 지우세요.
# 게시자 ID는 애드센스 > 계정 > 설정 > 계정 정보 에서 확인할 수 있습니다.
# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
""", encoding="utf-8")

(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("빌드 완료:", len(PAGES_FOR_SITEMAP), "페이지")
