from lib.db.connection import get_connection
from lib.db.schema import create_tables

def initialize_db():
    conn = get_connection()
    create_tables(conn)
    conn.close()
    print("Database tables created successfully")

if __name__ == '__main__':
    initialize_db()