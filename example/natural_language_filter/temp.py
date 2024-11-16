import sqlite3

conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()
# Create user_profiles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_email TEXT,
        contact_phone TEXT,
        description TEXT,
        experience TEXT,
        skills TEXT,
        website TEXT,
        social_media TEXT,
        vector_id INTEGER
    )
''')
# Create company_profiles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS company_profiles (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_email TEXT,
        contact_phone TEXT,
        description TEXT,
        services TEXT,
        experience TEXT,
        industry_keywords TEXT,
        website TEXT,
        social_media TEXT,
        vector_id INTEGER
    )
''')
conn.commit()