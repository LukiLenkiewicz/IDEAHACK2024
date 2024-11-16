import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('virtual_sibling.db')
cursor = conn.cursor()

# Insert a user profile (individual)
cursor.execute('''
INSERT INTO user_profiles (name, contact_email, contact_phone, description, experience, skills, website, social_media)
VALUES (
    'John Doe',
    'john.doe@example.com',
    '123-456-7890',
    'Freelance software developer specializing in web applications.',
    '5 years of experience in full-stack development, worked on various projects for startups.',
    'Python, JavaScript, React, Node.js',
    'https://github.com/LukiLenkiewicz/IDEAHACK2024',
    'https://linkedin.com/in/johndoe'
)
''')

# Insert a company profile
cursor.execute('''
INSERT INTO company_profiles (name, contact_email, contact_phone, description, services, experience, industry_keywords, website, social_media)
VALUES (
    'Tech Solutions Inc.',
    'contact@techsolutions.com',
    '987-654-3210',
    'We specialize in AI-driven marketing solutions.',
    'AI-powered marketing analytics and strategy design',
    '10 years of experience in marketing analytics and strategy design.',
    'AI, Marketing, Data Analysis',
    'https://techsolutions.com',
    'https://twitter.com/techsolutions'
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()