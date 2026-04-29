class DNAAnalyzer:
    """Class to handle core DNA sequence analysis logic."""
    
    def __init__(self, sequence: str):
        self.sequence = sequence.upper()
        
    def is_valid(self) -> bool:
        """Check if the sequence contains only valid nucleotides (A, T, G, C)."""
        valid_nucleotides = {'A', 'T', 'G', 'C'}
        return all(nucleotide in valid_nucleotides for nucleotide in self.sequence) and len(self.sequence) > 0
        
    def gc_content(self) -> float:
        """Calculate the GC content percentage of the sequence."""
        if not self.sequence:
            return 0.0
        g_count = self.sequence.count('G')
        c_count = self.sequence.count('C')
        return ((g_count + c_count) / len(self.sequence)) * 100
        
    def reverse_complement(self) -> str:
        """Generate the reverse complement of the DNA sequence."""
        complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        try:
            complement = ''.join(complement_map[base] for base in self.sequence)
            return complement[::-1]
        except KeyError:
            return ""
            
    def nucleotide_count(self) -> dict:
        """Count the frequency of each nucleotide in the sequence."""
        return {
            'A': self.sequence.count('A'),
            'T': self.sequence.count('T'),
            'G': self.sequence.count('G'),
            'C': self.sequence.count('C')
        }
