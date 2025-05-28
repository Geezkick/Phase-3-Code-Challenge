# lib/models/article.py
from lib.db.connection import get_connection
import sqlite3

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        article = cls(title=title, content=content, author_id=author_id, magazine_id=magazine_id)
        article.save()
        return article

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE articles SET title=?, content=?, author_id=?, magazine_id=? WHERE id=?",
                    (self.title, self.content, self.author_id, self.magazine_id, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                    (self.title, self.content, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()