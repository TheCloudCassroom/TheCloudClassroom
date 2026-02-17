"""
Crawl all individual course pages from production (thecloudclassroom.org)
and update the local SQLite database with the content.
"""

import sqlite3
import requests
import time
import json
import re
from bs4 import BeautifulSoup

PROD_BASE = "https://www.thecloudclassroom.org"
DB_PATH = "local.db"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_local_courses():
    """Get all course slugs from local DB."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, name, slug FROM events ORDER BY id")
    courses = [dict(r) for r in cur.fetchall()]
    conn.close()
    return courses


def fetch_course_page(slug):
    """Fetch a single course page from production."""
    url = f"{PROD_BASE}/product/{slug}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"  HTTP {resp.status_code} for {url}")
            return None
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def parse_course_page(html):
    """Parse a production course page and extract all relevant data."""
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Course name
    title_el = soup.select_one("h1.title.course-page")
    data["name"] = title_el.get_text(strip=True) if title_el else ""

    # Course image
    img_el = soup.select_one("img.image.course-page")
    if img_el:
        src = img_el.get("src", "")
        if src.startswith("//"):
            src = "https:" + src
        data["img"] = src
    else:
        data["img"] = ""

    # Price
    price_el = soup.select_one(".course-price")
    data["price"] = price_el.get_text(strip=True) if price_el else ""

    # Description - "About the Course" tab content (rich HTML)
    about_tab = soup.select_one('[data-w-tab="Tab 1"] .rich-text.w-richtext')
    if about_tab:
        # Get the inner HTML
        data["description"] = str(about_tab.decode_contents()).strip()
    else:
        data["description"] = ""

    # Course Content tab (rich HTML)
    content_tab = soup.select_one('[data-w-tab="Tab 2"]')
    if content_tab:
        rich_texts = content_tab.select(".rich-text-bullets.w-richtext")
        content_parts = []
        for rt in rich_texts:
            inner = str(rt.decode_contents()).strip()
            if inner:
                content_parts.append(inner)
        data["course_content"] = "\n".join(content_parts)
    else:
        data["course_content"] = ""

    # Grade levels
    level_links = soup.select(".course-detail-text.level")
    grades = []
    for link in level_links:
        txt = link.get_text(strip=True)
        if txt:
            grades.append(txt)
    data["grade"] = ", ".join(grades) if grades else ""

    # Duration
    duration_wrappers = soup.select(".course-detail-wrapper")
    data["duration"] = ""
    for wrapper in duration_wrappers:
        text_divs = wrapper.select(".course-detail-text")
        for td in text_divs:
            if "Duration:" in td.get_text():
                strong = wrapper.select_one(".course-detail-text.strong")
                if strong:
                    data["duration"] = strong.get_text(strip=True)
                break

    # Videos count
    data["videos"] = ""
    for wrapper in duration_wrappers:
        text_divs = wrapper.select(".course-detail-text")
        for td in text_divs:
            if "Videos:" in td.get_text():
                strong = wrapper.select_one(".course-detail-text.strong")
                if strong:
                    data["videos"] = strong.get_text(strip=True)
                break

    # Instructor name and image
    teacher_link = soup.select_one("a.course-teacher-wrapper")
    if teacher_link:
        name_el = teacher_link.select_one(".course-teacher-name")
        data["instructor_name"] = name_el.get_text(strip=True) if name_el else ""
        teacher_img = teacher_link.select_one("img.image.course-teacher")
        if teacher_img:
            src = teacher_img.get("src", "")
            if src.startswith("//"):
                src = "https:" + src
            data["instructor_img"] = src
        else:
            data["instructor_img"] = ""
        # instructor slug from href
        href = teacher_link.get("href", "")
        data["instructor_slug"] = href.split("/")[-1] if "/instructor/" in href else ""
        # teacher bio/work
        work_el = teacher_link.select_one(".teacher-work")
        data["instructor_bio"] = work_el.get_text(strip=True) if work_el else ""
    else:
        data["instructor_name"] = ""
        data["instructor_img"] = ""
        data["instructor_slug"] = ""
        data["instructor_bio"] = ""

    # Categories/subjects from level links
    category_links = soup.select(".level-wrapper .levels-list a.course-detail-text.level")
    categories = []
    for cl in category_links:
        href = cl.get("href", "")
        txt = cl.get_text(strip=True)
        if txt and "Grade" not in txt:
            categories.append(txt)
    data["category"] = ", ".join(categories) if categories else ""

    return data


def update_database(courses_data):
    """Update the local database with crawled data."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Add columns if they don't exist
    try:
        cur.execute("ALTER TABLE events ADD COLUMN course_content TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass  # column already exists
    try:
        cur.execute("ALTER TABLE events ADD COLUMN duration TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE events ADD COLUMN videos TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # Build instructor lookup - collect unique instructors
    instructors = {}  # name -> {img, bio, slug}
    for slug, data in courses_data.items():
        iname = data.get("instructor_name", "").strip()
        if iname:
            instructors[iname] = {
                "img": data.get("instructor_img", ""),
                "bio": data.get("instructor_bio", ""),
                "slug": data.get("instructor_slug", ""),
            }

    # Insert instructors and get their IDs
    instructor_ids = {}
    for name, info in instructors.items():
        # Check if instructor exists
        cur.execute("SELECT id FROM instructors WHERE name=?", (name,))
        row = cur.fetchone()
        if row:
            iid = row[0]
            cur.execute(
                "UPDATE instructors SET img=?, bio=? WHERE id=?",
                (info["img"], info["bio"], iid)
            )
        else:
            cur.execute(
                "INSERT INTO instructors (name, bio, img) VALUES (?, ?, ?)",
                (name, info["bio"], info["img"])
            )
            iid = cur.lastrowid
        instructor_ids[name] = iid

    # Update each course
    updated = 0
    for slug, data in courses_data.items():
        desc = data.get("description", "")
        img = data.get("img", "")
        price = data.get("price", "")
        grade = data.get("grade", "")
        duration = data.get("duration", "")
        videos = data.get("videos", "")
        course_content = data.get("course_content", "")

        # Update the event
        updates = []
        params = []
        if desc:
            updates.append("description=?")
            params.append(desc)
        if img:
            updates.append("img=?")
            params.append(img)
        if price:
            updates.append("price=?")
            params.append(price)
        if grade:
            updates.append("grade=?")
            params.append(grade)
        if duration:
            updates.append("duration=?")
            params.append(duration)
        if videos:
            updates.append("videos=?")
            params.append(videos)
        if course_content:
            updates.append("course_content=?")
            params.append(course_content)

        if updates:
            params.append(slug)
            sql = f"UPDATE events SET {', '.join(updates)} WHERE slug=?"
            cur.execute(sql, params)
            if cur.rowcount > 0:
                updated += 1

        # Update instructor linkage
        iname = data.get("instructor_name", "").strip()
        if iname and iname in instructor_ids:
            # Get event id
            cur.execute("SELECT id FROM events WHERE slug=?", (slug,))
            event_row = cur.fetchone()
            if event_row:
                eid = event_row[0]
                iid = instructor_ids[iname]
                # Remove old linkage
                cur.execute("DELETE FROM events_instructor WHERE event_id=?", (eid,))
                # Insert new linkage
                cur.execute(
                    "INSERT INTO events_instructor (event_id, instructor_id) VALUES (?, ?)",
                    (eid, iid)
                )

    conn.commit()
    conn.close()
    return updated


def main():
    courses = get_local_courses()
    print(f"Found {len(courses)} courses in local DB")

    courses_data = {}
    success = 0
    fail = 0

    for i, course in enumerate(courses):
        slug = course["slug"]
        print(f"[{i+1}/{len(courses)}] Crawling: {course['name']} ({slug})")

        html = fetch_course_page(slug)
        if html:
            data = parse_course_page(html)
            if data.get("name") or data.get("description"):
                courses_data[slug] = data
                success += 1
                desc_preview = data.get("description", "")[:80]
                instructor = data.get("instructor_name", "N/A")
                print(f"  OK - Instructor: {instructor}, Desc: {desc_preview}...")
            else:
                print(f"  WARN - Page loaded but no course data found")
                fail += 1
        else:
            fail += 1

        # Be respectful - small delay between requests
        time.sleep(0.5)

    print(f"\nCrawl complete: {success} succeeded, {fail} failed")

    if courses_data:
        print(f"\nUpdating database with {len(courses_data)} courses...")
        updated = update_database(courses_data)
        print(f"Updated {updated} course records in database")

    # Save raw data as JSON backup
    with open("crawled_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses_data, f, indent=2, ensure_ascii=False)
    print(f"Saved crawled data to crawled_courses.json")


if __name__ == "__main__":
    main()
