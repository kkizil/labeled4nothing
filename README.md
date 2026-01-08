# labeled4nothing

A Python utility to find unreferenced labels and numbered equations in LaTeX documents.

## Overview

When working on large LaTeX documents, it's easy to accumulate labels and numbered equations that are not referenced at all. This script scans your `.tex` files to identify:
1. All `\label{...}` commands that aren't used by any reference commands
2. All numbered equations (with or without labels) that are never referenced

This helps you keep your documents clean and maintainable!

## Features

### Label Detection
- 🔍 Detects all `\label{...}` commands in LaTeX files
- 🔗 Checks against common reference commands:
  - `\ref{...}` and `\ref*{...}`
  - `\eqref{...}`
  - `\Cref{...}` and `\cref{...}` (cleveref package)
  - `\autoref{...}` (hyperref package)
  - `\nameref{...}` and `\pageref{...}`
- 📝 Handles comma-separated references (e.g., `\Cref{fig:a,fig:b}`)

### Equation Detection
- 🔢 Identifies unreferenced numbered equations in these environments:
  - `equation`, `align`, `gather`, `multline`, `flalign`, `alignat`, `eqnarray`
- 📍 Reports line numbers for each unreferenced equation
- 📋 Reproduces full equation content for easy searching (Ctrl+F)
- ✅ Detects numbered equations both with and without labels

### Output
- 💾 Outputs results to a `.txt` file in the same directory
- 📊 Provides both detailed file output and console summary
- 🎯 Separate sections for labels and equations

## Installation

No installation required! Just download the script and run it with Python 3.

```bash
git clone https://github.com/kkizil/labeled4nothing.git
cd labeled4nothing
```

## Usage

```bash
python labeled4nothing.py <your-file.tex>
```

### Example

```bash
python labeled4nothing.py manuscript.tex
```

This will create `manuscript.txt` in the same directory containing all unreferenced labels and equations.

### Sample Output

**Console:**
```
Processed: manuscript.tex
Output written to: manuscript.txt

Summary:
  - 2 unreferenced label(s)
  - 3 unreferenced equation(s)

Unreferenced labels:
  - fig:old_diagram
  - sec:deprecated_section

Unreferenced equations at lines:
  - Line 45
  - Line 102
  - Line 234
```

**manuscript.txt:**
```
================================================================================
UNREFERENCED LABELS
================================================================================

  fig:old_diagram
  sec:deprecated_section

Total: 2 unreferenced label(s)

================================================================================
UNREFERENCED NUMBERED EQUATIONS
================================================================================

Equation #1 at line 45:
--------------------------------------------------------------------------------
\begin{equation}
E = mc^2
\label{eq:unused}
\end{equation}
--------------------------------------------------------------------------------

Equation #2 at line 102:
--------------------------------------------------------------------------------
\begin{align}
a &= b + c \\
d &= e + f
\end{align}
--------------------------------------------------------------------------------

Equation #3 at line 234:
--------------------------------------------------------------------------------
\begin{equation}
Q = \sqrt{\frac{2DS}{H}}
\end{equation}
--------------------------------------------------------------------------------

Total: 3 unreferenced equation(s)
```

## Limitations

- Currently processes single `.tex` files (doesn't follow `\input` or `\include` commands)
- Assumes standard LaTeX syntax
- Only detects standard numbered equation environments (not custom environments)

## Notes

- Starred environments (e.g., `equation*`) are correctly ignored as they don't produce numbers

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - feel free to use this tool in your projects.


---

**Note**: This tool helps identify potentially unused labels and equations, but always review the results before making changes:
- Labels might be referenced in external files or by custom commands
- Equations without references might still be important for completeness or pedagogical purposes (e.g., referencing in class)
- Some numbered equations may be intentionally included for future reference even if not cited in the text
