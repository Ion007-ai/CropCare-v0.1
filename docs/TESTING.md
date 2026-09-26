# Testing: CropCare

Author: Aayan Bhaisal | Reg. No. 26BAI10444 | VIT Bhopal University | B.Tech AI & ML, 1st Year

## Approach

1. **Automated tests** in `tests/test_cropcare.py` use plain `assert` statements and import the functions and classes straight from `cropcare.py`. Each test is a function; the runner at the bottom of the file prints PASS or FAIL for each one.
2. **Manual tests** walk through the real menus in `cropcare.py` with wrong answers.

The automated tests use temporary files (`temp_test_...`) and delete them, so your real `crops.txt` and `history.txt` are not touched.

## Running the automated tests

From the project folder (the one that has `cropcare.py` in it):

```
python tests/test_cropcare.py
```

Expected last line: `26 of 26 tests passed`.

## What the 26 tests cover

| Area | Tests | What is checked | Section of cropcare.py |
|---|---|---|---|
| Input checks | 4 | text, area (including `nan`, `inf`, negative), date (format, future, real date), crop choice with capital letters | Section 1 |
| Crops | 8 | Crop to line and back, damaged lines, new ID, finding a crop, saving and loading, missing file, damaged line skipped, saving to an impossible place | Sections 2 and 4 |
| Advisor | 7 | symptom list without repeats, score with sets (exact values), labels, best disease first, sorted and limited results, history saved and loaded, "No match" | Sections 5 and 6 |
| Reports | 6 | `total_area` with any number of values, summary text, summary for one crop, summary with no data, CSV export, CSV export to an impossible place | Section 7 |
| Disease list | 1 | every disease has a name, 3 or more symptoms without repeats, treatment, prevention, and no `\|` or `;` inside symptoms | Section 3 |

## Manual tests

Start `python cropcare.py` and fill in the Result column yourself. Take a screenshot of tests 2, 4, 5, 8 and 11 for the report.

| # | Steps | Expected | Result |
|---|---|---|---|
| 1 | Manage crops, Add: crop name `banana` | Message with the supported crops, asked again | [ ] |
| 2 | Add: area `abc`, then `-2`, then `2.5` | Two messages, then accepted | [ ] |
| 3 | Add: sowing date `2030-01-01` | Message that the date cannot be in the future | [ ] |
| 4 | Add: sowing date `15-11-2025` | Format message, asked again | [ ] |
| 5 | Add a valid crop, then View all crops | The crop appears with ID C001 | [ ] |
| 6 | Update C001: press Enter everywhere except area | Only the area changes | [ ] |
| 7 | Update `C999` | "There is no crop with ID C999" | [ ] |
| 8 | Delete C001, answer `n`, then again and answer `y` | First keeps it, second removes it | [ ] |
| 9 | Advisor with a Wheat crop: symptoms "black powder instead of grains in the ear" and "only a bare stalk is left" | Loose Smut first, 66.7%, High | [ ] |
| 10 | Advisor: type `0`, `99`, `a,b` as symptom numbers | Message and asked again each time | [ ] |
| 11 | History and reports: view history, summary, export CSV, save summary | Tables shown, files `history_export.csv` and `summary_report.txt` appear | [ ] |
| 12 | Put the text `broken line` on a new line in `crops.txt`, start the program | "Skipping a damaged line", program still starts | [ ] |
| 13 | Press Ctrl+C at a menu | "Goodbye!" without an error | [ ] |
