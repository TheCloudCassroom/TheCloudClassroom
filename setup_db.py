"""
Create a local SQLite database from seed_data.json.
Run this once: python setup_db.py
"""
import sqlite3
import json
import os

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/local.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "local.db")

SEED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data.json")

def setup():
    # Remove existing DB to start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create events table (with all columns including course_content, duration, videos)
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE,
            img TEXT,
            grade TEXT,
            link TEXT,
            price TEXT,
            status INTEGER DEFAULT 1,
            start_date DATE,
            end_date DATE,
            category TEXT,
            subject TEXT,
            description TEXT,
            course_content TEXT DEFAULT '',
            duration TEXT DEFAULT '',
            videos TEXT DEFAULT ''
        )
    """)

    # Create instructors table
    c.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT,
            img TEXT
        )
    """)

    # Create events_instructor join table
    c.execute("""
        CREATE TABLE IF NOT EXISTS events_instructor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            instructor_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        )
    """)

    # Load seed data from JSON
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Seed instructors
    for ins in data["instructors"]:
        c.execute(
            "INSERT OR IGNORE INTO instructors (id, name, bio, img) VALUES (?, ?, ?, ?)",
            (ins["id"], ins["name"], ins.get("bio", ""), ins.get("img", ""))
        )

    # Seed events
    for ev in data["events"]:
        c.execute(
            """INSERT OR IGNORE INTO events
               (id, name, slug, img, grade, link, price, status, start_date, end_date,
                category, subject, description, course_content, duration, videos)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (ev["id"], ev["name"], ev.get("slug"), ev.get("img"), ev.get("grade"),
             ev.get("link"), ev.get("price"), ev.get("status", 1),
             ev.get("start_date"), ev.get("end_date"), ev.get("category"),
             ev.get("subject"), ev.get("description"), ev.get("course_content", ""),
             ev.get("duration", ""), ev.get("videos", ""))
        )

    # Seed events_instructor relationships
    for ei in data["events_instructor"]:
        c.execute(
            "INSERT OR IGNORE INTO events_instructor (id, event_id, instructor_id) VALUES (?, ?, ?)",
            (ei["id"], ei["event_id"], ei["instructor_id"])
        )

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")
    print(f"  - {len(data['instructors'])} instructors")
    print(f"  - {len(data['events'])} courses")
    print(f"  - {len(data['events_instructor'])} instructor assignments")

if __name__ == "__main__":
    setup()
