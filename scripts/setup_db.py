from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    with open('lib/db/schema.sql', 'r') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup complete!")