import sqlite3

DB_NAME = "bmw_jobs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

def setup_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            ref_no TEXT,
            title TEXT,
            location TEXT,
            legal_entity TEXT,
            field TEXT,
            type TEXT,
            published_date TEXT,
            link TEXT,
            is_new INTEGER
        )
    ''')
    conn.commit()
    return conn

def upsert_job(conn, job):
    c = conn.cursor()
    c.execute('''
        INSERT INTO jobs (id, ref_no, title, location, legal_entity, field, type, published_date, link, is_new)
        VALUES (:id, :ref_no, :title, :location, :legal_entity, :field, :type, :published_date, :link, :is_new)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            location=excluded.location,
            legal_entity=excluded.legal_entity,
            field=excluded.field,
            type=excluded.type,
            published_date=excluded.published_date,
            link=excluded.link,
            is_new=excluded.is_new
    ''', job)
    conn.commit()
    
setup_db()