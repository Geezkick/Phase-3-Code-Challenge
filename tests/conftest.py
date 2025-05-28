# tests/conftest.py
import pytest
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

@pytest.fixture
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    # Clear tables
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    # Insert test data
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine", "Test Category")
    cursor.execute(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
        ("Test Article", "Content", author.id, magazine.id)
    )
    conn.commit()
    conn.close()
    yield
    # Clean up after tests
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()