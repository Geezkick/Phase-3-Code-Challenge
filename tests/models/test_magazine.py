# tests/models/test_magazine.py
import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

def test_magazine_creation(setup_database):
    magazine = Magazine.create("New Magazine", "New Category")
    assert magazine is not None
    assert magazine.name == "New Magazine"

def test_magazine_articles(setup_database):
    magazine = Magazine.find_by_name("Test Magazine")  # Use name instead of hardcoding ID
    articles = magazine.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_magazine_contributors(setup_database):
    magazine = Magazine.find_by_name("Test Magazine")  # Use name instead of hardcoding ID
    contributors = magazine.contributors()
    assert len(contributors) == 1
    assert contributors[0].name == "Test Author"