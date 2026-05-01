import os
import sqlite3
from fastapi import FastAPI, Query

# Initialize the FastAPI application
app = FastAPI()


# Function to establish a connection to the database
def get_db_connection():
    # Use absolute path to ensure the database file is found in the same directory as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'students.db')

    conn = sqlite3.connect(db_path)
    # Enable Row factory to access columns by name like a dictionary
    conn.row_factory = sqlite3.Row
    return conn


# 1. Path to return students based on a minimum GPA threshold
@app.get("/students/gpafrom/{start_gpa}")
async def get_students_by_gpa(start_gpa: float):
    conn = get_db_connection()
    # Query to select names of students with GPA greater than or equal to start_gpa
    query = 'SELECT name FROM students WHERE gpa >= ?'
    students = conn.execute(query, (start_gpa,)).fetchall()
    conn.close()

    names = [row['name'] for row in students]
    return {"number": len(names), "names": names}


# 2. Path to return students who started in a specific year
@app.get("/students/startyear/{year}")
async def get_students_by_year(year: int):
    conn = get_db_connection()
    # Query to select names of students based on start_year
    query = 'SELECT name FROM students WHERE start_year = ?'
    students = conn.execute(query, (year,)).fetchall()
    conn.close()

    names = [row['name'] for row in students]
    return {"start_year": year, "number": len(names), "names": names}


# 3. Path to return students within a specific start year range
# Modified alias to support underscore in the URL (from_year=2018)
@app.get("/students/yearrange/")
async def get_students_year_range(
        from_year: int = Query(..., alias="from_year"),
        to_year: int = Query(..., alias="to_year")
):
    conn = get_db_connection()
    # Query to select students between two years inclusive
    query = 'SELECT name FROM students WHERE start_year BETWEEN ? AND ?'
    students = conn.execute(query, (from_year, to_year)).fetchall()
    conn.close()

    names = [row['name'] for row in students]
    return {"number": len(names), "names": names}


# Execution block for running the server directly from PyCharm
if __name__ == "__main__":
    import uvicorn

    # Start the Uvicorn server on localhost at port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)