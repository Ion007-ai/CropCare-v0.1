# test_cropcare.py
# Simple tests using plain assert statements, for the single-file cropcare.py.
# Run from the project folder with:  python tests/test_cropcare.py
# CropCare | Aayan Bhaisal | Reg. No. 26BAI10444 | VIT Bhopal University | B.Tech AI & ML, 1st Year

import os
import sys

sys.path.append(".")    # so Python can find cropcare.py when we run from the project folder

from cropcare import (Crop, DISEASES, add_history, check_area, check_choice,
                      check_date, check_text, crop_from_line, export_csv,
                      find_crop, find_diseases, get_label, get_symptoms,
                      load_crops, load_history, make_new_id, make_summary,
                      save_crops, score_disease, total_area)

TEMP_CROPS = "temp_test_crops.txt"
TEMP_HISTORY = "temp_test_history.txt"
TEMP_CSV = "temp_test_export.csv"


def make_wheat():
    return Crop("C001", "Wheat", "North Field", 2.5, "2025-11-15", "Rabi")


# ---------- helper functions ----------

def test_check_text():
    assert check_text("North Field") == True
    assert check_text("") == False
    assert check_text("a" * 31) == False
    assert check_text("bad|text") == False
    assert check_text("bad;text") == False


def test_check_area():
    assert check_area("2.5") == 2.5
    assert check_area("3") == 3.0
    assert check_area("1.23456") == 1.23
    for bad in ["abc", "", "0", "-1", "nan", "inf", "10001"]:
        assert check_area(bad) is None


def test_check_date():
    assert check_date("2025-11-15") == "2025-11-15"
    assert check_date("2025-1-5") == "2025-01-05"      # is tidied up
    for bad in ["15-11-2025", "2025/11/15", "2025-13-01", "2025-02-30", "hello", "", "2999-01-01", "1999-12-31"]:
        assert check_date(bad) is None


def test_check_choice():
    assert check_choice("wheat", ["Rice", "Wheat"]) == "Wheat"
    assert check_choice("  RICE ", ["Rice", "Wheat"]) == "Rice"
    assert check_choice("banana", ["Rice", "Wheat"]) is None


# ---------- crops ----------

def test_crop_line_round_trip():
    crop = make_wheat()
    line = crop.to_line()
    assert line == "C001|Wheat|North Field|2.5|2025-11-15|Rabi"
    again = crop_from_line(line)
    assert again.name == "Wheat" and again.area == 2.5 and again.record_id == "C001"


def test_damaged_crop_lines_are_rejected():
    assert crop_from_line("hello") is None
    assert crop_from_line("X001|Wheat|A|2|2025-01-01|Rabi") is None
    assert crop_from_line("C001|Wheat|A|many|2025-01-01|Rabi") is None


def test_make_new_id():
    assert make_new_id([]) == "C001"
    crops = [make_wheat(), Crop("C007", "Rice", "B", 1, "2025-01-01", "Kharif")]
    assert make_new_id(crops) == "C008"


def test_find_crop():
    crops = [make_wheat()]
    assert find_crop(crops, "C001").name == "Wheat"
    assert find_crop(crops, "C999") is None


def test_save_and_load_crops():
    crops = [make_wheat(), Crop("C002", "Rice", "River Plot", 3.0, "2026-06-28", "Kharif")]
    assert save_crops(crops, TEMP_CROPS) == True
    loaded = load_crops(TEMP_CROPS)
    assert len(loaded) == 2
    assert loaded[1].name == "Rice" and loaded[1].field == "River Plot"
    os.remove(TEMP_CROPS)


def test_load_missing_file_gives_empty_list():
    assert load_crops("this_file_does_not_exist.txt") == []


def test_damaged_line_is_skipped_not_fatal():
    with open(TEMP_CROPS, "w") as file:
        file.write("C001|Wheat|North Field|2.5|2025-11-15|Rabi\n")
        file.write("this line is broken\n")
        file.write("\n")
    loaded = load_crops(TEMP_CROPS)
    assert len(loaded) == 1
    os.remove(TEMP_CROPS)


def test_save_to_impossible_place_returns_false():
    assert save_crops([make_wheat()], "no_such_folder/crops.txt") == False


# ---------- advisor ----------

def test_symptom_list_has_no_repeats_and_is_sorted():
    symptoms = get_symptoms("Wheat")
    assert len(symptoms) == len(set(symptoms))
    assert symptoms == sorted(symptoms)


def test_score_uses_sets():
    disease = {"symptoms": ["a", "b", "c"]}
    score, matched = score_disease(disease, ["a", "b"])       # 2 matched, 3 in total
    assert score == 66.7 and matched == {"a", "b"}
    assert score_disease(disease, ["a", "b", "z"])[0] == 50.0  # 2 matched, 4 in total
    assert score_disease(disease, ["a", "b", "c"])[0] == 100.0
    assert score_disease(disease, ["x"])[0] == 0.0


def test_labels():
    assert get_label(100) == "High"
    assert get_label(60) == "High"
    assert get_label(45) == "Medium"
    assert get_label(29.9) == "Low"


def test_best_disease_comes_first():
    results = find_diseases("Wheat", ["black powder instead of grains in the ear", "only a bare stalk is left"])
    assert results[0]["name"] == "Loose Smut"
    assert results[0]["score"] == 66.7


def test_results_sorted_and_limited():
    for crop_name in DISEASES:
        symptoms = get_symptoms(crop_name)
        results = find_diseases(crop_name, symptoms)         # choose every symptom
        assert len(results) <= 3
        scores = []
        for result in results:
            scores.append(result["score"])
        assert scores == sorted(scores, reverse=True)


def test_history_is_saved_and_loaded():
    history = []
    crop = make_wheat()
    chosen = ["yellow stripes on leaves", "yellow powder on leaves"]
    results = find_diseases("Wheat", chosen)
    record = add_history(history, crop, chosen, results, TEMP_HISTORY)
    assert record["id"] == "A001" and record["disease"] == "Yellow Rust"
    second = add_history(history, crop, chosen, results, TEMP_HISTORY)
    assert second["id"] == "A002"
    loaded = load_history(TEMP_HISTORY)
    assert len(loaded) == 2 and loaded[0]["crop_name"] == "Wheat"
    assert loaded[0]["symptoms"] == sorted(chosen)
    os.remove(TEMP_HISTORY)


def test_no_match_is_saved_as_no_match():
    history = []
    record = add_history(history, make_wheat(), ["yellow stripes on leaves"], [], TEMP_HISTORY)
    assert record["disease"] == "No match" and record["score"] == 0.0
    os.remove(TEMP_HISTORY)


# ---------- reports ----------

def make_sample_history():
    history = []
    wheat = make_wheat()
    tomato = Crop("C002", "Tomato", "Garden", 1.0, "2026-03-10", "Zaid")
    for crop, symptoms in [(wheat, ["yellow stripes on leaves"]), (wheat, ["yellow stripes on leaves"]),
                           (wheat, ["only a bare stalk is left"]), (tomato, ["dark sunken spots on the stem"])]:
        results = find_diseases(crop.name, symptoms)
        add_history(history, crop, symptoms, results, TEMP_HISTORY)
    os.remove(TEMP_HISTORY)
    return history


def test_total_area_with_any_number_of_values():
    assert total_area(2, 4, 6) == 12
    assert total_area() == 0
    assert total_area(1.5) == 1.5


def test_summary_text():
    crops = [make_wheat(), Crop("C002", "Tomato", "Garden", 1.0, "2026-03-10", "Zaid")]
    text = make_summary(crops, make_sample_history())
    assert "CROPS ON RECORD: 2" in text
    assert "Total area: 3.5 acres" in text
    assert "ADVISORIES: 4" in text
    assert "Yellow Rust: 2 time(s)" in text
    assert "Aayan Bhaisal" in text and "26BAI10444" in text


def test_summary_for_one_crop_only():
    crops = [make_wheat(), Crop("C002", "Tomato", "Garden", 1.0, "2026-03-10", "Zaid")]
    text = make_summary(crops, make_sample_history(), "Tomato")
    assert "CROPS ON RECORD: 1" in text and "ADVISORIES: 1" in text


def test_summary_with_no_data():
    text = make_summary([], [])
    assert "CROPS ON RECORD: 0" in text and "(none yet)" in text


def test_export_csv():
    count = export_csv(make_sample_history(), "Wheat", TEMP_CSV)
    assert count == 3
    with open(TEMP_CSV) as file:
        lines = file.readlines()
    assert len(lines) == 4                    # 1 header + 3 rows
    assert lines[0].startswith("id,time,crop_id")
    os.remove(TEMP_CSV)


def test_export_csv_to_impossible_place():
    assert export_csv([], "", "no_such_folder/out.csv") == -1


# ---------- the disease list itself ----------

def test_disease_list_is_complete():
    assert len(DISEASES) >= 5
    for crop_name in DISEASES:
        assert len(DISEASES[crop_name]) >= 2
        for disease in DISEASES[crop_name]:
            assert disease["name"] != ""
            assert len(disease["symptoms"]) >= 3
            assert len(disease["symptoms"]) == len(set(disease["symptoms"]))
            assert disease["treatment"] != "" and disease["prevention"] != ""
            for symptom in disease["symptoms"]:      # these characters would break the history file
                assert "|" not in symptom and ";" not in symptom


# ---------- run everything ----------

all_tests = [
    test_check_text, test_check_area, test_check_date, test_check_choice,
    test_crop_line_round_trip, test_damaged_crop_lines_are_rejected, test_make_new_id,
    test_find_crop, test_save_and_load_crops, test_load_missing_file_gives_empty_list,
    test_damaged_line_is_skipped_not_fatal, test_save_to_impossible_place_returns_false,
    test_symptom_list_has_no_repeats_and_is_sorted, test_score_uses_sets, test_labels,
    test_best_disease_comes_first, test_results_sorted_and_limited,
    test_history_is_saved_and_loaded, test_no_match_is_saved_as_no_match,
    test_total_area_with_any_number_of_values, test_summary_text,
    test_summary_for_one_crop_only, test_summary_with_no_data,
    test_export_csv, test_export_csv_to_impossible_place, test_disease_list_is_complete,
]

passed = 0
for test in all_tests:
    try:
        test()
        print("PASS:", test.__name__)
        passed = passed + 1
    except AssertionError:
        print("FAIL:", test.__name__)

print()
print(passed, "of", len(all_tests), "tests passed")
if passed != len(all_tests):
    sys.exit(1)
