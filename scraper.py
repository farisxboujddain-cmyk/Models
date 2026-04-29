import wikipediaapi
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.szjwoxmetphcsxdwomgz:ModelPass20265@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

wiki = wikipediaapi.Wikipedia(
    language='ar',
    user_agent='MyAIProject/1.0'
)

def save_article(title, content):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        """))
        conn.execute(text("""
            INSERT INTO articles (title, content) VALUES (:title, :content)
        """), {"title": title, "content": content})
        conn.commit()
    print(f"✅ تم حفظ: {title}")

def scrape(topic):
    page = wiki.page(topic)
    if page.exists():
        save_article(page.title, page.text)
    else:
        print(f"❌ ما لقيناش: {topic}")

scrape("الذكاء الاصطناعي")
scrape("تعلم الآلة")