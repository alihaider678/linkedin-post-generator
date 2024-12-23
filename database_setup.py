import sqlite3

# Function to create database and populate data
def setup_database():
    connection = sqlite3.connect("linkedin_posts.db")
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencer_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            engagement INTEGER NOT NULL,
            language TEXT NOT NULL,
            tags TEXT NOT NULL,
            line_count INTEGER NOT NULL,
            influencer_name TEXT NOT NULL
        )
    ''')

    # Populate with provided data
    influencers = [
        {
            "name": "Influencer 1",
            "posts": [
                ("Focus on Fundamentals, Not Just Tools!...", 300, "English", "Career, Growth", 6),
                ("LSTM model is easier than you think!...", 450, "English", "Machine Learning, LSTM", 9),
                ("Machine Learning is not what it used to be...", 500, "English", "Machine Learning, Startup", 8),
                ("AI in healthcare is projected to grow 20x...", 700, "English", "Healthcare, AI", 11),
                ("Attention Mechanism can be hard to get...", 350, "English", "Attention Mechanism, AI", 9),
            ],
        },
        {
            "name": "Influencer 2",
            "posts": [
                ("I scheduled two interviews for today...", 150, "English", "Recruitment, Work-Life Balance", 5),
                ("I’d love to not hear about ghosting...", 200, "English", "Recruitment, Ghosting", 5),
                ("If you're updating your resume today...", 400, "English", "Resume Tips, Career", 7),
                ("Missed opportunities are part of life...", 500, "English", "Opportunities, Career Growth", 8),
                ("Don’t miss these three essential...", 600, "English", "Resume Tips, Job Search", 9),
            ],
        },
        {
            "name": "Influencer 3",
            "posts": [
                ("Teacher uses AI to inspire students...", 300, "English", "AI, Education", 6),
                ("No needle vaccines in 1967!...", 400, "English", "Healthcare, Vaccines", 7),
                ("Here’s why clear documentation matters!...", 350, "English", "Documentation, Productivity", 5),
                ("You are the Universe?... ", 550, "English", "Philosophy, Neuroscience", 8),
                ("The best visual explanation of...", 450, "English", "Reinforcement Learning, AI", 7),
            ],
        },
    ]

    for influencer in influencers:
        for post in influencer["posts"]:
            cursor.execute('''
                INSERT INTO influencer_posts (text, engagement, language, tags, line_count, influencer_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (post[0], post[1], post[2], post[3], post[4], influencer["name"]))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()
