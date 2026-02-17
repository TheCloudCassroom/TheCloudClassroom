"""
Update detail_product.html template to display crawled course data.
"""

with open("templates/detail_product.html", "r", encoding="utf-8") as f:
    content = f.read()

# === 1. Fix the mobile card section (first instance) - grade levels ===
# Find the first level-wrapper course section (lines ~117-128)
old_levels_1 = '''                    <div class="level-wrapper course">
                      <div class="w-dyn-list">
                        <div role="list" class="levels-list w-dyn-items">
                          <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="course-detail-text level"></a></div>
                        </div>
                        <div class="w-dyn-empty">
                          <div>No items found.</div>
                        </div>
                      </div>
                    </div>'''

new_levels_1 = '''                    <div class="level-wrapper course">
                      <div class="w-dyn-list">
                        <div role="list" class="levels-list w-dyn-items">
                          {% for g in data.grade.split(', ') if data.grade %}
                          <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="course-detail-text level">{{ g }}</a></div>
                          {% endfor %}
                        </div>
                      </div>
                    </div>'''

content = content.replace(old_levels_1, new_levels_1, 1)

# === 2. Fix the sidebar section (second instance) - grade levels ===
old_levels_2 = '''                  <div class="level-wrapper">
                    <div class="w-dyn-list">
                      <div role="list" class="levels-list w-dyn-items">
                        <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="course-detail-text level"></a></div>
                      </div>
                      <div class="w-dyn-empty">
                        <div>No items found.</div>
                      </div>
                    </div>
                  </div>'''

new_levels_2 = '''                  <div class="level-wrapper">
                    <div class="w-dyn-list">
                      <div role="list" class="levels-list w-dyn-items">
                        {% for g in data.grade.split(', ') if data.grade %}
                        <div role="listitem" class="level-text-wrapper w-dyn-item"><a href="#" class="course-detail-text level">{{ g }}</a></div>
                        {% endfor %}
                      </div>
                    </div>
                  </div>'''

content = content.replace(old_levels_2, new_levels_2, 1)

# === 3. Fix Duration fields (both instances) - use \xa0 ===
# Duration - replace empty strong with template var
content = content.replace(
    'Duration:\xa0</div>\n                  <div class="course-detail-text strong"></div>',
    'Duration:\xa0</div>\n                  <div class="course-detail-text strong">{{ data.duration if data.duration else \'\' }}</div>'
)
content = content.replace(
    'Duration:\xa0</div>\n                    <div class="course-detail-text strong"></div>',
    'Duration:\xa0</div>\n                    <div class="course-detail-text strong">{{ data.duration if data.duration else \'\' }}</div>'
)

# Videos - replace empty strong with template var
content = content.replace(
    'Videos:\xa0</div>\n                  <div class="course-detail-text strong"></div>',
    'Videos:\xa0</div>\n                  <div class="course-detail-text strong">{{ data.videos if data.videos else \'0\' }}</div>'
)
content = content.replace(
    'Videos:\xa0</div>\n                    <div class="course-detail-text strong"></div>',
    'Videos:\xa0</div>\n                    <div class="course-detail-text strong">{{ data.videos if data.videos else \'0\' }}</div>'
)

# Also handle "Level: " with \xa0 for the first card section
content = content.replace(
    'Level:\xa0</div>\n                    <div class="level-wrapper course">',
    'Level:\xa0</div>\n                    <div class="level-wrapper course">'
)

# === 4. Fix Course Content tab - add template variable ===
old_content_tab = '''                  <div data-w-tab="Tab 2" class="w-tab-pane">
                    <h2 class="title course-content">Course Content</h2>
                    <div class="course-content-columns">
                      <div class="course-content-column-2">
                        <div class="rich-text-bullets w-richtext">{{ data.course_content|safe if data.course_content else \'\' }}</div>
                      </div>
                    </div>
                  </div>'''

# Check if already updated (from previous multi_replace)
if 'data.course_content' not in content:
    old_content_tab_orig = '''                  <div data-w-tab="Tab 2" class="w-tab-pane">
                    <h2 class="title course-content">Course Content</h2>
                    <div class="course-content-columns">
                      <div class="course-content-column-2">
                        <div class="rich-text-bullets w-richtext"></div>
                      </div>
                      <div class="spacer course-content"></div>
                      <div class="course-content-column-2">
                        <div class="rich-text-bullets w-richtext"></div>
                      </div>
                    </div>
                  </div>'''
    
    new_content_tab = '''                  <div data-w-tab="Tab 2" class="w-tab-pane">
                    <h2 class="title course-content">Course Content</h2>
                    <div class="course-content-columns">
                      <div class="course-content-column-2">
                        <div class="rich-text-bullets w-richtext">{{ data.course_content|safe if data.course_content else '' }}</div>
                      </div>
                    </div>
                  </div>'''
    content = content.replace(old_content_tab_orig, new_content_tab, 1)

# === 5. Remove opacity:0 from key animated elements ===
# Remove opacity:0 from inline styles but keep transforms
import re
# Pattern: remove ;opacity:0 or opacity:0; from style attributes
content = re.sub(r';opacity:0(?=")', '', content)
content = re.sub(r'opacity:0;', '', content)

with open("templates/detail_product.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Template updated successfully!")

# Verify changes
with open("templates/detail_product.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

checks = [
    ('grade loop', 'data.grade.split'),
    ('duration', 'data.duration'),
    ('videos', 'data.videos'),
    ('course_content', 'data.course_content'),
]
for label, needle in checks:
    found = any(needle in line for line in lines)
    print(f"  {label}: {'OK' if found else 'MISSING'}")

# Count opacity:0 remaining
opacity_count = sum(1 for line in lines if 'opacity:0' in line or 'opacity: 0' in line)
print(f"  opacity:0 remaining: {opacity_count}")
