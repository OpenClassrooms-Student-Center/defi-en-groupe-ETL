import json

from .webapp.persistence import save_students


def load(students):
    """ Load the students in the JSON file used by the web application """
    if type(students) is not list:
        raise TypeError("You must provide a list of dictionaries.")

    if not len(students):
        raise AttributeError("The list of students is empty.")

    if not all([type(elem) is dict for elem in students]):
        raise TypeError("You must provide a list of dictionaries.")

    save_students(students)
