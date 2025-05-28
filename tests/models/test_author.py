# lib/models/author.py
from lib.db.connection import get_connection
import sqlite3

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        author = cls(name=name)
        author.save()
        return author

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE authors SET name=? WHERE id=?",
                    (self.name, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name=?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(
            id=row['id'],
            title=row['title'],
            content=row['content'],
            author_id=row['author_id'],
            magazine_id=row['magazine_id']
        ) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(
            id=row['id'],
            name=row['name'],
            category=row['category']
        ) for row in rows]
    print("Loading test_author.py")
from lib.models.author import Author

def test_author_find_by_name(setup_database):
    print("Running test_author_find_by_name")
    author = Author.find_by_name("Test Author")
    print(f"Author found: {author}")
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles(setup_database):
    print("Running test_author_articles")
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    print(f"Articles: {[article.title for article in articles]}")
    assert len(articles) == 1
    assert articles[0].title == "Test Article"