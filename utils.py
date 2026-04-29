from analyzer import DNAAnalyzer

def validate_sequence(sequence: str) -> bool:
    """Helper function to validate the DNA sequence before analysis."""
    analyzer = DNAAnalyzer(sequence)
    return analyzer.is_valid()

def format_output(gc_content: float, rev_comp: str, counts: dict) -> str:
    """Format the analysis results into a readable string."""
    result = "DNA Sequence Analysis Results:\n"
    result += "-" * 30 + "\n\n"
    result += f"GC Content: {gc_content:.2f}%\n"
    result += f"Reverse Complement: {rev_comp}\n"
    result += f"Nucleotide Count: A:{counts.get('A', 0)} T:{counts.get('T', 0)} G:{counts.get('G', 0)} C:{counts.get('C', 0)}\n"
    return result
