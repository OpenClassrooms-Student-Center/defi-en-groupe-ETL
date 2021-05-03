def filter_grades(grades):
    """ Return a list containing only numerical grades """
    return [
        grade
        for grade in grades
        if type(grade) in (int, float)
    ]


def remove_lowest(grades):
    """
    Replace lowest grade in the list by None
    
    Do not make any changes if there are fewer than 3 grades in the list.
    """
    if len(filter_grades(grades)) <= 3:
        return grades

    idx_lowest = grades.index(min(filter_grades(grades)))
    grades[idx_lowest] = None

    return grades


def make_absent_none(grades):
    """ Replace missing grades (A) with None """ 
    while grades.count("A") and len(filter_grades(grades)):
        idx_absence = grades.index("A")
        grades[idx_absence] = None
    return grades


def round_grades(grades):
    """ Round up the grades to the next multiple of 5 """
    return [
        (g + 4) // 5 * 5 if type(g) in (int, float) else None
        for g in grades
    ]


def average(grades):
    """
    Return the average grade based on a list of grades

    The output should be rounded to 2 decimal places.
    If the list is empty, return 0.
    """
    filtered = filter_grades(grades)

    if not len(filtered):
        return 0

    average = sum(filtered) / len(filtered)
    return round(average, 2)


def gpa(student):
    """ Compute the GPA for a given student """
    gpa = (
        2 * student["sections"]["computing"]["average"]
        + student["sections"]["other"]["average"]
    ) / 3

    return round(gpa, 2)