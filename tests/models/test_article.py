from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection
import pytest

@pytest.fixture
def setup_db():
    # Setup test database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    
    # Create test data
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine", "Test Category")
    article = Article.create("Test Article", author, magazine)
    
    yield article  # This is where the test runs
    
    # Teardown
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_creation(setup_db):
    article = setup_db
    assert article.title == "Test Article"
    assert article.author().name == "Test Author"
    assert article.magazine().name == "Test Magazine"