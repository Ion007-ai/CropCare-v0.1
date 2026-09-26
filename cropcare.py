# =============================================================================
# CropCare - crop record book and disease advisor
#
# Author: Aayan Bhaisal | Reg. No. 26BAI10444
# VIT Bhopal University | B.Tech AI & ML, 1st Year
# Course: Python Essentials (VITyarthi, Build Your Own Project)
#
#
# This file is split into clearly marked sections instead of separate files:
#   SECTION 1: settings and small helper functions (ask, check, log)
#   SECTION 2: the Crop class (Module A data)
#   SECTION 3: the disease list (a dictionary used by Module B)
#   SECTION 4: Module A  - crop records   (add, view, update, delete)
#   SECTION 5: Module B  - disease advisor (symptom matching)
#   SECTION 6: history.txt reading and writing (used by Module B and C)
#   SECTION 7: Module C  - history and reports (summary, CSV/text export)
#   SECTION 8: the main menu and the entry point
# =============================================================================

import csv
import datetime
from array import array

# =============================================================================
# SECTION 1: settings and small helper functions
# =============================================================================

SEASONS = ["Kharif", "Rabi", "Zaid"]
CROPS_FILE = "crops.txt"
HISTORY_FILE = "history.txt"
LOG_FILE = "cropcare_log.txt"
EXPORT_CSV_FILE = "history_export.csv"
EXPORT_TEXT_FILE = "summary_report.txt"
TOP_RESULTS = 3

PROJECT_LINE = "CropCare | Aayan Bhaisal (26BAI10444) | VIT Bhopal University | B.Tech AI & ML, 1st Year"
DISCLAIMER = ("This tool gives educational advice only. Please confirm the disease "
              "and any spray with your local Krishi Vigyan Kendra (KVK) before using chemicals.")


def write_log(message):
    # adds one line with the time to the log file
    # if the file cannot be written, the program just carries on
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(time_now + " | " + message + "\n")
    except OSError:
        pass


# ---------- check functions (they only check, they do not ask) ----------

def check_text(text):
    # True if the text can be stored: 1 to 30 characters, no | or ;
    if text == "":
        return False
    if len(text) > 30:
        return False
    if "|" in text or ";" in text:
        return False
    return True


def check_area(text):
    # returns the area as a number, or None if it is not a good area
    try:
        area = float(text)
    except ValueError:
        return None
    if 0 < area <= 10000:      # this also rejects nan and inf
        return round(area, 2)
    return None


def check_date(text):
    # returns the date as YYYY-MM-DD text, or None if it is wrong or in the future
    try:
        date = datetime.datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None
    if date > datetime.date.today():
        return None
    if date.year < 2000:
        return None
    return date.strftime("%Y-%m-%d")


def check_choice(text, options):
    # compares without caring about capital letters
    # returns the correct spelling from options, or None
    for option in options:
        if option.lower() == text.strip().lower():
            return option
    return None


# ---------- ask functions (they keep asking until the answer is good) ----------

def ask_text(question):
    while True:
        text = input(question).strip()
        if check_text(text):
            return text
        print("  Please type 1 to 30 characters. The characters | and ; are not allowed.")


def ask_area(question):
    while True:
        area = check_area(input(question).strip())
        if area is not None:
            return area
        print("  Please type a number more than 0 and up to 10000, for example 2.5")


def ask_date(question):
    while True:
        date = check_date(input(question).strip())
        if date is not None:
            return date
        print("  Please use the format YYYY-MM-DD (for example 2025-11-15). The date cannot be in the future.")


def ask_choice(question, options):
    while True:
        choice = check_choice(input(question), options)
        if choice is not None:
            return choice
        print("  Please choose one of:", ", ".join(options))


def ask_int(question, low, high):
    while True:
        try:
            number = int(input(question))
        except ValueError:
            print("  Please type a whole number.")
            continue
        if low <= number <= high:
            return number
        print("  Please choose a number from", low, "to", high)


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer == "y" or answer == "yes":
            return True
        if answer == "n" or answer == "no":
            return False
        print("  Please type y or n.")


def ask_number_list(question, high):
    # the user types numbers like 1,3,4 and we return them as a list [1, 3, 4]
    while True:
        parts = input(question).replace(",", " ").split()
        chosen = []
        all_good = len(parts) > 0
        for part in parts:
            if part.isdigit() and 1 <= int(part) <= high:
                if int(part) not in chosen:
                    chosen.append(int(part))
            else:
                all_good = False
        if all_good:
            return chosen
        print("  Please type numbers from 1 to", high, "separated by commas, for example 1,3")


# =============================================================================
# SECTION 2: the Crop class
# =============================================================================

class Record:
    # parent class: anything we save has an id
    def __init__(self, record_id):
        self.record_id = record_id


class Crop(Record):
    # one crop growing in one field
    def __init__(self, crop_id, name, field, area, sowing_date, season):
        super().__init__(crop_id)
        self.name = name
        self.field = field
        self.area = area                  # in acres (a number)
        self.sowing_date = sowing_date    # text like 2025-11-15
        self.season = season

    def to_line(self):
        # one line of text for the crops file, parts separated by |
        parts = [self.record_id, self.name, self.field, str(self.area), self.sowing_date, self.season]
        return "|".join(parts)

    def __str__(self):
        return self.record_id + " " + self.name + " (" + self.field + ", " + str(self.area) + " acres)"


def crop_from_line(line):
    # turns one line of the crops file back into a Crop
    # returns None if the line is damaged
    parts = line.strip().split("|")
    if len(parts) != 6:
        return None
    if not (parts[0].startswith("C") and parts[0][1:].isdigit()):
        return None
    area = check_area(parts[3])
    if area is None:
        return None
    return Crop(parts[0], parts[1], parts[2], area, parts[4], parts[5])


# =============================================================================
# SECTION 3: the disease list (used by Module B)
# =============================================================================

DISEASES = {
    "Wheat": [
        {
            "name": "Yellow Rust",
            "symptoms": [
                "yellow stripes on leaves",
                "yellow powder on leaves",
                "leaves dry up early",
                "shriveled grains",
            ],
            "treatment": "Spray propiconazole (about 0.1%) or tebuconazole when the stripes first appear. Ask your local KVK for the exact dose.",
            "prevention": "Grow rust-resistant varieties, sow on time and avoid too much nitrogen.",
        },
        {
            "name": "Loose Smut",
            "symptoms": [
                "black powder instead of grains in the ear",
                "ears come out earlier than healthy ears",
                "only a bare stalk is left",
            ],
            "treatment": "Infected ears cannot be cured. Remove them in a bag and burn them. Treat next season's seed with carboxin or tebuconazole.",
            "prevention": "Use certified seed and treat the seed before sowing.",
        },
    ],
    "Rice": [
        {
            "name": "Rice Blast",
            "symptoms": [
                "spindle-shaped spots with grey centre on leaves",
                "brown border around leaf spots",
                "neck of the panicle turns brown and breaks",
                "black nodes on the stem",
            ],
            "treatment": "Spray tricyclazole (about 0.6 g per litre of water) when spots first appear. Confirm the dose with your KVK.",
            "prevention": "Use resistant varieties, treat the seed and do not give too much nitrogen at once.",
        },
        {
            "name": "Bacterial Leaf Blight",
            "symptoms": [
                "yellow stripes starting from the leaf tips",
                "wavy yellow or white leaf edges",
                "milky liquid on leaves in the morning",
                "leaves dry up and turn straw coloured",
            ],
            "treatment": "There is no single cure. Drain the field, stop nitrogen top dressing and spray copper oxychloride with streptocycline as your KVK advises.",
            "prevention": "Use resistant varieties and healthy seed, and avoid too much nitrogen.",
        },
    ],
    "Tomato": [
        {
            "name": "Early Blight",
            "symptoms": [
                "dark brown spots with rings on older leaves",
                "yellow area around the spots",
                "dark sunken spots on the stem",
                "dark spots near the fruit stalk",
            ],
            "treatment": "Remove badly affected lower leaves and spray mancozeb (about 0.25%) every 7 to 10 days.",
            "prevention": "Rotate crops, use mulch and avoid wetting the leaves.",
        },
        {
            "name": "Late Blight",
            "symptoms": [
                "dark water-soaked patches on leaves",
                "white fuzzy growth under leaves in humid weather",
                "firm brown patches on fruit",
                "spreads fast in cool wet weather",
            ],
            "treatment": "Spray mancozeb to protect the plants. If the disease has already started, use a metalaxyl plus mancozeb product as your KVK advises.",
            "prevention": "Use healthy seedlings and avoid watering over the leaves.",
        },
    ],
    "Potato": [
        {
            "name": "Late Blight",
            "symptoms": [
                "dark water-soaked patches on leaves",
                "white fuzzy growth under leaves in humid weather",
                "brown rot on tubers",
                "spreads fast in cool wet weather",
            ],
            "treatment": "Spray mancozeb to protect the crop. Once symptoms appear, use a metalaxyl plus mancozeb product as your KVK advises. Destroy infected plant tops before harvest.",
            "prevention": "Plant certified seed tubers, earth up the ridges well and watch the crop in cool wet weather.",
        },
        {
            "name": "Common Scab",
            "symptoms": [
                "rough corky patches on the tuber skin",
                "pitted brown spots on tubers",
                "leaves and plant look healthy",
            ],
            "treatment": "There is no cure once the tubers are affected. It is mostly a cosmetic problem, but do not keep scabby tubers for seed.",
            "prevention": "Keep the soil moist while tubers are forming, avoid liming and use certified seed.",
        },
    ],
    "Maize": [
        {
            "name": "Northern Leaf Blight",
            "symptoms": [
                "long cigar-shaped grey-green spots on leaves",
                "spots turn tan and dry",
                "spots start on the lower leaves",
            ],
            "treatment": "Spray mancozeb (about 0.25%) or propiconazole when spots first appear on the lower leaves. Confirm the dose with your KVK.",
            "prevention": "Grow resistant hybrids, rotate crops and plough in crop residue after harvest.",
        },
        {
            "name": "Common Rust",
            "symptoms": [
                "small reddish-brown powdery pustules on both sides of leaves",
                "pustules turn black late in the season",
                "yellow patches on leaves",
            ],
            "treatment": "Usually no spray is needed. If it appears early and heavily, spray mancozeb (about 0.25%) as your KVK advises.",
            "prevention": "Choose resistant hybrids and sow on time.",
        },
    ],
}

SUPPORTED_CROPS = sorted(DISEASES.keys())


# =============================================================================
# SECTION 4: Module A - crop records (add, view, update, delete)
# =============================================================================

def load_crops(filename=CROPS_FILE):
    # reads the file and returns a list of Crop objects
    crops = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() == "":
                    continue
                crop = crop_from_line(line)
                if crop is None:
                    print("Skipping a damaged line in", filename)
                    write_log("Skipped a damaged line in " + filename)
                else:
                    crops.append(crop)
    except FileNotFoundError:
        pass    # first run: nothing has been saved yet
    return crops


def save_crops(crops, filename=CROPS_FILE):
    # writes all crops to the file, returns True if it worked
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for crop in crops:
                file.write(crop.to_line() + "\n")
        return True
    except OSError:
        print("  Could not save the crops file. Your change was not saved.")
        write_log("Could not save " + filename)
        return False


def make_new_id(crops):
    # finds the highest number used so far and adds 1, for example C003 -> C004
    highest = 0
    for crop in crops:
        number = int(crop.record_id[1:])
        if number > highest:
            highest = number
    return "C" + str(highest + 1).zfill(3)


def find_crop(crops, crop_id):
    # returns the crop with this id, or None
    for crop in crops:
        if crop.record_id == crop_id:
            return crop
    return None


def show_crops(crops):
    if len(crops) == 0:
        print("  No crops saved yet.")
        return
    print("  ID     Crop     Field                 Acres   Sown on     Season")
    print("  " + "-" * 64)
    for crop in crops:
        print("  " + crop.record_id.ljust(7) + crop.name.ljust(9) + crop.field.ljust(22)
              + str(crop.area).rjust(6) + "  " + crop.sowing_date.ljust(12) + crop.season)


def add_crop(crops):
    print("\n--- Add a crop ---")
    print("Supported crops:", ", ".join(SUPPORTED_CROPS))
    name = ask_choice("Crop name: ", SUPPORTED_CROPS)
    field = ask_text("Field name (for example North Field): ")
    area = ask_area("Area in acres (for example 2.5): ")
    sowing_date = ask_date("Sowing date (YYYY-MM-DD): ")
    season = ask_choice("Season (Kharif / Rabi / Zaid): ", SEASONS)

    crop = Crop(make_new_id(crops), name, field, area, sowing_date, season)
    crops.append(crop)
    if save_crops(crops):
        print("  Saved:", crop)
        write_log("Added crop " + crop.record_id)
    else:
        crops.remove(crop)


def update_crop(crops):
    print("\n--- Update a crop ---")
    if len(crops) == 0:
        print("  No crops saved yet.")
        return
    show_crops(crops)
    crop_id = input("Crop ID to update (for example C001): ").strip().upper()
    crop = find_crop(crops, crop_id)
    if crop is None:
        print("  There is no crop with ID", crop_id)
        return

    print("Press Enter to keep the current value.")
    text = input("Crop name [" + crop.name + "]: ").strip()
    if text != "":
        name = check_choice(text, SUPPORTED_CROPS)
        if name is None:
            print("  Not changed: that crop is not supported.")
        else:
            crop.name = name

    text = input("Field name [" + crop.field + "]: ").strip()
    if text != "":
        if check_text(text):
            crop.field = text
        else:
            print("  Not changed: use 1 to 30 characters, no | or ;")

    text = input("Area in acres [" + str(crop.area) + "]: ").strip()
    if text != "":
        area = check_area(text)
        if area is None:
            print("  Not changed: the area must be a number more than 0.")
        else:
            crop.area = area

    text = input("Sowing date [" + crop.sowing_date + "]: ").strip()
    if text != "":
        date = check_date(text)
        if date is None:
            print("  Not changed: use YYYY-MM-DD and not a future date.")
        else:
            crop.sowing_date = date

    text = input("Season [" + crop.season + "]: ").strip()
    if text != "":
        season = check_choice(text, SEASONS)
        if season is None:
            print("  Not changed: choose Kharif, Rabi or Zaid.")
        else:
            crop.season = season

    if save_crops(crops):
        print("  Updated:", crop)
        write_log("Updated crop " + crop.record_id)


def delete_crop(crops):
    print("\n--- Delete a crop ---")
    if len(crops) == 0:
        print("  No crops saved yet.")
        return
    show_crops(crops)
    crop_id = input("Crop ID to delete (for example C001): ").strip().upper()
    crop = find_crop(crops, crop_id)
    if crop is None:
        print("  There is no crop with ID", crop_id)
        return
    if ask_yes_no("Delete " + str(crop) + "? Its advisory history stays saved."):
        crops.remove(crop)
        if save_crops(crops):
            print("  Deleted.")
            write_log("Deleted crop " + crop.record_id)
        else:
            crops.append(crop)
    else:
        print("  Not deleted.")


def crops_menu(crops):
    while True:
        print("\n=== MANAGE CROPS ===")
        print("1. Add a crop")
        print("2. View all crops")
        print("3. Update a crop")
        print("4. Delete a crop")
        print("5. Back")
        choice = ask_int("Choose an option: ", 1, 5)
        if choice == 1:
            add_crop(crops)
        elif choice == 2:
            print("\n--- Saved crops ---")
            show_crops(crops)
        elif choice == 3:
            update_crop(crops)
        elif choice == 4:
            delete_crop(crops)
        else:
            break


# =============================================================================
# SECTION 5: Module B - disease advisor
# =============================================================================

def get_symptoms(crop_name):
    # all the symptoms known for this crop, without repeats, in alphabetical order
    all_symptoms = set()
    for disease in DISEASES[crop_name]:
        for symptom in disease["symptoms"]:
            all_symptoms.add(symptom)
    return sorted(all_symptoms)


def score_disease(disease, chosen):
    # returns (score, matched) where matched is the set of symptoms in common
    disease_symptoms = set(disease["symptoms"])
    chosen_symptoms = set(chosen)
    matched = disease_symptoms & chosen_symptoms       # in both sets
    everything = disease_symptoms | chosen_symptoms    # in either set
    if len(everything) == 0:
        return 0.0, matched
    score = len(matched) / len(everything) * 100
    return round(score, 1), matched


def get_label(score):
    if score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"


def get_score(result):
    # used to sort the results
    return result["score"]


def find_diseases(crop_name, chosen):
    # returns the best matching diseases as a list of dictionaries, best first
    results = []
    for disease in DISEASES[crop_name]:
        score, matched = score_disease(disease, chosen)
        if score > 0:
            results.append({"name": disease["name"], "score": score, "matched": matched,
                            "treatment": disease["treatment"], "prevention": disease["prevention"]})
    results.sort(key=get_score, reverse=True)
    return results[:TOP_RESULTS]


def show_results(crop, results):
    print("\nPossible problems for", crop.name, "(" + crop.record_id + "):")
    if len(results) == 0:
        print("  No disease in the list matches these symptoms.")
        return
    rank = 1
    for result in results:
        print("\n" + str(rank) + ". " + result["name"] + " - match " + str(result["score"])
              + "% (" + get_label(result["score"]) + ")")
        print("   Matched symptoms:", "; ".join(sorted(result["matched"])))
        print("   Treatment:", result["treatment"])
        print("   Prevention:", result["prevention"])
        rank = rank + 1
    print("\n" + DISCLAIMER)


def run_advisor(crops, history):
    print("\n--- Disease advisor ---")
    if len(crops) == 0:
        print("  Add a crop first (Manage crops > Add a crop).")
        return
    show_crops(crops)
    crop_id = input("Crop ID to check (for example C001): ").strip().upper()
    crop = find_crop(crops, crop_id)
    if crop is None:
        print("  There is no crop with ID", crop_id)
        return

    symptoms = get_symptoms(crop.name)
    print("\nSymptoms known for " + crop.name + ":")
    number = 1
    for symptom in symptoms:
        print("  " + str(number).rjust(2) + ". " + symptom)
        number = number + 1

    numbers = ask_number_list("Type the numbers of the symptoms you see (example 1,3): ", len(symptoms))
    chosen = []
    for n in numbers:
        chosen.append(symptoms[n - 1])

    results = find_diseases(crop.name, chosen)
    show_results(crop, results)
    record = add_history(history, crop, chosen, results)
    print("  Saved to history as", record["id"])


# =============================================================================
# SECTION 6: history.txt reading and writing
# =============================================================================

def load_history(filename=HISTORY_FILE):
    # returns a list of dictionaries, one for each saved advisory
    history = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() == "":
                    continue
                parts = line.strip().split("|")
                if len(parts) != 7 or not (parts[0].startswith("A") and parts[0][1:].isdigit()):
                    print("Skipping a damaged line in", filename)
                    write_log("Skipped a damaged line in " + filename)
                    continue
                try:
                    score = float(parts[5])
                except ValueError:
                    print("Skipping a damaged line in", filename)
                    continue
                record = {"id": parts[0], "time": parts[1], "crop_id": parts[2],
                          "crop_name": parts[3], "disease": parts[4], "score": score,
                          "symptoms": parts[6].split(";")}
                history.append(record)
    except FileNotFoundError:
        pass
    return history


def save_history(history, filename=HISTORY_FILE):
    # writes the whole history to the file, returns True if it worked
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for record in history:
                parts = [record["id"], record["time"], record["crop_id"], record["crop_name"],
                         record["disease"], str(record["score"]), ";".join(record["symptoms"])]
                file.write("|".join(parts) + "\n")
        return True
    except OSError:
        print("  Could not save the history file.")
        write_log("Could not save " + filename)
        return False


def add_history(history, crop, chosen, results, filename=HISTORY_FILE):
    # adds one advisory (the top result) to the history and saves it
    highest = 0
    for record in history:
        number = int(record["id"][1:])
        if number > highest:
            highest = number

    if len(results) > 0:
        disease_name = results[0]["name"]
        score = results[0]["score"]
    else:
        disease_name = "No match"
        score = 0.0

    record = {
        "id": "A" + str(highest + 1).zfill(3),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "crop_id": crop.record_id,
        "crop_name": crop.name,
        "disease": disease_name,
        "score": score,
        "symptoms": sorted(chosen),
    }
    history.append(record)
    if save_history(history, filename):
        write_log("Advisory " + record["id"] + " saved for " + crop.record_id)
    else:
        history.remove(record)
    return record


# =============================================================================
# SECTION 7: Module C - history and reports
# =============================================================================

def total_area(*areas):
    # *areas lets us give any number of values, for example total_area(2, 3.5, 1)
    total = 0
    for area in areas:
        total = total + area
    return total


def make_summary(crops, history, crop_name=""):
    # builds the summary report as one piece of text
    # if crop_name is given, only that crop is included
    areas = array("d")          # an array that only holds decimal numbers
    area_by_crop = {}
    for crop in crops:
        if crop_name != "" and crop.name != crop_name:
            continue
        areas.append(crop.area)
        area_by_crop[crop.name] = area_by_crop.get(crop.name, 0) + crop.area

    advisories_by_crop = {}
    disease_counts = {}
    score_sum = 0
    advisory_count = 0
    for record in history:
        if crop_name != "" and record["crop_name"] != crop_name:
            continue
        advisory_count = advisory_count + 1
        score_sum = score_sum + record["score"]
        advisories_by_crop[record["crop_name"]] = advisories_by_crop.get(record["crop_name"], 0) + 1
        if record["disease"] != "No match":
            disease_counts[record["disease"]] = disease_counts.get(record["disease"], 0) + 1

    lines = []
    lines.append("=" * 56)
    lines.append(" CROPCARE SUMMARY REPORT")
    lines.append("=" * 56)
    lines.append("Made on : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if crop_name == "":
        lines.append("Crop    : all crops")
    else:
        lines.append("Crop    : " + crop_name)
    lines.append("")
    lines.append("CROPS ON RECORD: " + str(len(areas)))
    if len(areas) > 0:
        total = total_area(*areas)
        lines.append("  Total area: " + str(round(total, 2)) + " acres")
        lines.append("  Average area: " + str(round(total / len(areas), 2)) + " acres")
        lines.append("  Largest field: " + str(max(areas)) + " acres")
        for name in sorted(area_by_crop):
            lines.append("  - " + name + ": " + str(round(area_by_crop[name], 2)) + " acres")
    lines.append("")
    lines.append("ADVISORIES: " + str(advisory_count))
    for name in sorted(advisories_by_crop):
        lines.append("  - " + name + ": " + str(advisories_by_crop[name]))
    lines.append("")
    lines.append("MOST FREQUENT DIAGNOSES")
    if len(disease_counts) == 0:
        lines.append("  (none yet)")
    else:
        pairs = []
        for name in disease_counts:
            pairs.append((disease_counts[name], name))
        pairs.sort(reverse=True)            # biggest count first
        for count, name in pairs[:3]:
            lines.append("  - " + name + ": " + str(count) + " time(s)")
    if advisory_count > 0:
        lines.append("")
        lines.append("Average top-match score: " + str(round(score_sum / advisory_count, 1)) + "%")
    lines.append("")
    lines.append("-" * 56)
    lines.append(DISCLAIMER)
    lines.append(PROJECT_LINE)
    return "\n".join(lines)


def export_csv(history, crop_name="", filename=EXPORT_CSV_FILE):
    # saves the history as a CSV file (opens in Excel), returns how many rows were written
    # returns -1 if the file could not be written
    count = 0
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "time", "crop_id", "crop_name", "disease", "score_percent", "symptoms"])
            for record in history:
                if crop_name != "" and record["crop_name"] != crop_name:
                    continue
                writer.writerow([record["id"], record["time"], record["crop_id"], record["crop_name"],
                                 record["disease"], record["score"], "; ".join(record["symptoms"])])
                count = count + 1
    except OSError:
        return -1
    write_log("Exported " + str(count) + " rows to " + filename)
    return count


def export_text(text, filename=EXPORT_TEXT_FILE):
    # saves the summary text to a file, returns True if it worked
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text + "\n")
    except OSError:
        return False
    write_log("Saved summary to " + filename)
    return True


def show_history(history):
    print("\n--- Advisory history (latest 10) ---")
    if len(history) == 0:
        print("  No advisories yet.")
        return
    print("  ID     When                 Crop     Top match                Score")
    print("  " + "-" * 68)
    for record in history[-10:]:
        print("  " + record["id"].ljust(7) + record["time"].ljust(21) + record["crop_name"].ljust(9)
              + record["disease"].ljust(25) + str(record["score"]) + "%")


def ask_crop_filter():
    # returns a crop name, or "" for all crops
    while True:
        text = input("Only one crop? Type its name or press Enter for all: ").strip()
        if text == "":
            return ""
        name = check_choice(text, SUPPORTED_CROPS)
        if name is not None:
            return name
        print("  Please choose one of:", ", ".join(SUPPORTED_CROPS))


def reports_menu(crops, history):
    while True:
        print("\n=== HISTORY & REPORTS ===")
        print("1. View advisory history")
        print("2. Show summary report")
        print("3. Export history to CSV")
        print("4. Save summary to a text file")
        print("5. Back")
        choice = ask_int("Choose an option: ", 1, 5)
        if choice == 1:
            show_history(history)
        elif choice == 2:
            print()
            print(make_summary(crops, history, ask_crop_filter()))
        elif choice == 3:
            count = export_csv(history, ask_crop_filter())
            if count == -1:
                print("  Could not write the CSV file.")
            else:
                print("  Saved", count, "row(s) to", EXPORT_CSV_FILE)
        elif choice == 4:
            if export_text(make_summary(crops, history, ask_crop_filter())):
                print("  Saved to", EXPORT_TEXT_FILE)
            else:
                print("  Could not write the file.")
        else:
            break


# =============================================================================
# SECTION 8: main menu and entry point
# =============================================================================

def main():
    print("=" * 60)
    print("  CropCare - crop record book and disease advisor")
    print("  Aayan Bhaisal | Reg. No. 26BAI10444")
    print("  VIT Bhopal University | B.Tech AI & ML, 1st Year")
    print("=" * 60)
    print(DISCLAIMER)

    crops = load_crops()
    history = load_history()
    write_log("Program started")

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Manage crops")
        print("2. Disease advisor")
        print("3. History & reports")
        print("4. Exit")
        choice = ask_int("Choose an option: ", 1, 4)
        if choice == 1:
            crops_menu(crops)
        elif choice == 2:
            run_advisor(crops, history)
        elif choice == 3:
            reports_menu(crops, history)
        else:
            print("Goodbye!")
            write_log("Program closed")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
