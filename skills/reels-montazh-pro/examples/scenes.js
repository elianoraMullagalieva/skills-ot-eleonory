/* ===== ПРИМЕР библиотеки сцен (к демо-ролику selftest.py). =====
   Время — СЕКУНДЫ ИСХОДНИКА (длинной записи), а не ролика: одна библиотека на все ролики, plans.js выбирает куски.
   Здесь секунды берутся из words.js через W('слово', №вхождения). В реальном проекте обычно пишут числа
   прямо из расшифровки (СЛОВА_ПО_КУСКАМ.md): S(149.08,152.38,…).
   Правила: одна акцентная деталь на кадр, смены не чаще ~1.2 с, появление НА слове или на 0.1–0.2 с раньше. */
(()=>{
const H=STAGE_H, Wd=STAGE_W;

/* 1. «Привет, это (быстрый) тест монтажа» — сцена на КАЖДЫЙ дубль: какой дубль возьмёт план, тот и покажется */
for(let n=1;n<=3;n++){
  const a=W('привет',n,-1);if(a<0)continue;
  const m=W('монтажа',n,a+1.5);
  S(a-0.1,m+0.7,'D',
   `<div class="cx cap" id="c" style="top:${H*.26}px">это тест</div>
    <div class="cx hero" id="h" style="top:${H*.40}px">монтажа<span class="red">.</span></div>`,
   (t,q)=>{IN(q('#c'),t,a);IN(q('#h'),t,m-0.15,{s0:1.35,dy:0,e:'expo',blur:14});});
}

/* 2. «Сначала режем дубли» — лента дублей, красный рез, лишний кусок уходит вниз */
{const a=W('сначала',1,0),cut=W('режем',1,a+.5),d=W('дубли',1,cut+.4);
 const X0=Wd*.14,X1=Wd*.86,Y=H*.42,CW=(X1-X0)/5;
 S(a-0.1,d+0.9,'L',
  [0,1,2,3,4].map(i=>`<div class="card k" style="left:${X0+i*CW+4}px;top:${Y}px;width:${CW-8}px;height:${H*.18}px;border-radius:14px">
     <div class="sk" style="left:16px;right:16px;top:20px"></div><div class="sk" style="left:16px;width:40%;top:46px"></div></div>`).join('')+
  `<div class="a" id="cut" style="left:${X0+2*CW}px;top:${Y-40}px;width:4px;height:${H*.18+80}px;border-radius:2px;background:var(--red);transform-origin:50% 0"></div>
   <div class="cx mid" id="t" style="top:${H*.18}px">режем дубли</div>`,
  (t,q,qa)=>{WT(q('#t'),t,[cut,d]);
    qa('.k').forEach((k,i)=>{IN(k,t,a+i*.06,{dy:16,d:.4});
      if(i==2){const p=P(t,cut+.25,.5,'in');k.style.transform+=` translateY(${p*H*.5}px) rotate(${p*8}deg)`;k.style.opacity=1-p;}
      if(i>2){const p=P(t,cut+.45,.5,'soft');k.style.transform+=` translateX(${-p*CW}px)`;}});
    const c=q('#cut'),p=P(t,cut-.05,.3,'expo');c.style.transform=`scaleY(${p})`;c.style.opacity=t<cut+.6?1:1-P(t,cut+.6,.2);});
 window.SFX=(window.SFX||[]).concat([[cut,'click']]);}

/* 3. «потом добавляем графику» — вставка «записи экрана» покадрово (кадры: clip_frames.py → frames/screen) */
{const a=W('потом',1,0),g=W('графику',1,a+1),FROM=0;
 const WW=Math.round(Wd*.62),HH=Math.round(WW*10/16);
 const rec=timeMap([[a,0.5],[g,2.0],[g+1.5,3.5]]);   /* секунда исходника → секунда записи */
 S(a-0.1,g+1.4,'L',
  `<div class="card" id="win" style="left:${(Wd-WW)/2}px;top:${H*.12}px;width:${WW}px;height:${HH+44}px;overflow:hidden">
     <div class="a" style="left:18px;top:15px;display:flex;gap:8px">${[0,1,2].map(()=>`<i style="width:12px;height:12px;border-radius:50%;background:var(--line);display:block"></i>`).join('')}</div>
     <div class="a" style="left:0;top:44px;width:${WW}px;height:${HH}px;overflow:hidden;background:#fff">
       <img class="fr" style="position:absolute;left:0;top:0;width:${WW}px;height:${HH}px;transform-origin:0 0"></div></div>`,
  (t,q)=>{const w=q('#win');w._noFx=1;IN(w,t,a,{dy:24,d:.45,blur:6});
    setFrame(q('.fr'),'frames/screen',frameNo(rec(t),FROM));
    place(q('.fr'),WW,HH,L(1,1.25,P(t,g,1.0,'io')),.62,.4);});
 preload('frames/screen');
 window.SFX=(window.SFX||[]).concat([[g,'pop']]);}

/* 4. «Всё, готово» — галочка рисуется штрихом */
{const a=W('всё',1,0),r=W('готово',1,a+.5);
 S(a-0.1,r+1.2,'D',
  `<svg class="a" style="left:${Wd/2-60}px;top:${H*.2}px" width="120" height="120" viewBox="0 0 120 120">
     <circle class="st" cx="60" cy="60" r="54" pathLength="1" id="o" style="color:var(--red)"/>
     <path class="st" d="M34 62 L53 80 L88 42" pathLength="1" id="v" style="stroke-width:6"/></svg>
   <div class="cx mid" id="t" style="top:${H*.58}px">готово</div>`,
  (t,q)=>{DRAW(q('#o'),P(t,a,.6,'io'));DRAW(q('#v'),P(t,r,.45,'expo'));IN(q('#t'),t,r);});
 window.SFX=(window.SFX||[]).concat([[r,'send']]);}
})();
