import os
from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)

# Use local SQLite database
# On Vercel, the filesystem is read-only except /tmp, so create DB there
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/local.db"
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.db")

# Auto-initialize DB if it doesn't exist (needed for Vercel cold starts)
if not os.path.exists(DB_PATH):
    from setup_db import setup
    setup()

engine = create_engine(f"sqlite:///{DB_PATH}")
db = scoped_session(sessionmaker(bind=engine))
s = db()

# Sentry (optional - disabled for local dev)
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration
# sentry_sdk.init(
#     dsn="https://dad50acd268449f99482f3bbf4bb96dd@o393097.ingest.sentry.io/5462790",
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )

@app.route("/")
@app.route("/index.html")
def index():
    result = s.execute(text("SELECT * FROM events WHERE status=1 LIMIT 6"))
    listT = []
    for row in result:
        row_as_dict = dict(row._mapping)
        listT.append(row_as_dict)
    return render_template("index.html", results=listT)

@app.route("/courses")
@app.route("/course.html")
def courses():
    result = s.execute(text("SELECT * FROM events"))
    listT = []
    for row in result:
        row_as_dict = dict(row._mapping)
        listT.append(row_as_dict)
    return render_template("courses.html", results=listT)


@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if query:
        result = s.execute(
            text("SELECT * FROM events WHERE name LIKE :q"),
            {"q": f"%{query}%"}
        )
    else:
        result = s.execute(text("SELECT * FROM events"))
    listT = []
    for row in result:
        row_as_dict = dict(row._mapping)
        listT.append(row_as_dict)
    return render_template("courses.html", results=listT, search_query=query)


@app.route("/product/<string:slug>")
@app.route("/courses/<string:slug>")
def course_detail(slug):
    result = s.execute(text("SELECT * FROM events WHERE slug=:s"), {"s": slug})
    course = []
    for row in result:
        row_as_dict = dict(row._mapping)
        course.append(row_as_dict)

    if len(course) == 0:
        return render_template("404.html"), 404

    course_ins = s.execute(text("SELECT * FROM events_instructor WHERE event_id=:id"), {"id": course[0]["id"]})
    ins = []
    for row in course_ins:
        row_as_dict = dict(row._mapping)
        ins.append(row_as_dict)

    instructor_info = [{}]
    if ins:
        instructor_id = ins[0]["instructor_id"]
        result = s.execute(text("SELECT * FROM instructors WHERE id=:id"), {"id": instructor_id})
        instructor_info = []
        for row in result:
            row_as_dict = dict(row._mapping)
            instructor_info.append(row_as_dict)
        if not instructor_info:
            instructor_info = [{}]

    return render_template("detail_product.html", data=course[0], ins=instructor_info[0])


@app.route("/all-courses")
@app.route("/courses-all")
def courses_all():
    result = s.execute(text("SELECT * FROM events ORDER BY name"))
    info = []
    for row in result:
        row_as_dict = dict(row._mapping)
        # Handle date strings from SQLite
        end_date = row_as_dict.get("end_date")
        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if datetime(end_date.year, end_date.month, end_date.day) > datetime(datetime.now().year, datetime.now().month, datetime.now().day):
                row_as_dict["active"] = True
            else:
                row_as_dict["active"] = False
        else:
            row_as_dict["active"] = False
        info.append(row_as_dict)
    return render_template("courses-all.html", info=info)


@app.route("/instructors")
def instructors():
    return render_template("instructors.html")


@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")


@app.route("/about-us")
def about_us():
    return render_template("about-us.html")


@app.route("/community")
def community():
    return render_template("community.html")


@app.route("/<string:html>")
def other_file(html):
    try:
        return render_template(html)
    except:
        return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)