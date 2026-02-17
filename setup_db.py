"""
Create a local SQLite database with data matching the production site.
Run this once: python setup_db.py
"""
import sqlite3
import os

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/local.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "local.db")

def setup():
    # Remove existing DB to start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create events table
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
            description TEXT
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

    # Seed instructors
    instructors = [
        (1, "Cloud Classroom Team", "Cloud Classroom instructors and teaching assistants.", "/static/images/instructor-1.jpg"),
    ]
    c.executemany("INSERT OR IGNORE INTO instructors (id, name, bio, img) VALUES (?, ?, ?, ?)", instructors)

    # Seed events (courses) matching the production site at thecloudclassroom.org
    # Format: (id, name, slug, img, grade, link, price, status, start_date, end_date, category, subject, description)
    events = [
        (1, "AP US History Free Response Question Workshop", "2020-winter-ap-us-history-free-response",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155afa8d69b9e4b7ee82e43_AP%20US%20History%20Free%20Response.jpg", "G9-G12", "/product/2020-winter-ap-us-history-free-response", "$ 60.00 USD",
         1, "2020-12-01", "2026-12-31", "History", "AP US History", "Workshop focused on AP US History free response questions."),
        (2, "AP World History Free Response Question Workshop", "2020-winter-ap-world-history-free-response",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155afe47599001bdaf7cbfd_AP%20World%20History%20Free%20Response.jpg", "G9-G12", "/product/2020-winter-ap-world-history-free-response", "$ 60.00 USD",
         1, "2020-12-01", "2026-12-31", "History", "AP World History", "Workshop focused on AP World History free response questions."),
        (3, "Basic English Learning Grades 1-2 (G1-G2)", "2020-summer-basic-english-learning-grades-1-2",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a696514fd68346eeeb68_Basic%20English%20Learning%20Grade1-2.jpg", "G1-G2", "/product/2020-summer-basic-english-learning-grades-1-2", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Language Arts", "English", "Basic English reading and writing for grades 1-2."),
        (4, "Basic Geometry (G5 - G8)", "2021-summer-basic-geometry",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175014a53242000bc7f4cc1_Basic%20Geometry.png", "G5-G8", "/product/2021-summer-basic-geometry", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Math", "Geometry", "Introduction to basic geometry concepts."),
        (5, "Basic Math for Grade 2-3 (G2-G3)", "2020-summer-basic-math-for-grade-2-3",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a77ad1e84b4ea2c524c6_Basic%20Math%20for%20Grade2-3.jpg", "G2-G3", "/product/2020-summer-basic-math-for-grade-2-3", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Math", "Fundamental math skills for grades 2-3."),
        (6, "CS201(A) - Inroduction to Scratch US Class (G2-G5)", "2021-summer-inroduction-to-scratch-us-class",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bbe9726aac6903fe328f5_Introduction%20to%20Scratch%20(%20US%20).png", "G2-G5", "/product/2021-summer-inroduction-to-scratch-us-class", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Scratch", "Learn programming with Scratch - US class."),
        (7, "CS201(B) - Inroduction to Scratch China Class (G2-G5)", "2021-summer-inroduction-to-scratch-china-class",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bbe9726aac6903fe328f5_Introduction%20to%20Scratch%20(%20US%20).png", "G2-G5", "/product/2021-summer-inroduction-to-scratch-china-class", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Scratch", "Learn programming with Scratch - China class."),
        (8, "CS202 - Introduction to Scratch for Kenya (G3-G5)", "cs202-introduction-to-scratch-g3-g5",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a85c63cf824574b50da2b8_intro%20to%20scratch.png", "G3-G5", "/product/cs202-introduction-to-scratch-g3-g5", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Scratch", "Introduction to Scratch for students in Kenya."),
        (9, "CS304 - Introduction to Java (G5-G9)", "cs304-introduction-to-java-g5-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290fbd9ddf6bbb5793a7996_intro%20to%20java.png", "G5-G9", "/product/cs304-introduction-to-java-g5-g9", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Java", "Introduction to Java programming."),
        (10, "CS305 - Introduction to Python for Kenya (G4-G8)", "cs305-introduction-to-python-for-kenya-g4-g8",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a861eee8bcc8cd7c075e6b_intro%20to%20python.png", "G4-G8", "/product/cs305-introduction-to-python-for-kenya-g4-g8", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Python", "Introduction to Python for students in Kenya."),
        (11, "CS306 - Introduction to Web Development for Kenya (G4-G8)", "cs306-introduction-to-web-development-for-kenya-g4-g8",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a867c89558fd178166c0fc_intro%20to%20web%20dev.png", "G4-G8", "/product/cs306-introduction-to-web-development-for-kenya-g4-g8", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Web Development", "Introduction to web development for Kenya."),
        (12, "CS307 - Algorithm with Java", "cs307-algorithm-with-java",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb94781adae704033c0baf_CS307%20-%20Algorithm%20with%20Java.png", "G4-G8", "/product/cs307-algorithm-with-java", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Java", "Algorithms and data structures with Java."),
        (13, "CS308 - Basics of Web Development", "cs308-basics-of-web-development",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb95a3ba5b0b7c45061f57_CS308%20-%20Basics%20of%20Web%20Development.png", "G4-G8", "/product/cs308-basics-of-web-development", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Web Development", "Basics of HTML, CSS, and JavaScript."),
        (14, "CS401 - Introduction to Java for Kenya (G6-G9)", "cs401-introduction-to-java-for-kenya-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a86bc3a22a86887e3462ae_intro%20to%20Java.png", "G6-G9", "/product/cs401-introduction-to-java-for-kenya-g6-g9", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Java", "Introduction to Java for Kenya students."),
        (15, "Close Reading Session 1 Hamlet (G4-G9)", "2020-fall-close-reading-session-1-hamlet",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a1147e925115082ecf1d_Close%20Reading%20Session1%20Hamlet.jpg", "G4-G9", "/product/2020-fall-close-reading-session-1-hamlet", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "English", "Close reading analysis of Hamlet."),
        (16, "Digital Art Workshop (G3+)", "2020-winter-digital-art-workshop",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155b02b31fbafe20e219b13_Digital%20Art%20Workshop.jpg", "G3+", "/product/2020-winter-digital-art-workshop", "$ 60.00 USD",
         1, "2020-12-01", "2026-12-31", "Art", "Digital Art", "Learn digital art techniques and tools."),
        (17, "FR103 - French level 1 for beginners (G4-G9)", "french-level-1-for-beginners-fr103",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/604eccfd1a63f07b2d575d28_French.jpg", "G4-G9", "/product/french-level-1-for-beginners-fr103", "$ 180.00 USD",
         1, "2021-01-01", "2026-12-31", "Language", "French", "Beginning French language course."),
        (18, "FR105 - Basic French (G4-G9)", "2021-winter-fr105-basic-french",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e139e22d857b53b1df2eb2_French.png", "G4-G9", "/product/2021-winter-fr105-basic-french", "$ 180.00 USD",
         1, "2021-01-01", "2026-12-31", "Language", "French", "Basic French language skills."),
        (19, "FR105 - French Class for Beginners (G4-G9)", "fr105-french-class-for-beginners-g4-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e139e22d857b53b1df2eb2_French.png", "G4-G9", "/product/fr105-french-class-for-beginners-g4-g9", "$ 180.00 USD",
         1, "2021-06-01", "2026-12-31", "Language", "French", "French class for beginners."),
        (20, "French (G4-G9)", "2020-fall-french",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a2dd5318f26f0f6bee1b_French.jpg", "G4-G9", "/product/2020-fall-french", "$ 180.00 USD",
         1, "2020-09-01", "2026-12-31", "Language", "French", "French language course."),
        (21, "Geometry (G7-G10+)", "2020-summer-geometry-g7-g10",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a91d87dc7de5b2171932_Geometry%20G7-G10%2B.jpg", "G7-G10+", "/product/2020-summer-geometry-g7-g10", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Geometry", "Geometry for advanced students."),
        (22, "HIST102 - Introduction to Ancient Roman & Ottoman Empire (G3-G4)", "2021-spring-introduction-to-ancient-roman-ottoman-empire-hist102",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/617526ea28685f41555e0ecf_reading%20club%20g4-g6%20%E5%89%AF%E6%9C%AC.png", "G3-G4", "/product/2021-spring-introduction-to-ancient-roman-ottoman-empire-hist102", "$ 0.00 USD",
         1, "2021-03-01", "2026-12-31", "History", "History", "Explore ancient Roman and Ottoman Empire history."),
        (23, "HIST305 - European History (G6 - G12)", "2021-fall-hist305-european-history-g6-g12",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618fb0c04bdf486dfcf2b5e0_HIST305.jpg", "G6-G12", "/product/2021-fall-hist305-european-history-g6-g12", "$ 75.00 USD",
         1, "2021-09-01", "2026-12-31", "History", "History", "European history survey course."),
        (24, "HIST307 - England and the British Empire", "2021-winter-hist307-england-and-the-british-empire",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4933407d430540a39622_HIST307-test%20no%20tuition.png", "G4-G6", "/product/2021-winter-hist307-england-and-the-british-empire", "$ 75.00 USD",
         1, "2021-12-01", "2026-12-31", "History", "History", "History of England and the British Empire."),
        (25, "HIST307 - England and the British Empire (G4-G6)", "hist307-england-and-the-british-empire-g4-g6",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e13b6f3d3724977a2f0538_HIST307-England.png", "G4-G6", "/product/hist307-england-and-the-british-empire-g4-g6", "$ 75.00 USD",
         1, "2022-01-01", "2026-12-31", "History", "History", "England and the British Empire for younger students."),
        (26, "HIST311 - History of Art", "hist311-history-of-art",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb85896b4ad5fcc2e6bfb1_WRT408%20-%202023%20Summer.png", "G6-G9", "/product/hist311-history-of-art", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "History", "Art History", "Survey of art history."),
        (27, "HIST312 - History of Japan", "hist312-history-of-japan",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb929a7189ac01d323e36d_HIST312%20-%20Japan.png", "G6-G9", "/product/hist312-history-of-japan", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "History", "History", "History of Japan from ancient to modern times."),
        (28, "History Camp - Explore Ancient Egypt & Greece (G5 - G12)", "2020-december-winter-history-camp-g5-g12-explore-ancient-egypt-greece",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155af2cf43d8f0fea6b4536_2020%20December%20Winter%20History%20Camp(%20G5%20-%20G12).jpg", "G5-G12", "/product/2020-december-winter-history-camp-g5-g12-explore-ancient-egypt-greece", "$ 60.00 USD",
         1, "2020-12-01", "2026-12-31", "History", "History", "Explore ancient Egypt and Greece."),
        (29, "Introduction to Web Development", "2021-summer-intro-to-web-development",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bd21be2252ba57efa7222_Intro%20%20to%20Web%20Development.jpg", "G6-G9", "/product/2021-summer-intro-to-web-development", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Web Development", "Learn the basics of web development."),
        (30, "Introduction To Public Speaking", "2020-summer-introduction-to-public-speaking",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ac2d755a334f1300b791_IntroductionToPublicSpeaking.jpg", "G4-G9", "/product/2020-summer-introduction-to-public-speaking", "$ 60.00 USD",
         1, "2020-07-01", "2026-12-31", "Language Arts", "Public Speaking", "Build confidence in public speaking."),
        (31, "Introduction to Geometry (G7-G10+)", "2020-summer-introduction-to-geometry-g7-g10",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcc28445d1c82ba9eee0e_cover1.png", "G7-G10+", "/product/2020-summer-introduction-to-geometry-g7-g10", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Geometry", "Introduction to geometry concepts."),
        (32, "Introduction to Grade 3 Math (G3)", "2020-winter-introduction-to-grade-3-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175284d266d4a801a10bc20_Introduction%20to%20Grade%203%20Math.jpg", "G3", "/product/2020-winter-introduction-to-grade-3-math", "$ 0.00 USD",
         1, "2020-12-01", "2026-12-31", "Math", "Math", "Introduction to grade 3 math topics."),
        (33, "Introduction to Grade 4 Math (G4)", "2020-summer-introduction-to-grade-4-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155aaed6fae1b6e9739fed6_Introduction%20to%20Grade4%20Math.jpg", "G4", "/product/2020-summer-introduction-to-grade-4-math", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Math", "Introduction to grade 4 math topics."),
        (34, "Introduction to Grade 4 Math (G4)", "2020-winter-introduction-to-grade-4-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155b21b56bc133d916dccc0_Introduction%20to%20Grade%204%20Math.jpg", "G4", "/product/2020-winter-introduction-to-grade-4-math", "$ 0.00 USD",
         1, "2020-12-01", "2026-12-31", "Math", "Math", "Grade 4 math - winter session."),
        (35, "Introduction to Grade 4 Math (Grade 4)", "2021-summer-introduction-to-g4-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcb9eb531b9f825a552c2_intro%20to%20grade%204%20math%20%E5%89%AF%E6%9C%AC.png", "G4", "/product/2021-summer-introduction-to-g4-math", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Math", "Math", "Grade 4 math - summer session."),
        (36, "Introduction to Grade 5 Math (G5)", "2020-summer-introduction-to-grade-5-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175298c41c3c880ce55367f_Introduction%20to%20Grade5%20Math.jpg", "G5", "/product/2020-summer-introduction-to-grade-5-math", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Math", "Introduction to grade 5 math."),
        (37, "Introduction to Grade 5 Math (G5)", "2020-winter-introduction-to-grade-5-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6174fb0453242090227f387f_Introduction%20to%20Grade%205%20Math.jpg", "G5", "/product/2020-winter-introduction-to-grade-5-math", "$ 0.00 USD",
         1, "2020-12-01", "2026-12-31", "Math", "Math", "Grade 5 math - winter session."),
        (38, "Introduction to Grade 6 Math (Grade 6)", "2020-summer-introduction-to-grade-6-math",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6174f726d02509db585a0310_Introduction%20to%20Grade%206%20Math.jpg", "G6", "/product/2020-summer-introduction-to-grade-6-math", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Math", "Introduction to grade 6 math."),
        (39, "Introduction to Python & Games Dev", "2021-summer-introduction-to-python-games-dev",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a861eee8bcc8cd7c075e6b_intro%20to%20python.png", "G4-G8", "/product/2021-summer-introduction-to-python-games-dev", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Computer Science", "Python", "Learn Python through game development."),
        (40, "Introduction to Python (China Class)", "2020-fall-introduction-to-python-china-class",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752bdc192a7676a27afbcf_Introduction%20to%20Python.jpg", "G4-G6", "/product/2020-fall-introduction-to-python-china-class", "$ 0.00 USD",
         1, "2020-09-01", "2026-12-31", "Computer Science", "Python", "Introduction to Python - China class."),
        (41, "Introduction to Python US Class (G4-G6)", "2020-fall-introduction-to-python",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752a85e70dd0505761386d_Introduction%20to%20Python.jpg", "G4-G6", "/product/2020-fall-introduction-to-python", "$ 0.00 USD",
         1, "2020-09-01", "2026-12-31", "Computer Science", "Python", "Introduction to Python - US class."),
        (42, "Introduction to Web Development with Python & JavaScript", "2020-summer-introduction-to-web-development-with-python-javascript",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bd21be2252ba57efa7222_Intro%20%20to%20Web%20Development.jpg", "G6+", "/product/2020-summer-introduction-to-web-development-with-python-javascript", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Computer Science", "Web Development", "Full-stack web development with Python and JavaScript."),
        (43, "LA204 - the Lion & the Witch and the Wardrobe and Prince Caspian (G3-G4)", "literature-analysis-la204",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b5db81999dc17eeace7d61_LA%20204.png", "G3-G4", "/product/literature-analysis-la204", "$ 60.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Chronicles of Narnia."),
        (44, "LA205 - The Silver Chair & The Last Battle (G3-G4)", "literature-analysis-la205",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614d9f54266cd61b08d0ee8c_LA205.jpg", "G3-G4", "/product/literature-analysis-la205", "$ 60.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Narnia books."),
        (45, "LA206 - Novels by Andersen (G3 - G4)", "2021-fall-la206-literary-analysis-g3-g4",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618fab8297525729a51a26d2_LA206.jpg", "G3-G4", "/product/2021-fall-la206-literary-analysis-g3-g4", "$ 75.00 USD",
         1, "2021-09-01", "2026-12-31", "Language Arts", "Literature", "Analysis of novels by Andersen."),
        (46, "LA207 - Mr. Frizby and the Rats of Nimh (G3 - G4)", "2021-winter-la207-literary-analysis-g3-g4",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4a47ae40a20845712e91_LA207%20%20%E8%80%81%E9%BC%A0%20no%20tuition.png", "G3-G4", "/product/2021-winter-la207-literary-analysis-g3-g4", "$ 0.00 USD",
         1, "2021-12-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Mrs. Frisby and the Rats of NIMH."),
        (47, "LA207 - Mrs. Frizby and the Rats of Nimh (G3-G4)", "la207-mrs-frizby-and-the-rats-of-nimh-g3-g4",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4a47ae40a20845712e91_LA207%20%20%E8%80%81%E9%BC%A0%20no%20tuition.png", "G3-G4", "/product/la207-mrs-frizby-and-the-rats-of-nimh-g3-g4", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Mrs. Frisby."),
        (48, "LA208 - Diary of a Wimpy Kid & A Long Walk to Water (G3-G4)", "la208-diary-of-a-wimpy-kid-a-long-walk-to-water-g3-g4",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290ec114f89143deca3ef50_LA208-%E5%A4%8F%E4%BB%A4%E6%97%B6-%E6%8E%A8%E8%BF%9F.png", "G3-G4", "/product/la208-diary-of-a-wimpy-kid-a-long-walk-to-water-g3-g4", "$ 60.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Diary of a Wimpy Kid."),
        (49, "LA307 - Les Miserable & Death on the Nile (G4-G6)", "literature-analysis-la307",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b181f367986cef83cd55dc_LA%20307%20(1).png", "G4-G6", "/product/literature-analysis-la307", "$ 75.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Les Miserables and Death on the Nile."),
        (50, "LA308 - Dr. Jekyll and Mr. Hyde & Brave New World (G4-G6)", "literature-analysis-la308",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614e95e44145580725b31a4f_800657712247a1e7c2d52a1a80fa40c.jpg", "G4-G6", "/product/literature-analysis-la308", "$ 60.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of classic novels."),
        (51, "LA309 - The Hobbit & The Lord of The Rings (G4 - G6)", "2021-fall-la309-literary-analysis-g4-g6",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4cfee2aa7c1584547ac5_LA309%20%E6%8C%87%E7%8E%AF%E7%8E%8B%20no%20tuition.png", "G4-G6", "/product/2021-fall-la309-literary-analysis-g4-g6", "$ 105.00 USD",
         1, "2021-09-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Tolkien's works."),
        (52, "LA310 - Number the Stars & the Giver (G3-G6)", "la310-french-class-for-beginners-g4-g9-copy",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd47123ca60b2dd78b57d7_LA310%20%20%E6%95%B0%E6%98%9F%E6%98%9F%20no%20tuition.png", "G3-G6", "/product/la310-french-class-for-beginners-g4-g9-copy", "$ 60.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Number the Stars and The Giver."),
        (53, "LA311 - A Separate Peace & The Outsiders (G4-G6)", "la311-a-separate-peace-the-outsiders-g4-g6",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd41b8302a5e0d73fd7fef_LA311%20%E4%B8%80%E4%B8%AA%E4%BA%BA%E7%9A%84%E5%92%8C%E5%B9%B3%20no%20tuition.png", "G4-G6", "/product/la311-a-separate-peace-the-outsiders-g4-g6", "$ 60.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of A Separate Peace and The Outsiders."),
        (54, "LA405 - A Tale of Two Cities & The Demolished Man (G6-G9)", "literature-analysis-la405",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b5d8e7ca5d3a8ecb6eefb5_LA%20405%20(1).png", "G6-G9", "/product/literature-analysis-la405", "$ 75.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of classic novels."),
        (55, "LA406 - Fail Safe & Hunt for Red October (G6-G9)", "literature-analysis-la406",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614e9b7a84f75404062b5f7b_8f1ea80d9ee87307cd8cdd45d26de3d.jpg", "G6-G9", "/product/literature-analysis-la406", "$ 60.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of thriller novels."),
        (56, "LA408 - Pride and Prejudice & Jane Eyre (G6 - G9)", "2021-fall-la408-literary-analysis-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618bd484510f0adb861806df_LA408.jpg", "G6-G9", "/product/2021-fall-la408-literary-analysis-g6-g9", "$ 60.00 USD",
         1, "2021-09-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Pride and Prejudice and Jane Eyre."),
        (57, "LA409 - Gone With the Wind & Little Women (G6-G9)", "la409-literary-analysis-g6",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd47c3e586a8a8fd4ff58b_LA409%20%E9%A3%98-%E5%B0%8F%E5%A6%87%E4%BA%BA%20no%20tuition.png", "G6-G9", "/product/la409-literary-analysis-g6", "$ 75.00 USD",
         1, "2021-06-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Gone With the Wind and Little Women."),
        (58, "LA409 - Gone with the Wind & Little Women (G6-G9)", "la409-gone-with-the-wind-little-women-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e13ce83d372488442f0938_LA409%20%E9%A3%98-%E5%B0%8F%E5%A6%87%E4%BA%BA.png", "G6-G9", "/product/la409-gone-with-the-wind-little-women-g6-g9", "$ 75.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Analysis of Gone with the Wind and Little Women."),
        (59, "LA410 - War and Peace (G6-G9)", "la410-war-and-peace-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd423a5c5b0778ebbd0e11_LA410%20%E6%88%98%E4%BA%89%E4%B8%8E%E5%92%8C%E5%B9%B3%20no%20tuition.png", "G6-G9", "/product/la410-war-and-peace-g6-g9", "$ 75.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of War and Peace."),
        (60, "LA416 - Harry Potter Book 3 && 4 (G3-G9)", "la416-harry-potter-book-3-4-g3-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64b93312ee991bc33570e1af_LA416.png", "G3-G9", "/product/la416-harry-potter-book-3-4-g3-g9", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis of Harry Potter books 3 and 4."),
        (61, "Literacy Analysis Little Prince and Treasure Island (G4-G6)", "2020-fall-literacy-analysis-little-prince-and-treasure-island",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752d18d1bd77e62278d0de_Reading%20Club%20A%20The%20Little%20Prince%20and%20Treasure%20Island.jpg", "G4-G6", "/product/2020-fall-literacy-analysis-little-prince-and-treasure-island", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "Literature", "Analysis of The Little Prince and Treasure Island."),
        (62, "Literary Analysis Seminar (G6-G9)", "2020-summer-literary-analysis-seminar-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155acf4a50e133b8a660105_Literary%20Analysis%20Seminar%20G6-G9.jpg", "G6-G9", "/product/2020-summer-literary-analysis-seminar-g6-g9", "$ 60.00 USD",
         1, "2020-07-01", "2026-12-31", "Language Arts", "Literature", "Literary analysis seminar."),
        (63, "MTH303(B) - Pre Algebra China Class (G4-G6)", "2021-summer-pre-algebra-china-class",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bc74cb5292c2ca28372f1_poster.png", "G4-G6", "/product/2021-summer-pre-algebra-china-class", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Math", "Math", "Pre-algebra for China class."),
        (64, "MTH404 - Introduction to Algebra II", "2021-summer-introduction-to-algebra-ii",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcf70ac007ba0fbef6444_post.png", "G6-G9", "/product/2021-summer-introduction-to-algebra-ii", "$ 0.00 USD",
         1, "2021-06-01", "2026-12-31", "Math", "Algebra", "Introduction to Algebra II."),
        (65, "Pre Algebra (G5-G10+)", "2020-summer-pre-algebra",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61547bdcef9c358eec1a15ef_2020PreAlgebra.jpg", "G5-G10+", "/product/2020-summer-pre-algebra", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Math", "Math", "Pre-algebra course."),
        (66, "Reading Club - Charlie and the Chocolate Factory & Matilda (G3-G4)", "2020-fall-reading-club-g3-g4",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a450da3fadd8cfdbd7d0_Reading%20Club%20G3%20-%20G4.jpg", "G3-G4", "/product/2020-fall-reading-club-g3-g4", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "Reading", "Reading club for younger students."),
        (67, "Reading Club - Christmas Carol & Twenty Thousand Leagues Under the Sea (G4-G6)", "2020-fall-reading-club-g4-g6-2",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a5b5e5fb5e0cd6831278_Reading%20Club%20G4%20-%20G6%20third.jpg", "G4-G6", "/product/2020-fall-reading-club-g4-g6-2", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "Reading", "Reading club with classic novels."),
        (68, "Reading Club - Julius Caesar & The Last of Mohicans (G6-G9)", "2020-fall-reading-club-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a62f3e69985861abe7d2_Reading%20Club%20G6%20-%20G9.jpg", "G6-G9", "/product/2020-fall-reading-club-g6-g9", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "Reading", "Reading club for advanced students."),
        (69, "Reading Club - The Call of the Wild & Oliver Twist (G4-G6)", "2020-fall-reading-club-g4-g6-1",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a548e5fb5e93238311a9_Reading%20Club%20G4%20-%20G6%20Another.jpg", "G4-G6", "/product/2020-fall-reading-club-g4-g6-1", "$ 60.00 USD",
         1, "2020-09-01", "2026-12-31", "Language Arts", "Reading", "Reading club with adventure novels."),
        (70, "Reading Club - The Little Prince & Treasure Island (G4-G5)", "2020-summer-reading-club-g4-g5",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ad52f4812ff5c914d65c_Reading%20Club%20G4-G5.jpg", "G4-G5", "/product/2020-summer-reading-club-g4-g5", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "Language Arts", "Reading", "Summer reading club."),
        (71, "Reading Club - The Swiss Family Robinson & The Old Man and the Sea (G4-G6)", "2020-summer-reading-club-g4-g6",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ada59e31be960575bc30_Reading%20Club%20G4-G6.jpg", "G4-G6", "/product/2020-summer-reading-club-g4-g6", "$ 45.00 USD",
         1, "2020-07-01", "2026-12-31", "Language Arts", "Reading", "Summer reading club with classic novels."),
        (72, "SCI403 - Introduction to Fundamentalsin Science", "sci403-introduction-to-fundamentalsin-science",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb938fbdc6d35c9c2515cb_sci-403.png", "G6-G10", "/product/sci403-introduction-to-fundamentalsin-science", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "Science", "Science", "Introduction to fundamental science concepts."),
        (73, "SPN102- Spanish Class for Beginners II (G4-G9)", "spn102-spanish-class-for-beginners-g4-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/628efea46736c77670042f1b_SPN102.jpg", "G4-G9", "/product/spn102-spanish-class-for-beginners-g4-g9", "$ 180.00 USD",
         1, "2022-01-01", "2026-12-31", "Language", "Spanish", "Spanish for beginners level II."),
        (74, "SPN103 - Spanish class for beginners III (G4-G9)", "spn103-spanish-class-for-beginners-iii-g4-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290f82c9a6b934a26247b7d_SPN103.png", "G4-G9", "/product/spn103-spanish-class-for-beginners-iii-g4-g9", "$ 270.00 USD",
         1, "2022-01-01", "2026-12-31", "Language", "Spanish", "Spanish for beginners level III."),
        (75, "US History", "2020-summer-us-history",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a8d78a70300ad0c66da2_ExploreHistory%20-%20US%20History.jpg", "G6-G12", "/product/2020-summer-us-history", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "History", "US History", "US History survey course."),
        (76, "WRT403 - Creative Writing ( G6-G9 )", "2021-fall-creative-writing-wrt403",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618d22d91c6a81d1bf0ef93c_WRT403.png", "G6-G9", "/product/2021-fall-creative-writing-wrt403", "$ 270.00 USD",
         1, "2021-09-01", "2026-12-31", "Language Arts", "Writing", "Creative writing workshop."),
        (77, "WRT404 - Creative Writing II (G6-G9)", "wrt404-creative-writing-ii-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd49b57a651929a2f9ac62_WRT404%20%20no%20tuition.png", "G6-G9", "/product/wrt404-creative-writing-ii-g6-g9", "$ 180.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Writing", "Creative writing level II."),
        (78, "WRT404 - Creative Writing II (G6-G9)", "wrt404-creative-writing-ii-g6-g9-10",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd49b57a651929a2f9ac62_WRT404%20%20no%20tuition.png", "G6-G9", "/product/wrt404-creative-writing-ii-g6-g9-10", "$ 180.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Writing", "Creative writing level II - session 2."),
        (79, "WRT405 - Writing Workshop China Class (G6-G9)", "wrt405-writing-workshop-china-class-g6-g9",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd3c5304199df79620dd90_WRT405-China%20-%20no%20tuition.png", "G6-G9", "/product/wrt405-writing-workshop-china-class-g6-g9", "$ 225.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Writing", "Writing workshop for China class."),
        (80, "WRT408 - Poem Writing", "wrt408-poem-writing",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb85896b4ad5fcc2e6bfb1_WRT408%20-%202023%20Summer.png", "G6-G9", "/product/wrt408-poem-writing", "$ 0.00 USD",
         1, "2022-01-01", "2026-12-31", "Language Arts", "Writing", "Learn the art of poem writing."),
        (81, "World History", "2020-summer-world-history",
         "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a8236fae1bdc8839f09f_Explore%20History%20-%20World%20History.jpg", "G6-G12", "/product/2020-summer-world-history", "$ 0.00 USD",
         1, "2020-07-01", "2026-12-31", "History", "World History", "World History survey course."),
    ]
    c.executemany("""
        INSERT OR IGNORE INTO events (id, name, slug, img, grade, link, price, status, start_date, end_date, category, subject, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, events)

    # Seed events_instructor relationships (all linked to instructor 1 for simplicity)
    event_instructors = [(i, i, 1) for i in range(1, len(events) + 1)]
    c.executemany("INSERT OR IGNORE INTO events_instructor (id, event_id, instructor_id) VALUES (?, ?, ?)", event_instructors)

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")
    print(f"  - {len(instructors)} instructors")
    print(f"  - {len(events)} courses")

if __name__ == "__main__":
    setup()
