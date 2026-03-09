# app.py
from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

# Home page - view students
@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", students=students)

# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        dept = request.form["department"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO students(name,age,department) VALUES(%s,%s,%s)", (name,age,dept))
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")
    return render_template("add_student.html")

# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

# Edit student
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_student(id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        dept = request.form["department"]
        cur.execute("UPDATE students SET name=%s, age=%s, department=%s WHERE id=%s", (name, age, dept, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit_student.html", student=student)

if __name__ == "__main__":
    app.run(debug=True)