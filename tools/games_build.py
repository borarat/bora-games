# games.html 생성기 — catalog.json(게임 파일에서 뽑은 정보) → 밝은 디자인 + 영역·학년·기기 필터 + 검색
# 쓰는 법: python3 tools/games_build.py  (저장소 루트에서). 게임을 더하거나 뺄 때는 catalog.json을 고친 뒤 다시 실행한다. games.html은 손으로 고치지 않는다
import json,html
import os
HERE=os.path.dirname(os.path.abspath(__file__))
rows=json.load(open(os.path.join(HERE,'catalog.json'),encoding='utf8'))
FIX={'훈민정음 제자 원리 익히기':'G211','사랑손님과 어머니 시뮬레이션':'L401'}
HIDE={'조건 사냥꾼'}  # 미완성 — 리모델링 뒤 다시 넣는다 (교사 결정 2026.10.08)
rows=[r for r in rows if r['title'] not in HIDE]
for r in rows:
    if not r['code']: r['code']=FIX[r['title']]
AREA={'G':'문법','L':'문학','R':'읽기','W':'쓰기','S':'말하기듣기'}
AREA_LABEL={'문법':'문법','문학':'문학','읽기':'읽기','쓰기':'쓰기','말하기듣기':'말하기·듣기'}
GRADE={'1':'1학년','2':'2학년','3':'3학년','4':'학년 무관'}
# 표시 학년 — 목록에 보이는 학년(게임 코드와 무관, 내년 교육과정 통일 때 여기만 고친다). 한 게임에 여럿 가능, '4'=학년 무관
BOTH_STD={'9국04-01','9국02-05'}  # 음운·논증은 두 학년에 걸침
GRADE_OVERRIDE={  # 교사 확정 2026.10.08
 'G209':['2'],'G210':['2'],'G211':['2'],   # 한글 창제원리 3종 → 2학년 전용
 'L201':['4'],                              # 원미동 어휘 원정대 → 학년 무관
 'L302':['2','3'],'L303':['2','3'],         # 꺼삐딴 리 2종 → 2·3학년
}
def grades_of(c,std):
    if c in GRADE_OVERRIDE: return GRADE_OVERRIDE[c]
    g=c[1]
    if g=='4': return ['4']
    if any(s in BOTH_STD for s in std) and g in '23': return ['2','3']
    return [g]
def grade_label(gs):
    return '학년 무관' if gs==['4'] else '·'.join(gs)+'학년'

# 성취기준 2022 원문(배치표)·묶음 제목 — 목록을 성취기준별로 묶는다
STD2022={
 '9국01-04':('공감하며 대화','상대의 말을 경청하고 상대의 감정과 입장에 공감하는 반응을 보이며 대화한다.'),
 '9국01-06':('발표','다양한 자료를 재구성하여 내용을 체계적으로 조직하고 청중이 이해하기 쉽게 발표한다.'),
 '9국01-09':('갈등 조정','서로의 감정이나 바라는 바를 진솔하게 표현하면서 갈등을 조정한다.'),
 '9국02-05':('설명·논증 방법','글에 사용된 다양한 설명 방법과 논증 방법을 파악하고, 그 타당성을 평가하며 읽는다.'),
 '9국03-01':('설명하는 글','대상의 특성에 적합한 설명 방법을 활용하여 글을 쓴다.'),
 '9국03-03':('주장하는 글','주장을 뒷받침할 수 있는 타당한 근거를 들고 적절한 표현을 사용하여 주장하는 글을 쓴다.'),
 '9국03-07':('복합양식 자료로 쓰기','복합양식 자료를 활용하여 내용을 생성하고 글의 유형을 고려하여 내용을 조직하며 글을 쓴다.'),
 '9국03-08':('고쳐쓰기','쓰기 과정과 전략을 점검·조정하며 글을 쓰고, 독자를 고려하여 글을 고쳐 쓴다.'),
 '9국03-10':('쓰기 윤리','쓰기 윤리를 지키며 글을 쓰는 태도를 지닌다.'),
 '9국04-01':('음운·문자 체계','국어의 음운 체계와 문자 체계를 이해하고 국어생활에 활용한다.'),
 '9국04-02':('단어의 형성','단어의 짜임을 분석하여 새말 형성의 원리를 이해한다.'),
 '9국04-03':('품사','품사의 종류와 특성을 이해하고 국어 자료를 분석한다.'),
 '9국04-04':('문장의 짜임','문장의 짜임을 이해하고 표현 효과를 고려하여 문장을 구성한다.'),
 '9국04-05':('피동·인용 표현','피동 표현과 인용 표현의 의도와 효과를 분석하고 상황에 맞게 활용한다.'),
 '9국05-02':('갈등','갈등의 진행과 해결 과정을 파악하며 작품을 감상한다.'),
 '9국05-04':('서술자와 시점','보는 이나 말하는 이의 특성과 효과를 파악하며 작품을 감상한다.'),
 '9국05-05':('사회·문화적 상황','작품에 반영된 사회·문화적 상황을 이해하며 작품을 감상한다.'),
 '9국05-06':('개성적 표현','자신의 경험을 개성적인 발상과 표현으로 형상화한다.'),
 '9국05-08':('작품 해석과 비교','근거를 바탕으로 작품을 해석하고, 다른 해석들과 비교하여 자신의 해석을 평가한다.'),
}
HANGUL={'G209','G210','G211'}  # 한글 창제 원리 — 코드는 9국04-01이지만 음운 체계와 따로 묶는다(교사 큐레이션)
def group_of(c,std):
    if c in HANGUL: return '한글'
    return std[0] if std else 'none'
def group_meta(gid):  # (정렬키, 코드표시, 주제, 원문)
    if gid=='한글': return ('9국04-05a','9국04-01','한글 창제 원리','한글의 창제 원리와 제자 원리를 이해한다. (문자 체계, 9국04-01)')
    if gid=='none': return ('zzz','','그 외','성취기준을 아직 정하지 않은 게임')
    t=STD2022.get(gid,('',''))
    return (gid,gid,t[0],t[1])
DEV={'💻📱 노트북·모바일':('M1','노트북·모바일'),'💻 노트북 권장':('M2','노트북 권장'),'💻 노트북 전용':('M3','노트북 전용')}
# 성취기준 원문 (목록 머리말에 쓰던 것 + 교육과정 원문)
STD={
 '9국04-01':'음운 체계 — 국어의 음운 체계와 문자 체계를 이해하고 국어생활에 활용한다',
 '9국04-02':'단어의 형성 — 단어의 짜임을 분석하여 새말 형성의 원리를 이해한다',
 '9국04-03':'품사 — 품사의 종류와 특성을 이해하고 국어 자료를 분석한다',
 '9국04-04':'문장의 짜임 — 문장의 짜임을 이해하고 표현 효과를 고려하여 문장을 구성한다',
 '9국04-05':'능동·피동 — 피동 표현과 인용 표현의 의도와 효과를 분석하고 활용한다',
 '9국04-06':'문장의 짜임과 양상을 탐구하고 활용한다',
}
areas=['문법','문학','읽기','쓰기','말하기듣기']
games=[]
for r in rows:
    c=r['code'];a=AREA[c[0]];g=c[1]
    dev=DEV.get(r['badge'],('M2','노트북 권장'))
    gs=grades_of(c,r['std'])
    games.append(dict(title=r['title'],desc=r['desc'],href=r['href'],emoji=r['emoji'],code=c,area=a,grades=gs,gradeLabel=grade_label(gs),std=r['std'],dev=dev[0],devLabel=dev[1]))
# 영역 안에서는 성취기준 → 코드 순으로
order={a:i for i,a in enumerate(areas)}
games.sort(key=lambda x:(order[x['area']],x['std'][0] if x['std'] else 'zz',x['code']))
def esc(s):return html.escape(s,quote=True)
for x in games:
    x['group']=group_of(x['code'],x['std'])
def card_html(x):
    std=' '.join(f'<span class="std" title="{esc(STD2022.get(s,("",""))[1])}">{s}</span>' for s in x['std'])
    return f'''        <a class="card a-{x['area']}" href="{esc(x['href'])}" data-area="{x['area']}" data-grade="{' '.join(x['grades'])}" data-dev="{x['dev']}" data-text="{esc((x['title']+' '+x['desc']+' '+' '.join(x['std'])+' '+x['code']).lower())}">
          <div class="top"><span class="emoji">{x['emoji']}</span><span class="code">{x['code']}</span></div>
          <div class="title">{esc(x['title'])}</div>
          <div class="desc">{esc(x['desc'])}</div>
          <div class="meta"><span class="tag grade">{x['gradeLabel']}</span><span class="tag dev d-{x['dev']}">{x['devLabel']}</span>{std}</div>
        </a>'''
sections=[]
for a in areas:
    ags=[x for x in games if x['area']==a]
    gids=sorted(set(x['group'] for x in ags),key=lambda g:group_meta(g)[0])
    subs=[]
    for gid in gids:
        gm=group_meta(gid);members=[x for x in ags if x['group']==gid]
        members.sort(key=lambda x:x['code'])
        head=f'<span class="scode">{gm[1]}</span>' if gm[1] else ''
        subs.append(f'''      <div class="sub">
        <div class="subh">{head}<span class="stopic">{esc(gm[2])}</span><span class="stext">{esc(gm[3])}</span><span class="subcnt"></span></div>
        <div class="grid">
{chr(10).join(card_html(x) for x in members)}
        </div>
      </div>''')
    sections.append(f'''    <section class="area" id="{a}" data-area="{a}">
      <h2><span class="dot"></span>{AREA_LABEL[a]} <span class="cnt"></span></h2>
{chr(10).join(subs)}
    </section>''')
page=f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>게임 모음 | 보라라랩 국어 에듀테크 연구소</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
/* 첫 화면(index.html)과 같은 크림·파스텔 팔레트. 영역 색은 게임 화면 헤더 띠 색과 맞춤 */
:root{{--ink:#24324a;--ink2:#5a6478;--coral:#e56b5d;--blue:#7c3aed;--mint:#c9f2e5;--cream:#fff8ee;--lemon:#f7d774;--line:#eadfce;
  --c-문법:#7C5CBF;--c-문학:#2E9B79;--c-읽기:#3B86C9;--c-쓰기:#D4718F;--c-말하기듣기:#F58A2E;
  --l-문법:#F1ECFA;--l-문학:#E6F6EF;--l-읽기:#E8F1FA;--l-쓰기:#FBEAF0;--l-말하기듣기:#FFF0DF}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{color-scheme:light}}
body{{font-family:'Noto Sans KR','Malgun Gothic','맑은 고딕',sans-serif;background:var(--cream);color:var(--ink);min-height:100vh;word-break:keep-all}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 1.25rem 3rem}}
/* 머리 */
.head{{display:flex;align-items:flex-end;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding:2.2rem 0 1rem}}
.head .brand{{font-family:'Jua',sans-serif;font-size:1.05rem;color:var(--ink2)}}
.head .brand:before{{content:'';display:inline-block;width:.6rem;height:.6rem;border-radius:50%;background:var(--coral);margin-right:.4rem;vertical-align:1px}}
.head h1{{font-family:'Jua',sans-serif;font-size:clamp(2rem,4vw,2.7rem);line-height:1.15;margin-top:.2rem}}
.head h1 em{{font-style:normal;color:var(--blue);background:linear-gradient(transparent 60%,var(--lemon) 60%)}}
.head .sub{{font-family:'Gaegu',cursive;font-size:1.25rem;color:var(--ink2);margin-top:.2rem}}
.head .back{{font-family:'Jua',sans-serif;font-size:1rem;color:var(--ink);background:#fff;border:2px solid var(--ink);border-radius:999px;padding:.45rem 1.1rem;box-shadow:.22rem .2rem 0 var(--lemon)}}
/* 찾기 */
.tools{{position:sticky;top:0;z-index:5;background:rgba(255,248,238,.94);backdrop-filter:blur(6px);padding:.7rem 0 .8rem;border-bottom:1.5px solid var(--line);margin-bottom:1.2rem}}
.search{{display:flex;align-items:center;gap:.5rem;background:#fff;border:2px solid var(--line);border-radius:14px;padding:.45rem .9rem;margin-bottom:.6rem}}
.search:focus-within{{border-color:var(--blue)}}
.search input{{flex:1;border:none;outline:none;font:inherit;font-size:1.05rem;color:var(--ink);background:transparent;min-width:0}}
.search .clr{{border:none;background:transparent;color:var(--ink2);font-size:1.1rem;cursor:pointer;display:none;min-width:32px;min-height:32px}}
.search.has .clr{{display:block}}
.frow{{display:flex;flex-wrap:wrap;gap:.35rem .5rem;align-items:center;margin-top:.35rem}}
.frow .lab{{font-family:'Jua',sans-serif;font-size:.95rem;color:var(--ink2);margin-right:.2rem;min-width:2.6rem}}
.chip{{font:inherit;font-size:.92rem;font-weight:500;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:.32rem .85rem;cursor:pointer;min-height:36px;transition:all .15s}}
.chip:hover{{border-color:var(--ink2)}}
.chip.on{{background:var(--ink);border-color:var(--ink);color:#fff}}
.chip.on.c-문법{{background:var(--c-문법);border-color:var(--c-문법)}}.chip.on.c-문학{{background:var(--c-문학);border-color:var(--c-문학)}}.chip.on.c-읽기{{background:var(--c-읽기);border-color:var(--c-읽기)}}.chip.on.c-쓰기{{background:var(--c-쓰기);border-color:var(--c-쓰기)}}.chip.on.c-말하기듣기{{background:var(--c-말하기듣기);border-color:var(--c-말하기듣기)}}
.chip .n{{opacity:.65;font-size:.85em;margin-left:.2rem}}
.status{{font-size:.92rem;color:var(--ink2);margin-top:.5rem;display:flex;gap:.8rem;align-items:center;flex-wrap:wrap}}
.status b{{color:var(--ink)}}
.status .reset{{font:inherit;font-size:.9rem;color:var(--coral);background:none;border:none;cursor:pointer;text-decoration:underline;display:none}}
.status.filtered .reset{{display:inline}}
/* 영역 */
.area{{margin-bottom:2.2rem}}
.area h2{{font-family:'Jua',sans-serif;font-size:1.6rem;display:flex;align-items:center;gap:.5rem;margin-bottom:.8rem;padding-bottom:.4rem;border-bottom:2px solid var(--line)}}
.area h2 .dot{{width:.8rem;height:.8rem;border-radius:50%;background:var(--c)}}
.area h2 .cnt{{font-family:'Gaegu',cursive;font-size:1.1rem;color:var(--ink2);font-weight:400}}
.area[data-area="문법"]{{--c:var(--c-문법);--l:var(--l-문법)}}.area[data-area="문학"]{{--c:var(--c-문학);--l:var(--l-문학)}}.area[data-area="읽기"]{{--c:var(--c-읽기);--l:var(--l-읽기)}}.area[data-area="쓰기"]{{--c:var(--c-쓰기);--l:var(--l-쓰기)}}.area[data-area="말하기듣기"]{{--c:var(--c-말하기듣기);--l:var(--l-말하기듣기)}}
.area.empty{{display:none}}
.sub{{margin-bottom:1.3rem}}
.sub.empty{{display:none}}
.subh{{display:flex;align-items:baseline;gap:.5rem;flex-wrap:wrap;margin:.2rem 0 .7rem;padding-left:.1rem}}
.subh .scode{{font-family:'Jua',sans-serif;font-size:.88rem;color:var(--c);background:var(--l);border-radius:8px;padding:.12rem .55rem}}
.subh .stopic{{font-weight:700;color:var(--ink);font-size:1.02rem}}
.subh .stext{{font-size:.9rem;color:var(--ink2)}}
.subh .subcnt{{font-size:.85rem;color:var(--ink2);font-family:'Gaegu',cursive}}
@media(max-width:600px){{.subh .stext{{width:100%}}}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.9rem}}
/* 카드 */
.card{{background:#fff;border:1.5px solid var(--line);border-top:5px solid var(--c);border-radius:14px;padding:.95rem 1rem 1rem;display:flex;flex-direction:column;gap:.35rem;box-shadow:0 2px 8px rgba(36,50,74,.05);transition:transform .15s,box-shadow .15s}}
.card:hover{{transform:translateY(-3px);box-shadow:0 10px 22px rgba(36,50,74,.12)}}
.card.hide{{display:none}}
.card .top{{display:flex;justify-content:space-between;align-items:center}}
.card .emoji{{font-size:1.9rem;line-height:1}}
.card .code{{font-family:'Jua',sans-serif;font-size:.85rem;color:var(--c);background:var(--l);border-radius:8px;padding:.1rem .5rem}}
.card .title{{font-size:1.15rem;font-weight:700;line-height:1.3}}
.card .desc{{font-size:.93rem;color:var(--ink2);line-height:1.45;flex:1}}
.card .meta{{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.35rem}}
.tag{{font-size:.76rem;border-radius:999px;padding:.12rem .55rem;border:1px solid var(--line);color:var(--ink2);background:#fbf7f0}}
.tag.grade{{background:var(--l);border-color:transparent;color:var(--c);font-weight:700}}
.tag.d-M1{{background:#e8f6ee;border-color:transparent;color:#1f7a45}}
.tag.d-M3{{background:#fdecea;border-color:transparent;color:#b3362c}}
.none{{display:none;text-align:center;padding:3rem 1rem;font-family:'Gaegu',cursive;font-size:1.4rem;color:var(--ink2)}}
.none.on{{display:block}}
.foot{{text-align:center;font-size:.9rem;color:var(--ink2);padding:2rem 0 0;border-top:1.5px solid var(--line);margin-top:1rem;line-height:1.8}}
.foot a{{color:var(--blue)}}
@media(max-width:600px){{.tools{{position:static}}.head{{padding-top:1.4rem}}.grid{{grid-template-columns:1fr}}.frow .lab{{width:100%;min-width:0}}}}
</style>
</head>
<body>
<div class="wrap">
  <header class="head">
    <div>
      <div class="brand">보라라랩 에듀테크 연구소</div>
      <h1>국어 <em>게임</em> 모음</h1>
      <div class="sub">재미있게 배우고 연습하는 국어 개념</div>
    </div>
    <a class="back" href="index.html">← 홈으로</a>
  </header>

  <div class="tools">
    <label class="search" id="searchBox"><span aria-hidden="true">🔍</span><input id="q" type="search" placeholder="게임 이름, 설명, 성취기준 코드로 찾기 (예: 피동, 9국04-02, 두더지)" autocomplete="off"><button class="clr" id="clr" aria-label="지우기">✕</button></label>
    <div class="frow"><span class="lab">영역</span>
      <button class="chip on" data-f="area" data-v="">전체</button>
      {' '.join(f'<button class="chip c-{a}" data-f="area" data-v="{a}">{AREA_LABEL[a]}<span class="n"></span></button>' for a in areas)}
    </div>
    <div class="frow"><span class="lab">학년</span>
      <button class="chip on" data-f="grade" data-v="">전체</button>
      {' '.join(f'<button class="chip" data-f="grade" data-v="{g}">{GRADE[g]}<span class="n"></span></button>' for g in ['1','2','3','4'])}
    </div>
    <div class="frow"><span class="lab">기기</span>
      <button class="chip on" data-f="dev" data-v="">전체</button>
      <button class="chip" data-f="dev" data-v="M1">💻📱 노트북·모바일<span class="n"></span></button>
      <button class="chip" data-f="dev" data-v="M2">💻 노트북 권장<span class="n"></span></button>
      <button class="chip" data-f="dev" data-v="M3">💻 노트북 전용<span class="n"></span></button>
    </div>
    <div class="status" id="status"><span><b id="shown">{len(games)}</b>개 표시</span><button class="reset" id="reset">조건 지우기</button></div>
  </div>

{chr(10).join(sections)}
  <div class="none" id="none">조건에 맞는 게임이 없어요. 다른 조건으로 찾아보세요.</div>

  <footer class="foot">
    학년은 게임 코드 기준(1·2학년 2022 개정, 3학년 2015 개정)이며, 같은 내용을 두 학년이 배우는 게임도 있습니다.<br>
    보라라랩 국어 에듀테크 연구소 · <a href="privacy.html">개인정보처리방침</a> · Powered by GitHub Pages
  </footer>
</div>

<script>
/* 필터·검색 — 카드의 data-area / data-grade / data-dev / data-text 로 거른다. 조건은 주소(#area=문법&grade=2)에 남겨 공유할 수 있다 */
(function(){{
  var cards=[].slice.call(document.querySelectorAll('.card')),chips=[].slice.call(document.querySelectorAll('.chip'));
  var q=document.getElementById('q'),box=document.getElementById('searchBox'),st={{area:'',grade:'',dev:'',q:''}};
  function readHash(){{var h=location.hash.replace(/^#/,'');if(!h)return;if(!h.includes('='))h='area='+h;h.split('&').forEach(function(p){{var kv=p.split('=');if(kv[0] in st)st[kv[0]]=decodeURIComponent(kv[1]||'')}})}}
  function writeHash(){{var ps=[];for(var k in st)if(st[k])ps.push(k+'='+encodeURIComponent(st[k]));var h=ps.length?'#'+ps.join('&'):'';if(h!==location.hash)history.replaceState(null,'',location.pathname+h)}}
  function inc(field,v){{return (' '+field+' ').indexOf(' '+v+' ')>=0}}
  function match(c,skip){{var t=c.dataset;return (skip==='area'||!st.area||inc(t.area,st.area))&&(skip==='grade'||!st.grade||inc(t.grade,st.grade))&&(skip==='dev'||!st.dev||inc(t.dev,st.dev))&&(!st.q||t.text.indexOf(st.q)>=0)}}
  function apply(){{
    var n=0;cards.forEach(function(c){{var ok=match(c);c.classList.toggle('hide',!ok);if(ok)n++}});
    document.querySelectorAll('.sub').forEach(function(s){{var k=s.querySelectorAll('.card:not(.hide)').length;s.classList.toggle('empty',!k);var c=s.querySelector('.subcnt');if(c)c.textContent=k+'개'}});
    document.querySelectorAll('.area').forEach(function(s){{var k=s.querySelectorAll('.card:not(.hide)').length;s.classList.toggle('empty',!k);s.querySelector('.cnt').textContent=k+'개'}});
    document.getElementById('shown').textContent=n;document.getElementById('none').classList.toggle('on',!n);
    var f=!!(st.area||st.grade||st.dev||st.q);document.getElementById('status').classList.toggle('filtered',f);
    chips.forEach(function(ch){{var k=ch.dataset.f;ch.classList.toggle('on',st[k]===ch.dataset.v);var sp=ch.querySelector('.n');if(sp&&ch.dataset.v){{sp.textContent=' '+cards.filter(function(c){{return match(c,k)&&inc(c.dataset[k],ch.dataset.v)}}).length}}}});
    box.classList.toggle('has',!!st.q);writeHash();
  }}
  chips.forEach(function(ch){{ch.addEventListener('click',function(){{st[ch.dataset.f]=ch.dataset.v;apply()}})}});
  q.addEventListener('input',function(){{st.q=q.value.trim().toLowerCase();apply()}});
  document.getElementById('clr').addEventListener('click',function(){{q.value='';st.q='';apply();q.focus()}});
  document.getElementById('reset').addEventListener('click',function(){{st={{area:'',grade:'',dev:'',q:''}};q.value='';apply()}});
  readHash();q.value=st.q;apply();
}})();
</script>
</body>
</html>
'''
open(os.path.join(HERE,'..','games.html'),'w',encoding='utf8').write(page)
print(len(games),'games written')
