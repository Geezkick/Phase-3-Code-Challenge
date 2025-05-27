from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
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
    Article.create("Test Article", author, magazine)
    
    yield  # This is where the test runs
    
    # Teardown
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_author_creation(setup_db):
    author = Author.find_by_name("Test Author")
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_db):
    author = Author.find_by_name("Test Author")
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Test Magazine"