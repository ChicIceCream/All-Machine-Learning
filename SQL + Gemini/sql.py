import sqlite3

## Connect to sqlite
connection = sqlite3.connect("student.db")

## Create a cursor to insert record, create and stuff
cursor = connection.cursor()

## creating the table
table_info = """
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), 
SECTION VARCHAR(25), MARKS INT);
"""

cursor.execute(table_info)

## Insert some records

cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS)
VALUES ('John Doe', '10th', 'A', 85),
    ('Jane Smith', '9th', 'B', 92),
    ('Mike Johnson', '11th', 'C', 78);
''')

## Display all the values
data = cursor.execute('''SELECT * from STUDENT''')

print(f"The inserted records are : {[row for row in data]}")

## Close the connection

connection.commit()
connection.close()