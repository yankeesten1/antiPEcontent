'use strict';
let state, busy = false, dirty = false;
const dirtyDrafts = new Set();
const $ = selector => document.querySelector(selector);
function element(tag, text, className) {
  const item = document.createElement(tag);
  if (text !== undefined) item.textContent = text;
  if (className) item.className = className;
  return item;
}
async function api(path, data) {
  const response = await fetch(path, data === undefined ? {} : {
    method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRF-Token': state.csrf}, body: JSON.stringify(data)
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed');
  return result;
}
async function operation(action, success) {
  if (busy) return;
  busy = true;
  document.querySelectorAll('button').forEach(button => button.disabled = true);
  $('#notice').textContent = 'Working… Research may take a few minutes.';
  try {
    await action(); dirty = false; dirtyDrafts.clear(); await refresh(); $('#notice').textContent = success;
  } catch (error) {
    $('#notice').textContent = error.message;
  } finally {
    busy = false;
    document.querySelectorAll('button').forEach(button => button.disabled = button.dataset.unavailable === 'true');
  }
}
function renderDraft(draft) {
  const card = element('article', undefined, 'card');
  const head = element('div', undefined, 'card-head');
  const meta = element('div', undefined, 'meta');
  meta.append(element('span', `${draft.day} · #${draft.id}`), element('span', `${draft.kind === 'demo' ? 'sample / ' : ''}${draft.status.replaceAll('_', ' ')}`, 'badge'));
  head.append(meta, element('h2', draft.title));
  const image = element('img'); image.src = `/api/drafts/${draft.id}/image`; image.alt = `Post graphic: ${draft.title}`; image.loading = 'lazy';
  const body = element('div', undefined, 'card-body');
  const label = element('label', 'Caption'); label.htmlFor = `caption-${draft.id}`;
  const caption = element('textarea'); caption.id = label.htmlFor; caption.value = draft.caption; caption.maxLength = 2200;
  const count = element('div', `${caption.value.length} / 2,200`, 'count');
  caption.addEventListener('input', () => { dirty = true; dirtyDrafts.add(draft.id); count.textContent = `${caption.value.length} / 2,200`; });
  const sources = element('div', undefined, 'sources'); sources.append(element('strong', 'Evidence to review'));
  draft.sources.forEach(source => {
    const p = element('p'), a = element('a', source.title);
    if (source.url.startsWith('https://')) a.href = source.url;
    a.target = '_blank'; a.rel = 'noopener noreferrer'; p.append(a); sources.append(p);
  });
  const detail = element('details'); detail.append(element('summary', 'Image & publishing details'));
  detail.append(element('p', 'The preview is generated automatically. Instagram needs a public HTTPS JPEG URL. To replace the graphic, paste a new URL and review that image before approval.', 'hint'));
  const imageLabel = element('label', 'Public image URL'); imageLabel.htmlFor = `image-${draft.id}`;
  const imageUrl = element('input'); imageUrl.id = imageLabel.htmlFor; imageUrl.type = 'url'; imageUrl.value = draft.image_url; imageUrl.placeholder = 'https://your-site.example/media/post.jpg';
  imageUrl.addEventListener('input', () => { dirty = true; dirtyDrafts.add(draft.id); });
  detail.append(imageLabel, imageUrl, element('p', `Optional art direction: ${draft.image_brief}`, 'hint'));
  if (draft.image_url) {
    const external = element('a', 'Review the exact image URL sent to Instagram');
    if (draft.image_url.startsWith('https://')) external.href = draft.image_url;
    external.target = '_blank'; external.rel = 'noopener noreferrer'; detail.append(external);
  }
  const actions = element('div', undefined, 'card-actions');
  const save = element('button', 'Save edits', 'quiet'), publish = element('button', 'Approve & publish');
  const editable = ['draft', 'approved'].includes(draft.status);
  save.disabled = !editable; save.dataset.unavailable = String(!editable); caption.disabled = imageUrl.disabled = !editable;
  const unavailable = !editable || draft.kind === 'demo' || !state.settings.publishing_configured;
  publish.disabled = unavailable; publish.dataset.unavailable = String(unavailable);
  async function saveEdits() {
    await api(`/api/drafts/${draft.id}/edit`, {caption: caption.value, image_url: imageUrl.value, revision: draft.revision});
  }
  const discardOthers = () => [...dirtyDrafts].some(id => id !== draft.id) && !window.confirm('Other drafts have unsaved edits. Discard those edits and continue with this post?');
  save.addEventListener('click', () => {
    if (discardOthers()) return;
    operation(saveEdits, 'Edits saved. Any previous approval has been cleared.');
  });
  publish.addEventListener('click', () => {
    if (discardOthers()) return;
    if (!imageUrl.value) { $('#notice').textContent = 'A public JPEG image URL is required before publishing.'; return; }
    if (!window.confirm('Approve this caption and the exact image at the supplied URL for immediate publication to your connected Instagram account? Review the evidence and image before continuing.')) return;
    operation(async () => {
      await saveEdits();
      await api(`/api/drafts/${draft.id}/approve`, {revision: draft.revision + 1});
      await api(`/api/drafts/${draft.id}/publish`, {});
    }, 'Published to Instagram.');
  });
  actions.append(save, publish); body.append(label, caption, count, sources, detail);
  if (draft.error) body.append(element('p', draft.error, 'problem'));
  if (draft.instagram_media_id) body.append(element('p', `Instagram media ID: ${draft.instagram_media_id}`, 'hint'));
  body.append(actions); card.append(head, image, body); return card;
}
async function refresh() {
  state = await api('/api/inbox');
  $('#schedule').textContent = `Five drafts at ${state.settings.daily_time} · ${state.settings.timezone}. Server must stay running.`;
  const setup = $('#setup'); setup.replaceChildren();
  if (!state.settings.generation_configured) setup.append(element('p', 'Generation is not connected. Explore samples now; add an OpenAI API key securely to enable sourced daily drafts.'));
  if (!state.settings.publishing_configured) setup.append(element('p', 'Publishing is not connected. You need an Instagram professional account and Meta publishing permissions.'));
  if (!state.settings.public_url_configured) setup.append(element('p', 'Public image hosting is not connected. Instagram needs a public HTTPS image URL.'));
  setup.append(element('p', 'Delivery: this web inbox. ChatGPT messaging is not connected. Review sources before approving; automated research can make mistakes.'));
  const generate = $('#generate'); generate.disabled = !state.settings.generation_configured; generate.dataset.unavailable = String(generate.disabled);
  $('#batches').replaceChildren(...state.batches.filter(batch => batch.status !== 'ready').map(batch => element('p', `${batch.day} ${batch.kind}: ${batch.status}${batch.error ? ' — ' + batch.error : ''}`, 'problem')));
  $('#empty').hidden = state.drafts.length !== 0;
  $('#drafts').replaceChildren(...state.drafts.map(renderDraft));
}
$('#refresh').addEventListener('click', () => {
  if (dirty && !window.confirm('Discard unsaved edits and refresh the inbox?')) return;
  operation(async () => {}, 'Inbox refreshed.');
});
$('#demo').addEventListener('click', () => {
  if (dirty && !window.confirm('Discard unsaved edits and load samples?')) return;
  operation(() => api('/api/demo', {}), 'Sample concepts are available. Samples cannot be published.');
});
$('#generate').addEventListener('click', () => {
  if (dirty && !window.confirm('Discard unsaved edits and generate today’s batch?')) return;
  operation(() => api('/api/generate', {}), 'Today’s batch is available. Check batch status for any earlier failure.');
});
window.addEventListener('beforeunload', event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } });
refresh().catch(error => { $('#notice').textContent = error.message; });
