/**
 * DNA Sequence Analyzer – Core Logic & UI Interactions
 * Ports the Python analyzer.py logic to JavaScript
 */

// ════════════════════════════════════
// DNA Analysis Functions
// ════════════════════════════════════

/** Validate that the sequence contains only A, T, G, C */
function isValidSequence(seq) {
    if (!seq || seq.length === 0) return false;
    return /^[ATGC]+$/i.test(seq);
}

/** Calculate GC content as a percentage */
function gcContent(seq) {
    const upper = seq.toUpperCase();
    const gc = (upper.split('G').length - 1) + (upper.split('C').length - 1);
    return (gc / upper.length) * 100;
}

/** Generate reverse complement */
function reverseComplement(seq) {
    const complement = { A: 'T', T: 'A', G: 'C', C: 'G' };
    return seq.toUpperCase().split('').reverse().map(b => complement[b]).join('');
}

/** Count nucleotide frequencies */
function nucleotideCount(seq) {
    const upper = seq.toUpperCase();
    return {
        A: (upper.match(/A/g) || []).length,
        T: (upper.match(/T/g) || []).length,
        G: (upper.match(/G/g) || []).length,
        C: (upper.match(/C/g) || []).length,
    };
}

// ════════════════════════════════════
// UI Event Handlers
// ════════════════════════════════════

const NUC_COLORS = { A: '#58A6FF', T: '#F778BA', G: '#3FB950', C: '#F0883E' };

/** Main analyze function – called by the Analyze button */
function analyzeSequence() {
    const input = document.getElementById('dna-input').value.trim();
    const errorEl = document.getElementById('errorMsg');
    const resultsEl = document.getElementById('resultsSection');

    // Hide previous
    errorEl.classList.remove('visible');
    resultsEl.classList.add('hidden');

    if (!input) {
        showError('⚠️  Please enter a DNA sequence.');
        return;
    }
    if (!isValidSequence(input)) {
        showError('❌  Invalid sequence. Only A, T, G, and C are allowed.');
        return;
    }

    const seq = input.toUpperCase();
    const gc = gcContent(seq);
    const revComp = reverseComplement(seq);
    const counts = nucleotideCount(seq);
    const total = counts.A + counts.T + counts.G + counts.C;
    const atCount = counts.A + counts.T;
    const gcCount = counts.G + counts.C;

    // Sequence info bar
    const displaySeq = seq.length > 50 ? seq.slice(0, 50) + '…' : seq;
    document.getElementById('seqInfo').innerHTML =
        `Sequence Length: <strong>${seq.length} bp</strong> &middot; Input: <code>${displaySeq}</code>`;

    // GC Content
    document.getElementById('gcValue').textContent = gc.toFixed(2) + '%';

    // Stats
    document.getElementById('statsValue').textContent =
        `AT: ${atCount} (${(atCount / total * 100).toFixed(1)}%)  ·  GC: ${gcCount} (${(gcCount / total * 100).toFixed(1)}%)`;

    // Reverse Complement
    document.getElementById('revCompValue').textContent = revComp;

    // Frequency summary
    document.getElementById('freqSummary').textContent =
        `A:${counts.A}  T:${counts.T}  G:${counts.G}  C:${counts.C}`;

    // Frequency bars
    const barsContainer = document.getElementById('freqBars');
    barsContainer.innerHTML = '';
    for (const base of ['A', 'T', 'G', 'C']) {
        const pct = total > 0 ? (counts[base] / total * 100) : 0;
        const row = document.createElement('div');
        row.className = 'freq-row';
        row.innerHTML = `
            <span class="freq-label" style="color:${NUC_COLORS[base]}">${base}</span>
            <div class="freq-track"><div class="freq-fill" style="background:${NUC_COLORS[base]};"></div></div>
            <span class="freq-count">${counts[base]}</span>
            <span class="freq-pct">${pct.toFixed(1)}%</span>
        `;
        barsContainer.appendChild(row);
    }

    // Show results
    resultsEl.classList.remove('hidden');

    // Animate bars after a tick (so transitions trigger)
    requestAnimationFrame(() => {
        document.getElementById('gcBar').style.width = gc + '%';
        document.getElementById('atBar').style.width = (atCount / total * 100) + '%';
        barsContainer.querySelectorAll('.freq-fill').forEach((fill, i) => {
            const base = ['A', 'T', 'G', 'C'][i];
            const pct = total > 0 ? (counts[base] / total * 100) : 0;
            fill.style.width = pct + '%';
        });
    });
}

/** Clear all inputs and results */
function clearAll() {
    document.getElementById('dna-input').value = '';
    document.getElementById('sample-select').value = '';
    document.getElementById('errorMsg').classList.remove('visible');
    document.getElementById('resultsSection').classList.add('hidden');
    // Reset bars
    document.getElementById('gcBar').style.width = '0';
    document.getElementById('atBar').style.width = '0';
}

/** Show error message */
function showError(msg) {
    const el = document.getElementById('errorMsg');
    el.textContent = msg;
    el.classList.add('visible');
}

// ════════════════════════════════════
// Input Focus Glow & Sample Select
// ════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('dna-input');
    const wrapper = document.getElementById('inputWrapper');

    textarea.addEventListener('focus', () => wrapper.classList.add('focused'));
    textarea.addEventListener('blur', () => wrapper.classList.remove('focused'));

    // Enter key to analyze
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); analyzeSequence(); }
    });

    // Sample select
    document.getElementById('sample-select').addEventListener('change', function () {
        if (this.value) {
            textarea.value = this.value;
            textarea.focus();
        }
    });

    // Create floating particles
    createParticles();
    // Start helix animation
    initHelix();
});

// ════════════════════════════════════
// Floating Particles
// ════════════════════════════════════
function createParticles() {
    const container = document.getElementById('particles');
    const colors = ['#58A6FF', '#BC8CFF', '#F778BA', '#3FB950', '#F0883E'];
    for (let i = 0; i < 20; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = 2 + Math.random() * 4;
        p.style.width = size + 'px';
        p.style.height = size + 'px';
        p.style.left = Math.random() * 100 + '%';
        p.style.bottom = '-10px';
        p.style.background = colors[Math.floor(Math.random() * colors.length)];
        p.style.animationDuration = (10 + Math.random() * 15) + 's';
        p.style.animationDelay = (Math.random() * 10) + 's';
        container.appendChild(p);
    }
}

// ════════════════════════════════════
// DNA Double Helix Canvas Animation
// ════════════════════════════════════
function initHelix() {
    const canvas = document.getElementById('helixCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let phase = 0;

    function resize() {
        canvas.width = 140;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = 70, amp = 30, step = 6;

        for (let y = 0; y < canvas.height; y += step) {
            const t = y * 0.04 + phase;
            const x1 = cx + amp * Math.sin(t);
            const x2 = cx - amp * Math.sin(t);
            const depth = (Math.sin(t) + 1) / 2;

            // Strand 1
            ctx.beginPath();
            ctx.arc(x1, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${88 + 80 * depth}, ${166 - 60 * depth}, 255, 0.8)`;
            ctx.fill();

            // Strand 2
            ctx.beginPath();
            ctx.arc(x2, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${188 - 40 * (1 - depth)}, ${140 + 40 * (1 - depth)}, 255, 0.8)`;
            ctx.fill();

            // Cross-rungs
            if (y % 30 < step) {
                ctx.beginPath();
                ctx.moveTo(x1, y);
                ctx.lineTo(x2, y);
                ctx.strokeStyle = 'rgba(72, 79, 88, 0.5)';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
        phase += 0.02;
        requestAnimationFrame(draw);
    }
    draw();
}
