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

def main():
    print("Content-type: text/html\n")

    form = cgi.FieldStorage()
    name = form.getvalue("name")

    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()

        query = f"DELETE FROM student_grades WHERE name = '{name}'"
        cursor.execute(query)

        connection.commit()
        connection.close()

        print(f"<h2>Record for {name} Deleted Successfully!</h2>")

    except Exception as e:
        print(f"<h2>Error occurred: {e}</h2>")

if __name__ == "__main__":
    main()
