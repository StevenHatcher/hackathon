from cs50 import SQL

db = SQL("sqlite:///extracurr.db")

# Initialize the activity_points table with each activity and their points
for activity in ["Basketball", "Football", "Volleyball", "SLC", "Choir"]:
    db.execute("INSERT INTO activity_points(name, points) VALUES ((?), 10);", activity)

for activity in ["Chess", "AV", "Wrestling", "Dance"]:
    db.execute("INSERT INTO activity_points(name, points) VALUES ((?), 5);", activity)

for activity in ["GSA"]:
    db.execute("INSERT INTO activity_points(name, points) VALUES ((?), 1);", activity)

print("done")
