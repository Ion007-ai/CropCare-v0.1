# Requirements: CropCare

Author: Aayan Bhaisal | Reg. No. 26BAI10444 | VIT Bhopal University | B.Tech AI & ML, 1st Year

## 1. Problem statement

Small farmers and agriculture students have no simple way to compare crop symptoms with known diseases and no record of past problems. CropCare gives a crop record book, a symptom-based advisor and a history with reports. See `statement.md`.

## 2. Objectives

1. Store and manage crop records (create, read, update, delete).
2. Suggest likely diseases from the symptoms the user picks, with a score that can be explained.
3. Keep a history of advice and produce a summary and exports.
4. Practise the Python Essentials topics (data structures, functions, modules, OOP) in one working program.
5. Keep the code readable, using clearly marked sections, even though it is all in one file.

## 3. Functional requirements

**Module A: Crop records**

| ID | Requirement |
|---|---|
| FR-A1 | Add a crop with crop name, field name, area (acres), sowing date and season. The program gives an ID like C001. |
| FR-A2 | View all crops in a table. |
| FR-A3 | Update any detail of a crop. Pressing Enter keeps the old value. |
| FR-A4 | Delete a crop after a yes/no question. The history stays saved. |
| FR-A5 | Every answer is checked and the question is asked again if it is wrong. |
| FR-A6 | Every change is saved to `crops.txt`. |

**Module B: Disease advisor**

| ID | Requirement |
|---|---|
| FR-B1 | Choose one of the saved crops by its ID. |
| FR-B2 | Show the numbered list of symptoms known for that crop. |
| FR-B3 | The user types the numbers of the symptoms they see, for example `1,3`. |
| FR-B4 | Score every disease of that crop and show the best 3 with a percentage and a label (High, Medium, Low). |
| FR-B5 | Show the matched symptoms, treatment, prevention and a disclaimer. |
| FR-B6 | Save each advice to `history.txt`. |

**Module C: History and reports**

| ID | Requirement |
|---|---|
| FR-C1 | View the latest 10 advice records. |
| FR-C2 | Show a summary: crop areas, advice per crop, most frequent diseases, average score. |
| FR-C3 | Limit the summary and exports to one crop. |
| FR-C4 | Export the history to `history_export.csv` and the summary to `summary_report.txt`. |

**Workflow (FR-G):** main menu, then a module menu, then questions, then the result, then back to the menu.

## 4. Input and output

| Function | Input | Output |
|---|---|---|
| Add crop | crop name, field name, area, date `YYYY-MM-DD`, season | message with the new ID, line added to `crops.txt` |
| Update crop | crop ID, new values (Enter keeps the old) | updated crop, file rewritten |
| Delete crop | crop ID, y/n | message, file rewritten |
| Advisor | crop ID, symptom numbers | ranked diseases on screen, line added to `history.txt` |
| Summary | optional crop name | report text on screen |
| Export | optional crop name | `history_export.csv` or `summary_report.txt` |

## 5. Non-functional requirements

| ID | Category | Requirement | How it is met |
|---|---|---|---|
| NFR-1 | Usability | Every question says what format is expected, menus are numbered, wrong answers give a short message. | `ask_...` functions in Section 1 of `cropcare.py` |
| NFR-2 | Reliability | A damaged or missing data file must not crash the program. | `try / except` around file reading, damaged lines skipped, a missing file means an empty list |
| NFR-3 | Error handling | Wrong input is never accepted silently. Failed file writes tell the user and undo the change in memory. | check functions, `save_crops` and `save_history` return True or False |
| NFR-4 | Maintainability | The single file is split into 8 numbered sections with comment headers, and each function has one job. | `cropcare.py`, see `docs/CODE_WALKTHROUGH.md` |
| NFR-5 | Logging | Important actions are written with the time to `cropcare_log.txt`. | `write_log()` in Section 1 of `cropcare.py` |
| NFR-6 | Resource efficiency | Only the standard library is used, data is small and kept in memory while running. | no external packages |

## 6. Assumptions

- One user at a time.
- Area is in acres.
- The sowing date cannot be in the future.
- The program is run from the project folder.
- Treatment advice is educational and must be confirmed locally.
