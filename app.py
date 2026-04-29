"""
DNA Sequence Analyzer – VTU Biology for Engineers Project
app.py – Streamlit web app with premium dark theme matching the desktop version
"""

import streamlit as st
from analyzer import DNAAnalyzer
from utils import validate_sequence

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🧬 DNA Sequence Analyzer – VTU Project",
    page_icon="🧬",
    layout="centered",
)

# ──────────────────────────────────────────────
# Sample DNA sequences for suggestions
# ──────────────────────────────────────────────
SAMPLE_SEQUENCES = {
    "🧪 Simple Test Sequence": "ATGCGTAC",
    "💉 Insulin Gene Fragment": "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTG",
    "🔬 BRCA1 Exon Snippet": "ATGCGTACGATCGATCGATCGTAGCTAGCTAGCTA",
    "🟢 GFP Start Codon Region": "ATGAGTAAAGGAGAAGAACTTTTCACTGGAGTTGTC",
    "🩸 Hemoglobin Beta Chain": "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTT",
    "🧫 Lac Operon Promoter": "TTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGG",
    "🦠 COVID-19 Spike Fragment": "ATGTTTGTTTTTCTTGTTTTATTGCCACTAGTCTCTAGTCAGT",
    "🛡️ p53 Tumor Suppressor Start": "ATGGAGGAGCCGCAGTCAGATCCTAGCGTGAGTTTGC",
}

# ──────────────────────────────────────────────
# Inject full custom CSS to match the Tkinter dark theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Root variables ── */
:root {
    --bg-dark: #0D1117;
    --bg-card: #161B22;
    --bg-input: #1C2333;
    --border: #30363D;
    --accent-cyan: #58A6FF;
    --accent-green: #3FB950;
    --accent-purple: #BC8CFF;
    --accent-pink: #F778BA;
    --accent-orange: #F0883E;
    --text-primary: #E6EDF3;
    --text-secondary: #8B949E;
    --text-muted: #484F58;
}

/* ── Global overrides ── */
.stApp {
    background-color: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif !important;
}
header { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Animated DNA helix background ── */
@keyframes helixFloat {
    0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.08; }
    50% { transform: translateY(-20px) rotate(180deg); opacity: 0.15; }
}
@keyframes particleDrift {
    0% { transform: translateY(0) translateX(0); opacity: 0; }
    20% { opacity: 0.6; }
    80% { opacity: 0.6; }
    100% { transform: translateY(-100vh) translateX(30px); opacity: 0; }
}
.stApp::before {
    content: '🧬';
    position: fixed;
    right: 40px;
    top: 20%;
    font-size: 120px;
    animation: helixFloat 6s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
    filter: grayscale(50%);
}
.stApp::after {
    content: '🧬';
    position: fixed;
    right: 60px;
    bottom: 15%;
    font-size: 80px;
    animation: helixFloat 8s ease-in-out infinite reverse;
    pointer-events: none;
    z-index: 0;
    filter: grayscale(50%);
}

/* ── Floating particles ── */
.particles {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0; left: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.particle {
    position: absolute;
    width: 4px; height: 4px;
    background: var(--accent-cyan);
    border-radius: 50%;
    animation: particleDrift linear infinite;
}
.particle:nth-child(1) { left: 10%; animation-duration: 12s; animation-delay: 0s; }
.particle:nth-child(2) { left: 25%; animation-duration: 15s; animation-delay: 2s; background: var(--accent-purple); }
.particle:nth-child(3) { left: 40%; animation-duration: 10s; animation-delay: 4s; background: var(--accent-pink); }
.particle:nth-child(4) { left: 55%; animation-duration: 18s; animation-delay: 1s; }
.particle:nth-child(5) { left: 70%; animation-duration: 14s; animation-delay: 3s; background: var(--accent-green); }
.particle:nth-child(6) { left: 85%; animation-duration: 11s; animation-delay: 5s; background: var(--accent-orange); }
.particle:nth-child(7) { left: 15%; animation-duration: 16s; animation-delay: 6s; background: var(--accent-purple); }
.particle:nth-child(8) { left: 90%; animation-duration: 13s; animation-delay: 2s; }

/* ── Main container card ── */
.main-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px;
    position: relative;
    z-index: 1;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    backdrop-filter: blur(10px);
}

/* ── Title Section ── */
.app-title {
    font-family: 'Inter', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.5px;
}
.app-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* ── Gradient accent bar ── */
.gradient-bar {
    height: 3px;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple), var(--accent-pink), var(--accent-orange));
    margin: 18px 0 24px 0;
}

/* ── Input section label ── */
.input-label {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}
.input-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 10px;
}

/* ── Streamlit text_area & selectbox override ── */
.stTextArea textarea {
    background-color: var(--bg-input) !important;
    color: var(--accent-cyan) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    font-size: 15px !important;
    padding: 14px !important;
    transition: border-color 0.3s ease !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15) !important;
}
.stTextArea label, .stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] {
    background-color: var(--bg-input) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background-color: var(--bg-input) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Button overrides ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.25s ease !important;
    border: none !important;
}
.stButton > button[kind="primary"],
.stButton > button:first-child {
    background: var(--accent-cyan) !important;
    color: var(--bg-dark) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button:first-child:hover {
    background: #79B8FF !important;
    box-shadow: 0 4px 16px rgba(88, 166, 255, 0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Result cards ── */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.result-card:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 4px 20px rgba(88, 166, 255, 0.08);
}
.card-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 6px;
}
.card-value {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 26px;
    font-weight: 700;
    margin: 0;
}
.card-value-sm {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 15px;
    font-weight: 600;
    word-break: break-all;
    line-height: 1.6;
}

/* ── Progress bars ── */
.bar-track {
    background: var(--border);
    border-radius: 4px;
    height: 8px;
    margin-top: 10px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s ease;
}

/* ── Nucleotide frequency mini bars ── */
.freq-row {
    display: flex;
    align-items: center;
    margin: 5px 0;
    gap: 8px;
}
.freq-label {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 13px;
    width: 20px;
    text-align: center;
}
.freq-track {
    flex: 1;
    background: var(--border);
    border-radius: 3px;
    height: 6px;
    overflow: hidden;
}
.freq-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s ease;
}
.freq-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--text-secondary);
    width: 30px;
    text-align: right;
}

/* ── Sequence info bar ── */
.seq-info {
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 16px;
}

/* ── Results header ── */
.results-header {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 24px 0 16px 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 12px;
    margin-top: 30px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
}

/* ── Dot indicator ── */
.dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}

/* ── Error/warning override ── */
.stAlert { border-radius: 10px !important; }
</style>

<!-- Floating particles background -->
<div class="particles">
    <div class="particle"></div><div class="particle"></div>
    <div class="particle"></div><div class="particle"></div>
    <div class="particle"></div><div class="particle"></div>
    <div class="particle"></div><div class="particle"></div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Main Card Container Start
# ──────────────────────────────────────────────
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Title
st.markdown("""
<div style="display: flex; align-items: center; gap: 14px;">
    <span style="font-size: 42px;">🧬</span>
    <div>
        <p class="app-title">DNA Sequence Analyzer</p>
        <p class="app-subtitle">VTU Biology for Engineers Project</p>
    </div>
</div>
<div class="gradient-bar"></div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Input Section
# ──────────────────────────────────────────────
st.markdown('<p class="input-label">Enter DNA Sequence</p>', unsafe_allow_html=True)
st.markdown('<p class="input-hint">Only nucleotides A, T, G, C are accepted</p>', unsafe_allow_html=True)

# Session state for the sequence
if "seq_value" not in st.session_state:
    st.session_state.seq_value = ""

sequence_input = st.text_area(
    "DNA Sequence",
    value=st.session_state.seq_value,
    height=100,
    placeholder="e.g.  ATGCGTAC",
    label_visibility="collapsed",
)

# Suggestion dropdown
st.markdown('<p class="input-hint" style="margin-top:8px;">💡 Or pick a sample sequence:</p>', unsafe_allow_html=True)
selected_sample = st.selectbox(
    "Sample Sequences",
    options=["— Select a sample sequence —"] + list(SAMPLE_SEQUENCES.keys()),
    label_visibility="collapsed",
)

if selected_sample != "— Select a sample sequence —":
    st.session_state.seq_value = SAMPLE_SEQUENCES[selected_sample]
    st.rerun()

# Buttons
col_analyze, col_clear, _ = st.columns([2, 1, 3])
with col_analyze:
    analyze_clicked = st.button("⚡  Analyze Sequence", type="primary", use_container_width=True)
with col_clear:
    if st.button("🗑  Clear", use_container_width=True):
        st.session_state.seq_value = ""
        st.rerun()

# ──────────────────────────────────────────────
# Analysis Logic
# ──────────────────────────────────────────────
if analyze_clicked:
    sequence = sequence_input.strip().upper()

    if not sequence:
        st.warning("⚠️  Please enter a DNA sequence.")
    elif not validate_sequence(sequence):
        st.error("❌  Invalid sequence. Only A, T, G, and C are allowed.")
    else:
        analyzer = DNAAnalyzer(sequence)
        gc = analyzer.gc_content()
        rev_comp = analyzer.reverse_complement()
        counts = analyzer.nucleotide_count()
        total = sum(counts.values())

        # ── Results Header ──
        st.markdown('<p class="results-header">📊  Analysis Results</p>', unsafe_allow_html=True)

        # ── Sequence Info Bar ──
        display_seq = sequence[:50] + ("…" if len(sequence) > 50 else "")
        st.markdown(f'<div class="seq-info">Sequence Length: <strong>{len(sequence)} bp</strong>  ·  Input: <code>{display_seq}</code></div>', unsafe_allow_html=True)

        # ── Row 1: GC Content + Sequence Length ──
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.markdown(f"""
            <div class="result-card">
                <div class="card-label"><span class="dot" style="background:#3FB950;"></span>GC Content</div>
                <p class="card-value" style="color:#3FB950;">{gc:.2f}%</p>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{gc}%; background: linear-gradient(90deg, #3FB950, #58A6FF);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with r1c2:
            at_count = counts['A'] + counts['T']
            gc_count = counts['G'] + counts['C']
            st.markdown(f"""
            <div class="result-card">
                <div class="card-label"><span class="dot" style="background:#F0883E;"></span>Sequence Stats</div>
                <p class="card-value" style="color:#F0883E; font-size:20px;">AT: {at_count} ({at_count/total*100:.1f}%)  ·  GC: {gc_count} ({gc_count/total*100:.1f}%)</p>
                <div class="bar-track" style="margin-top:10px;">
                    <div class="bar-fill" style="width:{at_count/total*100}%; background: linear-gradient(90deg, #F778BA, #F0883E);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Row 2: Reverse Complement ──
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label"><span class="dot" style="background:#BC8CFF;"></span>Reverse Complement</div>
            <p class="card-value-sm" style="color:#BC8CFF;">{rev_comp}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Row 3: Nucleotide Frequency ──
        nuc_colors = {'A': '#58A6FF', 'T': '#F778BA', 'G': '#3FB950', 'C': '#F0883E'}

        freq_bars_html = ""
        for base in ['A', 'T', 'G', 'C']:
            pct = (counts[base] / total * 100) if total > 0 else 0
            color = nuc_colors[base]
            freq_bars_html += f"""
            <div class="freq-row">
                <span class="freq-label" style="color:{color};">{base}</span>
                <div class="freq-track">
                    <div class="freq-fill" style="width:{pct}%; background:{color};"></div>
                </div>
                <span class="freq-count">{counts[base]}</span>
            </div>
            """

        st.markdown(f"""
        <div class="result-card">
            <div class="card-label"><span class="dot" style="background:#58A6FF;"></span>Nucleotide Frequency</div>
            <p class="card-value" style="color:#E6EDF3; font-size:16px; margin-bottom:8px;">
                A:{counts['A']}  T:{counts['T']}  G:{counts['G']}  C:{counts['C']}
            </p>
            {freq_bars_html}
        </div>
        """, unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    Built with Python & Streamlit  ·  VTU 4th Semester Biology for Engineers Project
</div>
""", unsafe_allow_html=True)

# Close main card
st.markdown('</div>', unsafe_allow_html=True)
