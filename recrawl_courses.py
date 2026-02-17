"""
Re-crawl all course pages from production with corrected selectors.
Fixes:
  1. Description: extract from .paragraph.course-description (the actual text paragraph)
  2. Course content: extract from Tab 1 pane (the course timeline used in both tabs)
  3. Grades: extract from only the sidebar .card.course to avoid duplication
  4. Deduplicate grade entries
"""

import sqlite3
import requests
import time
import json
from bs4 import BeautifulSoup

PROD_BASE = "https://www.thecloudclassroom.org"
DB_PATH = "local.db"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_local_courses():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, name, slug FROM events ORDER BY id")
    courses = [dict(r) for r in cur.fetchall()]
    conn.close()
    return courses


def fetch_course_page(slug):
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

    # === FIX 1: Description from .paragraph.course-description ===
    desc_el = soup.select_one(".paragraph.course-description")
    if desc_el:
        # Get the inner HTML content
        data["description"] = str(desc_el.decode_contents()).strip()
    else:
        # Fallback: try to get text content from the top-content area
        top_content = soup.select_one(".top-content.course")
        if top_content:
            # Look for a paragraph or div after the title
            paras = top_content.select("p, .paragraph")
            desc_parts = []
            for p in paras:
                txt = p.get_text(strip=True)
                if txt and len(txt) > 20:  # skip short labels
                    desc_parts.append(str(p))
            data["description"] = "\n".join(desc_parts) if desc_parts else ""
        else:
            data["description"] = ""

    # === FIX 2: Course content from Tab 1 pane (course timeline) ===
    # On production, Tab 1 ("About the Course") pane contains the course timeline
    tab1_pane = soup.select_one('.w-tab-pane[data-w-tab="Tab 1"]')
    if tab1_pane:
        rt = tab1_pane.select_one(".rich-text.w-richtext")
        if rt:
            content = str(rt.decode_contents()).strip()
            # Clean up zero-width joiners and empty paragraphs
            if content and content != "<p>\u200d</p>":
                data["course_content"] = content
            else:
                data["course_content"] = ""
        else:
            data["course_content"] = ""
    else:
        data["course_content"] = ""

    # === FIX 3: Grades from sidebar card only, deduplicated ===
    sidebar_card = soup.select_one(".card.course:not(.course-mobile)")
    if not sidebar_card:
        # Fallback to first .card.course
        sidebar_card = soup.select_one(".card.course")

    if sidebar_card:
        lw = sidebar_card.select_one(".level-wrapper")
        if lw:
            links = lw.select("a")
            grades = []
            seen = set()
            for a in links:
                txt = a.get_text(strip=True)
                if txt and txt not in seen:
                    grades.append(txt)
                    seen.add(txt)
            data["grade"] = ", ".join(grades) if grades else ""
        else:
            data["grade"] = ""
    else:
        # Fallback: get from any level-wrapper but deduplicate
        all_lw = soup.select(".about-course .level-wrapper")
        if all_lw:
            lw = all_lw[0]
            links = lw.select("a")
            grades = []
            seen = set()
            for a in links:
                txt = a.get_text(strip=True)
                if txt and txt not in seen:
                    grades.append(txt)
                    seen.add(txt)
            data["grade"] = ", ".join(grades)
        else:
            data["grade"] = ""

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
        if data["duration"]:
            break  # Stop after first match (avoid duplicates from mobile+sidebar)

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
        if data["videos"]:
            break

    # Instructor
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
        href = teacher_link.get("href", "")
        data["instructor_slug"] = href.split("/")[-1] if "/instructor/" in href else ""
        work_el = teacher_link.select_one(".teacher-work")
        data["instructor_bio"] = work_el.get_text(strip=True) if work_el else ""
    else:
        data["instructor_name"] = ""
        data["instructor_img"] = ""
        data["instructor_slug"] = ""
        data["instructor_bio"] = ""

    return data


def update_database(courses_data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure columns exist
    for col in ["course_content", "duration", "videos"]:
        try:
            cur.execute(f"ALTER TABLE events ADD COLUMN {col} TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass

    # Build instructor lookup
    instructors = {}
    for slug, data in courses_data.items():
        iname = data.get("instructor_name", "").strip()
        if iname:
            instructors[iname] = {
                "img": data.get("instructor_img", ""),
                "bio": data.get("instructor_bio", ""),
            }

    # Insert/update instructors
    instructor_ids = {}
    for name, info in instructors.items():
        cur.execute("SELECT id FROM instructors WHERE name=?", (name,))
        row = cur.fetchone()
        if row:
            iid = row[0]
            cur.execute("UPDATE instructors SET img=?, bio=? WHERE id=?",
                        (info["img"], info["bio"], iid))
        else:
            cur.execute("INSERT INTO instructors (name, bio, img) VALUES (?, ?, ?)",
                        (name, info["bio"], info["img"]))
            iid = cur.lastrowid
        instructor_ids[name] = iid

    # Update each course
    updated = 0
    for slug, data in courses_data.items():
        updates = []
        params = []

        for field in ["description", "img", "price", "grade", "duration", "videos", "course_content"]:
            val = data.get(field, "")
            if val:
                updates.append(f"{field}=?")
                params.append(val)

        if updates:
            params.append(slug)
            sql = f"UPDATE events SET {', '.join(updates)} WHERE slug=?"
            cur.execute(sql, params)
            if cur.rowcount > 0:
                updated += 1

        # Update instructor linkage
        iname = data.get("instructor_name", "").strip()
        if iname and iname in instructor_ids:
            cur.execute("SELECT id FROM events WHERE slug=?", (slug,))
            event_row = cur.fetchone()
            if event_row:
                eid = event_row[0]
                iid = instructor_ids[iname]
                cur.execute("DELETE FROM events_instructor WHERE event_id=?", (eid,))
                cur.execute("INSERT INTO events_instructor (event_id, instructor_id) VALUES (?, ?)",
                            (eid, iid))

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
            courses_data[slug] = data
            success += 1

            desc_preview = data.get("description", "")[:80]
            cc_preview = data.get("course_content", "")[:60]
            grade = data.get("grade", "N/A")
            instructor = data.get("instructor_name", "N/A")
            print(f"  OK - Inst: {instructor}, Grade: {grade}")
            print(f"       Desc: {desc_preview}...")
            print(f"       Content: {cc_preview}...")
        else:
            fail += 1

        time.sleep(0.5)

    print(f"\nCrawl complete: {success} succeeded, {fail} failed")

    # Verify a sample
    sample = courses_data.get("cs308-basics-of-web-development", {})
    if sample:
        print("\n=== VERIFICATION: CS308 ===")
        print(f"Description starts with: {sample.get('description', '')[:100]}")
        print(f"Course content starts with: {sample.get('course_content', '')[:100]}")
        print(f"Grade: {sample.get('grade', '')}")

    if courses_data:
        print(f"\nUpdating database with {len(courses_data)} courses...")
        updated = update_database(courses_data)
        print(f"Updated {updated} course records in database")

    # Save backup
    with open("crawled_courses_v2.json", "w", encoding="utf-8") as f:
        json.dump(courses_data, f, indent=2, ensure_ascii=False)
    print(f"Saved crawled data to crawled_courses_v2.json")


if __name__ == "__main__":
    main()
