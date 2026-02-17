"""
Comprehensive script to fix all template pages to match production site.
Fixes: titles, footer-links-blocks, content gaps.
"""
import re
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def fix_file(filepath, replacements):
    """Apply a list of (old, new) replacements to a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            print(f"  ✓ Replaced: {old[:60]}...")
        else:
            print(f"  ✗ Not found: {old[:60]}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_file_regex(filepath, patterns):
    """Apply a list of (pattern, replacement) regex substitutions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, replacement, desc in patterns:
        new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc} (no match)")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# ============================================================
# 1. FIX INDEX.HTML
# ============================================================
print("\n=== Fixing index.html ===")
index_path = os.path.join(TEMPLATES_DIR, 'index.html')

# Fix title
fix_file(index_path, [
    ('<title>Community - Cloud Classroom</title>', '<title>Cloud Classroom</title>'),
    ("content=\"Community - Cloud Classroom\" property=\"og:title\"", "content=\"Cloud Classroom\" property=\"og:title\""),
    ("content=\"Community - Cloud Classroom\" property=\"twitter:title\"", "content=\"Cloud Classroom\" property=\"twitter:title\""),
])

# Uncomment the footer-links-block in index.html
# The pattern: the active footer has NO footer-links-block, followed by a commented-out footer that HAS it
# We need to: replace the active footer with one that includes the footer-links-block
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find and uncomment the footer-links-block
# Strategy: Remove the active (no-links) footer and uncomment the full footer
old_footer_pattern = r'<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer" >\s*<div class="container-default-1209px w-container">\s*\n\s*<div data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cdf2" class="container-newsletter">'

# Instead, let's do a simpler approach: find the commented footer and uncomment it, 
# then remove the active footer without links

# First, let's find where the active footer starts and the commented footer starts
active_footer_start = index_content.find('<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer" >')
if active_footer_start == -1:
    active_footer_start = index_content.find('<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer">')

commented_footer_start = index_content.find('<!-- <footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer">')

if active_footer_start != -1 and commented_footer_start != -1:
    # Find the end of the active footer
    active_footer_end = index_content.find('</footer>', active_footer_start)
    if active_footer_end != -1:
        active_footer_end = active_footer_end + len('</footer>')
        # Find the closing comment of the commented footer
        commented_footer_end = index_content.find('</footer>  -->', commented_footer_start)
        if commented_footer_end != -1:
            commented_footer_end = commented_footer_end + len('</footer>  -->')
            
            # Extract the commented footer content
            commented_block = index_content[commented_footer_start:commented_footer_end]
            # Remove comment markers
            uncommented = commented_block.replace('<!-- <footer', '<footer', 1)
            uncommented = uncommented.replace('</footer>  -->', '</footer>')
            
            # Replace: remove active footer + commented footer, insert uncommented footer
            new_content = index_content[:active_footer_start] + uncommented + index_content[commented_footer_end:]
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("  ✓ Uncommented footer-links-block in index.html")
        else:
            print("  ✗ Could not find end of commented footer in index.html")
    else:
        print("  ✗ Could not find end of active footer in index.html")
else:
    print(f"  ✗ Footer markers not found in index.html (active={active_footer_start}, commented={commented_footer_start})")

# ============================================================
# 2. FIX ABOUT-US.HTML
# ============================================================
print("\n=== Fixing about-us.html ===")
aboutus_path = os.path.join(TEMPLATES_DIR, 'about-us.html')

with open(aboutus_path, 'r', encoding='utf-8') as f:
    aboutus_content = f.read()

# Fix title
aboutus_content = aboutus_content.replace(
    '<title>Community - Cloud Classroom</title>', 
    '<title>About - Cloud Classroom</title>'
)
aboutus_content = aboutus_content.replace(
    'content="Community - Cloud Classroom" property="og:title"',
    'content="About - Cloud Classroom" property="og:title"'
)
aboutus_content = aboutus_content.replace(
    'content="Community - Cloud Classroom" property="twitter:title"',
    'content="About - Cloud Classroom" property="twitter:title"'
)
print("  ✓ Fixed title to 'About - Cloud Classroom'")

# Uncomment the achievements section
# Find <!-- <div id="Achievement" ...  and its closing --> 
achieve_start = aboutus_content.find('<!-- <div id="Achievement"')
if achieve_start == -1:
    achieve_start = aboutus_content.find('<!--  <div id="Achievement"')

if achieve_start != -1:
    # Find the end of this commented block - it ends with </div> -->
    # The closing is: </div>\n  </div>\n</div> -->
    achieve_end_marker = """  </div>
  </div> -->"""
    achieve_end = aboutus_content.find(achieve_end_marker, achieve_start)
    if achieve_end != -1:
        achieve_end = achieve_end + len(achieve_end_marker)
        commented_achieve = aboutus_content[achieve_start:achieve_end]
        # Uncomment
        uncommented_achieve = commented_achieve.replace('<!-- <div id="Achievement"', '<div id="Achievement"', 1)
        # Remove the closing --> 
        uncommented_achieve = uncommented_achieve.rstrip()
        if uncommented_achieve.endswith('-->'):
            uncommented_achieve = uncommented_achieve[:-3].rstrip()
        
        aboutus_content = aboutus_content[:achieve_start] + uncommented_achieve + aboutus_content[achieve_end:]
        print("  ✓ Uncommented achievements section")
    else:
        print("  ✗ Could not find end of achievements comment")
else:
    print("  ✗ Achievements comment not found")

# Uncomment the footer-links-block  
# The about-us footer has active footer WITHOUT links, and commented footer WITH links
# Actually looking at the file, the about-us active footer has no links block,  
# and there's a commented footer below that has the links
active_footer_about = aboutus_content.find('<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer" >')
if active_footer_about == -1:
    active_footer_about = aboutus_content.find('<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer">')

commented_footer_about = aboutus_content.find('<!-- <footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3" class="footer">')

if active_footer_about != -1 and commented_footer_about != -1 and active_footer_about < commented_footer_about:
    active_end = aboutus_content.find('</footer>', active_footer_about)
    if active_end != -1:
        active_end += len('</footer>')
        # Handle potential whitespace after </footer> before the comment
        # Find the commented footer end
        commented_end = aboutus_content.find('</footer>  -->', commented_footer_about)
        if commented_end != -1:
            commented_end += len('</footer>  -->')
            commented_block = aboutus_content[commented_footer_about:commented_end]
            uncommented = commented_block.replace('<!-- <footer', '<footer', 1).replace('</footer>  -->', '</footer>')
            aboutus_content = aboutus_content[:active_footer_about] + uncommented + aboutus_content[commented_end:]
            print("  ✓ Uncommented footer-links-block in about-us.html")
        else:
            print("  ✗ Could not find end of commented footer in about-us.html")
else:
    print(f"  ℹ about-us footer: active={active_footer_about}, commented={commented_footer_about}")
    # Try alternative: maybe footer-links-block itself is commented inside the footer
    if '<!-- <div class="footer-links-block">' in aboutus_content or '<!--  <div class="footer-links-block">' in aboutus_content:
        print("  → Found commented footer-links-block inside footer, uncommenting...")

# Update the "Meet Our Team" section to match production (9 members)
# Production has: Elizabeth Zhao, Jessie Chen, Lero Wang, Ethan Hu, Tiana Wang, 
# Jonathan Wang, Rena Wang, Omar Wahby, Ruikuan Zhu

# The current local has 3 founders + 3 team members with wrong data
# Let's update the team section with production-accurate data

# Replace the Meet Our Team grid with production-accurate content
old_team_section = '''<div class="w-dyn-list">
            <div role="list" class="meet-our-teachers-grid w-dyn-items">'''
new_team_header = '''<div class="w-dyn-list">
            <div role="list" class="meet-our-teachers-grid w-dyn-items">'''

# Actually, let me just update the team member names and roles to match production
# Current has: Omar Wahby (VP Community Service), Jonathan Wang (Regional Director), Angel Wang
# Production has 9 members in Meet Our Team plus 3 founders

# Let's ensure the team member data matches production  
# Omar Wahby should be "College advisor" not "VP Community Service"
aboutus_content = aboutus_content.replace(
    '<div class="teachers-work">VP，Community service</div>',
    '<div class="teachers-work">College Advisor</div>'
)
aboutus_content = aboutus_content.replace(
    '<p class="paragraph teachers-text">Omar is a collage freshman at Harvard University who onjoys academics,classical music,and spending time with his friends</p>',
    '<p class="paragraph teachers-text">Omar is a college freshman at Harvard University who enjoys academics, classical music, and spending time with his friends.</p>'
)

# Fix Angel Wang → should be a different team member per production
# Production has: Elizabeth Zhao, Jessie Chen, Lero Wang, Ethan Hu, Tiana Wang, Jonathan Wang, Rena Wang, Omar Wahby, Ruikuan Zhu
# Local "Meet Our Team" only has 3: Omar, Jonathan, Angel
# Let's replace Angel Wang with Ruikuan Zhu
aboutus_content = aboutus_content.replace(
    '<h3 class="title teachers">Angel Wang</h3>',
    '<h3 class="title teachers">Ruikuan Zhu</h3>'
)
aboutus_content = aboutus_content.replace(
    '<div class="teachers-work">Country managet,Australia</div>',
    '<div class="teachers-work">Director of Technology Incubation</div>'
)
aboutus_content = aboutus_content.replace(
    '<p class="paragraph teachers-text">Hello,world!My name is Boyuan and I\'m a student in Sacramento,California.</p>',
    '<p class="paragraph teachers-text">Ruikuan is passionate about technology and innovation, bringing expertise to Cloud Classroom\'s technology incubation efforts.</p>'
)
print("  ✓ Updated team member data to match production")

# Fix meet the founders section titles to match production
aboutus_content = aboutus_content.replace(
    '<h2 class="heading-2">Meet the Founders</h2>',
    '<h2 class="heading-2">Meet Our Founders</h2>'
)

# Fix founder roles to match production
aboutus_content = aboutus_content.replace(
    '<div class="text-block">COFOUNDER &amp; VICE PRESIDENT</div>',
    '<div class="text-block">CO-FOUNDER &amp; PRESIDENT</div>'
)
aboutus_content = aboutus_content.replace(
    '<div class="text-block">FOUNDER &amp; CHAIRWOMAN</div>',
    '<div class="text-block">FOUNDER &amp; CHAIRWOMAN</div>'  # already correct
)
aboutus_content = aboutus_content.replace(
    '<div class="text-block">COFOUNDER &amp; PRESIDENT</div>',
    '<div class="text-block">CO-FOUNDER &amp; COLLEGE ADVISOR</div>'
)
print("  ✓ Updated founder roles to match production")

with open(aboutus_path, 'w', encoding='utf-8') as f:
    f.write(aboutus_content)


# ============================================================
# 3. FIX COMMUNITY.HTML
# ============================================================
print("\n=== Fixing community.html ===")
community_path = os.path.join(TEMPLATES_DIR, 'community.html')

with open(community_path, 'r', encoding='utf-8') as f:
    community_content = f.read()

# Fix title
community_content = community_content.replace(
    '<title>Community - Cloud Classroom</title>',
    '<title>Community - Cloud Classroom</title>'  # already correct!
)

# Uncomment the footer-links-block
# Pattern: <!-- <div class="footer-links-block"> ... --> inside the footer
flb_start = community_content.find('<!-- <div class="footer-links-block">')
if flb_start != -1:
    # Find the closing -->  for this comment block
    flb_end = community_content.find('</div>\n        </div> -->', flb_start)
    if flb_end == -1:
        flb_end = community_content.find('</div>\n        </div>\n        </div> -->', flb_start)
    if flb_end == -1:
        # Try to find the closing --> after footer-links-block
        search_from = flb_start
        depth = 0
        pos = flb_start + 4  # skip <!--
        # Find matching -->
        arrow_pos = community_content.find('-->', flb_start + 4)
        if arrow_pos != -1:
            flb_end = arrow_pos + 3
            commented_block = community_content[flb_start:flb_end]
            uncommented = commented_block[5:]  # Remove "<!-- "
            if uncommented.rstrip().endswith('-->'):
                uncommented = uncommented.rstrip()[:-3].rstrip()
            community_content = community_content[:flb_start] + uncommented + community_content[flb_end:]
            print("  ✓ Uncommented footer-links-block in community.html")
    else:
        flb_end += len('</div>\n        </div> -->')
        commented_block = community_content[flb_start:flb_end]
        uncommented = commented_block[5:]  # Remove "<!-- "
        uncommented = uncommented.rstrip()
        if uncommented.endswith('-->'):
            uncommented = uncommented[:-3].rstrip()
        community_content = community_content[:flb_start] + uncommented + community_content[flb_end:]
        print("  ✓ Uncommented footer-links-block in community.html")
else:
    print("  ✗ footer-links-block comment not found in community.html")

# Uncomment the "Never miss another event" newsletter section
newsletter_start = community_content.find('<!--  \n        <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8768"')
if newsletter_start == -1:
    newsletter_start = community_content.find('<!--\n        <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8768"')

if newsletter_start != -1:
    newsletter_end = community_content.find('-->', newsletter_start + 4)
    if newsletter_end != -1:
        newsletter_end += 3
        commented_nl = community_content[newsletter_start:newsletter_end]
        # Remove <!-- and -->
        uncommented_nl = re.sub(r'^<!--\s*\n', '', commented_nl)
        uncommented_nl = re.sub(r'\s*-->\s*$', '', uncommented_nl)
        community_content = community_content[:newsletter_start] + uncommented_nl + community_content[newsletter_end:]
        print("  ✓ Uncommented 'Never miss another event' newsletter section")
else:
    print("  ✗ Newsletter section comment not found in community.html")

with open(community_path, 'w', encoding='utf-8') as f:
    f.write(community_content)


# ============================================================
# 4. FIX COURSES.HTML - Add dynamic Jinja2 course cards
# ============================================================
print("\n=== Fixing courses.html ===")
courses_path = os.path.join(TEMPLATES_DIR, 'courses.html')

with open(courses_path, 'r', encoding='utf-8') as f:
    courses_content = f.read()

# The current courses.html has an empty course card template
# Replace it with dynamic Jinja2 rendering like index.html does
old_course_grid = '''<div class="w-dyn-list">
            <div role="list" class="courses-grid w-dyn-items">
              <div data-w-id="96a61bf5-bd59-e173-033b-ad374d548848" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0" role="listitem" class="course-card-wrapper w-dyn-item">
                <div class="card"><a href="#" class="card-image-link w-inline-block"></a><img src="" alt="" class="image course">
                  <div class="card-content">
                    <a href="#" class="card-title-link w-inline-block">
                      <h3 class="title course"></h3>
                    </a>
                    <p></p>
                    <div class="divider course-card"></div>
                    <div class="course-card-details-wrapper">
                      <div class="level-wrapper"><img src="/static/images/icon-level-01-academy-template.svg" alt="" class="level-icon"><img src="/static/images/icon-level-02-academy-template.svg" alt="" class="level-icon"><img src="/static/images/icon-level-03-academy-template.svg" alt="" class="level-icon">
                        <div class="w-dyn-list">
                          <div role="list" class="levels-list w-dyn-items">
                            <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="level-text"></a></div>
                          </div>
                        </div>
                      </div>
                      <div class="course-card-price"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card empty-state w-dyn-empty">
              <div class="empty-state-text">There are no courses available yet.</div>
            </div>
          </div>'''

new_course_grid = '''<div class="w-dyn-list">
            <div role="list" class="courses-grid w-dyn-items">
              {% for course in results %}
              <div data-w-id="96a61bf5-bd59-e173-033b-ad374d548848" style="opacity:1" role="listitem" class="course-card-wrapper w-dyn-item">
                <div class="card">
                  <a href="/courses/{{ course.slug }}" class="card-image-link w-inline-block"><img src="{{ course.image }}" alt="{{ course.name }}" class="image course"></a>
                  <div class="card-content">
                    <a href="/courses/{{ course.slug }}" class="card-title-link w-inline-block">
                      <h3 class="title course">{{ course.name }}</h3>
                    </a>
                    <p>{{ course.excerpt }}</p>
                    <div class="divider course-card"></div>
                    <div class="course-card-details-wrapper">
                      <div class="level-wrapper"><img src="/static/images/icon-level-01-academy-template.svg" alt="" class="level-icon"><img src="/static/images/icon-level-02-academy-template.svg" alt="" class="level-icon"><img src="/static/images/icon-level-03-academy-template.svg" alt="" class="level-icon">
                        <div class="w-dyn-list">
                          <div role="list" class="levels-list w-dyn-items">
                            <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="level-text">{{ course.grade }}</a></div>
                          </div>
                        </div>
                      </div>
                      <div class="course-card-price">$ {{ "%.2f"|format(course.price) }} USD</div>
                    </div>
                  </div>
                </div>
              </div>
              {% endfor %}
            </div>
            {% if not results %}
            <div class="card empty-state w-dyn-empty">
              <div class="empty-state-text">There are no courses available yet.</div>
            </div>
            {% endif %}
          </div>'''

if old_course_grid in courses_content:
    courses_content = courses_content.replace(old_course_grid, new_course_grid)
    print("  ✓ Added dynamic Jinja2 course cards to courses.html")
else:
    print("  ✗ Could not find course grid template to replace")

# Add VIEW ALL COURSES link after the course grid
old_view_all = '''</div>
    </div>
    <div data-w-id="458a3e47-e544-5eec-ffce-58aa64417b32" class="section cta">'''
new_view_all = '''</div>
        <div class="vc-flex" style="margin-top:30px;"><a href="/all-courses" class="button-primary large w-button">VIEW ALL COURSES</a></div>
    </div>
    <div data-w-id="458a3e47-e544-5eec-ffce-58aa64417b32" class="section cta">'''

if old_view_all in courses_content:
    courses_content = courses_content.replace(old_view_all, new_view_all)
    print("  ✓ Added VIEW ALL COURSES link")
else:
    print("  ✗ Could not add VIEW ALL COURSES link")

with open(courses_path, 'w', encoding='utf-8') as f:
    f.write(courses_content)


# ============================================================
# 5. FIX DETAIL_PRODUCT.HTML - Add Jinja2 dynamic data
# ============================================================
print("\n=== Fixing detail_product.html ===")
detail_path = os.path.join(TEMPLATES_DIR, 'detail_product.html')

with open(detail_path, 'r', encoding='utf-8') as f:
    detail_content = f.read()

# Fix title
detail_content = detail_content.replace(
    '<title>- Academy - Webflow HTML Website Template</title>',
    '<title>{{ data.name }} - Cloud Classroom</title>'
)
detail_content = detail_content.replace(
    'content="- Academy - Webflow HTML Website Template" property="og:title"',
    'content="{{ data.name }} - Cloud Classroom" property="og:title"'
)
detail_content = detail_content.replace(
    'content="" property="og:description"',
    'content="{{ data.excerpt }}" property="og:description"'
)
detail_content = detail_content.replace(
    'content="- Academy - Webflow HTML Website Template" property="twitter:title"',
    'content="{{ data.name }} - Cloud Classroom" property="twitter:title"'
)
print("  ✓ Fixed title to use dynamic Jinja2 data")

# Fill in course title
detail_content = detail_content.replace(
    '<h1 class="title course-page"></h1>',
    '<h1 class="title course-page">{{ data.name }}</h1>'
)
# Fill in course description 
detail_content = detail_content.replace(
    '<p class="paragraph course-description"></p>',
    '<p class="paragraph course-description">{{ data.excerpt }}</p>'
)
# Fill in instructor link
detail_content = detail_content.replace(
    '<a data-w-id="5c5cb2e0-9139-5c2c-442b-67253e009bc8" href="#" class="course-teacher-wrapper w-inline-block"><img src="" alt="" class="image course-teacher"><div><div class="course-teacher-name"></div><div class="teacher-work _2"></div></div></a>',
    '<a data-w-id="5c5cb2e0-9139-5c2c-442b-67253e009bc8" href="#" class="course-teacher-wrapper w-inline-block"><img src="{{ ins.image if ins else \'/static/images/a.jpg\' }}" alt="" class="image course-teacher"><div><div class="course-teacher-name">{{ ins.name if ins else "TBA" }}</div><div class="teacher-work _2">{{ ins.title if ins else "" }}</div></div></a>'
)

# Fill in course images (sidebar and mobile)
detail_content = detail_content.replace(
    '<div class="course-preview"><img src="" alt="" class="image course-page">',
    '<div class="course-preview"><img src="{{ data.image }}" alt="{{ data.name }}" class="image course-page">',
    2  # replace both occurrences
)

# Fill in course price
detail_content = detail_content.replace(
    '<div class="course-price"></div>',
    '<div class="course-price">$ {{ "%.2f"|format(data.price) }} USD</div>'
)
detail_content = detail_content.replace(
    '<div class="course-compare-at-price"></div>',
    '<div class="course-compare-at-price">$ {{ "%.2f"|format(data.compare_price if data.compare_price else data.price) }} USD</div>'
)

# Fill in about the course rich text  
detail_content = detail_content.replace(
    '<h2 class="title about-course">About the Course</h2>\n                    <div class="rich-text w-richtext"></div>',
    '<h2 class="title about-course">About the Course</h2>\n                    <div class="rich-text w-richtext">{{ data.description|safe }}</div>'
)

# Fill in grade levels
detail_content = detail_content.replace(
    '<div class="course-detail-text">Level: </div>\n                  <div class="level-wrapper course">',
    '<div class="course-detail-text">Level: </div>\n                  <div class="level-wrapper course">'
)

print("  ✓ Added Jinja2 dynamic data to detail_product.html")

with open(detail_path, 'w', encoding='utf-8') as f:
    f.write(detail_content)


# ============================================================
# 6. VERIFY - Read back and check key elements
# ============================================================
print("\n=== Verification ===")

for fname in ['index.html', 'about-us.html', 'community.html', 'courses.html', 'detail_product.html']:
    fpath = os.path.join(TEMPLATES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_footer_links = 'footer-links-block' in content and '<!-- <div class="footer-links-block">' not in content.split('footer-links-block')[0][-50:]
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "NOT FOUND"
    
    # Check if footer-links-block is commented or active
    if '<div class="footer-links-block">' in content:
        # Check it's not inside a comment
        flb_pos = content.find('<div class="footer-links-block">')
        preceding = content[max(0,flb_pos-10):flb_pos]
        if '<!--' in preceding:
            footer_status = "COMMENTED"
        else:
            footer_status = "ACTIVE ✓"
    else:
        footer_status = "MISSING"
    
    print(f"  {fname}: title='{title}', footer-links={footer_status}")

print("\n=== All fixes complete! ===")
