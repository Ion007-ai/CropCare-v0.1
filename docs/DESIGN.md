# Design: CropCare

Author: Aayan Bhaisal | Reg. No. 26BAI10444 | VIT Bhopal University | B.Tech AI & ML, 1st Year

The diagrams are written in Mermaid, which GitHub shows automatically. For the PDF report, paste each block into https://mermaid.live and export it as a PNG (or redraw it in draw.io).

## 1. System architecture

All the code lives in one file, `cropcare.py`, split into 8 sections. The
diagram below shows the sections as if they were separate boxes, to make the
responsibilities clear, even though there is only one file on disk.

```mermaid
flowchart TB
    U(["User at the terminal"]) --> S8["Section 8: main menu"]

    S8 --> S4["Section 4: Module A - crop records"]
    S8 --> S5["Section 5: Module B - disease advisor"]
    S8 --> S7["Section 7: Module C - history and reports"]

    S4 --> S2["Section 2: Record, Crop classes"]
    S5 --> S3["Section 3: DISEASES dictionary"]
    S5 --> S6["Section 6: history.txt reading/writing"]
    S7 --> S6

    S4 --> F1[("crops.txt")]
    S6 --> F2[("history.txt")]
    S7 --> F3[("history_export.csv and summary_report.txt")]

    S4 -.-> S1["Section 1: ask, check, log helpers"]
    S5 -.-> S1
    S7 -.-> S1
    S1 --> LG[("cropcare_log.txt")]
```

## 2. Workflow diagram

```mermaid
flowchart TD
    A(["Start"]) --> B["Load crops.txt and history.txt"]
    B --> C["Main menu"]
    C --> D{"Choice"}

    D -- "1 Manage crops" --> E["Add, view, update or delete"]
    E --> F{"Answer valid?"}
    F -- No --> G["Show message and ask again"]
    G --> E
    F -- Yes --> H["Save to crops.txt"]
    H --> C

    D -- "2 Disease advisor" --> I["Choose a saved crop"]
    I --> J["Show symptom list for that crop"]
    J --> K["User types symptom numbers"]
    K --> L["Score each disease with sets"]
    L --> M["Show top 3 with treatment and prevention"]
    M --> N["Save advice to history.txt"]
    N --> C

    D -- "3 History and reports" --> O["View history, summary or export"]
    O --> C

    D -- "4 Exit" --> Z(["End"])
```

## 3. Use case diagram

Mermaid has no real UML use case shape, so this uses an actor and ovals. Redraw it in draw.io with the standard stick figure if you prefer.

```mermaid
flowchart LR
    U(["User: farmer or student"])

    subgraph SYS["CropCare"]
        UC1(("Add crop"))
        UC2(("View crops"))
        UC3(("Update crop"))
        UC4(("Delete crop"))
        UC5(("Get disease advice"))
        UC6(("Choose crop"))
        UC7(("Choose symptoms"))
        UC8(("Save advice to history"))
        UC9(("View history"))
        UC10(("Show summary"))
        UC11(("Export CSV or text"))
    end

    U --- UC1
    U --- UC2
    U --- UC3
    U --- UC4
    U --- UC5
    U --- UC9
    U --- UC10
    U --- UC11
    UC5 -.->|include| UC6
    UC5 -.->|include| UC7
    UC5 -.->|include| UC8
```

## 4. Class diagram and component diagram

The program has only two classes. Most of the logic is in functions inside the modules.

```mermaid
classDiagram
    class Record {
        +record_id
        +__init__(record_id)
    }
    class Crop {
        +name
        +field
        +area
        +sowing_date
        +season
        +to_line()
        +__str__()
    }
    Record <|-- Crop
```

Component diagram (which section calls which, inside the one file):

```mermaid
flowchart LR
    Sec8["Section 8: main()"] --> Sec4["Section 4: crop records"]
    Sec8 --> Sec5["Section 5: disease advisor"]
    Sec8 --> Sec7["Section 7: reports"]
    Sec4 --> Sec2["Section 2: Crop class"]
    Sec4 --> Sec3["Section 3: DISEASES"]
    Sec4 --> Sec1["Section 1: helpers"]
    Sec5 --> Sec4
    Sec5 --> Sec3
    Sec5 --> Sec6["Section 6: history.txt"]
    Sec5 --> Sec1
    Sec7 --> Sec4
    Sec7 --> Sec1
    Sec6 --> Sec1
    Sec2 --> Sec1
```

## 5. Sequence diagrams

### 5.1 Add a crop

```mermaid
sequenceDiagram
    actor User
    participant Main as Section 8 (main menu)
    participant CR as Section 4 (crop records)
    participant HP as Section 1 (helpers)
    participant F as crops.txt

    User->>Main: choose 1 Manage crops
    Main->>CR: crops_menu(crops)
    User->>CR: choose 1 Add a crop
    loop for each question
        CR->>HP: ask_...(question)
        HP->>User: ask
        User-->>HP: answer
        alt answer wrong
            HP-->>User: show message and ask again
        else answer good
            HP-->>CR: checked value
        end
    end
    CR->>CR: create Crop and add it to the list
    CR->>F: save_crops(crops)
    CR-->>User: Saved: C001 Wheat (...)
```

### 5.2 Get disease advice

```mermaid
sequenceDiagram
    actor User
    participant DA as Section 5 (disease advisor)
    participant DD as Section 3 (DISEASES)
    participant HI as Section 6 (history.txt)
    participant F as history.txt

    User->>DA: choose 2 Disease advisor, crop ID
    DA->>DD: get_symptoms(crop name)
    DD-->>DA: list of symptoms
    DA-->>User: show numbered symptoms
    User->>DA: symptom numbers
    loop each disease of the crop
        DA->>DA: score_disease(disease, chosen)
    end
    DA-->>User: top 3 with treatment and prevention
    DA->>HI: add_history(...)
    HI->>F: save_history(history)
    HI-->>DA: record
    DA-->>User: Saved to history as A001
```

## 6. Storage design

Data is saved in text files, so the ER diagram is the logical model. The disease list lives inside the program as a Python dictionary.

### 6.1 ER diagram

```mermaid
erDiagram
    CROP ||--o{ ADVISORY : "gets"
    DISEASE ||--o{ ADVISORY : "is top match of"

    CROP {
        string id PK
        string name
        string field
        float area_acres
        string sowing_date
        string season
    }
    DISEASE {
        string crop_name
        string name
        list symptoms
        string treatment
        string prevention
    }
    ADVISORY {
        string id PK
        string time
        string crop_id FK
        string crop_name
        string disease
        float score_percent
        list symptoms
    }
```

`DISEASE` is not a file. It is the dictionary `DISEASES` in Section 3 of `cropcare.py`. A crop is linked to its diseases by the crop name. The advisory line stores the crop name and disease name as text so the history is still readable after a crop is deleted.

### 6.2 Schema design

**crops.txt**: one crop per line, parts separated by `|`

```
C001|Wheat|North Field|2.5|2025-11-15|Rabi
id | crop | field | acres | sowing date | season
```

**history.txt**: one advice per line, symptoms separated by `;`

```
A001|2026-09-19 10:28:25|C001|Wheat|Loose Smut|66.7|symptom one;symptom two
id | time | crop id | crop | top disease | score | symptoms
```

**DISEASES dictionary**

```
DISEASES = { "Wheat": [ {"name": ..., "symptoms": [...], "treatment": ..., "prevention": ...}, ... ], "Rice": [...], ... }
```

| Field | Rule |
|---|---|
| id | `C` or `A` followed by digits, made by the program |
| field name | 1 to 30 characters, no `\|` or `;` |
| area | more than 0 and at most 10000 acres |
| sowing date | `YYYY-MM-DD`, real date, not in the future, year 2000 or later |
| season | Kharif, Rabi or Zaid |

## 7. Design decisions and reasons

| Decision | Instead of | Reason |
|---|---|---|
| Command-line menus | a window (Tkinter) or a website | the course teaches core Python, so the focus stays on the logic |
| Rule-based advisor using sets | machine learning | the course does not cover ML libraries and there is no labelled data. Every score can be explained by hand. |
| Score = matched / all symptoms in both sets | only counting matches | counting alone favours diseases with long symptom lists. This also lowers the score when the user chooses symptoms the disease does not have. |
| Symptoms chosen from a numbered list | typing free text | no spelling problems, so matching is exact |
| Only crops that are in the disease list can be saved | any crop name | a crop without disease data would be useless in the advisor |
| Plain text files with `\|` between parts | JSON or a database | easy to open and read in Notepad, and uses only what the course teaches |
| History stores names as text | storing only ids | the history stays readable after deletions |
| Separate files for each job | one long file | easier to read, test and explain |
| Plain `assert` tests | a test framework | nothing to install, easy to read |

## 8. Disease list, scoring method and evaluation

The assignment asks for these three items for computation-heavy courses. They are included in case the evaluator looks for them.

**Dataset description.** `DISEASES` in Section 3 of `cropcare.py` has 10 diseases for 5 crops (2 each for Wheat, Rice, Tomato, Potato and Maize). Each disease has 3 or 4 symptom phrases, a treatment note and a prevention note. It was written from general agricultural knowledge. Before submitting, check each entry against sources such as ICAR, a state agricultural university or KVK material and list them in the references.

**Scoring method.** For a disease with symptom set D and chosen symptom set S the score is `|D ∩ S| / |D ∪ S| * 100`. It is 100 when S equals D and 0 when they share nothing. A score of 60 or more is High, 30 or more is Medium, below that is Low.

**Evaluation.** There is no labelled field data, so an accuracy percentage would mean nothing and none is claimed. The logic is checked with tests: exact scores, sorted results, the limit of 3, and checks that every disease entry is complete. Manual tests are in `docs/TESTING.md`.

## 9. Future enhancements

- More crops and diseases, and pests.
- Give distinctive symptoms more weight than common ones.
- A window (Tkinter) or a web page, and Hindi language support.
- A machine learning version trained on a labelled dataset (for example from Kaggle) to compare with this rule-based one.
