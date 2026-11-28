/* 脆自動助手 前端 */
const svg = (d, extra = '') => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ${extra}>${d}</svg>`;
const I = {
  home: svg('<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'),
  user: svg('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
  users: svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>'),
  spark: svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>'),
  cal: svg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>'),
  radar: svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="1"/>'),
  chat: svg('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-5A8 8 0 1 1 21 12Z"/>'),
  gear: svg('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>'),
  plus: svg('<path d="M12 5v14M5 12h14"/>'),
  trash: svg('<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>'),
  edit: svg('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4Z"/>'),
  play: svg('<path d="M6 4l14 8-14 8z"/>'),
  send: svg('<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7Z"/>'),
  globe: svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
  check: svg('<path d="M20 6 9 17l-5-5"/>'),
  x: svg('<path d="M18 6 6 18M6 6l12 12"/>'),
  refresh: svg('<path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5M3 21v-5h5"/>'),
  image: svg('<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>'),
  wand: svg('<path d="m15 4 5 5L9 20H4v-5z"/><path d="M13 6l5 5"/>'),
  clock: svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
  heart: svg('<path d="M19.5 12.6 12 20l-7.5-7.4A5 5 0 1 1 12 6a5 5 0 1 1 7.5 6.6Z"/>'),
  alert: svg('<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/>'),
  info: svg('<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>'),
  list: svg('<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'),
  link: svg('<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'),
  corner: svg('<path d="M15 10l5 5-5 5"/><path d="M4 4v7a4 4 0 0 0 4 4h12"/>'),
  power: svg('<path d="M12 2v10"/><path d="M18.4 6.6a9 9 0 1 1-12.8 0"/>'),
  shield: svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>'),
};

const S = {
  view: 'home', state: {}, accounts: [], logs: [], lastLog: 0,
  commentTab: 'sent', postTab: 'scheduled', histTab: 'sent', histSrc: 'all', images: [], editing: false,
};
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const short = t => (t || '').slice(5, 16);

async function api(method, url, body) {
  const r = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  let data = null;
  try { data = await r.json(); } catch { }
  if (!r.ok) throw new Error((data && data.detail) || `錯誤 ${r.status}`);
  return data;
}

function toast(msg, err = false) {
  const t = document.createElement('div');
  t.className = 'toast' + (err ? ' err' : '');
  t.innerHTML = (err ? I.alert : I.check) + `<span>${esc(msg)}</span>`;
  $('#toasts').appendChild(t);
  setTimeout(() => t.remove(), err ? 6000 : 3000);
}

async function busy(btn, fn) {
  btn && btn.classList.add('loading');
  try { return await fn(); }
  catch (e) { toast(e.message, true); }
  finally { btn && btn.classList.remove('loading'); }
}

function modal(html) {
  $('#modal').innerHTML = html;
  $('#modalBack').classList.add('show');
  S.editing = true;
}
/* 刪除前的二次確認視窗 */
function confirmDelete(title, msgHtml, onOk) {
  modal(`<h2>${title}</h2><div class="muted">${msgHtml}</div>
    <div class="row end" style="margin-top:18px"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn danger" id="delOk">${I.trash}確定刪除</button></div>`);
  $('#delOk').onclick = e => busy(e.currentTarget, async () => { await onOk(); closeModal(); });
}
function closeModal() { $('#modalBack').classList.remove('show'); S.editing = false; }
$('#modalBack').addEventListener('mousedown', e => { if (e.target.id === 'modalBack') closeModal(); });

const accountOptions = (sel) => S.accounts.map(a => `<option value="${a.id}" ${a.id == sel ? 'selected' : ''}>${esc(a.name)}${a.username ? ' @' + esc(a.username) : ''}</option>`).join('');
const needAccount = () => S.accounts.length ? '' : `<div class="notice">${I.alert}<div>還沒有帳號。請先到「帳號」頁新增並登入 Threads。</div></div>`;
const emptyBox = (icon, title, sub) => `<div class="empty">${icon}<b>${title}</b>${sub || ''}</div>`;
/* 圖片選擇器：縮圖 + 加入按鈕，最多 max 張 */
async function uploadFiles(files) {
  const out = [];
  for (const f of files) {
    const data = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(f); });
    try { out.push((await api('POST', '/api/upload', { name: f.name, data })).path); } catch (e) { toast(e.message, true); }
  }
  return out;
}
const isVideo = p => /\.(mp4|mov|webm)$/i.test(p);
function imagePicker(el, list, max = 5) {
  el._imgs = (list || []).slice(0, max);
  const draw = () => {
    el.innerHTML = `<div class="thumbs">${el._imgs.map((p, i) => `<div class="thumb">${isVideo(p) ? `<div style="display:grid;place-items:center;height:100%">${I.play}</div>` : `<img src="/api/file?path=${encodeURIComponent(p)}">`}<button type="button" data-rm="${i}" title="移除">${I.x}</button></div>`).join('')}
      ${el._imgs.length < max ? `<label class="add-thumb" title="加入圖片">${I.plus}<span>${el._imgs.length}/${max}</span><input type="file" accept="image/*,video/mp4,video/quicktime,video/webm" multiple hidden></label>` : ''}</div>`;
    el.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => { el._imgs.splice(+b.dataset.rm, 1); draw(); });
    const inp = el.querySelector('input[type=file]');
    if (inp) inp.onchange = async () => {
      const files = [...inp.files].slice(0, max - el._imgs.length);
      if (inp.files.length > files.length) toast(`最多 ${max} 張，多的已略過`, true);
      el._imgs.push(...await uploadFiles(files)); draw();
    };
  };
  draw();
  return () => el._imgs.slice();
}
const parseImgs = v => { try { return JSON.parse(v || '[]'); } catch { return []; } };

/* 頻率提醒：不限制數值，只在超過建議值時提醒 */
const LIMITS = {
  post: { safe: 5, high: 15, unit: '篇／天', tip: '每天發太多篇，容易被判定為洗版而降低觸及或限制帳號' },
  comment: { safe: 6, high: 15, unit: '則／小時', tip: '留言太密集，容易被 Threads 判定為機器人而限制或停權' },
};
function limitWarnHtml(kind, value) {
  const L = LIMITS[kind], v = +value || 0;
  if (v <= L.safe) return '';
  const strong = v > L.high;
  return `<div class="notice ${strong ? '' : 'soft'}">${I.alert}<div>${strong ? '頻率非常高' : '超過建議值'}（建議 ${L.safe} ${L.unit}以內）：${L.tip}。${strong ? '請確認帳號能承受，建議先用小號測試。' : ''}</div></div>`;
}
function bindLimitWarn(input, box, kind) {
  const draw = () => { box.innerHTML = limitWarnHtml(kind, input.value); };
  input.addEventListener('input', draw); draw();
}
const hourOpts = (sel, from, to) => Array.from({ length: to - from + 1 }, (_, i) => i + from).map(h => `<option value="${h}" ${h == sel ? 'selected' : ''}>${String(h).padStart(2, '0')}:00</option>`).join('');

/* ---------------- 頁面 ---------------- */
const VIEWS = {
  home: { title: '總覽', sub: '自動化執行狀況一覽', icon: I.home },
  accounts: { title: '帳號', sub: '每個帳號使用獨立的瀏覽器，登入一次就會記住', icon: I.users },
  autopost: { title: '自動發文', sub: 'AI 依主題寫文，每天在指定時段隨機發出', icon: I.spark },
  posts: { title: '手動排程', sub: '自己寫或請 AI 幫寫，排定時間發出', icon: I.cal },
  patrol: { title: '自動海巡', sub: '搜尋關鍵字，AI 寫留言後自動送出', icon: I.radar },
  history: { title: '發文紀錄', sub: '自動發文與手動排程的所有貼文與發佈結果', icon: I.list },
  comments: { title: '留言紀錄', sub: '海巡產生的留言與送出結果', icon: I.chat },
  settings: { title: '設定', sub: 'AI 金鑰、帳號定位與頻率限制', icon: I.gear },
};

function renderNav() {
  const st = S.state;
  const badges = { comments: st.pending_comments || st.queued || 0, posts: st.pending_posts || st.scheduled || 0, history: st.pending_posts || 0 };
  $('#nav').innerHTML = Object.entries(VIEWS).map(([k, v]) =>
    `<button class="nav-item ${S.view === k ? 'active' : ''}" data-go="${k}">${v.icon}<span>${v.title}</span>${badges[k] ? `<span class="badge">${badges[k]}</span>` : ''}</button>`).join('');
  const on = st.running;
  const t = $('#runToggle');
  t.className = 'run-toggle' + (on ? ' on' : '');
  t.innerHTML = `<span class="dot"></span><span class="lbl">${on ? '自動執行中' : '已暫停'}</span><span class="sub">${on ? '點擊暫停' : '點擊啟動'}</span>`;
  if (st.version) $('#ver').textContent = 'v' + st.version;
  $('#busy').innerHTML = st.busy ? `<span class="spin"></span>${esc(st.busy)}…` : '';
  $('#busy').title = st.activity && st.activity.label ? `${st.activity.detail}
${st.activity.step || ''}` : '';
}

document.addEventListener('click', e => {
  const g = e.target.closest('[data-go]');
  if (g) go(g.dataset.go);
});
$('#runToggle').onclick = async () => { await api('POST', '/api/worker/toggle'); await refreshState(); };

async function go(v) {
  S.view = v;
  S.editing = false;
  $('#pageTitle').textContent = VIEWS[v].title;
  $('#pageSub').textContent = VIEWS[v].sub;
  $('#topActions').innerHTML = '';
  renderNav();
  await render();
}

async function render() {
  S.accounts = await api('GET', '/api/accounts');
  await R[S.view]();
}

const R = {};

/* ---- 總覽 ---- */
R.home = async () => {
  const st = S.state;
  const autopost = await api('GET', '/api/autopost');
  const tasks = await api('GET', '/api/tasks');
  const settings = await api('GET', '/api/settings');
  const steps = [
    [settings.ai_tested === '1', '設定 AI 寫手', 'Claude 或 ChatGPT，可用訂閱登入', 'settings'],
    [S.accounts.some(a => a.logged_in), '新增帳號並登入 Threads', '在專屬瀏覽器登入一次即可', 'accounts'],
    [autopost.some(a => a.enabled), '開啟自動發文', '填主題、每天篇數、發文時段', 'autopost'],
    [tasks.some(t => t.enabled), '建立海巡任務', '設定關鍵字，自動找文留言', 'patrol'],
  ];
  $('#view').innerHTML = `
  <div class="card now-card" id="nowCard"></div>
  <div class="grid g4" style="margin-top:16px">
    ${stat(I.send, '今日發文', st.posted_today, `${st.autopost || 0} 個帳號開啟自動發文`)}
    ${stat(I.cal, '排程中貼文', st.scheduled, '到時間會自動發出')}
    ${stat(I.chat, '今日留言', st.commented_today, `每帳號每小時上限 ${st.hourly_limit} 則`)}
    ${stat(I.list, '留言佇列', st.queued, `${st.tasks || 0} 個海巡任務執行中`)}
  </div>
  <div class="grid" style="grid-template-columns: 360px 1fr; margin-top:16px; align-items:start">
    <div class="card">
      <div class="card-h"><h3>${I.check}開始使用</h3><span class="faint">${steps.filter(s => s[0]).length} / 4</span></div>
      <div class="steps">${steps.map((s, i) => `
        <div class="step ${s[0] ? 'done' : ''}">
          <div class="n">${s[0] ? I.check : i + 1}</div>
          <div class="body"><b>${s[1]}</b><span>${s[2]}</span></div>
          ${s[0] ? '' : `<button class="btn sm" data-go="${s[3]}">前往</button>`}
        </div>`).join('')}
      </div>
    </div>
    <div class="card">
      <div class="card-h"><h3>${I.list}執行紀錄</h3><span class="faint">即時更新</span></div>
      <div class="logs" id="logs"></div>
    </div>
  </div>`;
  drawLogs();
  drawNow();
};
const stat = (icon, k, v, s) => `<div class="card stat"><div class="k">${icon}${k}</div><div class="v">${v ?? 0}</div><div class="s">${s}</div></div>`;

/* ---- 總覽：目前狀態 + 接下來 ---- */
const dur = sec => sec < 60 ? `${sec} 秒` : sec < 3600 ? `${Math.floor(sec / 60)} 分 ${sec % 60} 秒` : `${Math.floor(sec / 3600)} 小時 ${Math.floor(sec % 3600 / 60)} 分`;
const until = sec => sec <= 30 ? '馬上' : sec < 3600 ? `${Math.round(sec / 60)} 分鐘後` : sec < 86400 ? `${Math.floor(sec / 3600)} 小時 ${Math.round(sec % 3600 / 60)} 分後` : '明天';
const KIND_PILL = { '自動發文': 'info', '發文': 'info', '海巡': 'warn', '留言': 'ok' };
function drawNow() {
  const el = $('#nowCard');
  if (!el) return;
  const st = S.state, a = st.activity || {}, up = st.upcoming || [];
  S.nowBase = { at: Date.now(), elapsed: a.elapsed || 0 };
  let head;
  if (!st.running) {
    head = `<div class="now-main paused"><span class="now-dot"></span><div><b>已暫停</b><span>自動工作都停下來了，按左下角「點擊啟動」繼續</span></div></div>`;
  } else if (a.label) {
    head = `<div class="now-main busy"><span class="now-spin"></span><div>
      <b>${esc(a.label)}<span class="now-time" id="nowElapsed">已進行 ${dur(a.elapsed || 0)}</span></b>
      <span>${esc(a.detail)}</span>
      ${a.step ? `<span class="now-step">${I.corner}${esc(a.step)}</span>` : ''}</div></div>`;
  } else {
    const n = up[0];
    head = `<div class="now-main idle"><span class="now-dot"></span><div><b>待命中</b>
      <span>${n ? `下一件事：${until(n.in)}（${n.at.slice(11, 16)}）${esc(n.kind)} · ${esc(n.text)}` : '目前沒有排定的工作，到「自動發文」或「自動海巡」建立規則'}</span></div></div>`;
  }
  el.innerHTML = `<div class="card-h"><h3>${I.radar}目前狀態</h3><span class="faint">每 3 秒更新</span></div>
    <div class="now-grid">${head}
      <div class="now-next"><div class="now-sub">接下來</div>
        ${up.length ? up.map(u => `<div class="now-row"><span class="t">${u.at.slice(11, 16)}</span><span class="pill ${KIND_PILL[u.kind] || 'plain'}">${esc(u.kind)}</span><span class="m">${esc(u.text)}</span><span class="r">${until(u.in)}</span></div>`).join('')
          : '<div class="faint" style="padding:6px 0">沒有排定的工作</div>'}
      </div></div>`;
}
setInterval(() => {
  const el = $('#nowElapsed');
  if (el && S.nowBase) el.textContent = '已進行 ' + dur(S.nowBase.elapsed + Math.floor((Date.now() - S.nowBase.at) / 1000));
}, 1000);

function drawLogs() {
  const el = $('#logs');
  if (!el) return;
  const stick = el.scrollHeight - el.scrollTop - el.clientHeight < 40;
  el.innerHTML = S.logs.length ? S.logs.map(l => `<div class="log ${l.level}"><span class="t">${l.ts.slice(11, 19)}</span><span class="m">${esc(l.msg)}</span></div>`).join('')
    : emptyBox(I.list, '還沒有紀錄', '');
  if (stick) el.scrollTop = el.scrollHeight;
}

/* ---- 帳號 ---- */
R.accounts = async () => {
  $('#topActions').innerHTML = `<button class="btn accent" id="addAcc">${I.plus}新增帳號</button>`;
  $('#addAcc').onclick = () => accountModal();
  $('#view').innerHTML = `
  <div class="notice info" style="margin-bottom:16px">${I.info}<div>
    新增帳號後按「開啟瀏覽器登入」，在跳出的 Chrome 視窗登入 Threads，登入完回來按「檢查登入」。<br>
    之後自動發文、海巡都會用這個瀏覽器執行，執行時視窗請不要關閉，也不要手動操作它。</div></div>
  ${S.accounts.length ? `<div class="grid g3">${S.accounts.map(accCard).join('')}</div>` :
      `<div class="card">${emptyBox(I.users, '還沒有帳號', '按右上角「新增帳號」開始')}</div>`}`;
  $('#view').querySelectorAll('[data-act]').forEach(b => b.onclick = () => accAction(b, b.dataset.act, +b.dataset.id));
};

function accCard(a) {
  const status = a.checked_at ? (a.logged_in ? '<span class="pill ok">已登入</span>' : '<span class="pill err">未登入</span>') : '<span class="pill">尚未檢查</span>';
  return `<div class="card acc">
    <div class="acc-top">
      <div class="avatar">${esc((a.name || '?').slice(0, 1))}</div>
      <div style="flex:1;min-width:0">
        <div class="acc-name">${esc(a.name)}</div>
        <div class="acc-user">${a.username ? '@' + esc(a.username) : '尚未取得帳號名稱'}</div>
      </div>
      <button class="btn ghost icon sm" title="改名" data-act="rename" data-id="${a.id}">${I.edit}</button>
      <button class="btn ghost icon sm danger" title="刪除" data-act="del" data-id="${a.id}">${I.trash}</button>
    </div>
    <div class="row">${status}${a.browser_open ? '<span class="pill info">瀏覽器開啟中</span>' : ''}</div>
    <div class="row">
      <button class="btn sm primary" data-act="open" data-id="${a.id}">${I.globe}開啟瀏覽器登入</button>
      <button class="btn sm" data-act="check" data-id="${a.id}">${I.refresh}檢查登入</button>
    </div>
    ${a.browser_open ? `<button class="btn sm ghost" data-act="close" data-id="${a.id}">${I.power}關閉瀏覽器</button>` : ''}
  </div>`;
}

function accountModal(a) {
  modal(`<h2>${a ? '帳號改名' : '新增帳號'}</h2>
    <div class="stack">
      <div class="field"><label>顯示名稱</label><input class="input" id="accName" value="${esc(a?.name || '')}" placeholder="例如：洗車店主帳"></div>
      <div class="row end"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn accent" id="accSave">${I.check}儲存</button></div>
    </div>`);
  $('#accName').focus();
  $('#accSave').onclick = e => busy(e.currentTarget, async () => {
    const name = $('#accName').value.trim();
    if (a) await api('PUT', `/api/accounts/${a.id}`, { name });
    else await api('POST', '/api/accounts', { name });
    closeModal(); render();
  });
}

async function accAction(btn, act, id) {
  const a = S.accounts.find(x => x.id === id);
  if (act === 'rename') return accountModal(a);
  if (act === 'del') {
    return modal(`<h2>刪除帳號</h2><p class="muted">確定要刪除「${esc(a.name)}」？此帳號的海巡任務、自動發文規則與未發出的排程會一併刪除，瀏覽器登入資料保留。</p>
      <div class="row end" style="margin-top:18px"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn danger" id="delOk">${I.trash}刪除</button></div>`),
      $('#delOk').onclick = e => busy(e.currentTarget, async () => { await api('DELETE', `/api/accounts/${id}`); closeModal(); render(); });
  }
  await busy(btn, async () => {
    if (act === 'open') { await api('POST', `/api/accounts/${id}/open`); toast('已開啟瀏覽器，登入完成後回來按「檢查登入」'); }
    if (act === 'close') await api('POST', `/api/accounts/${id}/close`);
    if (act === 'check') {
      const r = await api('POST', `/api/accounts/${id}/check`);
      r.logged ? toast('已登入' + (r.username ? ` @${r.username}` : '')) : toast('尚未登入，請在瀏覽器完成登入', true);
    }
    await render();
  });
}

/* ---- 內建風格範本（點一下帶入，可再自行修改） ---- */
const WRITE_PRESETS = [
  ['老闆親自經營', '我是自己開店的老闆，用第一人稱分享每天遇到的客人、工作日常和心得。講話直白、偶爾自嘲，讓人覺得是真人在經營，不硬推銷，最多在結尾輕輕帶一句店裡的服務。'],
  ['專業知識分享', '以這個領域的專業人士身分寫作，把一個實用觀念講清楚：先點出大家常見的誤解，再用白話解釋正確做法。口吻有自信但不說教，避免艱澀術語，結尾可以問大家有沒有遇過。'],
  ['幽默吐槽', '語氣幽默、愛吐槽，像在跟朋友抱怨日常的荒謬小事。可以用誇張比喻和反差製造笑點，但不酸人、不罵特定對象，讓人看了會想留言說「真的」。'],
  ['溫暖療癒', '語氣溫柔、像寫給朋友的小日記，分享生活裡讓人覺得被療癒的瞬間或小感悟。句子短、節奏慢，不灌雞湯、不說教，讓讀的人覺得被理解。'],
  ['懶人包清單', '用條列整理重點，像懶人包一樣好掃讀：一句吸睛開頭，接著 3～5 點具體建議，每點一行。內容要實用、可以馬上照做，結尾邀請大家補充。'],
  ['故事敘事', '用說故事的方式寫：從一個具體場景或對話開頭，有起伏、有轉折，最後帶出一個小心得。細節要真實可信，像真人經歷，不要寫成寓言或廣告。'],
  ['提問互動', '以拋問題為主，讓人很想回答：分享自己的一個選擇或困擾，給出兩三個選項或情境，請大家說說自己的做法或站哪邊。語氣輕鬆，問題要好回答。'],
  ['真心評測', '以消費者的角度分享使用心得，優點缺點都講，口吻誠實中肯，像在跟朋友推薦或避雷。具體說出用了多久、在什麼情況下用，不誇大、不像業配。'],
  ['犀利觀點', '針對一個常見現象提出自己的看法，觀點鮮明但有理有據，敢說出大家心裡想但沒說的話。語氣犀利不失禮貌，避開政治與人身攻擊，結尾問大家同不同意。'],
  ['輕鬆碎念', '像隨手發的動態，短短幾句碎念當下的心情或觀察，口語、隨性、有生活感。不需要完整結論，可以帶一點小幽默，讓人覺得這個帳號很像朋友。'],
];
const PATROL_PRESETS = [
  ['真誠參與討論', '像一般網友真誠地參與討論，針對貼文內容回應自己的想法或類似經驗。語氣自然親切，不推銷、不留連結、不提自己的店或品牌。'],
  ['專業建議', '以這個領域的專業人士角度，針對貼文的問題給一個具體、可以馬上做的建議。口吻友善不說教，不主動推銷，不留連結。'],
  ['同理共鳴', '先對貼文作者的處境或心情表示理解，再分享一點自己的類似經驗。語氣溫暖、像朋友安慰，不給說教式的建議。'],
  ['幽默回應', '用輕鬆幽默的方式回應貼文，可以接梗或自嘲，讓人看了會心一笑。不酸人、不嘲笑作者，貼文在抱怨嚴肅問題時就正經回。'],
  ['經驗分享', '分享一個跟貼文主題相關的親身經驗（具體的時間、情境、結果），讓留言有參考價值。像過來人提醒，不推銷。'],
  ['好奇追問', '針對貼文裡的細節表達好奇，問一個具體、好回答的問題，讓作者想回覆。偶爾附上一句自己的看法，不要每則都只是問句。'],
  ['稱讚鼓勵', '具體指出貼文裡做得好或說得好的地方並給予鼓勵，避免空泛的「好棒」「推」。語氣真誠，不浮誇，不像機器人。'],
  ['補充資訊', '針對貼文內容補充一個對方可能不知道的小知識或注意事項，簡短清楚。語氣謙虛，用「我自己是…」「之前聽過…」這類口吻，不糾正、不說教。'],
  ['在地朋友', '以在地人的身分回應，口吻像住附近的朋友，可以提到在地生活經驗或常見狀況。親切隨和，不推銷特定店家。'],
  ['低調品牌', '以品牌小編的身分自然參與討論，先回應貼文本身提供價值；只有在對方明確求推薦時，才可以輕輕提到自家服務，不留連結、不硬推。'],
];

function presetChips(list) {
  return `<div class="presets">${list.map(([name], i) => `<button type="button" class="preset" data-preset="${i}">${esc(name)}</button>`).join('')}</div>`;
}

function bindPresets(root, list, box) {
  const btns = [...root.querySelectorAll('[data-preset]')];
  const mark = () => btns.forEach(b => b.classList.toggle('on', box.value.trim() === list[+b.dataset.preset][1]));
  btns.forEach(b => b.onclick = () => {
    const [name, text] = list[+b.dataset.preset];
    box.focus(); box.select();
    // 用 insertText 取代，瀏覽器的復原（Ctrl+Z）還能拿回原本的內容
    if (!document.execCommand('insertText', false, text)) box.value = text;
    mark();
    toast(`已套用「${name}」，可以直接修改；按 Ctrl+Z 可復原`);
  });
  box.addEventListener('input', mark);
  mark();
}

/* ---- 自動發文 ---- */
R.autopost = async () => {
  const rules = await api('GET', '/api/autopost');
  $('#view').innerHTML = needAccount() + `<div class="stack">${rules.map(ruleCard).join('')}</div>`;
  rules.forEach(r => {
    const root = $(`#rule-${r.account_id}`);
    root.querySelectorAll('.seg button').forEach(b => b.onclick = () => {
      b.parentElement.querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on');
    });
    bindPresets(root, WRITE_PRESETS, root.querySelector('[name=persona]'));
    bindLimitWarn(root.querySelector('[name=per_day]'), root.querySelector('[data-warn]'), 'post');
    const getImgs = imagePicker(root.querySelector('[data-imgs]'), parseImgs(r.images));
    root.querySelector('[data-save]').onclick = e => busy(e.currentTarget, async () => {
      const v = n => root.querySelector(`[name=${n}]`);
      await api('PUT', `/api/autopost/${r.account_id}`, {
        enabled: v('enabled').checked ? 1 : 0, topics: v('topics').value, persona: v('persona').value,
        per_day: Math.max(1, Math.round(+v('per_day').value) || 1), start_hour: +v('start_hour').value, end_hour: +v('end_hour').value,
        length: root.querySelector('.seg-len .on').dataset.v,
        review: +root.querySelector('.seg-rev .on').dataset.v,
        images: getImgs(),
      });
      toast('已儲存，系統會重新安排下一篇時間');
      R.autopost();
    });
    root.querySelector('[data-test]').onclick = e => busy(e.currentTarget, async () => {
      const topics = root.querySelector('[name=topics]').value.split('\n').map(s => s.trim()).filter(Boolean);
      if (!topics.length) throw new Error('請先填主題');
      const res = await api('POST', '/api/ai/posts', {
        topic: topics[Math.floor(Math.random() * topics.length)], persona: root.querySelector('[name=persona]').value,
        count: 1, length: root.querySelector('.seg-len .on').dataset.v,
      });
      modal(`<h2>AI 試寫結果</h2><div class="quote">${esc(res.items[0] || '')}</div>
        <p class="faint">這只是預覽，不會發出。不滿意可以調整「寫作風格」再試。</p>
        <div class="row end"><button class="btn primary" onclick="closeModal()">好</button></div>`);
    });
  });
};

function ruleCard(r) {
  const next = r.enabled && r.next_at ? `下一篇預計 ${short(r.next_at)}` : '未開啟';
  return `<div class="card" id="rule-${r.account_id}">
    <div class="card-h">
      <h3>${I.spark}${esc(r.account_name)}${r.username ? `<span class="faint">@${esc(r.username)}</span>` : ''}</h3>
      <div class="row">
        <span class="pill ${r.enabled ? 'ok' : ''}">今日已發 ${r.today} / ${r.per_day}</span>
        <span class="faint">${next}</span>
        <label class="switch" title="開啟自動發文"><input type="checkbox" name="enabled" ${r.enabled ? 'checked' : ''}><span></span></label>
      </div>
    </div>
    <div class="grid g2">
      <div class="field"><label>發文主題</label>
        <textarea class="textarea" name="topics" rows="5" placeholder="一行一個，每次隨機挑一個寫&#10;例如：&#10;洗車常見迷思&#10;鍍膜值不值得&#10;客人愛車小故事">${esc(r.topics)}</textarea>
        <span class="hint">每次發文從這裡隨機挑一個主題，AI 會避開最近發過的內容</span></div>
      <div class="field"><label>寫作風格</label>
        ${presetChips(WRITE_PRESETS)}
        <textarea class="textarea" name="persona" rows="5" placeholder="例如：台中洗車店老闆，講話直白幽默，偶爾自嘲，不推銷">${esc(r.persona)}</textarea>
        <span class="hint">點上面的範本直接套用，或自己寫；口吻、身分、禁忌都可以寫在這裡</span></div>
    </div>
    <div class="field" style="margin-top:16px"><label>附加圖片（最多 5 張，每篇自動貼文都會附上）</label><div data-imgs></div></div>
    <div class="row between" style="margin-top:16px;align-items:flex-end">
      <div class="row" style="gap:16px;align-items:flex-end">
        <div class="field"><label>每天發幾篇</label><input class="input" type="number" min="1" name="per_day" value="${r.per_day}" style="width:100px"></div>
        <div class="field"><label>發文時段</label>
          <div class="row" style="gap:6px"><select class="select" name="start_hour" style="width:104px">${hourOpts(r.start_hour, 0, 23)}</select>
          <span class="muted">到</span><select class="select" name="end_hour" style="width:104px">${hourOpts(r.end_hour, 1, 24)}</select></div></div>
        <div class="field"><label>篇幅</label>
          <div class="seg seg-len">${['短', '中', '長'].map(x => `<button data-v="${x}" class="${(r.length || '中') === x ? 'on' : ''}">${x}</button>`).join('')}</div></div>
        <div class="field"><label>發文方式</label>
          <div class="seg seg-rev"><button data-v="0" class="${r.review ? '' : 'on'}">自動發出</button><button data-v="1" class="${r.review ? 'on' : ''}">審核後才發</button></div></div>
      </div>
      <div class="row">
        <button class="btn" data-test>${I.wand}試寫一篇</button>
        <button class="btn accent" data-save>${I.check}儲存</button>
      </div>
    </div>
    <div data-warn style="margin-top:12px"></div>
  </div>`;
}

/* ---- 手動排程 ---- */
R.posts = async () => {
  const posts = await api('GET', '/api/posts');
  const groups = { pending: ['pending'], scheduled: ['scheduled', 'sending'], sent: ['sent'], failed: ['failed'] };
  const cnt = k => posts.filter(p => groups[k].includes(p.status)).length;
  const list = posts.filter(p => groups[S.postTab].includes(p.status));
  const keepText = $('#cText')?.value ?? '';
  const keepAcc = $('#cAcc')?.value;
  $('#view').innerHTML = needAccount() + `
  <div class="split">
    <div class="card">
      <div class="card-h"><h3>${I.edit}寫一篇</h3><button class="btn sm" id="aiHelp">${I.wand}AI 幫我寫</button></div>
      <div class="stack">
        <div class="field"><label>發文帳號</label><select class="select" id="cAcc">${accountOptions(keepAcc)}</select></div>
        <div class="field"><label>內容</label><textarea class="textarea" id="cText" rows="8" placeholder="想說什麼？">${esc(keepText)}</textarea><div class="counter" id="cCount"></div></div>
        <div class="field"><label>圖片／影片</label>
          <div class="thumbs" id="thumbs"></div>
          <label class="drop">${I.image}選擇檔案（最多 10 個）<input type="file" id="cFiles" accept="image/*,video/mp4,video/quicktime,video/webm" multiple hidden></label></div>
        <div class="field"><label>發文時間</label>
          <div class="row"><div class="seg" id="cWhen"><button data-v="now" class="on">立即</button><button data-v="at">指定時間</button></div>
          <input class="input" type="datetime-local" id="cAt" style="width:220px;display:none"></div></div>
        <button class="btn accent block" id="cAdd">${I.send}加入排程</button>
      </div>
    </div>
    <div class="card">
      <div class="tabs">${[['pending', '待審核'], ['scheduled', '排程中'], ['sent', '已發佈'], ['failed', '失敗']].map(([k, l]) =>
        `<button class="${S.postTab === k ? 'on' : ''}" data-tab="${k}">${l}<span class="c">${cnt(k)}</span></button>`).join('')}</div>
      <div class="list">${list.length ? list.map(postItem).join('') : emptyBox(I.cal, '這裡沒有貼文', '')}</div>
    </div>
  </div>`;
  drawThumbs();
  const count = () => { const n = $('#cText').value.length; $('#cCount').textContent = `${n} / 500`; $('#cCount').classList.toggle('over', n > 500); };
  $('#cText').oninput = count; count();
  $('#cWhen').querySelectorAll('button').forEach(b => b.onclick = () => {
    $('#cWhen').querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on');
    $('#cAt').style.display = b.dataset.v === 'at' ? '' : 'none';
    if (b.dataset.v === 'at' && !$('#cAt').value) {
      const d = new Date(Date.now() + 3600e3 - new Date().getTimezoneOffset() * 60e3);
      $('#cAt').value = d.toISOString().slice(0, 16);
    }
  });
  $('#cFiles').onchange = async e => {
    for (const f of [...e.target.files].slice(0, 10 - S.images.length)) {
      const data = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(f); });
      try { const r = await api('POST', '/api/upload', { name: f.name, data }); S.images.push(r.path); } catch (err) { toast(err.message, true); }
    }
    e.target.value = ''; drawThumbs();
  };
  $('#cAdd').onclick = e => busy(e.currentTarget, async () => {
    const text = $('#cText').value.trim();
    if (!text) throw new Error('請輸入內容');
    if (text.length > 500) throw new Error('Threads 單篇上限 500 字');
    if (!$('#cAcc').value) throw new Error('請先新增帳號');
    const at = $('#cWhen .on').dataset.v === 'at' ? $('#cAt').value : null;
    await api('POST', '/api/posts', { account_id: +$('#cAcc').value, items: [{ text, images: S.images, scheduled_at: at }] });
    S.images = []; $('#cText').value = '';
    toast(at ? '已加入排程' : '已加入，馬上發出'); S.postTab = 'scheduled'; R.posts();
  });
  $('#aiHelp').onclick = aiModal;
  $('#view').querySelectorAll('[data-tab]').forEach(b => b.onclick = () => { S.postTab = b.dataset.tab; R.posts(); });
  $('#view').querySelectorAll('[data-pact]').forEach(b => b.onclick = () => postAction(b, b.dataset.pact, +b.dataset.id, posts));
};

/* ---- 發文紀錄 ---- */
R.history = async () => {
  const posts = await api('GET', '/api/posts');
  const groups = { pending: ['pending'], scheduled: ['scheduled', 'sending'], sent: ['sent'], failed: ['failed'] };
  const srcOk = p => S.histSrc === 'all' || (S.histSrc === 'auto' ? p.source === 'auto' : p.source !== 'auto');
  const mine = posts.filter(srcOk);
  const cnt = k => mine.filter(p => groups[k].includes(p.status)).length;
  const list = mine.filter(p => groups[S.histTab].includes(p.status));
  $('#view').innerHTML = `<div class="card">
    <div class="row between" style="flex-wrap:wrap;gap:10px">
      <div class="tabs">${[['sent', '已發佈'], ['scheduled', '排程中'], ['pending', '待審核'], ['failed', '失敗']].map(([k, l]) =>
        `<button class="${S.histTab === k ? 'on' : ''}" data-htab="${k}">${l}<span class="c">${cnt(k)}</span></button>`).join('')}</div>
      <div class="seg" id="hSrc">${[['all', '全部'], ['auto', 'AI 自動發文'], ['manual', '手動排程']].map(([k, l]) =>
        `<button data-v="${k}" class="${S.histSrc === k ? 'on' : ''}">${l}</button>`).join('')}</div>
    </div>
    ${S.histTab === 'sent' && list.some(p => !p.url) ? `<div class="row between" style="margin:10px 0 4px"><span class="faint">有 ${list.filter(p => !p.url).length} 篇還沒有連結（較早發的貼文），可以到個人檔案頁比對內文補上</span><button class="btn sm" id="findUrls">${I.globe}補上連結</button></div>` : ''}
    ${S.histTab === 'pending' && list.length ? '<div class="faint" style="margin:10px 0 4px">這些貼文來自「審核後才發」的自動發文設定，按「核准發出」才會發</div>' : ''}
    <div class="list">${list.length ? list.map(postItem).join('') : emptyBox(I.list, '這裡沒有貼文', '')}</div></div>`;
  $('#view').querySelectorAll('[data-htab]').forEach(b => b.onclick = () => { S.histTab = b.dataset.htab; R.history(); });
  if ($('#findUrls')) $('#findUrls').onclick = e => busy(e.currentTarget, async () => {
    toast('正在到個人檔案頁比對，需要一點時間…');
    const r = await api('POST', '/api/posts/find_urls');
    toast(r.missing ? `補上 ${r.found} 篇，另有 ${r.missing} 篇找不到（可能已刪除或太舊）` : `已補上 ${r.found} 篇連結`, !!r.missing && !r.found);
    R.history();
  });
  $('#hSrc').querySelectorAll('button').forEach(b => b.onclick = () => { S.histSrc = b.dataset.v; R.history(); });
  $('#view').querySelectorAll('[data-pact]').forEach(b => b.onclick = () => postAction(b, b.dataset.pact, +b.dataset.id, posts));
};

function drawThumbs() {
  const el = $('#thumbs'); if (!el) return;
  el.innerHTML = S.images.map((p, i) => `<div class="thumb">${/\.(mp4|mov|webm)$/i.test(p) ? `<div style="display:grid;place-items:center;height:100%">${I.play}</div>` : `<img src="/api/file?path=${encodeURIComponent(p)}">`}<button data-rm="${i}">${I.x}</button></div>`).join('');
  el.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => { S.images.splice(+b.dataset.rm, 1); drawThumbs(); });
}

function postItem(p) {
  const imgs = JSON.parse(p.images || '[]');
  const st = { pending: '<span class="pill warn">待審核</span>', scheduled: '<span class="pill info">排程中</span>', sending: '<span class="pill warn">發送中</span>', sent: '<span class="pill ok">已發佈</span>', failed: '<span class="pill err">失敗</span>' }[p.status] || '';
  const when = p.status === 'sent' ? `發佈於 ${short(p.posted_at)}` : `預定 ${short(p.scheduled_at)}`;
  return `<div class="item"><div class="body">
      <div class="meta">${st}<span>${esc(p.account_name || '')}</span><span>${when}</span>${p.source === 'auto' ? '<span class="pill plain">AI 自動</span>' : ''}${imgs.length ? `<span>${imgs.length} 個附件</span>` : ''}${p.url ? `<a class="link" href="${esc(p.url)}" target="_blank">${I.globe.replace('<svg', '<svg style="width:12px;height:12px;vertical-align:-2px"')} 在 Threads 查看</a>` : ''}</div>
      <div class="text clamp">${esc(p.text)}</div>
      ${p.error ? `<div class="err-text">${esc(p.error)}</div>` : ''}
    </div>
    <div class="acts">${p.status === 'sending' ? '' : `
      ${p.status !== 'sent' ? `<button class="btn sm" data-pact="now" data-id="${p.id}" title="立即發出">${I.send}${p.status === 'failed' ? '重試' : p.status === 'pending' ? '核准發出' : '立即發'}</button>` : ''}
      ${p.status !== 'sent' ? `<button class="btn sm icon" data-pact="edit" data-id="${p.id}" title="編輯">${I.edit}</button>` : ''}
      <button class="btn sm icon danger" data-pact="del" data-id="${p.id}" title="刪除">${I.trash}</button>`}
    </div></div>`;
}

async function postAction(btn, act, id, posts) {
  const p = posts.find(x => x.id === id);
  if (act === 'now') return busy(btn, async () => { await api('POST', `/api/posts/${id}/now`); toast('已排入，馬上發出'); R[S.view](); });
  if (act === 'del') {
    const note = p.status === 'sent'
      ? '<p style="margin-top:8px">只會刪除本機紀錄，<b>不會</b>刪除 Threads 上已發佈的貼文。</p>'
      : '<p style="margin-top:8px">刪除後這篇就不會發出。</p>';
    return confirmDelete('刪除貼文', `<p>確定要刪除這篇貼文？刪除後無法復原。</p>
      <div class="quote" style="margin-top:10px">${esc((p.text || '').slice(0, 160))}${(p.text || '').length > 160 ? '…' : ''}</div>${note}`,
      async () => { await api('DELETE', `/api/posts/${id}`); toast('已刪除'); R[S.view](); });
  }
  if (act === 'edit') {
    modal(`<h2>編輯貼文</h2><div class="stack">
      <div class="field"><label>帳號</label><select class="select" id="eAcc">${accountOptions(p.account_id)}</select></div>
      <div class="field"><label>內容</label><textarea class="textarea" id="eText" rows="8">${esc(p.text)}</textarea></div>
      <div class="field"><label>發文時間</label><input class="input" type="datetime-local" id="eAt" value="${p.scheduled_at.slice(0, 16).replace(' ', 'T')}"></div>
      <div class="row end"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn accent" id="eSave">${I.check}儲存</button></div></div>`);
    $('#eSave').onclick = e => busy(e.currentTarget, async () => {
      await api('PUT', `/api/posts/${id}`, { text: $('#eText').value, scheduled_at: $('#eAt').value, account_id: +$('#eAcc').value });
      closeModal(); R[S.view]();
    });
  }
}

function aiModal() {
  modal(`<h2>AI 幫我寫</h2><div class="stack">
    <div class="field"><label>主題</label><input class="input" id="aTopic" placeholder="例如：冬天洗車要注意什麼"></div>
    <div class="field"><label>風格（選填）</label><input class="input" id="aPersona" placeholder="例如：幽默、像朋友聊天"></div>
    <div class="row"><div class="field"><label>篇數</label><select class="select" id="aCount" style="width:100px">${[1, 2, 3, 4, 5].map(n => `<option ${n === 3 ? 'selected' : ''}>${n}</option>`).join('')}</select></div>
      <div class="field"><label>篇幅</label><div class="seg" id="aLen"><button data-v="短">短</button><button data-v="中" class="on">中</button><button data-v="長">長</button></div></div></div>
    <button class="btn accent" id="aGo">${I.wand}產生</button>
    <div id="aOut" class="stack"></div></div>`);
  $('#aLen').querySelectorAll('button').forEach(b => b.onclick = () => { $('#aLen').querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on'); });
  $('#aGo').onclick = e => busy(e.currentTarget, async () => {
    if (!$('#aTopic').value.trim()) throw new Error('請輸入主題');
    const r = await api('POST', '/api/ai/posts', { topic: $('#aTopic').value, persona: $('#aPersona').value, count: +$('#aCount').value, length: $('#aLen .on').dataset.v });
    $('#aOut').innerHTML = r.items.map((t, i) => `<div class="quote">${esc(t)}<div class="row end" style="margin-top:8px"><button class="btn sm" data-use="${i}">${I.check}用這篇</button></div></div>`).join('');
    $('#aOut').querySelectorAll('[data-use]').forEach(b => b.onclick = () => { $('#cText').value = r.items[+b.dataset.use]; $('#cText').oninput(); closeModal(); });
  });
}

/* ---- 自動海巡 ---- */
R.patrol = async () => {
  const tasks = await api('GET', '/api/tasks');
  $('#topActions').innerHTML = `<button class="btn accent" id="addTask">${I.plus}新增海巡任務</button>`;
  $('#addTask').onclick = () => taskModal();
  $('#view').innerHTML = needAccount() + `
  <div class="notice info" style="margin-bottom:16px">${I.info}<div>海巡會定時搜尋關鍵字的新貼文，由 AI 判斷是否適合留言並寫好內容，直接排入送出佇列。
    送出速度受「設定」裡的每小時上限控制（目前每帳號每小時 ${S.state.hourly_limit} 則），佇列太多時會自動暫停海巡。</div></div>
  ${tasks.length ? `<div class="grid g2">${tasks.map(taskCard).join('')}</div>` : `<div class="card">${emptyBox(I.radar, '還沒有海巡任務', '按右上角「新增海巡任務」，設定要追蹤的關鍵字')}</div>`}`;
  $('#view').querySelectorAll('[data-tact]').forEach(b => b.onclick = () => taskAction(b, b.dataset.tact, +b.dataset.id, tasks));
  $('#view').querySelectorAll('[data-ton]').forEach(b => b.onchange = async () => { await api('PUT', `/api/tasks/${b.dataset.ton}`, { enabled: b.checked ? 1 : 0 }); R.patrol(); refreshState(); });
};

function taskCard(t) {
  const kws = t.keywords.split(/[,，\n]/).map(s => s.trim()).filter(Boolean);
  return `<div class="card task ${t.enabled ? '' : 'off'}">
    <div class="card-h" style="margin:0">
      <h3>${I.radar}${esc(t.name)}${t.mode === 'review' ? '<span class="pill warn">審核後才送</span>' : '<span class="pill ok">自動送出</span>'}<span class="pill plain">留言${esc(t.length || '中')}</span></h3>
      <label class="switch" title="啟用"><input type="checkbox" data-ton="${t.id}" ${t.enabled ? 'checked' : ''}><span></span></label>
    </div>
    <div class="faint">帳號：${esc(t.account_name || '已刪除')}　上次執行：${t.last_run ? short(t.last_run) : '尚未執行'}${parseImgs(t.images).length ? `　每則附 ${parseImgs(t.images).length} 張圖` : ''}</div>
    <div class="kw">${kws.map(k => `<span>${esc(k)}</span>`).join('')}</div>
    <div class="kv">
      <div><small>執行頻率</small><b>每 ${t.interval_min} 分鐘</b></div>
      <div><small>每輪最多</small><b>${t.max_per_run} 則留言</b></div>
      <div><small>搜尋排序</small><b>${t.recent ? '最近' : '最相關'}${t.min_likes ? `・讚≥${t.min_likes}` : ''}</b></div>
    </div>
    ${t.persona ? `<div class="quote">${esc(t.persona)}</div>` : ''}
    <div class="row end">
      <button class="btn sm danger" data-tact="del" data-id="${t.id}">${I.trash}刪除</button>
      <button class="btn sm" data-tact="edit" data-id="${t.id}">${I.edit}編輯</button>
      <button class="btn sm primary" data-tact="run" data-id="${t.id}">${I.play}立即執行</button>
    </div>
  </div>`;
}

function taskModal(t) {
  t = t || { account_id: S.accounts[0]?.id, name: '', keywords: '', recent: 1, persona: '', length: '中', mode: 'auto', interval_min: 60, max_per_run: 5, min_likes: 0, enabled: 1 };
  modal(`<h2>${t.id ? '編輯海巡任務' : '新增海巡任務'}</h2><div class="stack">
    <div class="grid g2">
      <div class="field"><label>任務名稱</label><input class="input" id="tName" value="${esc(t.name)}" placeholder="例如：洗車相關討論"></div>
      <div class="field"><label>使用帳號</label><select class="select" id="tAcc">${accountOptions(t.account_id)}</select></div>
    </div>
    <div class="field"><label>關鍵字</label><textarea class="textarea" id="tKw" rows="3" placeholder="用逗號或換行分隔，例如：洗車, 汽車美容, 鍍膜推薦">${esc(t.keywords)}</textarea></div>
    <div class="field"><label>留言策略</label>${presetChips(PATROL_PRESETS)}<textarea class="textarea" id="tPersona" rows="3" placeholder="例如：以洗車師傅的角度給實用建議，語氣親切，不主動推銷，不留連結">${esc(t.persona)}</textarea>
      <span class="hint">點上面的範本直接套用，或自己寫；跟主題無關或爭議性的貼文會自動略過</span></div>
    <div class="field"><label>留言篇幅</label><div class="seg" id="tLen">${[['短', '短（20 字內）'], ['中', '中（40 字內）'], ['長', '長（60～120 字）']].map(([v, l]) =>
      `<button data-v="${v}" class="${(t.length || '中') === v ? 'on' : ''}">${l}</button>`).join('')}</div>
      <span class="hint">短的像隨手回應；長的會分享經驗或看法，比較像真心參與討論</span></div>
    <div class="grid g3">
      <div class="field"><label>每幾分鐘執行</label><input class="input" type="number" min="10" id="tInt" value="${t.interval_min}"></div>
      <div class="field"><label>每輪最多留言</label><input class="input" type="number" min="1" max="30" id="tMax" value="${t.max_per_run}"></div>
      <div class="field"><label>最低讚數</label><input class="input" type="number" min="0" id="tLikes" value="${t.min_likes}"></div>
    </div>
    <div class="field"><label>留言附加圖片（最多 5 張，每則留言都會附上）</label><div id="tImgs"></div>
      <span class="hint">同一組圖片每則都附，太常出現可能被當成洗版，建議放 1～2 張就好</span></div>
    <div class="field"><label>留言方式</label><div class="seg" id="tMode"><button data-v="auto" class="${t.mode !== 'review' ? 'on' : ''}">自動送出</button><button data-v="review" class="${t.mode === 'review' ? 'on' : ''}">審核後才送出</button></div>
      <span class="hint">選「審核後才送出」時，AI 寫好的留言會放在「留言紀錄 → 待審核」，你按核准才會送</span></div>
    <div class="field"><label>搜尋排序</label><div class="seg" id="tRecent"><button data-v="1" class="${t.recent ? 'on' : ''}">最近（新貼文）</button><button data-v="0" class="${t.recent ? '' : 'on'}">最相關（熱門）</button></div></div>
    <div class="row end"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn accent" id="tSave">${I.check}儲存</button></div>
  </div>`);
  bindPresets($('#modal'), PATROL_PRESETS, $('#tPersona'));
  const getTaskImgs = imagePicker($('#tImgs'), parseImgs(t.images));
  ['#tRecent', '#tMode', '#tLen'].forEach(sel => $(sel).querySelectorAll('button').forEach(b => b.onclick = () => { $(sel).querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on'); }));
  $('#tSave').onclick = e => busy(e.currentTarget, async () => {
    const d = {
      account_id: +$('#tAcc').value, name: $('#tName').value.trim() || '未命名任務', keywords: $('#tKw').value.trim(),
      persona: $('#tPersona').value.trim(), interval_min: Math.max(10, +$('#tInt').value || 60),
      max_per_run: Math.max(1, +$('#tMax').value || 5), min_likes: +$('#tLikes').value || 0,
      recent: +$('#tRecent .on').dataset.v, length: $('#tLen .on').dataset.v, mode: $('#tMode .on').dataset.v, enabled: t.enabled ?? 1, images: getTaskImgs(),
    };
    if (!d.account_id) throw new Error('請先新增帳號');
    if (!d.keywords) throw new Error('請輸入關鍵字');
    if (t.id) await api('PUT', `/api/tasks/${t.id}`, d); else await api('POST', '/api/tasks', d);
    closeModal(); R.patrol(); refreshState();
  });
}

async function taskAction(btn, act, id, tasks) {
  const t = tasks.find(x => x.id === id);
  if (act === 'edit') return taskModal(t);
  if (act === 'del') return confirmDelete('刪除海巡任務', `<p>確定要刪除「${esc(t.name)}」？刪除後無法復原，已產生的留言紀錄會保留。</p>`,
    async () => { await api('DELETE', `/api/tasks/${id}`); toast('已刪除'); R.patrol(); });
  if (act === 'run') return busy(btn, async () => { await api('POST', `/api/tasks/${id}/run`); toast('已排入，稍後開始執行，進度看「總覽」紀錄'); });
}

/* ---- 留言紀錄 ---- */
const CTABS = [['pending', '待審核'], ['approved', '待送出'], ['sent', '已送出'], ['failed', '失敗'], ['skipped,rejected', '略過／取消']];
R.comments = async () => {
  const rows = await api('GET', `/api/comments?status=${S.commentTab}`);
  $('#view').innerHTML = `<div class="card">
    <div class="tabs">${CTABS.map(([k, l]) => `<button class="${S.commentTab === k ? 'on' : ''}" data-ctab="${k}">${l}${k === 'approved' && S.state.queued ? `<span class="c">${S.state.queued}</span>` : ''}${k === 'pending' && S.state.pending_comments ? `<span class="c">${S.state.pending_comments}</span>` : ''}</button>`).join('')}</div>
    ${S.commentTab === 'pending' && rows.length ? `<div class="row between" style="margin:10px 0 4px"><span class="faint">這些留言來自「審核後才送出」的海巡任務，核准後會依每小時上限陸續送出</span><button class="btn sm accent" id="approveAll">${I.check}全部核准</button></div>` : ''}
    ${S.commentTab === 'approved' && rows.length ? `<div class="notice info" style="margin:10px 0 4px">${I.clock}<div>全自動送出，不用按任何東西。依每小時上限 ${S.state.hourly_limit} 則、每則間隔約 ${Math.round(60 / Math.max(1, S.state.hourly_limit))} 分鐘陸續送出${S.state.next_comment ? `，<b>下一則預計 ${esc(S.state.next_comment)} 送出</b>` : ''}。送出前都可以修改或取消。</div></div>` : ''}
    <div class="list">${rows.length ? rows.map(commentItem).join('') : emptyBox(I.chat, '這裡沒有留言', '')}</div></div>`;
  $('#view').querySelectorAll('[data-ctab]').forEach(b => b.onclick = () => { S.commentTab = b.dataset.ctab; R.comments(); });
  if ($('#approveAll')) $('#approveAll').onclick = e => busy(e.currentTarget, async () => { await api('POST', '/api/comments/approve_all'); toast('已全部核准'); await refreshState(); R.comments(); });
  $('#view').querySelectorAll('[data-cact]').forEach(b => b.onclick = () => commentAction(b, b.dataset.cact, +b.dataset.id, rows));
};

function commentItem(c) {
  const canEdit = ['pending', 'approved', 'failed', 'skipped', 'rejected'].includes(c.status);
  const acts = {
    pending: `<button class="btn sm icon" data-cact="edit" data-id="${c.id}" title="修改">${I.edit}</button><button class="btn sm icon" data-cact="redraft" data-id="${c.id}" title="AI 重寫">${I.refresh}</button><button class="btn sm danger" data-cact="cancel" data-id="${c.id}">${I.x}拒絕</button><button class="btn sm accent" data-cact="retry" data-id="${c.id}">${I.check}核准</button>`,
    approved: `<button class="btn sm icon" data-cact="edit" data-id="${c.id}" title="修改">${I.edit}</button><button class="btn sm icon" data-cact="redraft" data-id="${c.id}" title="AI 重寫">${I.refresh}</button><button class="btn sm danger" data-cact="cancel" data-id="${c.id}">${I.x}取消</button>`,
    failed: `<button class="btn sm icon" data-cact="edit" data-id="${c.id}" title="修改">${I.edit}</button><button class="btn sm" data-cact="retry" data-id="${c.id}">${I.refresh}重試</button>`,
    skipped: `<button class="btn sm" data-cact="${c.draft ? 'retry' : 'redraft-send'}" data-id="${c.id}">${I.send}還是要留言</button>`,
    rejected: `<button class="btn sm" data-cact="retry" data-id="${c.id}">${I.send}恢復送出</button>`,
  }[c.status] || '';
  return `<div class="item"><div class="body">
    <div class="meta"><span>${esc(c.account_name || '')}</span><a class="link" href="${esc(c.post_url)}" target="_blank">@${esc(c.author)}</a>
      <span class="pill plain">${esc(c.keyword)}</span><span>${I.heart.replace('<svg', '<svg style="width:12px;height:12px;vertical-align:-2px"')} ${c.likes}</span>
      <span>${c.status === 'sent' ? '送出於 ' + short(c.sent_at) : '找到於 ' + short(c.created_at)}</span>${parseImgs(c.images).length ? `<span class="pill plain">${I.image.replace('<svg', '<svg style="width:12px;height:12px"')} ${parseImgs(c.images).length} 張圖</span>` : ''}</div>
    <div class="quote">${esc((c.post_text || '').slice(0, 260))}${(c.post_text || '').length > 260 ? '…' : ''}</div>
    ${c.draft ? `<div class="reply-line">${I.corner}<div class="text" id="draft-${c.id}">${esc(c.draft)}</div></div>` : (c.status === 'skipped' ? '<div class="faint" style="margin-top:8px">AI 判斷不適合留言</div>' : '')}
    ${c.error ? `<div class="err-text">${esc(c.error)}</div>` : ''}
  </div><div class="acts">${canEdit ? acts : ''}</div></div>`;
}

async function commentAction(btn, act, id, rows) {
  const c = rows.find(x => x.id === id);
  if (act === 'edit') {
    modal(`<h2>修改留言</h2><div class="quote" style="margin-bottom:14px">${esc((c.post_text || '').slice(0, 300))}</div>
      <div class="field"><label>留言內容</label><textarea class="textarea" id="dText" rows="4">${esc(c.draft)}</textarea></div>
      <div class="row end" style="margin-top:16px"><button class="btn ghost" onclick="closeModal()">取消</button><button class="btn accent" id="dSave">${I.check}儲存</button></div>`);
    $('#dSave').onclick = e => busy(e.currentTarget, async () => { await api('PUT', `/api/comments/${id}`, { draft: $('#dText').value }); closeModal(); R.comments(); });
    return;
  }
  await busy(btn, async () => {
    if (act === 'cancel') await api('POST', `/api/comments/${id}/cancel`);
    if (act === 'retry') await api('POST', `/api/comments/${id}/retry`, {});
    if (act === 'redraft') { const r = await api('POST', `/api/comments/${id}/redraft`); if (!r.draft) toast('AI 仍判斷不適合留言', true); }
    if (act === 'redraft-send') {
      const r = await api('POST', `/api/comments/${id}/redraft`);
      if (!r.draft) throw new Error('AI 仍判斷不適合留言，可以改用「修改」自己寫');
      await api('POST', `/api/comments/${id}/retry`, {});
    }
    await refreshState(); R.comments();
  });
}

/* ---- 設定 ---- */
const PROV = {
  claude_cli: { desc: '用你的 Claude Pro／Max 訂閱（透過本機 Claude Code），不另外計費', login: '登入 Claude', loginHint: '會開一個視窗，照指示用瀏覽器登入你的 Claude 帳號', key: 'cli_model' },
  codex_cli: { desc: '用你的 ChatGPT Plus／Pro 訂閱（透過本機 Codex CLI），不另外計費', login: '登入 ChatGPT', loginHint: '會開一個視窗，選「Sign in with ChatGPT」登入', key: 'codex_model' },
  claude_api: { desc: '使用 Anthropic API Key，依用量計費', key: 'model' },
  openai_api: { desc: '使用 OpenAI API Key，依用量計費', key: 'openai_model' },
};
S.autoDetected = {};

async function detectModels(p, btn) {
  const out = $('#modelHint');
  if (out) out.textContent = p === 'claude_cli' ? '偵測中，會逐一試用各模型，約 20～60 秒…' : '偵測中…';
  await busy(btn, async () => {
    const r = await api('POST', '/api/ai/models', { provider: p });
    toast(`偵測到 ${r.models.length} 個可用模型`);
  });
  if (S.view === 'settings') R.settings();
}

R.settings = async () => {
  const s = await api('GET', '/api/settings');
  S.provider = S.provider || s.ai_provider;
  const p = S.provider, meta = PROV[p];
  const list = s.models[p] || [];
  const cur = s[meta.key] || '';
  const isCli = p.endsWith('_cli');
  // 模型清單（可點選，旁邊顯示 推薦／最強／最省 等標籤）
  let mlist = list.slice();
  if (isCli && !mlist.some(m => m.id === '')) mlist.unshift({ id: '', name: '預設模型', version: '', tags: [['預設', 'def']], desc: '按「偵測可用模型」可看到實際版本' });
  if (!isCli && cur && !mlist.some(m => m.id === cur)) mlist.unshift({ id: cur, name: cur, version: cur, tags: [], desc: '' });
  const modelRows = mlist.length ? mlist.map(m => {
    const v = m.version && !m.name.includes(m.version) ? m.version : '';
    return `<button type="button" class="model ${m.id === cur ? 'on' : ''}" data-model="${esc(m.id)}">
      <span class="radio"></span>
      <span class="model-main"><span class="model-name">${esc(m.name)}${v ? `<code>${esc(v)}</code>` : ''}</span>
        ${m.desc ? `<span class="model-desc">${esc(m.desc)}</span>` : ''}</span>
      <span class="model-tags">${(m.tags || []).map(([t, k]) => `<span class="tag ${k}">${esc(t)}</span>`).join('')}</span>
    </button>`;
  }).join('') : `<div class="faint" style="padding:14px">尚未偵測，請按「偵測可用模型」</div>`;
  const keyField = {
    claude_api: `<div class="field"><label>Claude API Key</label><input class="input" type="password" id="sKey" placeholder="${s.api_key_masked ? '已設定：' + esc(s.api_key_masked) + '（要更換才填）' : 'sk-ant-…'}"><span class="hint">到 console.anthropic.com 建立，只存在這台電腦</span></div>`,
    openai_api: `<div class="field"><label>OpenAI API Key</label><input class="input" type="password" id="sOKey" placeholder="${s.openai_key_masked ? '已設定：' + esc(s.openai_key_masked) + '（要更換才填）' : 'sk-…'}"><span class="hint">到 platform.openai.com 建立，只存在這台電腦</span></div>`,
  }[p] || '';
  const loginRow = meta.login ? `<div class="row"><button class="btn" data-login="${p}">${I.globe}${meta.login}</button><span class="faint">${meta.loginHint}</span></div>` : '';
  $('#view').innerHTML = `<div class="stack">
    <div class="card"><div class="card-h"><h3>${I.wand}AI 寫手</h3>${s.ai_tested === '1' && p === s.ai_provider ? '<span class="pill ok">已測試可用</span>' : '<span class="pill warn">尚未測試</span>'}</div>
      <div class="prov">${Object.entries(s.providers).map(([k, name]) => `
        <button class="prov-item ${p === k ? 'on' : ''}" data-prov="${k}">
          <div class="prov-top"><span class="radio"></span><b>${name}</b><span class="prov-st" id="st-${k}"></span></div>
          <span class="prov-desc">${PROV[k].desc}</span>
        </button>`).join('')}</div>
      <div class="stack" style="margin-top:18px">
        ${loginRow}${keyField}
        <div class="field"><label>模型</label>
          <input type="hidden" id="sModelSel" value="${esc(cur)}">
          <div class="models">${modelRows}</div>
          <div class="row" style="margin-top:4px"><button class="btn sm" id="sDetect">${I.refresh}偵測可用模型</button>
          <span class="hint" id="modelHint">${list.length ? `已偵測到 ${list.length} 個可用模型` : (isCli ? '登入後會自動偵測，也可以手動按「偵測可用模型」' : '填好金鑰並儲存後，按「偵測可用模型」')}</span></div></div>
        <div class="row"><button class="btn primary" id="sTest">${I.play}測試 AI</button><span class="faint" id="testOut"></span></div>
      </div>
    </div>
    <div class="grid g2" style="align-items:start">
      <div class="card"><div class="card-h"><h3>${I.user}帳號定位</h3></div>
        <div class="field"><label>所有發文、留言共用的背景設定</label><textarea class="textarea" id="sBrand" rows="5" placeholder="例如：台中專業汽車美容店，主打鍍膜與內裝清潔，老闆親自經營">${esc(s.brand_persona)}</textarea></div></div>
      <div class="card"><div class="card-h"><h3>${I.shield}頻率限制</h3></div><div class="stack">
        <div class="field"><label>每個帳號每小時最多留言</label><input class="input" type="number" min="1" id="sHour" value="${esc(s.hourly_comment_limit)}" style="width:140px">
          <span class="hint">留言會平均分散在一小時內並加上隨機誤差。數量由你決定，新帳號建議 3～6 則</span></div>
        <div id="hourWarn"></div>
        <div class="faint">自動留言、自動發文有違反 Threads 使用條款的風險，由使用者自行承擔。</div>
      </div></div>
    </div>
    <div class="row end"><button class="btn accent" id="sSave">${I.check}儲存設定</button></div>
  </div>`;
  const collect = () => {
    const d = { ai_provider: p, brand_persona: $('#sBrand').value, hourly_comment_limit: Math.max(1, Math.round(+$('#sHour').value) || 6) };
    d[meta.key] = $('#sModelSel').value;
    if ($('#sKey')) d.api_key = $('#sKey').value;
    if ($('#sOKey')) d.openai_key = $('#sOKey').value;
    return d;
  };
  bindLimitWarn($('#sHour'), $('#hourWarn'), 'comment');
  $('#view').querySelectorAll('[data-model]').forEach(b => b.onclick = () => {
    $('#view').querySelectorAll('[data-model]').forEach(x => x.classList.remove('on'));
    b.classList.add('on'); $('#sModelSel').value = b.dataset.model;
  });
  $('#view').querySelectorAll('[data-prov]').forEach(b => b.onclick = () => { S.provider = b.dataset.prov; R.settings(); });
  $('#view').querySelectorAll('[data-login]').forEach(b => b.onclick = () => busy(b, async () => {
    await api('POST', '/api/ai/login', { provider: b.dataset.login });
    S.autoDetected[b.dataset.login] = false;
    toast('已開啟登入視窗，登入完成後這頁會自動偵測可用模型');
    pollLogin(b.dataset.login);
  }));
  $('#sDetect').onclick = async e => { if (!isCli) await api('PUT', '/api/settings', collect()); detectModels(p, e.currentTarget); };
  $('#sSave').onclick = e => busy(e.currentTarget, async () => { await api('PUT', '/api/settings', collect()); toast('已儲存'); refreshState(); R.settings(); });
  $('#sTest').onclick = e => busy(e.currentTarget, async () => {
    await api('PUT', '/api/settings', collect());
    $('#testOut').textContent = isCli ? '測試中，訂閱登入模式約需 10～30 秒…' : '測試中…';
    try { const r = await api('POST', '/api/ai/test'); toast('AI 回覆：' + r.reply); }
    finally { $('#testOut').textContent = ''; }
    R.settings();
  });
  api('GET', '/api/ai/status').then(st => {
    for (const [k, v] of Object.entries(st)) {
      const el = $('#st-' + k); if (!el) continue;
      el.innerHTML = !v.installed ? '<span class="pill err">未安裝</span>' : v.logged_in ? '<span class="pill ok">已登入</span>' : '<span class="pill warn">未登入</span>';
    }
    // 已登入但還沒偵測過模型 → 自動偵測一次
    const cur = st[p];
    if (cur && cur.logged_in && !list.length && !S.autoDetected[p] && S.view === 'settings') {
      S.autoDetected[p] = true;
      detectModels(p, $('#sDetect'));
    }
  }).catch(() => { });
};

let loginTimer = null;
function pollLogin(p) {
  clearInterval(loginTimer);
  let n = 0;
  loginTimer = setInterval(async () => {
    if (++n > 60) return clearInterval(loginTimer);
    try {
      const st = await api('GET', '/api/ai/status');
      if (st[p] && st[p].logged_in) {
        clearInterval(loginTimer);
        toast('登入成功，開始偵測可用模型');
        S.provider = p;
        if (S.view === 'settings') { await R.settings(); }
        else detectModels(p);
      }
    } catch { }
  }, 5000);
}

/* ---------------- 輪詢 ---------------- */
async function refreshState() {
  try { S.state = await api('GET', '/api/state'); renderNav(); drawNow(); } catch { }
}
async function refreshLogs() {
  try {
    const rows = await api('GET', `/api/logs${S.lastLog ? '?after=' + S.lastLog : ''}`);
    if (rows.length) {
      S.logs = S.logs.concat(rows).slice(-300);
      S.lastLog = rows[rows.length - 1].id;
      drawLogs();
      if (rows.some(r => r.level === 'ok' || r.level === 'error')) softRefresh();
    }
  } catch { }
}
function softRefresh() {
  // 使用者正在輸入或開著視窗時不重畫，避免打斷
  const a = document.activeElement;
  if (S.editing || (a && ['INPUT', 'TEXTAREA', 'SELECT'].includes(a.tagName))) return;
  if (['comments', 'posts', 'history', 'accounts'].includes(S.view)) R[S.view]();
}

(async () => {
  await refreshState();
  await refreshLogs();
  await go('home');
  setInterval(refreshState, 3000);
  setInterval(refreshLogs, 3000);
})();
