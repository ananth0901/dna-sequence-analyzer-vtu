import streamlit as st
from analyzer import DNAAnalyzer
from utils import validate_sequence

st.set_page_config(
    page_title="DNA Sequence Analyzer",
    page_icon="🧬",
    layout="centered"
)

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0D1117;
        color: #E6EDF3;
    }
    
    /* Hide top header bar in Streamlit */
    header {visibility: hidden;}
    
    /* Styled Cards */
    .metric-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        font-family: 'Consolas', monospace;
    }
    .metric-label {
        font-size: 13px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 DNA Sequence Analyzer")
st.markdown("**VTU Biology for Engineers Project**")
st.markdown("---")

# Pre-filled sample state
if 'sample_seq' not in st.session_state:
    st.session_state.sample_seq = ""

col_input, col_btn = st.columns([4, 1])

with col_btn:
    st.markdown("<br><br>", unsafe_allow_html=True) # Spacer
    if st.button("💡 Sample", help="Load a sample DNA sequence"):
        st.session_state.sample_seq = "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTG"
        st.rerun()

with col_input:
    sequence_input = st.text_area(
        "Enter DNA Sequence (A, T, G, C):", 
        value=st.session_state.sample_seq,
        height=120, 
        placeholder="e.g., ATGCGTAC..."
    )

analyze_clicked = st.button("⚡ Analyze Sequence", type="primary", use_container_width=True)

if analyze_clicked or sequence_input:
    sequence = sequence_input.strip().upper()
    
    if sequence:
        if not validate_sequence(sequence):
            st.error("Invalid Sequence: The sequence contains invalid characters. Only A, T, G, and C are allowed.")
        else:
            analyzer = DNAAnalyzer(sequence)
            gc = analyzer.gc_content()
            rev_comp = analyzer.reverse_complement()
            counts = analyzer.nucleotide_count()
            total = sum(counts.values())
            
            st.markdown("### 📊 Analysis Results")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Row 1: Main Stats
            m1, m2 = st.columns(2)
            
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">GC Content</div>
                    <div class="metric-value" style="color: #3FB950;">{gc:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Sequence Length</div>
                    <div class="metric-value" style="color: #58A6FF;">{len(sequence)} bp</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Row 2: Reverse Complement
            st.markdown(f"""
            <div class="metric-card" style="text-align: left;">
                <div class="metric-label">Reverse Complement</div>
                <div class="metric-value" style="color: #BC8CFF; font-size: 16px; word-wrap: break-word;">{rev_comp}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Row 3: Nucleotide counts
            st.markdown("#### Nucleotide Frequency")
            c1, c2, c3, c4 = st.columns(4)
            bases = [('A', '#58A6FF', c1), ('T', '#F778BA', c2), ('G', '#3FB950', c3), ('C', '#F0883E', c4)]
            
            for base, color, col in bases:
                with col:
                    st.markdown(f"""
                    <div class="metric-card" style="padding: 15px;">
                        <div class="metric-label">{base}</div>
                        <div class="metric-value" style="color: {color};">{counts[base]}</div>
                    </div>
                    """, unsafe_allow_html=True)
