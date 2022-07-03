from psycopg2 import connect, ProgrammingError, Error
# from psycopg2.extras import RealDictCursor

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = 'python_messenger'


class Connection:
    def __init__(self):
        self.conn = self.make_connection()
        self.conn.autocommit = True

    def close(self):
        self.conn.close()

    def make_connection(self):
        conn = None
        try:
            conn = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
            return conn
        except Error as e:
            print(f"Couldn't make a connection - ERROR: {e}")
            conn.close()

    def get_cursor(self):
        conn = self.conn
        try:
            # cur = conn.cursor(cursor_factory=RealDictCursor)
            cur = conn.cursor()  # trying regular cursor
            return cur
        except (ProgrammingError, IndexError) as e:
            print(f"Couldn't create and return cursor - ERROR: {e}")
            conn.close()
