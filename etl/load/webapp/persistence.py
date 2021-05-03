"""Persistence module for the web application

Manages the JSON file used by Flask to display information
"""
import json
from pathlib import Path

# We will use a file located in the same folder as this file
STUDENTS_FILE = Path(__file__).parent / "students.json"


def get_students():
    """ Load students from the local JSON file """
    try:
        with open(STUDENTS_FILE, "r") as fp:
            return json.load(fp)
    except FileNotFoundError:
        # Returns an empty list if the file does not exist
        return list()



def save_students(students):
    """ Save students to the local JSON file """
    data = {student["id"]: student for student in students}
    with open(STUDENTS_FILE, "w") as fp:
        json.dump(data, fp)
