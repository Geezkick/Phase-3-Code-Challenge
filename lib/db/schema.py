def create_tables(conn):
    """Create all database tables"""
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            UNIQUE(name, category)
        );
        
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
            FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
            UNIQUE(title, author_id, magazine_id)
        );
    """)
    conn.commit()