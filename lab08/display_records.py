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

    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()

        query = "SELECT name, midterm1, midterm2, final FROM student_grades"
        cursor.execute(query)

        records = cursor.fetchall()
        connection.close()

        print("<h2>Student Records</h2>")
        print("<table border='1'>")
        print("<tr><th>Name</th><th>Midterm Exam 1</th><th>Midterm Exam 2</th><th>Final Exam</th><th>Average Score</th></tr>")
        for record in records:
            name, midterm1, midterm2, final = record
            average = calculate_average(midterm1, midterm2, final)
            print(f"<tr><td>{name}</td><td>{midterm1}</td><td>{midterm2}</td><td>{final}</td><td>{average}</td></tr>")
        print("</table>")

    except Exception as e:
        print(f"<h2>Error occurred: {e}</h2>")

if __name__ == "__main__":
    main()
