#!/usr/bin/env python3
"""
labeled4nothing.py - Find unreferenced labels and equations in LaTeX files

This script scans a .tex file for:
1. All \label{...} commands that are not referenced
2. All numbered equations (with or without labels) that are never referenced

Results are written to a .txt file in the same directory.

Usage:
    python labeled4nothing.py <input.tex>
"""

import re
import sys
import os
from pathlib import Path


def extract_labels(content):
    """
    Extract all labels from LaTeX content.

    Args:
        content (str): The LaTeX file content

    Returns:
        set: Set of all label names found in the file
    """
    # Match \label{...} commands
    label_pattern = r'\\label\{([^}]+)\}'
    labels = set(re.findall(label_pattern, content))
    return labels


def extract_references(content):
    """
    Extract all label references from LaTeX content.

    Args:
        content (str): The LaTeX file content

    Returns:
        set: Set of all referenced label names
    """
    # Match various reference commands: \ref, \eqref, \Cref, \cref, \autoref, \nameref, \pageref, etc.
    # This pattern matches commands like \ref{label}, \Cref{label1,label2}, etc.
    ref_pattern = r'\\(?:eq|C|c|auto|name|page|)?[Rr]ef\*?\{([^}]+)\}'

    references = set()
    matches = re.findall(ref_pattern, content)

    # Handle comma-separated references (e.g., \Cref{label1,label2})
    for match in matches:
        # Split by comma and strip whitespace
        refs = [ref.strip() for ref in match.split(',')]
        references.update(refs)

    return references


def extract_numbered_equations(content):
    """
    Extract all numbered equation environments from LaTeX content.

    Args:
        content (str): The LaTeX file content

    Returns:
        list: List of tuples (line_number, equation_content, label_or_none)
    """
    lines = content.split('\n')
    equations = []

    # Numbered equation environments (not equation*, align*, etc.)
    numbered_envs = [
        'equation', 'align', 'gather', 'multline', 'flalign',
        'alignat', 'eqnarray'
    ]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for beginning of numbered equation environment
        for env in numbered_envs:
            begin_pattern = r'\\begin\{' + env + r'\}'
            end_pattern = r'\\end\{' + env + r'\}'

            if re.search(begin_pattern, line):
                # Found start of numbered equation environment
                start_line = i + 1  # Line numbers are 1-indexed
                equation_lines = []
                label = None

                # Collect the equation content until \end{env}
                j = i
                while j < len(lines):
                    equation_lines.append(lines[j])

                    # Check for label in this line
                    label_match = re.search(r'\\label\{([^}]+)\}', lines[j])
                    if label_match:
                        label = label_match.group(1)

                    # Check for end of environment
                    if re.search(end_pattern, lines[j]):
                        equation_content = '\n'.join(equation_lines)
                        equations.append((start_line, equation_content.strip(), label))
                        i = j
                        break
                    j += 1

                break
        i += 1

    return equations


def find_unreferenced_labels(tex_file_path):
    """
    Find all unreferenced labels in a LaTeX file.

    Args:
        tex_file_path (str): Path to the .tex file

    Returns:
        list: Sorted list of unreferenced label names
    """
    # Read the LaTeX file
    with open(tex_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract labels and references
    labels = extract_labels(content)
    references = extract_references(content)

    # Find unreferenced labels
    unreferenced = labels - references

    return sorted(unreferenced)


def find_unreferenced_equations(tex_file_path):
    """
    Find all numbered equations that are never referenced.

    Args:
        tex_file_path (str): Path to the .tex file

    Returns:
        list: List of tuples (line_number, equation_content) for unreferenced equations
    """
    # Read the LaTeX file
    with open(tex_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract all numbered equations
    equations = extract_numbered_equations(content)

    # Extract all references
    references = extract_references(content)

    # Find unreferenced equations
    unreferenced_equations = []
    for line_num, eq_content, label in equations:
        # An equation is unreferenced if:
        # 1. It has no label, OR
        # 2. It has a label but the label is not referenced
        if label is None or label not in references:
            unreferenced_equations.append((line_num, eq_content))

    return unreferenced_equations


def main():
    """Main function to process command line arguments and generate output."""
    if len(sys.argv) != 2:
        print("Usage: python labeled4nothing.py <input.tex>")
        sys.exit(1)

    tex_file_path = sys.argv[1]

    # Check if file exists
    if not os.path.exists(tex_file_path):
        print(f"Error: File '{tex_file_path}' not found.")
        sys.exit(1)

    # Check if file has .tex extension
    if not tex_file_path.lower().endswith('.tex'):
        print("Warning: Input file does not have a .tex extension.")

    # Find unreferenced labels and equations
    try:
        unreferenced_labels = find_unreferenced_labels(tex_file_path)
        unreferenced_equations = find_unreferenced_equations(tex_file_path)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

    # Create output file path (same directory, .txt extension)
    tex_path = Path(tex_file_path)
    output_file_path = tex_path.with_suffix('.txt')

    # Write results to output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        # Section 1: Unreferenced labels
        f.write("=" * 80 + "\n")
        f.write("UNREFERENCED LABELS\n")
        f.write("=" * 80 + "\n\n")

        if unreferenced_labels:
            for label in unreferenced_labels:
                f.write(f"  {label}\n")
            f.write("\n")
            f.write(f"Total: {len(unreferenced_labels)} unreferenced label(s)\n")
        else:
            f.write("No unreferenced labels found.\n")

        # Section 2: Unreferenced equations
        f.write("\n" + "=" * 80 + "\n")
        f.write("UNREFERENCED NUMBERED EQUATIONS\n")
        f.write("=" * 80 + "\n\n")

        if unreferenced_equations:
            for idx, (line_num, eq_content) in enumerate(unreferenced_equations, 1):
                f.write(f"Equation #{idx} at line {line_num}:\n")
                f.write("-" * 80 + "\n")
                f.write(eq_content + "\n")
                f.write("-" * 80 + "\n\n")
            f.write(f"Total: {len(unreferenced_equations)} unreferenced equation(s)\n")
        else:
            f.write("No unreferenced equations found.\n")

    # Print summary to console
    print(f"Processed: {tex_file_path}")
    print(f"Output written to: {output_file_path}")
    print(f"\nSummary:")
    print(f"  - {len(unreferenced_labels)} unreferenced label(s)")
    print(f"  - {len(unreferenced_equations)} unreferenced equation(s)")

    if unreferenced_labels:
        print("\nUnreferenced labels:")
        for label in unreferenced_labels:
            print(f"  - {label}")

    if unreferenced_equations:
        print(f"\nUnreferenced equations at lines:")
        for line_num, _ in unreferenced_equations:
            print(f"  - Line {line_num}")


if __name__ == "__main__":
    main()
