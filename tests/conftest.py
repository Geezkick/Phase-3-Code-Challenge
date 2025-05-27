import pytest
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
    """)
    conn.commit()
    conn.close()