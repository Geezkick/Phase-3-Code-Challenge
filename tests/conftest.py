import pytest
from lib.db.connection import get_connection
from lib.db.schema import create_tables

@pytest.fixture(autouse=True)
def db_setup():
    """Initialize fresh database for each test"""
    conn = get_connection()
    create_tables(conn)
    
    # Optional: Add test data
    cursor = conn.cursor()
    cursor.executescript("""
        INSERT INTO authors (name) VALUES ('Test Author');
        INSERT INTO magazines (name, category) VALUES ('Test Magazine', 'Test Category');
        INSERT INTO articles (title, author_id, magazine_id) 
        VALUES ('Test Article', 1, 1);
    """)
    conn.commit()
    
    yield  # Test runs here
    
    # Cleanup
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()