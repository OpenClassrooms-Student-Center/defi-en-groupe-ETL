import json
import operator
from collections import OrderedDict

from flask import Blueprint, render_template, request

from .persistence import STUDENTS_FILE, get_students

students_bp = Blueprint("students", __name__)


@students_bp.route("/")
def list_students():
    students = get_students()

    namesort = "name"
    avgsort = "average"

    sort_key = request.args.get("sort")

    reverse = False
    if sort_key and len(sort_key):
        if sort_key[0] == "-" and len(sort_key) > 1:
            reverse = True
            sort_key = sort_key[1:]

        if sort_key == "name":
            values = sorted(
                students.values(), key=operator.itemgetter("name"), reverse=reverse
            )
            namesort = ["-", ""][reverse] + namesort
        elif sort_key == "average":
            values = sorted(
                students.values(), key=operator.itemgetter("average"), reverse=reverse
            )
            avgsort = ["-", ""][reverse] + avgsort
        else:
            values = students.values()

        students = OrderedDict({s["id"]: s for s in values})

    return render_template(
        "home.html", students=students, namesort=namesort, avgsort=avgsort
    )


@students_bp.route("/student/<string:id_student>/")
def student(id_student):
    students = get_students()
    student = students[id_student]

    return render_template("student.html", student=student)
