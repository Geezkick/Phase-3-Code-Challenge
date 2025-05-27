class Author:
    # ... (init and properties as shown earlier)
    
    def articles(self):
        """Get all articles by this author with caching"""
        if not hasattr(self, '_articles'):
            from lib.models.article import Article
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                WHERE author_id = ?
                ORDER BY title
            """, (self.id,))
            self._articles = [Article(**dict(row)) for row in cursor.fetchall()]
            conn.close()
        return self._articles