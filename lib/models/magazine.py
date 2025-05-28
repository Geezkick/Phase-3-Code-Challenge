# lib/models/magazine.py
from lib.db.connection import get_connection
import sqlite3

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        magazine = cls(name=name, category=category)
        magazine.save()
        return magazine

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE magazines SET name=?, category=? WHERE id=?",
                    (self.name, self.category, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
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
        cursor.execute("SELECT * FROM magazines WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name=?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(
            id=row['id'],
            title=row['title'],
            content=row['content'],
            author_id=row['author_id'],
            magazine_id=row['magazine_id']
        ) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(
            id=row['id'],
            name=row['name']
        ) for row in rows]