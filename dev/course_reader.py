import csv
import psycopg2

__author__ = "dbc5ba"

# Daniel Codos (dbc5ba)


def load_course_database(db_name, csv_filename):
    PG_USER = "postgres"
    PG_USER_PASS = "dan"
    PG_HOST_INFO = " host=/tmp/" # use "" for OS X or Windows
    conn = psycopg2.connect("dbname=" + db_name + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur = conn.cursor()
    with open(csv_filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO coursedata (deptID, courseNum, semester, meetingType, seatsTaken, seatsOffered, instructor) VALUES (%s, %s, %s, %s, %s, %s, %s)", tuple(row))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_course_database("course1", "seas-courses-5years.csv")