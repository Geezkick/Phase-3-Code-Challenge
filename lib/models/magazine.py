from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name=?, category=? WHERE id=?", 
                         (self.name, self.category, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                          (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM magazines WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @classmethod
    def create(cls, name, category):
        magazine = cls(name=name, category=category)
        magazine.save()
        return magazine

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
        return [Article(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(id=row['id'], name=row['name']) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['title'] for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(id=row['id'], name=row['name']) for row in rows]

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None