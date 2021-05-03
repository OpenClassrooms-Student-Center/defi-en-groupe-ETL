from pathlib import Path
import csv
from collections import defaultdict

_convert_grades = lambda l: ["A" if i == "A" else float(i) for i in l]

def get_name2id():
    """ Build a mapping student name -> student ID """
    with open("data/students.csv", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        return {
            line["name"]: line["id"]
            for line in reader
        }


def chichigneux():
    """ Extract data from Chichigneux CSV file """

    with open("data/chichigneux.csv", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)

        # Labels are all the fields but the name
        labels = [
            field
            for field in reader.fieldnames
            if field.strip() != "Name"
        ]

        data = [line for line in reader]

    # Get the name/ID mapping
    name2id = get_name2id()

    # Build the output dictionary
    return {
        name2id[line["Name"]]: {
            "labels": labels,
            "grades": _convert_grades([line[key] for key in labels]),
        }
        for line in data
    }


def grapencourt():
    """ Extract data from Grapencourt files """

    # Base folder for grade files
    folder = Path("data") / "grapencourt"

    # Default student dict
    student_dict_factory = lambda: {
        "labels": list(),
        "grades": list(),
    }
    students = defaultdict(student_dict_factory)

    # Let's look at all the grade files
    for filename in folder.glob("*.txt"):
        # And build a nice looking label based on the filename
        nice_name = " ".join(filename.stem.title().split("_"))

        # Read the data
        with open(filename, "r", encoding="utf-8") as fp:
            lines = [line.strip() for line in fp.read().split("\n") if line.strip()]
        
        # Process the data
        for line in lines:
            student_id, *grades = line.split(" ")
            grades = _convert_grades(grades)
            new_labels = [f"{nice_name} {idx+1}" for idx in range(len(grades))]
            students[student_id]["labels"].extend(new_labels)
            students[student_id]["grades"].extend(grades)

    return students

def chichigneux_grapencourt():
    """
    Extract data from both Chichigneux and Grapencourt, and collate all together

    Student names and IDs need to be mapped first!
    """

    students_chi = chichigneux()
    students_gra = grapencourt()

    name2id = get_name2id()

    return [
        {
            "id": student_id,
            "name": name,
            "sections": {
                "computing": students_gra[student_id],
                "other": students_chi[student_id],
            }
        }
        for name, student_id in name2id.items()
    ]