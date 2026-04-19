"""
El Matador — News Credibility Analyzer
ML-Based Credibility Analysis · Streamlit UI
"""

import os
import streamlit as st
import joblib
from typing import Tuple, Dict, List, Any
from credibility_analyzer import CredibilityAnalyzer

# ── page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="El Matador — News Credibility Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM
#  Brand colors: Red (#e63946) · Yellow (#fbbf24) · Blue (#3b82f6)
# ══════════════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
  /* Surfaces */
  --surface:         #10131a;
  --surface-lowest:  #0b0e15;
  --surface-low:     #191b23;
  --surface-ctr:     #1e2029;
  --surface-high:    #272a31;
  --surface-highest: #32353c;

  /* Brand: Red → Yellow → Blue */
  --red:       #e63946;
  --red-dark:  #b71c2c;
  --red-glow:  rgba(230,57,70,.22);
  --yellow:    #fbbf24;
  --yellow-dk: #d97706;
  --yel-glow:  rgba(251,191,36,.18);
  --blue:      #3b82f6;
  --blue-lt:   #93c5fd;
  --blue-glow: rgba(59,130,246,.20);

  /* Text */
  --on-surface:     #e3e4ea;
  --on-surface-var: #a9abb5;
  --outline:        #424754;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  font-family: 'Inter', sans-serif !important;
  background: var(--surface) !important;
  color: var(--on-surface) !important;
}

/* Ambient glow — red + yellow */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 55% 35% at 80% 5%,  rgba(230,57,70,.05)  0%, transparent 70%),
    radial-gradient(ellipse 40% 30% at 10% 90%, rgba(251,191,36,.04) 0%, transparent 70%);
  pointer-events: none; z-index: 0;
}

/* hide Streamlit chrome */
#MainMenu, footer,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebar"] { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── sticky nav ───────────────────────────────────────────────────── */
.em-nav {
  position: sticky; top: 0; z-index: 200;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 2.5rem; height: 56px;
  background: rgba(16,19,26,.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(66,71,84,.18);
}
.em-logo {
  font-size: 1.1rem; font-weight: 900; letter-spacing: -.02em;
  background: linear-gradient(135deg, var(--red) 0%, var(--yellow) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.em-logo-sub {
  font-size: .68rem; font-weight: 500; letter-spacing: .08em;
  text-transform: uppercase; color: var(--on-surface-var);
  margin-left: .6rem;
}

/* ── page wrapper ─────────────────────────────────────────────────── */
.em-page {
  max-width: 1100px; margin: 0 auto;
  padding: 3rem 2rem 6rem;
}

/* ── hero ─────────────────────────────────────────────────────────── */
.em-hero { text-align: center; margin-bottom: 2.5rem; }
.em-hero h1 {
  font-size: clamp(1.9rem, 4vw, 2.75rem);
  font-weight: 900; letter-spacing: -.03em; line-height: 1.1;
  margin-bottom: .65rem;
}
.em-hero h1 span {
  background: linear-gradient(135deg, var(--red) 0%, var(--yellow) 60%, var(--blue) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.em-hero p {
  font-size: .88rem; color: var(--on-surface-var);
  max-width: 480px; margin: 0 auto; line-height: 1.65;
}

/* ── input card ───────────────────────────────────────────────────── */
.em-input-card {
  background: var(--surface-low);
  border-radius: 1.5rem;
  padding: 2rem 2.25rem 1.75rem;
  margin-bottom: 1.5rem;
}

/* textarea override */
textarea, .stTextArea textarea {
  background: var(--surface-high) !important;
  border: 1px solid rgba(66,71,84,.35) !important;
  border-radius: .75rem !important;
  color: var(--on-surface) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: .88rem !important; line-height: 1.65 !important;
  resize: vertical !important;
  transition: border-color .2s, box-shadow .2s !important;
}
textarea:focus, .stTextArea textarea:focus {
  border-color: var(--red) !important;
  box-shadow: 0 0 0 3px rgba(230,57,70,.15), 0 2px 0 var(--red) !important;
  outline: none !important;
}

/* button override */
.stButton > button {
  background: linear-gradient(135deg, var(--red) 0%, var(--yellow) 100%) !important;
  color: #1a0a00 !important;
  font-weight: 700 !important; font-family: 'Inter', sans-serif !important;
  border: none !important; border-radius: 1rem !important;
  padding: .6rem 1.5rem !important; font-size: .85rem !important;
  letter-spacing: .01em !important; width: 100% !important;
  transition: opacity .2s, transform .15s, box-shadow .2s !important;
  box-shadow: 0 4px 20px rgba(230,57,70,.3) !important;
}
.stButton > button:hover {
  opacity: .92 !important; transform: translateY(-1px) !important;
  box-shadow: 0 8px 30px rgba(230,57,70,.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* selectbox */
.stSelectbox > div > div {
  background: var(--surface-high) !important;
  border: 1px solid rgba(66,71,84,.35) !important;
  border-radius: .75rem !important;
  color: var(--on-surface) !important;
  font-family: 'Inter', sans-serif !important;
}

.em-char { font-size: .72rem; color: var(--on-surface-var); margin-top: .4rem; }

/* ── Streamlit tabs ───────────────────────────────────────────────── */
[data-testid="stTabs"] { background: transparent !important; }
[data-testid="stTabsTabList"] {
  background: transparent !important;
  border-bottom: 1px solid rgba(66,71,84,.20) !important;
}
button[data-testid="stTabsTab"] {
  background: transparent !important; color: var(--on-surface-var) !important;
  font-family: 'Inter', sans-serif !important; font-size: .875rem !important;
  font-weight: 500 !important; border: none !important; border-radius: 0 !important;
  padding: .6rem 1.1rem !important; transition: color .2s !important;
}
button[data-testid="stTabsTab"]:hover {
  color: var(--on-surface) !important;
  background: rgba(66,71,84,.08) !important;
}
button[data-testid="stTabsTab"][aria-selected="true"] {
  color: var(--on-surface) !important;
  border-bottom: 2px solid var(--red) !important;
  margin-bottom: -1px !important;
}
[data-testid="stTabsTabPanel"] {
  padding-top: 1.5rem !important; background: transparent !important;
}

/* ── stat cards ───────────────────────────────────────────────────── */
.em-stat {
  background: var(--surface-high); border-radius: 1.5rem;
  padding: 1.5rem 1.75rem 1.75rem;
  position: relative; overflow: hidden; height: 100%;
}
.em-stat::before {
  content: ''; position: absolute; inset: 0; border-radius: inherit;
  background: linear-gradient(145deg, rgba(255,255,255,.025) 0%, transparent 60%);
  pointer-events: none;
}
.em-stat-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: .5rem;
  font-size: 13px; margin-bottom: .75rem;
}
.em-stat-icon.red    { background: rgba(230,57,70,.15); }
.em-stat-icon.yellow { background: rgba(251,191,36,.15); }
.em-stat-icon.blue   { background: rgba(59,130,246,.13); }
.em-stat-lbl {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--on-surface-var); margin-bottom: .45rem;
}
.em-stat-val {
  font-size: 1.7rem; font-weight: 800; letter-spacing: -.03em;
  color: var(--on-surface); margin-bottom: .5rem;
}
.em-stat-val.red    { color: var(--red); }
.em-stat-val.yellow { color: var(--yellow); }
.em-stat-val.blue   { color: var(--blue-lt); }
.em-stat-meta { font-size: .74rem; color: var(--on-surface-var); line-height: 1.5; }
.em-bar {
  height: 3px; background: rgba(66,71,84,.3); border-radius: 99px; overflow: hidden;
  margin-top: .85rem;
}
.em-bar-fill {
  height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, var(--red), var(--yellow));
  box-shadow: 0 0 8px var(--red-glow);
}
.em-chips { display: flex; gap: .45rem; margin-top: .7rem; flex-wrap: wrap; }
.em-chip {
  display: inline-flex; align-items: center; gap: .28rem;
  padding: .18rem .6rem; border-radius: 99px;
  font-size: .62rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
}
.em-chip::before {
  content: ''; width: 5px; height: 5px; border-radius: 50%; background: currentColor;
}
.em-chip.verified { background: rgba(59,130,246,.15); color: var(--blue-lt); }
.em-chip.pending  { background: rgba(251,191,36,.13); color: var(--yellow); }

/* ── article card ─────────────────────────────────────────────────── */
.em-article-card {
  background: var(--surface-low); border-radius: 1.5rem; padding: 2rem 2.25rem;
}
.em-legend-row {
  display: flex; align-items: center; gap: 1.25rem;
  margin-bottom: 1.5rem; padding-bottom: 1rem;
  border-bottom: 1px solid rgba(66,71,84,.15); flex-wrap: wrap;
}
.em-legend-lbl {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--on-surface-var); flex-shrink: 0;
}
.em-legend-items { display: flex; gap: 1rem; flex-wrap: wrap; }
.em-legend-item {
  display: flex; align-items: center; gap: .38rem;
  font-size: .62rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: var(--on-surface-var);
}
.em-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.em-dot.suspicious { background: var(--red);    box-shadow: 0 0 6px var(--red-glow); }
.em-dot.emotional  { background: var(--yellow); box-shadow: 0 0 6px var(--yel-glow); }
.em-dot.credible   { background: var(--blue-lt);box-shadow: 0 0 6px var(--blue-glow); }

.em-article-body { font-size: .88rem; line-height: 1.9; color: var(--on-surface); }
.em-article-body p { margin-bottom: 1.2rem; }
.em-article-body p:last-child { margin-bottom: 0; }

.hl { display: inline; padding: .08em .22em; border-radius: .22em; cursor: default; }
.hl.credible {
  background: rgba(59,130,246,.12); color: var(--blue-lt);
  text-decoration: underline; text-decoration-color: rgba(147,197,253,.3);
  text-underline-offset: 2px;
}
.hl.emotional { background: rgba(251,191,36,.13); color: var(--yellow); }
.hl.suspicious {
  background: rgba(230,57,70,.13); color: var(--red);
  text-decoration: line-through; text-decoration-color: rgba(230,57,70,.35);
}

/* ── summary ──────────────────────────────────────────────────────── */
.em-summary-card {
  background: var(--surface-low); border-radius: 1.5rem; padding: 1.75rem 2rem;
}
.em-summary-card h3 {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--on-surface-var); margin-bottom: 1.25rem;
}
.em-signal-row {
  display: flex; align-items: center; gap: .9rem; margin-bottom: .8rem;
}
.em-signal-name {
  font-size: .78rem; color: var(--on-surface-var); width: 145px; flex-shrink: 0;
}
.em-signal-track {
  flex: 1; height: 4px; background: rgba(66,71,84,.3); border-radius: 99px; overflow: hidden;
}
.em-signal-fill { height: 100%; border-radius: 99px; }
.em-signal-fill.high   { background: linear-gradient(90deg, var(--blue), var(--blue-lt)); }
.em-signal-fill.medium { background: linear-gradient(90deg, var(--yellow-dk), var(--yellow)); }
.em-signal-fill.low    { background: linear-gradient(90deg, var(--red-dark), var(--red)); }
.em-signal-pct {
  font-size: .74rem; font-weight: 600; color: var(--on-surface);
  width: 34px; text-align: right; flex-shrink: 0;
}

.em-verdict-pill {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .5rem 1rem; border-radius: 99px;
  font-size: .75rem; font-weight: 700; letter-spacing: .04em; margin-top: 1.25rem;
}
.em-verdict-pill.real    { background: rgba(59,130,246,.14);  color: var(--blue-lt); box-shadow: 0 0 20px var(--blue-glow); }
.em-verdict-pill.mid     { background: rgba(251,191,36,.14);  color: var(--yellow);  box-shadow: 0 0 20px var(--yel-glow); }
.em-verdict-pill.fake    { background: rgba(230,57,70,.16);   color: var(--red);     box-shadow: 0 0 20px var(--red-glow); }
.em-verdict-pill.unknown { background: rgba(66,71,84,.35);    color: var(--on-surface-var); }
.em-verdict-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

.em-rec-box {
  margin-top: 1.25rem; background: rgba(230,57,70,.06);
  border-radius: 1rem; padding: 1rem 1.15rem; border-left: 3px solid var(--red);
}
.em-rec-heading {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--red); margin-bottom: .45rem;
}
.em-rec-text { font-size: .8rem; color: var(--on-surface-var); line-height: 1.6; }

/* ── technical breakdown ─────────────────────────────────────────── */
.em-metric-card {
  background: var(--surface-high); border-radius: 1.5rem;
  padding: 1.5rem 1.6rem; position: relative; overflow: hidden;
}
.em-metric-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(145deg, rgba(255,255,255,.02) 0%, transparent 55%);
  pointer-events: none;
}
.em-metric-lbl {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--on-surface-var); margin-bottom: .5rem;
}
.em-metric-val { font-size: 2rem; font-weight: 800; letter-spacing: -.04em; }
.em-metric-val.blue   { color: var(--blue-lt); text-shadow: 0 0 20px var(--blue-glow); }
.em-metric-val.yellow { color: var(--yellow);  text-shadow: 0 0 20px var(--yel-glow); }
.em-metric-val.red    { color: var(--red);     text-shadow: 0 0 20px var(--red-glow); }
.em-metric-suffix { font-size: 1rem; font-weight: 500; color: var(--on-surface-var); }

.em-pt-wrap { background: var(--surface-low); border-radius: 1.5rem; overflow: hidden; margin-top: 1.25rem; }
.em-pt-header {
  display: grid; grid-template-columns: 1fr 110px 80px;
  padding: .7rem 1.75rem; background: var(--surface-ctr);
}
.em-pt-header span {
  font-size: .62rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--on-surface-var);
}
.em-pt-row {
  display: grid; grid-template-columns: 1fr 110px 80px;
  align-items: center; padding: .85rem 1.75rem; gap: 1rem;
  border-top: 1px solid rgba(66,71,84,.10); transition: background .18s;
}
.em-pt-row:hover { background: rgba(66,71,84,.08); }
.em-pt-name { font-size: .82rem; color: var(--on-surface); }
.em-pt-mini { height: 4px; background: rgba(66,71,84,.3); border-radius: 99px; overflow: hidden; }
.em-pt-fill { height: 100%; border-radius: 99px; }
.em-pt-fill.low    { background: linear-gradient(90deg, var(--red-dark), var(--red)); }
.em-pt-fill.medium { background: linear-gradient(90deg, var(--yellow-dk), var(--yellow)); }
.em-pt-fill.ok     { background: linear-gradient(90deg, var(--blue), var(--blue-lt)); }
.em-badge { display: inline-block; padding: .14rem .52rem; border-radius: 99px; font-size: .62rem; font-weight: 700; letter-spacing: .05em; }
.em-badge.low    { background: rgba(230,57,70,.16);  color: var(--red); }
.em-badge.medium { background: rgba(251,191,36,.14); color: var(--yellow); }
.em-badge.ok     { background: rgba(59,130,246,.13); color: var(--blue-lt); }

/* ── claims ───────────────────────────────────────────────────────── */
.em-claim {
  background: var(--surface-low); border-radius: 1rem;
  padding: 1.1rem 1.35rem; border-left: 3px solid var(--red); margin-bottom: .9rem;
}
.em-claim-num {
  font-size: .62rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: var(--red); margin-bottom: .4rem;
}
.em-claim-text { font-size: .84rem; color: var(--on-surface); font-style: italic; line-height: 1.65; }
.em-no-claims {
  background: rgba(59,130,246,.06); border-radius: 1rem;
  padding: 1.25rem 1.5rem; border-left: 3px solid var(--blue);
  font-size: .84rem; color: var(--on-surface-var); line-height: 1.6;
}

/* ── explain box ──────────────────────────────────────────────────── */
.em-explain {
  background: var(--surface-low); border-radius: 1.25rem;
  padding: 1.5rem 1.75rem; font-size: .86rem; color: var(--on-surface-var);
  line-height: 1.75; margin-bottom: 1.1rem;
}
.em-action-box { border-radius: 1.25rem; padding: 1.25rem 1.5rem; font-size: .86rem; line-height: 1.65; }
.em-action-box.high-risk   { background: rgba(230,57,70,.10); border-left: 3px solid var(--red);    color: var(--red); }
.em-action-box.medium-risk { background: rgba(251,191,36,.10); border-left: 3px solid var(--yellow); color: var(--yellow); }
.em-action-box.low-risk    { background: rgba(59,130,246,.08); border-left: 3px solid var(--blue);   color: var(--blue-lt); }

/* ── empty state ─────────────────────────────────────────────────── */
.em-empty { text-align: center; padding: 4rem 2rem; color: var(--on-surface-var); }
.em-empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: .35; }
.em-empty-text { font-size: .9rem; line-height: 1.65; max-width: 380px; margin: 0 auto; }

/* ── footer ───────────────────────────────────────────────────────── */
.em-footer {
  margin-top: 4rem; display: flex; align-items: center;
  justify-content: space-between; padding: 1.5rem 0;
  border-top: 1px solid rgba(66,71,84,.14);
  font-size: .72rem; color: var(--on-surface-var); flex-wrap: wrap; gap: 1rem;
}
.em-footer-logo {
  font-size: .95rem; font-weight: 900; letter-spacing: -.01em;
  background: linear-gradient(135deg, var(--red) 0%, var(--yellow) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--surface-low); }
::-webkit-scrollbar-thumb { background: var(--outline); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def load_model():
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    mp = os.path.join(model_dir, "best_model.joblib")
    vp = os.path.join(model_dir, "tfidf_vectorizer.joblib")
    if not os.path.exists(mp) or not os.path.exists(vp):
        raise FileNotFoundError(
            "Model files not found in models/. Run `python train_model.py` first."
        )
    return joblib.load(mp), joblib.load(vp)


@st.cache_resource
def load_analyzer():
    return CredibilityAnalyzer()


EXAMPLES = {
    "Credible — Vaccine Clinical Trial": """Scientists at Stanford University have published a peer-reviewed study in the journal Nature showing that a new vaccine candidate demonstrates 89% efficacy in phase 3 clinical trials involving 30,000 participants across 15 countries.

Dr. Sarah Chen, lead researcher at Stanford's Department of Immunology, stated that the results would be submitted to the FDA for emergency use authorization within the next month.

The study tracked participants for an average of 6 months following vaccination. The research team reported that serious adverse events occurred in less than 0.1% of participants, comparable to rates seen with other approved vaccines.

Independent experts praised the rigorous methodology. Dr. Michael Rodriguez, an epidemiologist at Johns Hopkins University, noted that the sample size is robust and the data sharing is commendable.""",

    "Suspicious — Conspiracy Article": """SHOCKING DISCOVERY: Government Scientists ADMIT Vaccines Contain Dangerous Chemicals That Big Pharma Doesn't Want You to Know About!!!

An EXPLOSIVE new report reveals that mainstream media has been HIDING the truth. Anonymous sources close to the CDC have leaked documents showing that pharmaceutical companies are adding mysterious substances to vaccines without proper testing.

Experts say this could be the biggest cover-up in medical history! Many believe doctors are being SILENCED by powerful corporations who control the entire healthcare system.

They don't want you to know the truth. Wake up, people! Don't let them inject you with unknown substances. Share this before it gets censored!""",
}

MIN_LEN, MAX_LEN = 50, 50_000


# ── HTML component builders ────────────────────────────────────────────────

def ring_html(score: int, classification: str) -> str:
    colors = {
        "REAL":       ("#3b82f6", "#93c5fd"),
        "MISLEADING": ("#d97706", "#fbbf24"),
        "FAKE":       ("#b71c2c", "#e63946"),
        "UNVERIFIED": ("#424754", "#a9abb5"),
    }
    c1, c2 = colors.get(classification, colors["UNVERIFIED"])
    circ = 2 * 3.14159 * 86
    offset = circ * (1 - score / 100)
    return f"""
<div style="display:flex;justify-content:center;margin:1.5rem 0 2rem">
 <div style="position:relative;width:200px;height:200px">
  <svg viewBox="0 0 200 200" width="200" height="200"
       style="position:absolute;inset:0;transform:rotate(-90deg);
              filter:drop-shadow(0 0 18px {c1}55)">
   <defs>
    <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%">
     <stop offset="0%" stop-color="{c1}"/>
     <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
   </defs>
   <circle cx="100" cy="100" r="86" fill="none" stroke="rgba(66,71,84,.25)" stroke-width="10"/>
   <circle cx="100" cy="100" r="86" fill="none" stroke="url(#rg)" stroke-width="10"
           stroke-linecap="round"
           stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}"/>
  </svg>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;
              align-items:center;justify-content:center">
   <div style="font-size:2.6rem;font-weight:900;letter-spacing:-.04em;
               background:linear-gradient(135deg,{c2} 0%,{c1} 100%);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;line-height:1">{score}%</div>
   <div style="font-size:.62rem;font-weight:700;letter-spacing:.12em;
               text-transform:uppercase;color:#a9abb5;margin-top:.35rem">
    {classification}
   </div>
  </div>
 </div>
</div>"""


def stat_ml(confidence: int) -> str:
    label = "High Accuracy" if confidence >= 75 else "Moderate Accuracy"
    return f"""<div class="em-stat">
  <div class="em-stat-icon blue">🧠</div>
  <div class="em-stat-lbl">ML Prediction</div>
  <div class="em-stat-val blue">{label}</div>
  <div class="em-bar"><div class="em-bar-fill" style="width:{confidence}%"></div></div>
</div>"""


def stat_patterns(anomalies: int, meta: str) -> str:
    cls = "yellow" if anomalies > 0 else ""
    return f"""<div class="em-stat">
  <div class="em-stat-icon yellow">⚠</div>
  <div class="em-stat-lbl">Pattern Detection</div>
  <div class="em-stat-val {cls}">{anomalies} Anomali{'es' if anomalies != 1 else 'y'}</div>
  <div class="em-stat-meta">{meta}</div>
</div>"""


def stat_claims(total: int, verified: int, pending: int) -> str:
    return f"""<div class="em-stat">
  <div class="em-stat-icon red">📋</div>
  <div class="em-stat-lbl">Flagged Claims</div>
  <div class="em-stat-val red">{total} Detected</div>
  <div class="em-chips">
    <span class="em-chip verified">{verified} Verified</span>
    <span class="em-chip pending">{pending} Pending</span>
  </div>
</div>"""


def verdict_pill(classification: str, score: int) -> str:
    if score >= 75:
        cls, label = "real",    "High Credibility"
    elif score >= 40:
        cls, label = "mid",     "Moderate Credibility"
    elif classification == "UNVERIFIED":
        cls, label = "unknown", "Unverified"
    else:
        cls, label = "fake",    "Low Credibility"
    return f'<span class="em-verdict-pill {cls}"><span class="em-verdict-dot"></span>{label}</span>'


def signal_bar(name: str, pct: int, level: str) -> str:
    return f"""<div class="em-signal-row">
  <span class="em-signal-name">{name}</span>
  <div class="em-signal-track">
    <div class="em-signal-fill {level}" style="width:{pct}%"></div>
  </div>
  <span class="em-signal-pct">{pct}%</span>
</div>"""


def pt_row(name: str, width: int, level: str) -> str:
    badge = {"low": "High", "medium": "Moderate", "ok": "Clean"}.get(level, "—")
    return f"""<div class="em-pt-row">
  <span class="em-pt-name">{name}</span>
  <div class="em-pt-mini"><div class="em-pt-fill {level}" style="width:{width}%"></div></div>
  <span class="em-badge {level}">{badge}</span>
</div>"""


def count_anomalies(p: Dict) -> int:
    return sum([
        p.get("sensational_phrases", 0) > 3,
        p.get("excessive_caps", 0) > 0.1,
        p.get("vague_sources", 0) > 2,
        p.get("conspiracy_framing", 0) > 0,
        p.get("emotional_manipulation", 0) > 2,
        p.get("one_sided", 0) > 0.7,
        p.get("no_evidence", 0) > 0.7,
        p.get("extreme_adjectives", 0) > 5,
        p.get("clickbait", 0) > 0,
    ])


def plevel(v: float, lo=.35, hi=.65) -> str:
    if v >= hi: return "low"
    if v >= lo: return "medium"
    return "ok"


def build_article_html(text: str, suspicious: List[str]) -> str:
    import html as hl
    safe = hl.escape(text)
    for claim in suspicious:
        sc = hl.escape(claim.strip())
        if sc and sc in safe:
            safe = safe.replace(sc, f'<span class="hl suspicious">{sc}</span>', 1)
    paras = safe.split("\n\n") if "\n\n" in safe else safe.split("\n")
    return "".join(f"<p>{p.strip()}</p>" for p in paras if p.strip())


# ══════════════════════════════════════════════════════════════════════════════
#  RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render_nav():
    st.markdown("""
<nav class="em-nav">
  <div style="display:flex;align-items:center">
    <span class="em-logo">El Matador</span>
    <span class="em-logo-sub">News Credibility Analyzer</span>
  </div>
</nav>""", unsafe_allow_html=True)


def render_hero():
    st.markdown("""
<div class="em-hero">
  <h1><span>Analysis Results</span></h1>
  <p>Real-time breakdown of linguistic patterns, factual claims, and overall credibility signals.</p>
</div>""", unsafe_allow_html=True)


def render_input() -> Tuple[str, bool]:
    st.markdown('<div class="em-input-card">', unsafe_allow_html=True)

    opts = ["— Paste your own article —"] + list(EXAMPLES.keys())
    sel = st.selectbox("Load example", opts, key="ex_pick", label_visibility="collapsed")
    if sel != opts[0]:
        st.session_state.article_text = EXAMPLES[sel]

    if "article_text" not in st.session_state:
        st.session_state.article_text = ""

    text = st.text_area(
        "Article", value=st.session_state.article_text,
        height=220, key="article_input",
        placeholder="Paste news article text here (minimum 50 characters)…",
        label_visibility="collapsed",
    )
    st.session_state.article_text = text

    n = len(text)
    if 0 < n < MIN_LEN:
        st.markdown(f'<div class="em-char" style="color:var(--red)">'
                    f'{n} / {MIN_LEN} minimum characters required</div>',
                    unsafe_allow_html=True)
    elif n > 0:
        st.markdown(f'<div class="em-char">{n:,} characters</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    clicked = st.button("Analyze Article →", disabled=(n < MIN_LEN or n > MAX_LEN), key="btn_analyze")
    return text, clicked


def render_results(result: Dict, text: str):
    cls   = result["classification"]
    score = result["credibility_score"]
    conf  = result["confidence"]
    risk  = result["risk_level"]
    pats  = result.get("patterns", {})
    susp  = result.get("suspicious_claims", [])
    inds  = result.get("key_indicators", [])
    tone  = result.get("emotional_tone", "N/A")
    summ  = result.get("analysis_summary", "")
    expl  = result.get("explanation", "")
    rec   = result.get("recommended_action", "")
    pscore = result.get("pattern_score", 0.0)
    anomalies = count_anomalies(pats)

    # Ring
    st.markdown(ring_html(score, cls), unsafe_allow_html=True)

    # Stat cards
    c1, c2, c3 = st.columns(3, gap="medium")
    meta = (", ".join(inds[:2]) if inds else "No major anomalies detected.")[:80]
    verified = max(0, len(susp) - len([s for s in susp if "vague" in s.lower()]))
    pending  = len(susp) - verified
    with c1: st.markdown(stat_ml(conf), unsafe_allow_html=True)
    with c2: st.markdown(stat_patterns(anomalies, meta), unsafe_allow_html=True)
    with c3: st.markdown(stat_claims(len(susp), verified, pending), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    t1, t2, t3 = st.tabs(["Summary", "Highlighted Article", "Technical Breakdown"])

    # ── Summary ──────────────────────────────────────────────────────────
    with t1:
        left, right = st.columns([1.4, 1], gap="medium")

        with left:
            ps = int((1 - pscore) * 100)
            em = int(min(1, pats.get("emotional_manipulation", 0) / 4) * 100)
            vg = int(min(1, pats.get("vague_sources", 0) / 3) * 100)
            ev = int((1 - pats.get("no_evidence", 0)) * 100)
            co = int(min(1, pats.get("conspiracy_framing", 0) / 2) * 100)
            bl = int((1 - pats.get("one_sided", 0)) * 100)

            def lvl(v, inv=False):
                vn = v / 100
                if inv: return "high" if vn >= .65 else ("medium" if vn >= .4 else "low")
                return "low" if vn >= .65 else ("medium" if vn >= .35 else "ok")

            bars = (
                signal_bar("Source Credibility",  ps, "high" if ps >= 65 else ("medium" if ps >= 40 else "low")) +
                signal_bar("Emotional Language",   em, "low"  if em >= 65 else ("medium" if em >= 35 else "ok")) +
                signal_bar("Vague Attribution",    vg, "low"  if vg >= 65 else ("medium" if vg >= 35 else "ok")) +
                signal_bar("Evidence Density",     ev, "high" if ev >= 65 else ("medium" if ev >= 40 else "low")) +
                signal_bar("Conspiracy Framing",   co, "low"  if co >= 65 else ("medium" if co >= 35 else "ok")) +
                signal_bar("Narrative Balance",    bl, "high" if bl >= 65 else ("medium" if bl >= 40 else "low"))
            )
            st.markdown(f"""<div class="em-summary-card">
  <h3>Signal Breakdown</h3>{bars}{verdict_pill(cls, score)}
</div>""", unsafe_allow_html=True)

        with right:
            if "neutral" in tone.lower():
                tone_cls = "real"
            elif "highly" in tone.lower():
                tone_cls = "fake"
            else:
                tone_cls = "mid"
            st.markdown(f"""<div class="em-summary-card">
  <h3>Assessment</h3>
  <p style="font-size:.85rem;color:var(--on-surface-var);line-height:1.7;margin-bottom:1rem">{summ}</p>
  <div class="em-rec-box">
    <div class="em-rec-heading">Recommendation</div>
    <div class="em-rec-text">{rec}</div>
  </div>
  <div style="margin-top:1.35rem">
    <div style="font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
                color:var(--on-surface-var);margin-bottom:.65rem">Emotional Tone</div>
    <span class="em-verdict-pill {tone_cls}">
      <span class="em-verdict-dot"></span>{tone}
    </span>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Highlighted Article ───────────────────────────────────────────────
    with t2:
        body = build_article_html(text, susp)
        st.markdown(f"""<div class="em-article-card">
  <div class="em-legend-row">
    <span class="em-legend-lbl">Legend:</span>
    <div class="em-legend-items">
      <span class="em-legend-item"><span class="em-dot suspicious"></span>Suspicious</span>
      <span class="em-legend-item"><span class="em-dot emotional"></span>Emotional</span>
      <span class="em-legend-item"><span class="em-dot credible"></span>Credible</span>
    </div>
  </div>
  <div class="em-article-body">{body}</div>
</div>""", unsafe_allow_html=True)

    # ── Technical Breakdown ───────────────────────────────────────────────
    with t3:
        m1, m2, m3 = st.columns(3, gap="medium")
        with m1:
            st.markdown(f"""<div class="em-metric-card">
  <div class="em-metric-lbl">Model Confidence</div>
  <div class="em-metric-val blue">{conf}<span class="em-metric-suffix">%</span></div>
</div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="em-metric-card">
  <div class="em-metric-lbl">Pattern Score</div>
  <div class="em-metric-val yellow">{pscore:.2f}</div>
</div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="em-metric-card">
  <div class="em-metric-lbl">Suspicious Claims</div>
  <div class="em-metric-val red">{len(susp)}</div>
</div>""", unsafe_allow_html=True)

        def prow(key, label, maxv, invert=False):
            raw = pats.get(key, 0)
            pct = int(min(100, (raw / maxv) * 100)) if maxv else 0
            lvl = plevel(pct / 100)
            if invert:
                lvl = {"low": "ok", "ok": "low", "medium": "medium"}.get(lvl, lvl)
                pct = 100 - pct
            return pt_row(label, pct, lvl)

        rows = "".join([
            prow("sensational_phrases",    "Sensational Language",    5),
            prow("vague_sources",          "Vague Source References", 3),
            prow("conspiracy_framing",     "Conspiracy Framing",      2),
            prow("no_evidence",            "Evidence Density",        1, invert=True),
            prow("emotional_manipulation", "Emotional Manipulation",  4),
            prow("excessive_caps",         "Excessive Capitalization",0.3),
            prow("clickbait",              "Clickbait Patterns",      2),
            prow("one_sided",              "One-Sided Narrative",     1),
        ])
        st.markdown(f"""<div class="em-pt-wrap">
  <div class="em-pt-header"><span>Pattern</span><span>Intensity</span><span>Rating</span></div>
  {rows}
</div>""", unsafe_allow_html=True)

        # Flagged claims
        st.markdown("<br><div style='font-size:.62rem;font-weight:700;letter-spacing:.1em;"
                    "text-transform:uppercase;color:var(--on-surface-var);margin-bottom:.85rem'>"
                    "Flagged Claims</div>", unsafe_allow_html=True)
        if susp:
            st.markdown("".join(
                f'<div class="em-claim"><div class="em-claim-num">Claim #{i+1}</div>'
                f'<div class="em-claim-text">"{c.strip()}"</div></div>'
                for i, c in enumerate(susp[:5])
            ), unsafe_allow_html=True)
        else:
            st.markdown('<div class="em-no-claims">No highly suspicious claims detected. '
                        'Always verify important claims through authoritative sources.</div>',
                        unsafe_allow_html=True)

        # Explanation
        st.markdown("<br>", unsafe_allow_html=True)
        action_cls = {"High Risk": "high-risk", "Medium Risk": "medium-risk", "Low Risk": "low-risk"}.get(risk, "medium-risk")
        st.markdown(f"""<div style="font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
color:var(--on-surface-var);margin-bottom:.85rem">Detailed Explanation</div>
<div class="em-explain">{expl}</div>
<div class="em-action-box {action_cls}">{rec}</div>""", unsafe_allow_html=True)


def render_empty():
    st.markdown("""<div class="em-empty">
  <div class="em-empty-icon">🎯</div>
  <div class="em-empty-text">
    Paste a news article above and click <strong>Analyze Article</strong>
    to see a full credibility breakdown — score, patterns, highlighted claims, and more.
  </div>
</div>""", unsafe_allow_html=True)


def render_footer():
    st.markdown("""<div class="em-footer">
  <span class="em-footer-logo">El Matador</span>
  <span>© 2024 El Matador. News Credibility Analyzer.</span>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    inject_css()
    render_nav()

    st.markdown('<div class="em-page">', unsafe_allow_html=True)
    render_hero()

    try:
        with st.spinner("Loading model…"):
            model, vectorizer = load_model()
            analyzer = load_analyzer()
    except FileNotFoundError as e:
        st.error(f"**Model not found** — {e}")
        st.info("Run `python train_model.py` to train the model, then restart the app.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    text, clicked = render_input()

    if "results" not in st.session_state:
        st.session_state.results = None

    if clicked and text.strip():
        with st.spinner("Analyzing…"):
            try:
                st.session_state.results = analyzer.analyze(text, model, vectorizer)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.session_state.results = None

    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.results:
        render_results(st.session_state.results, text)
    else:
        render_empty()

    render_footer()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
