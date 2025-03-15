from cs50 import SQL
from flask import Flask, render_template, request
import pandas as pd
from csv import DictReader

app = Flask(__name__)

db = SQL("sqlite:///microgrid.db")

## database instructions


@app.route("/")
def index():
    """Load homepage"""
    return render_template("index.html")

@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    """Store user inputted values into the database"""
    devices = ["solar", "wind", "generator", "thermal"]
    if request.method == "POST":
        device = request.form.get("device")
        
# @app.route("/student_search", methods=["GET", "POST"])
# def student():
#     """Search database by student"""
#     global grades
#     if request.method == "POST":
#         student = request.form.get("student")
#         grade = request.form.get("grade")
#         # Check if the student is in the database yet
#         try:
#             grade = int(grade)
#             if grade in grades:
#                 student = f"%{student}%"
#                 info = db.execute(
#                     "SELECT * FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                     student,
#                     grade,
#                 )
#                 if len(info) < 1:
#                     return "Student does not exist in the database. Please check the name spelling and grade."
#                 # If the student is the the database, collect the points and activities for that student
#                 # and output it to a new webpage
#                 else:
#                     points = []
#                     activities = []
#                     for i in range(len(info)):
#                         points.append(
#                             db.execute(
#                                 "SELECT SUM(points) FROM activities WHERE student_id = (?);",
#                                 info[i]["id"],
#                             )
#                         )
#                         activity = db.execute(
#                             "SELECT DISTINCT activity FROM activities WHERE student_id = (?);",
#                             info[i]["id"],
#                         )
#                         if activity == []:
#                             activity = [{"activity": "None"}]
#                         activities.append(activity)
#                     return render_template(
#                         "student_searched.html",
#                         info=info,
#                         points=points,
#                         activities=activities,
#                         len_info=len(info),
#                     )
#             else:
#                 return "Invalid Grade"
#         except TypeError:
#             return "Please enter a valid grade."

#     else:
#         return render_template("student_search.html")


# @app.route("/grade_search", methods=["GET", "POST"])
# def grade():
#     """Search by Grade"""
#     global grades
#     if request.method == "POST":
#         grade = request.form.get("grade")
#         # Select students and their points from the database for the user-specified grade
#         try:
#             grade = int(grade)
#             if grade in grades:
#                 points = []
#                 info = db.execute(
#                     "SELECT * FROM students WHERE grade = (?) ORDER BY student_name;",
#                     grade,
#                 )
#                 for i in range(len(info)):
#                     points.append(
#                         db.execute(
#                             "SELECT SUM(points) FROM activities WHERE student_id = (?);",
#                             info[i]["id"],
#                         )
#                     )
#                 # Output all the students for that grade in a new webpage
#                 return render_template(
#                     "grade_searched.html",
#                     info=info,
#                     points=points,
#                     grade=grade,
#                     len_info=len(info),
#                 )
#         except TypeError:
#             return "Please select a valid grade."
#     else:
#         return render_template("grade_search.html")


# @app.route("/activity_search", methods=["GET", "POST"])
# def activity():
#     """Search by Activity"""
#     if request.method == "POST":
#         activity_input = request.form.get("select")
#         # Check if the activity is valid, then select from the activities database every student
#         # who participated in it and their total points
#         if activity_input in activities_list:
#             points = []
#             activities_info = []
#             names = db.execute(
#                 "SELECT DISTINCT students.student_name, students.id FROM students JOIN activities ON students.id = activities.student_id WHERE activities.activity = (?);",
#                 activity_input,
#             )
#             info = db.execute(
#                 "SELECT students.student_name, students.id, students.grade FROM students JOIN activities ON students.id = activities.student_id WHERE activities.activity = (?);",
#                 activity_input,
#             )
#             for i in range(len(info)):
#                 points.append(
#                     db.execute(
#                         "SELECT SUM(points) FROM activities WHERE student_id = (?);",
#                         info[i]["id"],
#                     )
#                 )
#                 # Organize the students for the chosen activity in a dictionary
#                 for j in range(len(names)):
#                     if names[j]["id"] == info[i]["id"]:
#                         activities_dict = {}
#                         activities_dict["name"] = names[j]["student_name"]
#                         activities_dict["points"] = points[i][0]["SUM(points)"]
#                         activities_dict["grade"] = info[i]["grade"]
#                         activities_info.append(activities_dict)
#             # Output the students and their points for the chosen activity
#             return render_template(
#                 "activity_searched.html",
#                 info=activities_info,
#                 points=points,
#                 len_info=len(info),
#                 chosen_activity=activity_input,
#             )
#     else:
#         return render_template("activity_search.html", activities=activities_list)


# @app.route("/points_search", methods=["GET", "POST"])
# def points():
#     """Search by Points and Grade"""
#     global grades
#     if request.method == "POST":
#         points = request.form.get("points")
#         grade = request.form.get("grade")
#         # Check to make sure the year and grade are valid
#         try:
#             points = int(points)
#             grade = int(grade)
#         except ValueError:
#             return "Please enter a positive integer"
#         except TypeError:
#             return "Please select a valid grade."
#         if points < 0:
#             return "Please enter a positive integer"
#         # Select the students from the specified grade from the database
#         # and append them and their points to a list
#         if grade in grades:
#             total_points = []
#             points_info = []
#             info = db.execute(
#                 "SELECT * FROM students WHERE grade = (?) ORDER BY student_name;", grade
#             )
#             for i in range(len(info)):
#                 total_points.append(
#                     db.execute(
#                         "SELECT SUM(points) FROM activities WHERE student_id = (?);",
#                         info[i]["id"],
#                     )
#                 )
#             # Check if each student in the grade is above or equal to the desired points
#             # threshold. If they are, append them to a list
#             for j in range(len(info)):
#                 if total_points[j][0]["SUM(points)"] is not None:
#                     if total_points[j][0]["SUM(points)"] >= points:
#                         points_dict = {}
#                         points_dict["name"] = info[j]["student_name"]
#                         points_dict["points"] = total_points[j][0]["SUM(points)"]
#                         points_info.append(points_dict)
#             # Output the students and their points for the specified grade and points threshold
#             return render_template(
#                 "points_searched.html",
#                 info=points_info,
#                 grade=grade,
#                 points=points,
#                 len_info=len(points_info),
#             )
#     else:
#         return render_template("points_search.html")


# @app.route("/activity", methods=["GET", "POST"])
# def add_activity():
#     """Add a possible activity"""
#     global activities_list
#     if request.method == "POST":
#         activity = request.form.get("activity")
#         points = request.form.get("points")
#         # Check to make sure the activity already doesn't exist in the database
#         if activity not in activities_list:
#             # Check to make sure the points entered is a valid positive integer
#             try:
#                 points = int(points)
#             except ValueError:
#                 return "Please enter a positive integer"
#             if points < 0:
#                 return "Please enter a positive integer"
#             activities_list.append(activity)
#             db.execute(
#                 "INSERT INTO activity_points(name, points) VALUES ((?), (?));",
#                 activity,
#                 points,
#             )
#         else:
#             return "Activity already exists"
#         # Sort the activities alphabetically and output the entire list of activities
#         # to a new webpage
#         activities_list = sorted(activities_list)
#         return render_template("added_activity.html", activities=activities_list)
#     else:
#         return render_template("activity.html")


# @app.route("/add", methods=["GET", "POST"])
# def add():
#     """Add a student to an activity"""
#     global activities_list
#     global years
#     global grades
#     if request.method == "POST":
#         student = request.form.get("student")
#         grade = request.form.get("grade")
#         activity = request.form.get("activity")
#         year = request.form.get("year")
#         # Check to make sure the year and selected grade is valid
#         try:
#             grade = int(grade)
#             year = int(year)
#             if year in years:
#                 if grade in grades:
#                     # Check if the student already exists in the database
#                     if activity in activities_list:
#                         info = db.execute(
#                             "SELECT * FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                             f"%{student}%",
#                             grade,
#                         )
#                         # If the student is not in the database, the user asked if they want
#                         # to add the student
#                         if len(info) < 1:
#                             return render_template(
#                                 "add_student.html",
#                                 student=request.form.get("student"),
#                                 grade=grade,
#                                 activity=activity,
#                                 year=year,
#                             )
#                         # If the student exists in the database, insert their points and activity
#                         # into the activities table
#                         else:
#                             points = db.execute(
#                                 "SELECT points FROM activity_points WHERE name = (?);",
#                                 activity,
#                             )
#                             id = db.execute(
#                                 "SELECT id FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                                 student,
#                                 grade,
#                             )
#                             db.execute(
#                                 "INSERT INTO activities(student_id, activity, points, year) VALUES ((?), (?), (?), (?));",
#                                 id[0]["id"],
#                                 activity,
#                                 points[0]["points"],
#                                 year,
#                             )
#                             # Output confirmation that the student and their activity was successfully added
#                             return render_template(
#                                 "added.html",
#                                 student=request.form.get("student"),
#                                 activity=activity,
#                             )
#                     else:
#                         return (
#                             "Invalid activity. Please add activity before continuing."
#                         )
#                 else:
#                     return "Invalid grade."
#             else:
#                 return "Invalid year."
#         except ValueError:
#             return "Please submit a valid year and grade."
#         except TypeError:
#             return "Please submit a valid year and grade."
#     else:
#         return render_template("add.html", activities=activities_list, years=years)


# @app.route("/add_student", methods=["GET", "POST"])
# def add_student():
#     """Add a student to the database"""
#     student = request.form.get("student")
#     grade = request.form.get("grade")
#     activity = request.form.get("activity")
#     year = request.form.get("year")
#     if request.method == "POST":
#         # If the user does not want to add the student to the database
#         # the user is redirected back to the page to add students to activities
#         if student == "no" or grade == "no" or activity == "no" or year == "no":
#             return render_template("add.html")
#         else:
#             # If the user wants to add the student to the database,
#             # the student's grade, name, activity, and points are inserted
#             # into the database
#             try:
#                 grade = int(grade)
#                 year = int(year)
#                 db.execute(
#                     "INSERT INTO students(student_name, grade) VALUES ((?), (?));",
#                     student,
#                     grade,
#                 )
#                 points = db.execute(
#                     "SELECT points FROM activity_points WHERE name = (?);", activity
#                 )
#                 id = db.execute(
#                     "SELECT id FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                     f"%{student}%",
#                     grade,
#                 )
#                 db.execute(
#                     "INSERT INTO activities(student_id, activity, points, year) VALUES ((?), (?), (?), (?));",
#                     id[0]["id"],
#                     activity,
#                     points[0]["points"],
#                     year,
#                 )
#                 # Output a confirmation that the student has been successfully added to the database
#                 return render_template(
#                     "added.html", student=request.form.get("student"), activity=activity
#                 )
#             except ValueError:
#                 return "Please select a valid year and grade."
#             except TypeError:
#                 return "Please select a valid year and grade."
#     else:
#         return render_template("add.html")


# @app.route("/team", methods=["GET", "POST"])
# def team():
#     """Add a whole team to an activity"""
#     global activities_list
#     global years
#     if request.method == "POST":
#         team = request.form.get("team")
#         activity = request.form.get("activity")
#         year = request.form.get("year")
#         # Check if the activity and year are valid
#         if activity in activities_list:
#             try:
#                 year = int(year)
#                 if year in years:
#                     # From the form's textarea, write the user's input into a TXT file
#                     with open("team.txt", "w") as file:
#                         file.write("last_name,first_name,grade")
#                         file.write("\n")
#                         file.write(team)
#                     # Source: https://datatofish.com/convert-text-file-to-csv-using-python-tool-included/
#                     # Read the TXT file, remove the whitespaces and output to a CSV fil
#                     read_file = pd.read_csv(r"team.txt", skipinitialspace=True)
#                     read_file.to_csv(r"team.csv", index=None)
#                     # Modified from https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/
#                     # From the CSV file, organize each student's information into a dictionary and append to a list
#                     with open("team.csv", "r") as f:
#                         dict_team = DictReader(f)
#                         list_team = list(dict_team)
#                         add_student = []
#                         for person in list_team:
#                             student = f"%{person['first_name']} {person['last_name']}%"
#                             grade = int(person["grade"])
#                             info = db.execute(
#                                 "SELECT * FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                                 student,
#                                 grade,
#                             )
#                             # If the student is not in the database, they are added to the list of students to be added
#                             if len(info) < 1:
#                                 add_student.append(person)
#                             # If the student is in the database, they are added to the activities database for the specified year
#                             else:
#                                 points = db.execute(
#                                     "SELECT points FROM activity_points WHERE name = (?);",
#                                     activity,
#                                 )
#                                 id = db.execute(
#                                     "SELECT id FROM students WHERE student_name LIKE (?) AND grade = (?);",
#                                     student,
#                                     grade,
#                                 )
#                                 db.execute(
#                                     "INSERT INTO activities(student_id, activity, year, points) VALUES (?, ?, ?, ?);",
#                                     id[0]["id"],
#                                     activity,
#                                     year,
#                                     points[0]["points"],
#                                 )
#                         # If there are any students from the team not in the database, the user is asked if they want to
#                         # add each student in the list
#                         if len(add_student) > 0:
#                             return render_template(
#                                 "add_student_team.html",
#                                 students=add_student,
#                                 activity=activity,
#                                 year=year,
#                             )
#                         # Output of a confirmation that the team was successfully added
#                         else:
#                             return render_template(
#                                 "added_team.html", activity=activity, year=year
#                             )
#                 else:
#                     return "Invalid year"
#             except TypeError:
#                 return "Please select a valid year."
#             except ValueError:
#                 return "Please select a valid year."
#         else:
#             return "Invalid activity"
#     else:
#         return render_template("team.html", activities=activities_list, years=years)


# @app.route("/add_student_team", methods=["GET", "POST"])
# def add_student_team():
#     """Add students not in the database"""
#     global years
#     global activities_list
#     students = request.form.getlist("student")
#     activity = request.form.get("activity")
#     year = request.form.get("year")
#     if request.method == "POST":
#         # Check if the year and activity are valid
#         if activity in activities_list:
#             try:
#                 year = int(year)
#                 if year in years:
#                     i = 0
#                     # For all students, ask the user which ones they want to add to the database
#                     # Students that are selected by the user are added to the students and activities tables
#                     for student in students:
#                         student_grades = request.form.getlist("grade")
#                         grade = student_grades[i]
#                         grade = int(grade)
#                         if student == "no":
#                             i += 1
#                             continue
#                         else:
#                             db.execute(
#                                 "INSERT INTO students(student_name, grade) VALUES (?, ?);",
#                                 student,
#                                 grade,
#                             )
#                             points = db.execute(
#                                 "SELECT points FROM activity_points WHERE name = (?);",
#                                 activity,
#                             )
#                             id = db.execute(
#                                 "SELECT id FROM students WHERE student_name = (?) AND grade = (?);",
#                                 student,
#                                 grade,
#                             )
#                             db.execute(
#                                 "INSERT INTO activities(student_id, activity, year, points) VALUES (?, ?, ?, ?);",
#                                 id[0]["id"],
#                                 activity,
#                                 year,
#                                 points[0]["points"],
#                             )
#                             i += 1
#                     # Output a confirmation to the user that the team has been successfully added to
#                     # the activities table
#                     return render_template(
#                         "added_team.html", activity=activity, year=year
#                     )
#                 else:
#                     return "Invalid year"
#             except TypeError:
#                 return "Please select a valid year."
#             except ValueError:
#                 return "Please select a valid year."
#         else:
#             return "Invalid activity"
#     else:
#         return render_template("team.html", activities=activities_list, years=years)
