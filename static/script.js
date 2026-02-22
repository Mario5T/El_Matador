/**
 * VerifyAI — Frontend Logic
 * Handles article submission, API communication, and result rendering.
 */

// ── DOM References ──────────────────────────────────────────────
const titleInput      = document.getElementById('article-title');
const textInput       = document.getElementById('article-text');
const analyzeBtn      = document.getElementById('analyze-btn');
const charCounter     = document.getElementById('char-counter');
const emptyState      = document.getElementById('empty-state');
const loadingState    = document.getElementById('loading-state');
const resultsContent  = document.getElementById('results-content');

const verdictBadge    = document.getElementById('verdict-badge');
const verdictIcon     = document.getElementById('verdict-icon');
const verdictLabel    = document.getElementById('verdict-label');
const confidenceValue = document.getElementById('confidence-value');
const confidenceBar   = document.getElementById('confidence-bar');
const detailClass     = document.getElementById('detail-class');
const detailLabel     = document.getElementById('detail-label');
const detailConf      = document.getElementById('detail-confidence');
const disclaimerText  = document.getElementById('disclaimer-text');


// ── Character Counter ───────────────────────────────────────────
textInput.addEventListener('input', () => {
    charCounter.textContent = textInput.value.length.toLocaleString();
});

titleInput.addEventListener('input', () => {
    // Just trigger a recount combining both
    charCounter.textContent = (titleInput.value.length + textInput.value.length).toLocaleString();
});


// ── Analyze Article ─────────────────────────────────────────────
async function analyzeArticle() {
    const title = titleInput.value.trim();
    const text  = textInput.value.trim();

    if (!text && !title) {
        shakeElement(textInput);
        return;
    }

    // Combine title + text (same as training pipeline)
    const fullText = (title ? title + ' ' : '') + text;

    // UI → loading
    setState('loading');
    analyzeBtn.disabled = true;
    analyzeBtn.classList.add('analyzing');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: fullText }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server error');
        }

        renderResult(data);
    } catch (err) {
        console.error('Prediction error:', err);
        alert('Error: ' + err.message);
        setState('empty');
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('analyzing');
    }
}


// ── Render Result ───────────────────────────────────────────────
function renderResult(data) {
    const isCredible = data.label === 1;
    const conf       = data.confidence;
    const confPct    = conf !== null ? Math.round(conf * 100) : null;

    // Verdict badge
    verdictBadge.className = 'verdict-badge ' + (isCredible ? 'credible' : 'fake');
    verdictIcon.textContent = isCredible ? '✓' : '✗';
    verdictLabel.textContent = isCredible ? 'Likely Credible' : 'Likely Fake';

    // Confidence
    if (confPct !== null) {
        confidenceValue.textContent = confPct + '%';
        confidenceBar.className = 'confidence-bar-fill ' + (isCredible ? 'credible' : 'fake');
        // Animate bar after a tiny delay
        setTimeout(() => {
            confidenceBar.style.width = confPct + '%';
        }, 100);
    } else {
        confidenceValue.textContent = 'N/A';
        confidenceBar.style.width = '0%';
    }

    // Detail rows
    detailClass.textContent = data.label_text;
    detailLabel.textContent = 'Label ' + data.label + (isCredible ? ' (Credible)' : ' (Fake)');
    detailConf.textContent  = confPct !== null ? confPct + '%' : 'N/A';

    // Disclaimer
    disclaimerText.textContent = data.disclaimer;

    // Show results
    setState('results');
}


// ── State Management ────────────────────────────────────────────
function setState(state) {
    emptyState.classList.toggle('hidden', state !== 'empty');
    loadingState.classList.toggle('hidden', state !== 'loading');
    resultsContent.classList.toggle('hidden', state !== 'results');

    // Reset confidence bar when going to loading
    if (state === 'loading') {
        confidenceBar.style.width = '0%';
    }
}


// ── Clear Form ──────────────────────────────────────────────────
function clearForm() {
    titleInput.value = '';
    textInput.value = '';
    charCounter.textContent = '0';
    setState('empty');
}


// ── Shake Animation (validation feedback) ───────────────────────
function shakeElement(el) {
    el.style.animation = 'none';
    el.offsetHeight; // trigger reflow
    el.style.animation = 'shake 0.4s ease';
    setTimeout(() => { el.style.animation = ''; }, 400);
}

// Add shake keyframes dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%      { transform: translateX(-6px); }
        40%      { transform: translateX(6px); }
        60%      { transform: translateX(-4px); }
        80%      { transform: translateX(4px); }
    }
`;
document.head.appendChild(style);


// ── Keyboard Shortcut ───────────────────────────────────────────
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        analyzeArticle();
    }
});
