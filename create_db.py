import psycopg2
from psycopg2 import connect, ProgrammingError, Error

# from psycopg2.extras import RealDictCursor

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = 'python_messenger'
try:
    conn = connect(host=HOST, user=USER, password=PASSWORD)
    conn.autocommit = True
    with conn.cursor() as cur:
        sql = f"CREATE DATABASE {DB}"  # can't use parametrization with %s placeholder here ... %s always add quotes
        try:
            cur.execute(sql)
        except ProgrammingError as e:
            print(e)

except (ProgrammingError, psycopg2.OperationalError) as e:
    conn = None
    print(f"connection failed with error {e}")

if conn:
    conn.close()

with connect(host=HOST, user=USER, password=PASSWORD, database=DB) as conn:
    with conn.cursor() as cur:
        sql = """CREATE TABLE users(
                            id serial PRIMARY KEY,
                            username varchar(255),
                            hashed_password varchar(80));"""
        try:
            cur.execute(sql)
        except ProgrammingError as e:
            conn.rollback()
            print(e)

        sql = """CREATE TABLE messages(
                            id serial PRIMARY KEY NOT NULL ,
                            from_id int NOT NULL,
                            to_id int NOT NULL ,
                            creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
                            text varchar(255),
                            FOREIGN KEY(from_id) REFERENCES users(id),
                            FOREIGN KEY(to_id) REFERENCES users(id)
                            );"""
        try:
            cur.execute(sql)
        except ProgrammingError as e:
            conn.rollback()
            print(e)
