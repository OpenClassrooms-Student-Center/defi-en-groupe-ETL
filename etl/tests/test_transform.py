from etl.transform.operations import (average, make_absent_none, remove_lowest,
                                      round_grades)
from etl.transform.transform import transform_one


def test_remove_lowest_less_than_three():
    grades = [100, 100, 0]

    assert remove_lowest(grades) == [100, 100, 0]


def test_remove_lowest():
    grades = [100, 100, 100, 0]
    assert remove_lowest(grades) == [100, 100, 100, None]


def test_make_absent_none():
    grades = [100, "A", 100]
    assert make_absent_none(grades) == [100, None, 100]


def test_round_grades():
    grades = [0, 1, 15, 19, 92, 98, 100]
    assert round_grades(grades) == [0, 5, 15, 20, 95, 100, 100]


def test_average_empty_grades():
    grades = []
    assert average(grades) == 0

    grades = [None, None]
    assert average(grades) == 0


def test_average():
    grades = [100, 0]
    assert average(grades) == 50

    grades = [100, 0, None]
    assert average(grades) == 50

    grades = [100, 0, 0]
    assert average(grades) == 33.33


def test_transform_one_graduated():
    student = {
        "name": "Tim",
        "id": "A012345",
        "sections": {
            "computing": {"grades": [100, "A", 100, 0]},
            "other": {"grades": ["A", 0, 80]},
        },
    }

    transformed = transform_one(student)

    assert transformed["sections"]["computing"]["average"] == 66.67
    assert transformed["sections"]["other"]["average"] == 40.00
    assert transformed["average"] == 57.78
    assert transformed["graduated"] == True


def test_transform_one_no_graduated():
    student = {
        "name": "Tim",
        "id": "A012345",
        "sections": {
            "computing": {"grades": ["A", "A", "A", 13]},
            "other": {"grades": ["A", "A", 60]},
        },
    }

    transformed = transform_one(student)

    assert transformed["sections"]["computing"]["average"] == 15.0
    assert transformed["sections"]["other"]["average"] == 60.0
    assert transformed["average"] == 30.0
    assert transformed["graduated"] == False
