"""
DNA Sequence Analyzer – VTU Biology for Engineers Project
main.py – Premium GUI entry point with high-visual dark theme
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
import math
import random
from analyzer import DNAAnalyzer
from utils import validate_sequence, format_output

# ──────────────────────────────────────────────
# Color Palette & Design Tokens
# ──────────────────────────────────────────────
COLORS = {
    "bg_dark":       "#0D1117",
    "bg_card":       "#161B22",
    "bg_input":      "#1C2333",
    "border":        "#30363D",
    "accent_cyan":   "#58A6FF",
    "accent_green":  "#3FB950",
    "accent_purple": "#BC8CFF",
    "accent_pink":   "#F778BA",
    "accent_orange": "#F0883E",
    "text_primary":  "#E6EDF3",
    "text_secondary":"#8B949E",
    "text_muted":    "#484F58",
    "error_red":     "#F85149",
    "success_green": "#3FB950",
    "helix_a":       "#58A6FF",
    "helix_b":       "#BC8CFF",
}

# ──────────────────────────────────────────────
# Sample DNA sequences for suggestions
# ──────────────────────────────────────────────
SAMPLE_SEQUENCES = [
    {"name": "Insulin Gene Fragment",       "seq": "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTG"},
    {"name": "BRCA1 Exon Snippet",          "seq": "ATGCGTACGATCGATCGATCGTAGCTAGCTAGCTA"},
    {"name": "GFP Start Codon Region",      "seq": "ATGAGTAAAGGAGAAGAACTTTTCACTGGAGTTGTC"},
    {"name": "Hemoglobin Beta Chain",       "seq": "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTT"},
    {"name": "Simple Test Sequence",        "seq": "ATGCGTAC"},
    {"name": "Lac Operon Promoter",         "seq": "TTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGG"},
    {"name": "COVID-19 Spike Fragment",     "seq": "ATGTTTGTTTTTCTTGTTTTATTGCCACTAGTCTCTAGTCAGT"},
    {"name": "p53 Tumor Suppressor Start",  "seq": "ATGGAGGAGCCGCAGTCAGATCCTAGCGTGAGTTTGC"},
]


class DNAHelixCanvas(tk.Canvas):
    """Animated double-helix background decoration."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], highlightthickness=0, **kwargs)
        self.phase = 0.0
        self.particles = [
            {"x": random.randint(0, 800), "y": random.randint(0, 700),
             "r": random.uniform(1, 3), "speed": random.uniform(0.2, 0.8),
             "alpha_phase": random.uniform(0, 2 * math.pi)}
            for _ in range(40)
        ]
        self._animate()

    def _animate(self):
        self.delete("helix")
        w = self.winfo_width() or 800
        h = self.winfo_height() or 700

        # Draw floating particles
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < -10:
                p["y"] = h + 10
                p["x"] = random.randint(0, w)
            brightness = int(40 + 20 * math.sin(self.phase + p["alpha_phase"]))
            color = f"#{brightness:02x}{brightness + 10:02x}{brightness + 20:02x}"
            self.create_oval(
                p["x"] - p["r"], p["y"] - p["r"],
                p["x"] + p["r"], p["y"] + p["r"],
                fill=color, outline="", tags="helix"
            )

        # Draw the double helix on the right side
        cx = w - 60
        amplitude = 25
        step = 6
        for y in range(0, h, step):
            t = y * 0.04 + self.phase
            x1 = cx + amplitude * math.sin(t)
            x2 = cx - amplitude * math.sin(t)

            # Strand colors with depth effect
            depth1 = (math.sin(t) + 1) / 2
            depth2 = 1 - depth1

            r1 = int(88 + 80 * depth1)
            g1 = int(166 - 60 * depth1)
            b1 = 255
            c1 = f"#{r1:02x}{g1:02x}{b1:02x}"

            r2 = int(188 - 40 * depth2)
            g2 = int(140 + 40 * depth2)
            b2 = 255
            c2 = f"#{r2:02x}{g2:02x}{b2:02x}"

            self.create_oval(x1 - 3, y - 3, x1 + 3, y + 3, fill=c1, outline="", tags="helix")
            self.create_oval(x2 - 3, y - 3, x2 + 3, y + 3, fill=c2, outline="", tags="helix")

            # Cross-rungs every 30px
            if y % 30 < step:
                self.create_line(x1, y, x2, y, fill=COLORS["text_muted"], width=1, tags="helix")

        self.phase += 0.03
        self.after(50, self._animate)


class SuggestionDropdown(tk.Toplevel):
    """Floating suggestion dropdown with sample DNA sequences."""

    def __init__(self, parent, entry_widget, suggestions, on_select):
        super().__init__(parent)
        self.overrideredirect(True)          # Borderless window
        self.attributes("-topmost", True)
        self.configure(bg=COLORS["border"])
        self.on_select = on_select
        self.entry_widget = entry_widget

        # Inner frame
        inner = tk.Frame(self, bg=COLORS["bg_card"], padx=1, pady=1)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Header
        header = tk.Label(
            inner, text="💡 Sample Sequences", font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_card"], fg=COLORS["accent_cyan"], anchor="w", padx=10, pady=6
        )
        header.pack(fill=tk.X)

        # Separator
        sep = tk.Frame(inner, bg=COLORS["border"], height=1)
        sep.pack(fill=tk.X)

        # Scrollable list
        canvas = tk.Canvas(inner, bg=COLORS["bg_card"], highlightthickness=0, height=260)
        scrollbar = tk.Scrollbar(inner, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas, bg=COLORS["bg_card"])

        self.list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)

        for item in suggestions:
            self._add_item(item)

        # Position below the entry widget
        self._reposition()
        self.bind("<FocusOut>", lambda e: self.destroy())

    def _reposition(self):
        x = self.entry_widget.winfo_rootx()
        y = self.entry_widget.winfo_rooty() + self.entry_widget.winfo_height() + 4
        w = self.entry_widget.winfo_width()
        self.geometry(f"{w}x300+{x}+{y}")

    def _add_item(self, item):
        frame = tk.Frame(self.list_frame, bg=COLORS["bg_card"], cursor="hand2", padx=10, pady=6)
        frame.pack(fill=tk.X)

        name_lbl = tk.Label(
            frame, text=f"🧬  {item['name']}", font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"], fg=COLORS["text_primary"], anchor="w", cursor="hand2"
        )
        name_lbl.pack(fill=tk.X)

        seq_preview = item["seq"][:36] + ("…" if len(item["seq"]) > 36 else "")
        seq_lbl = tk.Label(
            frame, text=seq_preview, font=("Consolas", 9),
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"], anchor="w", cursor="hand2"
        )
        seq_lbl.pack(fill=tk.X)

        sep = tk.Frame(self.list_frame, bg=COLORS["border"], height=1)
        sep.pack(fill=tk.X)

        # Hover effects
        def on_enter(e):
            frame.config(bg=COLORS["bg_input"])
            name_lbl.config(bg=COLORS["bg_input"], fg=COLORS["accent_cyan"])
            seq_lbl.config(bg=COLORS["bg_input"])

        def on_leave(e):
            frame.config(bg=COLORS["bg_card"])
            name_lbl.config(bg=COLORS["bg_card"], fg=COLORS["text_primary"])
            seq_lbl.config(bg=COLORS["bg_card"])

        def on_click(e, seq=item["seq"]):
            self.on_select(seq)
            self.destroy()

        for widget in (frame, name_lbl, seq_lbl):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)


class DNAAnalyzerApp:
    """Main application class – premium dark-themed DNA analyzer GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("🧬 DNA Sequence Analyzer – VTU Project")
        self.root.geometry("860x720")
        self.root.minsize(780, 650)
        self.root.configure(bg=COLORS["bg_dark"])
        self.suggestion_window = None

        # Try to set the icon (non-critical if it fails)
        try:
            self.root.iconname("DNA")
        except Exception:
            pass

        self._build_ui()

    # ──────────────────────────────────────────
    # UI Construction
    # ──────────────────────────────────────────
    def _build_ui(self):
        # Animated helix background canvas
        self.helix_canvas = DNAHelixCanvas(self.root)
        self.helix_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Main content card (semi-transparent look via dark card)
        card = tk.Frame(self.root, bg=COLORS["bg_card"], highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=30, pady=25)
        card.place(relx=0.05, rely=0.03, relwidth=0.72, relheight=0.94)

        # ─── Title Section ───
        title_frame = tk.Frame(card, bg=COLORS["bg_card"])
        title_frame.pack(fill=tk.X, pady=(0, 5))

        emoji_lbl = tk.Label(title_frame, text="🧬", font=("Segoe UI Emoji", 28),
                             bg=COLORS["bg_card"])
        emoji_lbl.pack(side=tk.LEFT, padx=(0, 10))

        title_text_frame = tk.Frame(title_frame, bg=COLORS["bg_card"])
        title_text_frame.pack(side=tk.LEFT)

        tk.Label(title_text_frame, text="DNA Sequence Analyzer",
                 font=("Segoe UI", 20, "bold"), bg=COLORS["bg_card"],
                 fg=COLORS["text_primary"]).pack(anchor="w")
        tk.Label(title_text_frame, text="VTU Biology for Engineers Project",
                 font=("Segoe UI", 10), bg=COLORS["bg_card"],
                 fg=COLORS["text_secondary"]).pack(anchor="w")

        # Accent bar under title
        accent_bar = tk.Canvas(card, height=3, bg=COLORS["bg_card"], highlightthickness=0)
        accent_bar.pack(fill=tk.X, pady=(10, 15))
        accent_bar.bind("<Configure>", lambda e: self._draw_gradient_bar(accent_bar))

        # ─── Input Section ───
        input_section = tk.Frame(card, bg=COLORS["bg_card"])
        input_section.pack(fill=tk.X, pady=(0, 5))

        tk.Label(input_section, text="Enter DNA Sequence",
                 font=("Segoe UI", 11, "bold"), bg=COLORS["bg_card"],
                 fg=COLORS["text_primary"]).pack(anchor="w")
        tk.Label(input_section, text="Only nucleotides A, T, G, C are accepted",
                 font=("Segoe UI", 9), bg=COLORS["bg_card"],
                 fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 6))

        # Input field with border effect
        entry_border = tk.Frame(input_section, bg=COLORS["border"], padx=2, pady=2)
        entry_border.pack(fill=tk.X)

        self.sequence_entry = tk.Entry(
            entry_border, font=("Consolas", 14), bg=COLORS["bg_input"],
            fg=COLORS["accent_cyan"], insertbackground=COLORS["accent_cyan"],
            relief="flat", bd=8
        )
        self.sequence_entry.pack(fill=tk.X)
        self.sequence_entry.bind("<FocusIn>", lambda e: entry_border.config(bg=COLORS["accent_cyan"]))
        self.sequence_entry.bind("<FocusOut>", lambda e: entry_border.config(bg=COLORS["border"]))
        self.sequence_entry.bind("<Return>", lambda e: self._analyze())

        # ─── Buttons Row ───
        btn_frame = tk.Frame(card, bg=COLORS["bg_card"])
        btn_frame.pack(fill=tk.X, pady=12)

        self.analyze_btn = tk.Button(
            btn_frame, text="⚡  Analyze Sequence", font=("Segoe UI", 11, "bold"),
            bg=COLORS["accent_cyan"], fg=COLORS["bg_dark"], activebackground="#79B8FF",
            activeforeground=COLORS["bg_dark"], relief="flat", bd=0, padx=20, pady=8,
            cursor="hand2", command=self._analyze
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.suggest_btn = tk.Button(
            btn_frame, text="💡  Suggestions", font=("Segoe UI", 10),
            bg=COLORS["bg_input"], fg=COLORS["text_secondary"], activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"], relief="flat", bd=0, padx=16, pady=8,
            cursor="hand2", command=self._show_suggestions
        )
        self.suggest_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.clear_btn = tk.Button(
            btn_frame, text="🗑  Clear", font=("Segoe UI", 10),
            bg=COLORS["bg_input"], fg=COLORS["text_secondary"], activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"], relief="flat", bd=0, padx=16, pady=8,
            cursor="hand2", command=self._clear
        )
        self.clear_btn.pack(side=tk.LEFT)

        # Button hover effects
        for btn, hover_bg, normal_bg in [
            (self.analyze_btn, "#79B8FF", COLORS["accent_cyan"]),
            (self.suggest_btn, COLORS["border"], COLORS["bg_input"]),
            (self.clear_btn,   COLORS["border"], COLORS["bg_input"]),
        ]:
            btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=normal_bg: b.config(bg=c))

        # ─── Results Section ───
        results_header = tk.Frame(card, bg=COLORS["bg_card"])
        results_header.pack(fill=tk.X, pady=(5, 6))
        tk.Label(results_header, text="📊  Analysis Results",
                 font=("Segoe UI", 12, "bold"), bg=COLORS["bg_card"],
                 fg=COLORS["text_primary"]).pack(anchor="w")

        # Results container with border
        results_border = tk.Frame(card, bg=COLORS["border"], padx=1, pady=1)
        results_border.pack(fill=tk.BOTH, expand=True)

        results_inner = tk.Frame(results_border, bg=COLORS["bg_input"], padx=15, pady=12)
        results_inner.pack(fill=tk.BOTH, expand=True)

        # Individual result cards will be placed here
        self.results_container = results_inner

        # Placeholder text
        self.placeholder = tk.Label(
            self.results_container,
            text="Enter a DNA sequence above and click Analyze\nto see results here.",
            font=("Segoe UI", 11), bg=COLORS["bg_input"], fg=COLORS["text_muted"],
            justify="center"
        )
        self.placeholder.pack(expand=True)

        # ─── Footer ───
        footer = tk.Label(card, text="Built with Python & Tkinter  •  VTU 4th Semester Project",
                          font=("Segoe UI", 8), bg=COLORS["bg_card"], fg=COLORS["text_muted"])
        footer.pack(side=tk.BOTTOM, pady=(8, 0))

    # ──────────────────────────────────────────
    # Gradient accent bar
    # ──────────────────────────────────────────
    def _draw_gradient_bar(self, canvas):
        canvas.delete("all")
        w = canvas.winfo_width()
        if w < 2:
            return
        colors_list = [
            COLORS["accent_cyan"], COLORS["accent_purple"],
            COLORS["accent_pink"], COLORS["accent_orange"]
        ]
        segments = len(colors_list) - 1
        seg_w = w / segments
        for i in range(segments):
            c1 = self.root.winfo_rgb(colors_list[i])
            c2 = self.root.winfo_rgb(colors_list[i + 1])
            for x in range(int(seg_w)):
                ratio = x / seg_w
                r = int(c1[0] + (c2[0] - c1[0]) * ratio) >> 8
                g = int(c1[1] + (c2[1] - c1[1]) * ratio) >> 8
                b = int(c1[2] + (c2[2] - c1[2]) * ratio) >> 8
                color = f"#{r:02x}{g:02x}{b:02x}"
                px = int(i * seg_w + x)
                canvas.create_line(px, 0, px, 3, fill=color)

    # ──────────────────────────────────────────
    # Suggestions dropdown
    # ──────────────────────────────────────────
    def _show_suggestions(self):
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            self.suggestion_window.destroy()
            self.suggestion_window = None
            return
        self.suggestion_window = SuggestionDropdown(
            self.root, self.sequence_entry, SAMPLE_SEQUENCES, self._insert_suggestion
        )

    def _insert_suggestion(self, seq):
        self.sequence_entry.delete(0, tk.END)
        self.sequence_entry.insert(0, seq)
        self.sequence_entry.focus_set()

    # ──────────────────────────────────────────
    # Clear
    # ──────────────────────────────────────────
    def _clear(self):
        self.sequence_entry.delete(0, tk.END)
        for widget in self.results_container.winfo_children():
            widget.destroy()
        self.placeholder = tk.Label(
            self.results_container,
            text="Enter a DNA sequence above and click Analyze\nto see results here.",
            font=("Segoe UI", 11), bg=COLORS["bg_input"], fg=COLORS["text_muted"],
            justify="center"
        )
        self.placeholder.pack(expand=True)

    # ──────────────────────────────────────────
    # Core analysis
    # ──────────────────────────────────────────
    def _analyze(self):
        sequence = self.sequence_entry.get().strip()

        if not sequence:
            messagebox.showwarning("Input Required", "Please enter a DNA sequence.")
            return

        if not validate_sequence(sequence):
            messagebox.showerror(
                "Invalid Sequence",
                "The sequence contains invalid characters.\nOnly A, T, G, and C are allowed."
            )
            return

        # Run analysis
        analyzer = DNAAnalyzer(sequence)
        gc = analyzer.gc_content()
        rev_comp = analyzer.reverse_complement()
        counts = analyzer.nucleotide_count()
        total = sum(counts.values())

        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        # ── Sequence info bar ──
        info = tk.Label(
            self.results_container,
            text=f"Sequence Length: {len(sequence)} bp   |   Input: {sequence[:40]}{'…' if len(sequence) > 40 else ''}",
            font=("Consolas", 9), bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
            anchor="w", padx=10, pady=6
        )
        info.pack(fill=tk.X, pady=(0, 10))

        # ── Result cards in a grid ──
        grid = tk.Frame(self.results_container, bg=COLORS["bg_input"])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # Card: GC Content
        self._result_card(grid, 0, 0, "GC Content", f"{gc:.2f}%",
                          self._gc_bar_widget, gc, COLORS["accent_green"])

        # Card: Reverse Complement
        self._result_card(grid, 0, 1, "Reverse Complement", rev_comp,
                          None, None, COLORS["accent_purple"])

        # Card: Nucleotide Frequency
        self._result_card(grid, 1, 0, "Nucleotide Count",
                          f"A:{counts['A']}  T:{counts['T']}  G:{counts['G']}  C:{counts['C']}",
                          self._freq_bars_widget, (counts, total), COLORS["accent_cyan"])

        # Card: Sequence Stats
        at = counts['A'] + counts['T']
        gc_count = counts['G'] + counts['C']
        self._result_card(grid, 1, 1, "Sequence Stats",
                          f"AT: {at} ({at/total*100:.1f}%)  |  GC: {gc_count} ({gc_count/total*100:.1f}%)",
                          None, None, COLORS["accent_orange"])

    def _result_card(self, parent, row, col, title, value, extra_widget_fn, extra_data, accent):
        """Create a styled result card in the grid."""
        card = tk.Frame(parent, bg=COLORS["bg_card"], padx=14, pady=12,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        parent.rowconfigure(row, weight=1)

        # Accent dot + title
        title_frame = tk.Frame(card, bg=COLORS["bg_card"])
        title_frame.pack(fill=tk.X, pady=(0, 4))

        dot = tk.Canvas(title_frame, width=10, height=10, bg=COLORS["bg_card"], highlightthickness=0)
        dot.pack(side=tk.LEFT, padx=(0, 6), pady=2)
        dot.create_oval(1, 1, 9, 9, fill=accent, outline="")

        tk.Label(title_frame, text=title, font=("Segoe UI", 10, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)

        # Value
        val_lbl = tk.Label(card, text=value, font=("Consolas", 12, "bold"),
                           bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                           wraplength=280, justify="left", anchor="w")
        val_lbl.pack(fill=tk.X, pady=(2, 4))

        # Optional extra visualization widget
        if extra_widget_fn:
            extra_widget_fn(card, extra_data)

    def _gc_bar_widget(self, parent, gc_value):
        """Mini progress bar for GC content."""
        bar_bg = tk.Frame(parent, bg=COLORS["border"], height=8)
        bar_bg.pack(fill=tk.X, pady=(4, 0))
        bar_bg.update_idletasks()

        bar_fill = tk.Frame(bar_bg, bg=COLORS["accent_green"], height=8)
        bar_fill.place(relx=0, rely=0, relwidth=gc_value / 100, relheight=1)

    def _freq_bars_widget(self, parent, data):
        """Mini horizontal bars for each nucleotide."""
        counts, total = data
        nucleotide_colors = {
            'A': COLORS["accent_cyan"],
            'T': COLORS["accent_pink"],
            'G': COLORS["accent_green"],
            'C': COLORS["accent_orange"],
        }
        bar_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        bar_frame.pack(fill=tk.X, pady=(4, 0))

        for base in ['A', 'T', 'G', 'C']:
            row = tk.Frame(bar_frame, bg=COLORS["bg_card"])
            row.pack(fill=tk.X, pady=1)

            tk.Label(row, text=base, font=("Consolas", 8, "bold"), width=2,
                     bg=COLORS["bg_card"], fg=nucleotide_colors[base]).pack(side=tk.LEFT)

            track = tk.Frame(row, bg=COLORS["border"], height=6)
            track.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

            frac = counts[base] / total if total > 0 else 0
            fill = tk.Frame(track, bg=nucleotide_colors[base], height=6)
            fill.place(relx=0, rely=0, relwidth=frac, relheight=1)


# ──────────────────────────────────────────────
# Application Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = DNAAnalyzerApp(root)
    root.mainloop()
