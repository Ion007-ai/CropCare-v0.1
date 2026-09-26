# CropCare: Crop Record Book and Disease Advisor

A single-file Python program that keeps a farmer's crop records and suggests likely diseases from the symptoms the user picks.

**Author:** Aayan Bhaisal
**Registration No.:** 26BAI10444
**University:** VIT Bhopal University
**Programme:** B.Tech AI & ML, 1st Year
**Course:** Python Essentials (VITyarthi, Build Your Own Project)

## Overview

Small farmers and agriculture students often keep crop details on paper and have no quick way to compare the symptoms they see with known diseases. CropCare stores crop records, matches the symptoms you choose against a built-in disease list, and keeps a history of every advice so you can look back later.

The advisor does not use machine learning. For each disease of the chosen crop it compares two sets (the disease's symptoms and the symptoms you chose) and gives a score: matched symptoms divided by all symptoms in both sets, times 100.

The code is kept as one Python file rather than several files, so everything is in `cropcare.py`, split into eight clearly marked sections (see "File structure" below). The tests are in one file too.

## Features

**Module A: Crop records**
- Add, view, update and delete crops (crop, field name, area in acres, sowing date, season).
- Every answer is checked and the question is asked again if it is wrong.

**Module B: Disease advisor**
- Pick a saved crop, then pick the symptoms you see from a numbered list.
- Get up to 3 possible diseases with a match percentage, a label (High, Medium, Low), treatment and prevention advice.
- Every advice is saved in a history file.

**Module C: History and reports**
- View the history, show a summary report, export the history to a CSV file, save the summary to a text file.
- All of these can be limited to one crop.

The built-in list has 10 diseases for 5 crops: Wheat, Rice, Tomato, Potato, Maize.

## Technologies used

- Python 3.8 or newer (only the standard library, nothing to install)
- Standard modules: `datetime`, `csv`, `array`
- Plain text files for saving data
- Git and GitHub for version control

## File structure

```
cropcare_project/
├── cropcare.py       the whole program, in 8 sections (see below)
├── tests/
│   └── test_cropcare.py    26 tests, imports functions from cropcare.py
├── docs/              requirements, design, testing, code walkthrough
├── README.md
└── statement.md
```

`cropcare.py` is organised top to bottom like this:

| Section | Contents |
|---|---|
| 1 | Settings and helper functions: asking questions, checking answers, writing the log |
| 2 | The `Record` and `Crop` classes |
| 3 | `DISEASES`: the disease list (a dictionary) |
| 4 | Module A: crop records (add, view, update, delete) |
| 5 | Module B: disease advisor (symptom matching) |
| 6 | Reading and writing `history.txt` |
| 7 | Module C: history and reports (summary, CSV/text export) |
| 8 | The main menu and the entry point (`if __name__ == "__main__":`) |

## How to install and run

1. Install Python 3.8 or newer. Check with `python --version`.
2. Download or clone the repository and open a terminal in the project folder.
3. Run:
   ```
   python cropcare.py
   ```
4. Use the numbered menus. The files `crops.txt` and `history.txt` are created in the project folder the first time you save something.

Always run the program from the project folder, because the data files are saved in the folder you run it from.

## How to test

From the project folder:

```
python tests/test_cropcare.py
```

Each test prints PASS or FAIL and the last line shows how many passed (expected: `26 of 26 tests passed`). The tests use temporary files, so your real data is not touched. More detail is in `docs/TESTING.md`.

## Screenshots

Real terminal sessions of the program are in `docs/screenshots/`:

- `01_add_crop.png` - adding a crop (a bad area value is rejected, then corrected)
- `02_disease_advisor.png` - the advisor rejecting an out-of-range symptom number, then giving a ranked result
- `03_summary_report.png` - viewing the advisory history and the summary report
- `04_delete_crop.png` - deleting a crop: an unknown ID is rejected, then a delete is declined and confirmed

## Diagrams and report

- `docs/diagrams/` has the Mermaid source (`.mmd`) for every diagram in this project.
- `docs/images/` has each diagram already rendered as a PNG.
- `report/CropCare_Project_Report.pdf` is the full project report, with the diagrams and
  screenshots embedded, including a completed Challenges Faced and Learnings section.

## Course topics used

| Python Essentials module | Where it is used |
|---|---|
| Input and output, type conversion | `input()`, `print()`, `float()`, `int()`, `str()` in the ask and check functions (Section 1) |
| Operators, precedence | the score formula `len(matched) / len(everything) * 100`, comparisons such as `0 < area <= 10000` (Section 5) |
| Data structures | lists of crops, dictionaries for the disease list and for counting, sets for matching symptoms, tuples for pairs |
| Control flow | `while True` menus, `if / elif / else`, `for` loops, `break`, `continue` |
| Functions | default values (`filename=CROPS_FILE`), `*areas` in `total_area`, return values |
| Modules | `import datetime`, `import csv`, `from array import array` |
| Arrays | `array("d")` holding the crop areas in Section 7 |
| Object-oriented programming | `Record` (parent) and `Crop` (child), `__init__`, `__str__`, `super()` (Section 2) |

## Limitations

- Only 5 crops and 10 diseases. It is not a replacement for an agriculture expert.
- The symptoms come from a fixed list, so there is no free text or photo input.
- Data is saved in plain text files for one user.
- Everything is in one file, so it is longer than usual for a beginner file. The section comments are there to make it easy to navigate.

## Disclaimer

This tool gives educational advice only. Please confirm the disease and any spray with your local Krishi Vigyan Kendra (KVK) before using chemicals.
