from .operations import (average, gpa, make_absent_none, remove_lowest,
                         round_grades)


def transform_one(student_orig):
    """ Transform one student """

    if type(student_orig) is not dict:
        raise TypeError("You must provide a dictionary to transform_one().")
    # We make a copy of the student data
    student = student_orig.copy()

    # These are the sections we are interested about
    mapping = {"computing": None, "other": None}

    for section in mapping:
        # Get the grades for that section
        grades = student["sections"][section]["grades"]
        
        # Make a copy
        new_grades = grades.copy()

        # Transform the grades
        for operation in (remove_lowest, round_grades, make_absent_none):
            new_grades = operation(new_grades)

        # Set the grades, and compute the average
        student["sections"][section]["final_grades"] = new_grades
        student["sections"][section]["average"] = average(new_grades)

    student["graduated"] = False

    # Did the student graduate?
    student["average"] = gpa(student)
    if student["average"] >= 50:
        student["graduated"] = True

    # Return the transformed data
    return student


def transform(students):
    """ Transform a list of students """
    if type(students) is not list:
        raise TypeError("You must provide a list of students to transform().")

    return [transform_one(student) for student in students]

