# tests/models/test_article.py
import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_creation(setup_database):
    author = Author.create("New Author")
    magazine = Magazine.create("New Magazine", "New Category")
    article = Article.create("New Article", "New Content", author.id, magazine.id)
    assert article is not None
    assert article.title == "New Article"