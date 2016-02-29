import psycopg2

__author__ = "dbc5ba"

# Daniel Codos (dbc5ba)


def instructor_numbers(dept_id):
    db_name = "course1"
    PG_USER = "postgres"
    PG_USER_PASS = "dan"
    PG_HOST_INFO = " host=/tmp/" # use "" for OS X or Windows
    conn = psycopg2.connect("dbname=" + db_name + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur = conn.cursor()
    cur.execute("SELECT sum(seatsTaken), instructor FROM coursedata WHERE deptID = %s GROUP BY instructor", (dept_id,))
    instructors = {}
    for result in cur.fetchall():
        instructors[result[1]] = result[0]
    conn.commit()
    cur.close()
    conn.close()
    return instructors

if __name__ == "__main__":
    print(instructor_numbers('APMA'))