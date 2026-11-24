'use client';

import { useEffect, useState } from 'react';
import { predictDemoSentiment } from './demo-predictor.mjs';

const chapters = [
  { id: 'scraping', number: '۰۱', title: 'جمع‌آوری دیدگاه‌ها', short: 'استخراج از وب' },
  { id: 'labeling', number: '۰۲', title: 'ساخت داده قابل فهم', short: 'امتیاز و احساس' },
  { id: 'nlp', number: '۰۳', title: 'آماده‌سازی زبان', short: 'پاک‌سازی و توکن' },
  { id: 'vectors', number: '۰۴', title: 'تبدیل متن به عدد', short: 'TF–IDF' },
  { id: 'models', number: '۰۵', title: 'یادگیری ماشین', short: 'آموزش مدل‌ها' },
  { id: 'results', number: '۰۶', title: 'ارزیابی عملکرد', short: 'معیارها و مقایسه' },
  { id: 'playground', number: '۰۷', title: 'آزمایشگاه شما', short: 'پیش‌بینی تعاملی' },
];

const models = {
  'Logistic Regression': { title: 'رگرسیون لجستیک', detail: 'احتمال تعلق متن به هر کلاس را با یک مرز تصمیم یاد می‌گیرد.', positive: 1.12, negative: 1.05, tag: 'مرز تصمیم' },
  'Linear SVM': { title: 'ماشین بردار پشتیبان', detail: 'به‌دنبال مرزی با بیشترین فاصله میان نمونه‌های دو کلاس است.', positive: 1.2, negative: 1.14, tag: 'بیشترین حاشیه' },
  'MultinomialNB': { title: 'بیز ساده چندجمله‌ای', detail: 'با احتمال رخداد واژه‌ها، محتمل‌ترین کلاس را انتخاب می‌کند.', positive: 0.96, negative: 1.08, tag: 'احتمال واژه‌ها' },
  RandomForest: { title: 'جنگل تصادفی', detail: 'رأی چندین درخت تصمیم را ترکیب می‌کند؛ گزینه‌ای برای آزمایش‌های بعدی پروژه.', positive: 1.05, negative: 1.02, tag: 'رأی درخت‌ها' },
};

function Icon({ name, size = 20 }) {
  const paths = {
    spark: <><path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-2-5.8L4 11l6-2.2L12 3Z"/><path d="m19 14 1.1 2.9L23 18l-2.9 1.1L19 22l-1.1-2.9L15 18l2.9-1.1L19 14Z"/></>,
    arrow: <><path d="M7 17 17 7M7 7h10v10"/></>,
    globe: <><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></>,
    code: <><path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 4l-4 16"/></>,
    layers: <><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/></>,
    chart: <><path d="M4 19V5M4 19h17"/><path d="m7 15 4-4 3 2 6-7"/></>,
    play: <><path d="m8 5 12 7-12 7V5Z"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
    chevron: <path d="m7 10 5 5 5-5"/>,
    mouse: <><rect x="6" y="3" width="12" height="18" rx="6"/><path d="M12 3v5"/></>,
    sliders: <><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M2 14h4M10 8h4M18 16h4"/></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

function SectionHeading({ eyebrow, title, children }) {
  return <><div className="eyebrow"><span />{eyebrow}</div><h2>{title}</h2><p className="section-copy">{children}</p></>;
}

function BrowserScene() {
  const reviews = [
    ['کتابخانه نیمه‌شب', '★★★★★', 'خواندنش واقعاً لذت‌بخش بود؛ پیشنهادش می‌کنم.'],
    ['هدفون بی‌سیم', '★★★☆☆', 'کیفیت صدا خوبه ولی باتری زود تموم می‌شه.'],
    ['کفش روزمره', '★☆☆☆☆', 'بعد از دو روز دوختش باز شد.'],
  ];
  return <div className="browser-window">
    <div className="browser-top"><div className="traffic"><i/><i/><i/></div><div className="address">shop.example / reviews</div><span className="browser-lock">● امن</span></div>
    <div className="shop-head"><div className="shop-logo">ن</div><div><b>نظرات کاربران</b><small>تجربه واقعی خریداران</small></div><span className="shop-count">۲۴۸ نظر</span></div>
    <div className="scrape-status"><span className="pulse-dot"/> در حال پیمایش صفحه و پیدا کردن دیدگاه‌ها <span>LIVE</span></div>
    <div className="review-stack">{reviews.map((r, i) => <div className={`review-card review-${i + 1}`} key={r[0]}><div className="review-meta"><b>{r[0]}</b><span>{r[1]}</span></div><p>{r[2]}</p><small>خریدار تأییدشده · چند روز پیش</small><div className="extract-corner"><Icon name="arrow" size={13}/></div></div>)}</div>
    <div className="browser-footer"><span>صفحه ۱ از ۱۲</span><div className="progress-track"><i style={{ width: '38%' }}/></div><b>۹۶ نظر پیدا شد</b></div>
    <div className="float-chip chip-a"><Icon name="code" size={15}/> HTML → Review</div><div className="float-chip chip-b"><span className="green-dot"/> داده دریافت شد</div>
  </div>;
}

function LabelScene() {
  const rows = [['این کتاب فوق‌العاده بود، عاشقش شدم.', 5, 'مثبت'], ['کیفیت محصول معمولی بود.', 3, 'خنثی'], ['اصلاً پیشنهاد نمی‌کنم، خیلی ضعیف بود.', 1, 'منفی']];
  return <div className="data-scene"><div className="scene-topline"><span>RAW REVIEWS</span><span>LABELING ENGINE <i className="live-pip"/></span></div><div className="data-table"><div className="table-head"><span>متن دیدگاه</span><span>امتیاز</span><span>برچسب</span></div>{rows.map((r,i)=><div className="table-row" key={r[0]}><span>{r[0]}</span><b className="stars">{'★'.repeat(r[1])}{'☆'.repeat(5-r[1])}</b><em className={i===0?'sent-positive':i===2?'sent-negative':'sent-neutral'}>{r[2]}</em></div>)}</div><div className="label-equation"><div><small>امتیاز بالا</small><b>۴ و ۵</b><span>Positive</span></div><div className="equation-arrow">←</div><div><small>امتیاز پایین</small><b>۱ و ۲</b><span>Negative</span></div></div><div className="scene-note"><Icon name="spark" size={16}/> هر دیدگاه به یک نمونه آموزشی قابل استفاده تبدیل می‌شود.</div></div>;
}

function NLPScene() {
  const tokens = ['این', 'کتاب', 'واقعاً', 'فوق‌العاده', 'بود'];
  return <div className="nlp-scene"><div className="nlp-input"><span>ورودی خام</span><p>«این کتاب واقعاً فوق‌العاده بود!!! 😍»</p></div><div className="process-step"><span className="step-index">۱</span><div><b>نرمال‌سازی</b><small>یکسان‌سازی نویسه‌ها و فاصله‌ها</small></div><code>ی ← ي</code></div><div className="process-step"><span className="step-index">۲</span><div><b>پاک‌سازی</b><small>حذف نشانه‌ها، اعداد و ایموجی</small></div><code>!!! 😍 → ∅</code></div><div className="process-step"><span className="step-index">۳</span><div><b>توکن‌سازی و توقف‌واژه</b><small>شکستن جمله به واژه‌های معنادار</small></div><code>Hazm</code></div><div className="token-cloud">{tokens.map((t,i)=><span key={t} className={i===0?'muted-token':i===3?'hot-token':''}>{t}</span>)}</div><div className="nlp-output"><small>متن آماده برای بردارسازی</small><b>کتاب · واقعاً · فوق‌العاده</b></div></div>;
}

function VectorScene() {
  const words = ['فوق‌العاده', 'کتاب', 'ضعیف', 'پیشنهاد', 'خراب', 'زیبا'];
  const vals = [0.92,0.61,0.08,0.77,0.02,0.48];
  return <div className="vector-scene"><div className="vector-title"><div><span>DOCUMENT</span><b>«کتاب فوق‌العاده بود»</b></div><div className="tfidf-mark">TF–IDF</div></div><div className="vector-caption">هر واژه به یک وزن عددی تبدیل می‌شود</div><div className="vector-grid">{words.map((w,i)=><div className="vector-cell" key={w}><span>{w}</span><div className="vector-bar"><i style={{height:`${vals[i]*100}%`}}/></div><b>{vals[i].toFixed(2)}</b></div>)}</div><div className="vector-result"><span>[</span>{vals.slice(0,4).map((v,i)=><b key={i}>{v.toFixed(2)}</b>)}<span>… ]</span><small>بردار ویژگی با ۱۰٬۰۰۰ بُعد بالقوه</small></div><div className="scene-note"><Icon name="layers" size={16}/> واژه‌های مهم‌تر، وزن بیشتری در تصمیم مدل می‌گیرند.</div></div>;
}

function ModelScene({ selected, onSelect }) {
  const list = ['MultinomialNB', 'Logistic Regression', 'Linear SVM'];
  return <div className="model-scene"><div className="model-switcher">{list.map(m=><button key={m} className={selected===m?'chosen':''} onClick={()=>onSelect(m)}>{m==='MultinomialNB'?'Naive Bayes':m==='Logistic Regression'?'Logistic Reg.':'Linear SVM'}</button>)}</div><div className="model-illustration"><div className="data-points"><span/><span/><span/><span/><span/><span/><span/><span/><span/><span/></div><div className={`decision-boundary boundary-${selected==='Linear SVM'?'svm':selected==='MultinomialNB'?'nb':'lr'}`}/><div className="class-label positive-label">مثبت +</div><div className="class-label negative-label">منفی −</div></div><div className="model-explain"><span className="model-icon"><Icon name="chart" size={22}/></span><div><b>{models[selected].title}</b><p>{models[selected].detail}</p></div></div><div className="model-stats"><div><small>ورودی</small><b>بردار TF–IDF</b></div><div><small>خروجی</small><b>کلاس احساس</b></div><div><small>روش</small><b>{models[selected].tag}</b></div></div></div>;
}

function ResultsScene() {
  const rows = [{name:'Logistic Regression',acc:66.84,f1:79.61},{name:'Linear SVM',acc:66.84,f1:79.61},{name:'Multinomial NB',acc:65.79,f1:78.69}];
  return <div className="results-scene"><div className="result-warning"><span>!</span><p>اعداد زیر از فایل مقایسه موجود در مخزن خوانده شده‌اند و باید با ارزیابی یکسان دوباره اعتبارسنجی شوند.</p></div><div className="metric-cards"><div><small>Accuracy</small><b>۶۶.۸٪</b><span>درصد پیش‌بینی درست</span></div><div><small>F1-score</small><b>۷۹.۶٪</b><span>میانگین دقت و بازیابی کلاس مثبت</span></div></div><div className="compare-list">{rows.map(r=><div className="compare-row" key={r.name}><div><b>{r.name}</b><span>{r.acc.toFixed(2)}%</span></div><div className="compare-track"><i style={{width:`${r.acc}%`}}/></div></div>)}</div><div className="result-foot">منبع: <code>models/model_comparison.csv</code></div></div>;
}

function PlaygroundScene({ prediction, textValue, setTextValue, model, setModel, maxFeatures, setMaxFeatures, testSize, setTestSize, ngram, setNgram, onPredict }) {
  return <div className="playground-scene"><div className="play-head"><span className="play-pulse"/> LIVE PLAYGROUND <span>تنظیمات قابل تغییر</span></div><label className="field-label" htmlFor="model-select">مدل یادگیری ماشین</label><select id="model-select" value={model} onChange={e=>setModel(e.target.value)}>{Object.entries(models).map(([key,v])=><option key={key} value={key}>{v.title}{key==='RandomForest'?' · آزمایشی':''}</option>)}</select><div className="range-line"><label htmlFor="features-range">تعداد ویژگی‌های TF–IDF</label><b>{Number(maxFeatures).toLocaleString('fa-IR')}</b></div><input id="features-range" type="range" min="1000" max="12000" step="500" value={maxFeatures} onChange={e=>setMaxFeatures(Number(e.target.value))}/><div className="range-line"><label htmlFor="test-range">سهم داده آزمون</label><b>{testSize}٪</b></div><input id="test-range" type="range" min="10" max="35" step="5" value={testSize} onChange={e=>setTestSize(Number(e.target.value))}/><label className="field-label" htmlFor="ngram-select">محدوده واژه‌ها (N-gram)</label><select id="ngram-select" value={ngram} onChange={e=>setNgram(e.target.value)}><option value="1">Unigram (تک‌واژه)</option><option value="2">Unigram + Bigram</option><option value="3">تا Trigram</option></select><div className="play-divider"/><label className="field-label" htmlFor="review-input">یک نظر بنویسید و احساس آن را پیش‌بینی کنید</label><textarea id="review-input" value={textValue} onChange={e=>setTextValue(e.target.value)} maxLength={240} placeholder="مثلاً: کیفیت محصول عالی بود و از خریدم خیلی راضی هستم..."/><button className="predict-button" onClick={onPredict}><Icon name="spark" size={17}/> تحلیل این دیدگاه <Icon name="arrow" size={16}/></button>{prediction&&<div className={`prediction-result ${prediction.sentiment==='مثبت'?'pred-positive':'pred-negative'}`}><div className="prediction-top"><span>{prediction.sentiment==='مثبت'?'احساس مثبت':'احساس منفی'}</span><b>{prediction.confidence}٪</b></div><div className="prediction-meter"><i style={{width:`${prediction.confidence}%`}}/></div><p>{prediction.reason}</p><small>خروجی نمایشی رابط · مدل واقعی هنوز به API متصل نشده است</small></div>}<div className="demo-disclaimer">این محیط برای نمایش تعاملات رابط ساخته شده است. تغییر تنظیمات فعلاً در پیش‌بینی شبیه‌سازی‌شده اثر می‌گذارد.</div></div>;
}

export default function Home() {
  const [active, setActive] = useState('scraping');
  const [model, setModel] = useState('Logistic Regression');
  const [sceneModel, setSceneModel] = useState('Logistic Regression');
  const [maxFeatures, setMaxFeatures] = useState(5000);
  const [testSize, setTestSize] = useState(20);
  const [ngram, setNgram] = useState('2');
  const [textValue, setTextValue] = useState('کیفیت این محصول عالی بود و از خریدم خیلی راضی هستم.');
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const nodes = document.querySelectorAll('[data-chapter]');
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if (visible) setActive(visible.target.dataset.chapter);
    }, { rootMargin: '-22% 0px -48% 0px', threshold: [0.05,0.2,0.45] });
    nodes.forEach(node=>observer.observe(node));
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (prediction) {
      setPrediction(predictDemoSentiment({ text: textValue, model, maxFeatures, testSize, ngram }));
    }
  }, [model, maxFeatures, testSize, ngram, textValue]);

  function predict() {
    setPrediction(predictDemoSentiment({ text: textValue, model, maxFeatures, testSize, ngram }));
  }

  const activeIndex = chapters.findIndex(c=>c.id===active);
  return <main>
    <header className="site-header"><a className="brand" href="#top"><span className="brand-mark"><Icon name="spark" size={19}/></span><span>sentiment<span className="brand-light">lab</span><small>REVIEW INTELLIGENCE</small></span></a><nav className="top-nav"><a href="#scraping">مسیر پروژه</a><a href="#results">نتایج</a><a href="#playground">آزمایشگاه</a></nav><a className="header-cta" href="#playground">امتحانش کن <Icon name="arrow" size={15}/></a></header>

    <section className="hero" id="top"><div className="hero-grid"/><div className="hero-content"><div className="hero-pill"><span/> یک سفر از داده تا درک احساس</div><h1>هر نظر، یک داستان.<br/><span>ما احساسش را پیدا می‌کنیم.</span></h1><p>از دل هزاران دیدگاه پراکنده، الگوهای پنهان را بیرون می‌کشیم؛ با وب‌اسکرپینگ، پردازش زبان طبیعی و یادگیری ماشین.</p><div className="hero-actions"><a href="#scraping" className="primary-link">شروع سفر <Icon name="arrow" size={17}/></a><a href="#playground" className="secondary-link"><Icon name="play" size={15}/> تست زنده مدل</a></div><div className="hero-proof"><div className="proof-avatars"><i>ب</i><i>ط</i><i>T</i></div><span>۳ منبع داده</span><b/> <span>۶ مرحله پردازش</span><b/> <span>یک تصمیم هوشمند</span></div></div><div className="hero-art"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="hero-core"><div className="core-face"><Icon name="spark" size={46}/></div><span>AI</span></div><div className="orbit-node node-one"><Icon name="globe"/></div><div className="orbit-node node-two"><Icon name="code"/></div><div className="orbit-node node-three"><Icon name="chart"/></div><div className="orbit-node node-four">♥</div><div className="floating-word word-one">احساس مثبت</div><div className="floating-word word-two">تحلیل متن</div><div className="floating-word word-three">داده واقعی</div></div><a className="scroll-cue" href="#scraping"><Icon name="mouse" size={17}/> برای کشف مراحل اسکرول کنید <Icon name="chevron" size={16}/></a></section>

    <section className="intro-strip"><div><span className="strip-number">۰۱ / ۰۷</span><b>از صفحه وب شروع می‌کنیم</b><small>هر مرحله، یک قطعه از پازل تحلیل احساسات</small></div><div className="strip-stat"><b>۳</b><span>منبع استخراج</span></div><div className="strip-stat"><b>۲</b><span>کلاس احساس</span></div><div className="strip-stat"><b>∞</b><span>دیدگاه قابل بررسی</span></div></section>

    <div className="story-layout"><aside className="story-nav"><div className="nav-caption">نقشه مسیر</div><div className="nav-progress"><i style={{height:`${((activeIndex+1)/chapters.length)*100}%`}}/></div>{chapters.map(c=><a key={c.id} href={`#${c.id}`} className={active===c.id?'active':''}><span>{c.number}</span><div><b>{c.title}</b><small>{c.short}</small></div></a>)}<div className="nav-bottom"><span className="nav-live"/> در حال پیمایش مسیر</div></aside>

      <div className="chapters">
        <section className="chapter" id="scraping" data-chapter="scraping"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 01 · WEB SCRAPING" title={<>اول، گوش می‌دهیم.<br/><span>از دل وب.</span></>}>نظر کاربران در صفحه‌های مختلف پراکنده است. خزنده ما صفحه محصول یا کتاب را باز می‌کند، بخش دیدگاه‌ها را پیدا می‌کند و اطلاعات هر نظر را به شکل ساختاریافته بیرون می‌کشد.</SectionHeading><div className="mini-points"><div><span className="point-icon purple"><Icon name="globe"/></span><div><b>تشخیص منبع</b><small>باسلام، طاقچه و Trustpilot</small></div></div><div><span className="point-icon blue"><Icon name="code"/></span><div><b>پیمایش و استخراج</b><small>صفحه‌بندی، متن نظر و امتیاز</small></div></div><div><span className="point-icon green"><Icon name="check"/></span><div><b>خروجی ساختاریافته</b><small>داده خام برای مراحل بعدی</small></div></div></div><div className="chapter-foot"><span>ابزارهای این مرحله</span><b>Python</b><b>Selenium</b><b>BeautifulSoup</b></div></div><div className="chapter-visual"><div className="visual-label"><span>THE COLLECTOR</span><b>01 — 07</b></div><BrowserScene/><div className="visual-caption"><span>از صفحه وب تا ردیف‌های داده</span><b>SCROLL TO EXPLORE ↓</b></div></div></section>

        <section className="chapter" id="labeling" data-chapter="labeling"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 02 · DATASET" title={<>هر ستاره،<br/><span>یک نشانه است.</span></>}>متن به‌تنهایی برای آموزش کافی نیست. امتیاز ثبت‌شده کنار هر نظر، یک برچسب اولیه در اختیار ما می‌گذارد. با این برچسب‌ها نمونه‌های مثبت و منفی را می‌سازیم تا مدل رابطه میان واژه‌ها و احساس را یاد بگیرد.</SectionHeading><div className="label-rules"><div><span className="rule-stars positive-stars">★★★★★</span><div><b>۴ و ۵ ستاره</b><small>احساس مثبت · کلاس ۱</small></div></div><div><span className="rule-stars negative-stars">★☆☆☆☆</span><div><b>۱ و ۲ ستاره</b><small>احساس منفی · کلاس ۰</small></div></div></div><p className="subtle-note">امتیاز ۳ ستاره می‌تواند خنثی یا مبهم باشد؛ سیاست برچسب‌گذاری باید در هر مجموعه‌داده مشخص شود.</p><div className="chapter-foot"><span>ساختار هر نمونه</span><b>متن دیدگاه</b><b>امتیاز</b><b>برچسب احساس</b></div></div><div className="chapter-visual"><div className="visual-label"><span>FROM STARS TO LABELS</span><b>02 — 07</b></div><LabelScene/><div className="visual-caption"><span>داده خام حالا قابل یادگیری است</span><b>LABELING ENGINE</b></div></div></section>

        <section className="chapter" id="nlp" data-chapter="nlp"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 03 · NLP PIPELINE" title={<>قبل از فهمیدن،<br/><span>باید مرتب کنیم.</span></>}>زبان طبیعی پر از شکل‌های نوشتاری متفاوت، فاصله‌ها، نشانه‌ها و واژه‌های پرتکرار است. در مسیر NLP متن را نرمال‌سازی و پاک‌سازی می‌کنیم، سپس آن را به توکن‌های کوچک‌تر می‌شکنیم تا برای ماشین قابل پردازش شود.</SectionHeading><div className="pipeline-list"><div><b>۰۱</b><span>Normalization</span><small>یکسان‌سازی شکل حروف و نیم‌فاصله</small></div><div><b>۰۲</b><span>Cleaning</span><small>حذف علائم، اعداد و نویز متنی</small></div><div><b>۰۳</b><span>Tokenization</span><small>تقسیم جمله به واژه‌های مستقل</small></div><div><b>۰۴</b><span>Stop words</span><small>حذف واژه‌های پرتکرار کم‌اثر</small></div></div><div className="chapter-foot"><span>ابزار پردازش فارسی</span><b>Hazm</b><b>Regex</b><b>Python</b></div></div><div className="chapter-visual"><div className="visual-label"><span>TEXT UNDER THE MICROSCOPE</span><b>03 — 07</b></div><NLPScene/><div className="visual-caption"><span>از جمله طبیعی تا توکن‌های تمیز</span><b>NLP PIPELINE</b></div></div></section>

        <section className="chapter" id="vectors" data-chapter="vectors"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 04 · FEATURE ENGINEERING" title={<>ماشین کلمه نمی‌خواند؛<br/><span>عدد می‌بیند.</span></>}>مدل‌های کلاسیک با متن خام کار نمی‌کنند. TF–IDF هر دیدگاه را به یک بردار عددی تبدیل می‌کند. وزن هر واژه به حضور آن در یک متن و کمیاب بودنش در کل مجموعه وابسته است؛ n-gramها هم ترکیب واژه‌های کنار هم را وارد ویژگی‌ها می‌کنند.</SectionHeading><div className="formula-card"><span>TF–IDF</span><p>وزن واژه = فراوانی در متن × اهمیت معکوس در مجموعه</p><small>واژه پرتکرار در یک نظر، اما کمیاب در کل داده، وزن بیشتری می‌گیرد.</small></div><div className="chapter-foot"><span>تنظیمات نمونه</span><b>max_features = 10k</b><b>ngram = (1, 2)</b></div></div><div className="chapter-visual"><div className="visual-label"><span>WORDS → NUMBERS</span><b>04 — 07</b></div><VectorScene/><div className="visual-caption"><span>هر دیدگاه، یک بردار ویژگی</span><b>TF–IDF SPACE</b></div></div></section>

        <section className="chapter" id="models" data-chapter="models"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 05 · MACHINE LEARNING" title={<>سه ذهن متفاوت،<br/><span>یک مسئله مشترک.</span></>}>حالا بردارهای عددی وارد مدل می‌شوند. هر الگوریتم از زاویه‌ای متفاوت الگوها را یاد می‌گیرد. مدل با نمونه‌های برچسب‌دار آموزش می‌بیند و برای دیدگاه تازه، کلاس محتمل را پیش‌بینی می‌کند.</SectionHeading><div className="model-bullets"><div><b>Naive Bayes</b><small>احتمال واژه‌ها در هر کلاس</small></div><div><b>Logistic Regression</b><small>یادگیری مرز تصمیم خطی</small></div><div><b>Linear SVM</b><small>بیشینه‌کردن فاصله دو کلاس</small></div></div><p className="subtle-note">Random Forest در آزمایش‌های ثبت‌شده فعلی حضور ندارد؛ در آزمایشگاه انتهایی به‌عنوان گزینه توسعه آینده قابل انتخاب است.</p><div className="chapter-foot"><span>الگوریتم‌های موجود در مخزن</span><b>scikit-learn</b><b>SMOTE در آزمایش‌ها</b></div></div><div className="chapter-visual"><div className="visual-label"><span>INSIDE THE MODEL</span><b>05 — 07</b></div><ModelScene selected={sceneModel} onSelect={setSceneModel}/><div className="visual-caption"><span>مدل را انتخاب کن و مرز تصمیم را ببین</span><b>MODEL LAB</b></div></div></section>

        <section className="chapter" id="results" data-chapter="results"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 06 · EVALUATION" title={<>یادگیری تمام شد؛<br/><span>حالا وقت سنجش است.</span></>}>مدل خوب فقط مدلی نیست که روی داده آموزشی جواب بدهد. عملکرد را با داده کنارگذاشته‌شده می‌سنجیم و Accuracy، Precision، Recall و F1 را کنار هم می‌گذاریم تا نقاط قوت و ضعف هر مدل روشن شود.</SectionHeading><div className="metric-explain"><div><b>Accuracy</b><small>چه سهمی از کل پیش‌بینی‌ها درست بوده؟</small></div><div><b>Precision</b><small>از مثبت‌های پیش‌بینی‌شده چندتا واقعاً مثبت‌اند؟</small></div><div><b>Recall</b><small>چند درصد مثبت‌های واقعی را پیدا کردیم؟</small></div><div><b>F1</b><small>تعادل Precision و Recall چقدر است؟</small></div></div><p className="subtle-note">ارقام فعلی از خروجی تاریخی آزمایش باسلام آمده‌اند؛ پیش از تصمیم نهایی باید روش ارزیابی و داده آزمون یکسان‌سازی شوند.</p><div className="chapter-foot"><span>خروجی‌های ارزیابی</span><b>Confusion Matrix</b><b>Classification Report</b></div></div><div className="chapter-visual"><div className="visual-label"><span>MODEL SCORECARD</span><b>06 — 07</b></div><ResultsScene/><div className="visual-caption"><span>اعداد، داستان عملکرد مدل را می‌گویند</span><b>EVALUATION</b></div></div></section>

        <section className="chapter playground-chapter" id="playground" data-chapter="playground"><div className="chapter-copy"><SectionHeading eyebrow="STAGE 07 · YOUR TURN" title={<>حالا نوبت شماست.<br/><span>مدل را به چالش بکش.</span></>}>یک نظر بنویس، مدل را انتخاب کن و تنظیمات را تغییر بده. نتیجه را همان لحظه ببین و بررسی کن که انتخاب الگوریتم و ویژگی‌ها چطور مسیر تصمیم را تغییر می‌دهند.</SectionHeading><div className="play-features"><div><Icon name="sliders"/><span>تنظیم ویژگی‌ها و سهم آزمون</span></div><div><Icon name="layers"/><span>مقایسه الگوریتم‌های مختلف</span></div><div><Icon name="spark"/><span>تحلیل متن دلخواه</span></div></div><div className="final-statement">از داده‌های پراکنده،<br/><b>به تصمیمی قابل توضیح.</b></div></div><div className="chapter-visual playground-visual"><div className="visual-label"><span>INTERACTIVE EXPERIMENT</span><b>07 — 07</b></div><PlaygroundScene prediction={prediction} textValue={textValue} setTextValue={setTextValue} model={model} setModel={setModel} maxFeatures={maxFeatures} setMaxFeatures={setMaxFeatures} testSize={testSize} setTestSize={setTestSize} ngram={ngram} setNgram={setNgram} onPredict={predict}/><div className="visual-caption"><span>آزمایشگاه تعاملی تحلیل احساسات</span><b>YOUR PLAYGROUND</b></div></div></section>
      </div>
    </div>

    <footer className="site-footer"><div className="footer-brand"><span className="brand-mark"><Icon name="spark" size={19}/></span><b>sentiment<span>lab</span></b></div><p>هر دیدگاه، سرنخی برای شناخت بهتر تجربه کاربران است.</p><div className="footer-meta"><span>Sentiment Analysis Reviews</span><span>Built with curiosity & data</span><a href="#top">بازگشت به بالا ↑</a></div></footer>
  </main>;
}
