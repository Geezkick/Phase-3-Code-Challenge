from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction
    articles_data: list of dicts with 'title' and 'magazine_id' keys
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author_name,)
        )
        author_id = cursor.lastrowid
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()

def transfer_articles(from_author_id, to_author_id):
    """
    Transfer all articles from one author to another in a transaction
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Update articles
        cursor.execute(
            "UPDATE articles SET author_id=? WHERE author_id=?",
            (to_author_id, from_author_id)
        )
        
        # Delete original author if they have no more articles
        cursor.execute(
            "DELETE FROM authors WHERE id=? AND NOT EXISTS (SELECT 1 FROM articles WHERE author_id=?)",
            (from_author_id, from_author_id)
        )
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()