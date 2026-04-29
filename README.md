# DNA Sequence Analyzer – VTU Biology for Engineers Project

## Description
A standalone desktop application that analyzes DNA sequences using computational techniques. It accepts a DNA sequence, validates the input, and performs fundamental bioinformatics calculations. Designed specifically for academic use.

## Features
- Validates DNA sequences (allows only A, T, G, C)
- Calculates GC Content percentage
- Generates the Reverse Complement of the sequence
- Computes Nucleotide Frequency (counts of A, T, G, C)
- Clean, user-friendly Graphical User Interface (GUI) built with Tkinter

## Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** Tkinter (Standard Library)
- **Architecture:** Modular, standalone (No Database)

## Project Structure
```text
dna-sequence-analyzer-vtu/
│
├── main.py          # GUI entry point
├── analyzer.py      # Core DNA logic class
├── utils.py         # Helper functions
├── requirements.txt # Project dependencies
└── README.md        # Documentation
```

## How to Run
1. Ensure you have Python installed (Python 3.6+ recommended).
2. Clone or download this project.
3. Open a terminal or command prompt in the project directory.
4. Run the application using the command:
   ```bash
   python main.py
   ```

## Example Input / Output
**Input:** `ATGCGTAC`

**Output:**
```text
GC Content: 50.00%
Reverse Complement: GTACGCAT
Nucleotide Count: A:2 T:2 G:2 C:2
```

## Project Type
Standalone bioinformatics software. Suitable for 4th-semester engineering project submission.
