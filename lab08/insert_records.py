#!/usr/bin/env python3
import cgi
import cgitb
import pymysql

cgitb.enable()

# Database connection settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "student_db"

def calculate_average(midterm1, midterm2, final):
    return (midterm1 + midterm2 + 2 * final) / 4

def main():
    print("Content-type: text/html\n")

    form = cgi.FieldStorage()
    name = form.getvalue("name")
    midterm1 = int(form.getvalue("midterm1"))
    midterm2 = int(form.getvalue("midterm2"))
    final = int(form.getvalue("final"))

    average = calculate_average(midterm1, midterm2, final)

    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()

        query = f"INSERT INTO student_grades (name, midterm1, midterm2, final) VALUES ('{name}', {midterm1}, {midterm2}, {final})"
        cursor.execute(query)

        connection.commit()
        connection.close()

        print("<h2>Record Added Successfully!</h2>")
        print(f"<p>Name: {name}</p>")
        print(f"<p>Midterm Exam 1: {midterm1}</p>")
        print(f"<p>Midterm Exam 2: {midterm2}</p>")
        print(f"<p>Final Exam: {final}</p>")
        print(f"<p>Average Score: {average}</p>")

    except Exception as e:
        print(f"<h2>Error occurred: {e}</h2>")

if __name__ == "__main__":
    main()
