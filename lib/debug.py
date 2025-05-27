from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def debug():
    # Seed the database first
    seed_database()
    
    # Test queries
    author = Author.find_by_name("John Doe")
    print(f"Author: {author.name}")
    print("Articles:")
    for article in author.articles():
        print(f"- {article.title}")
    
    print("\nMagazines contributed to:")
    for magazine in author.magazines():
        print(f"- {magazine.name} ({magazine.category})")
    
    print("\nTopic areas:")
    print(author.topic_areas())
    
    magazine = Magazine.find_by_name("Tech Today")
    print(f"\nMagazine: {magazine.name}")
    print("Contributing authors with >2 articles:")
    for author in magazine.contributing_authors():
        print(f"- {author.name}")
    
    top_magazine = Magazine.top_publisher()
    print(f"\nTop publisher: {top_magazine.name}")

if __name__ == '__main__':
    debug()