from lib.models.magazine import Magazine
from lib.models.author import Author
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
    author1 = Author.create("Author 1")
    author2 = Author.create("Author 2")
    magazine = Magazine.create("Test Magazine", "Test Category")
    Article.create("Article 1", author1, magazine)
    Article.create("Article 2", author1, magazine)
    Article.create("Article 3", author2, magazine)
    
    yield  # This is where the test runs
    
    # Teardown
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_magazine_creation(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    assert magazine is not None
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Test Category"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    articles = magazine.articles()
    assert len(articles) == 3
    assert {a.title for a in articles} == {"Article 1", "Article 2", "Article 3"}

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert {c.name for c in contributors} == {"Author 1", "Author 2"}