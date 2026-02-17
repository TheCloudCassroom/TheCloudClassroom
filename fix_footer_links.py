"""Fix footer links in all template files to use clean URLs."""
import re
import os

base = os.path.dirname(os.path.abspath(__file__))

# All templates that might have old .html links in footers
files_to_update = [
    os.path.join(base, 'templates', 'about-us.html'),
    os.path.join(base, 'templates', 'courses.html'),
    os.path.join(base, 'templates', 'detail_product.html'),
    os.path.join(base, 'templates', 'community.html'),
    os.path.join(base, 'templates', 'index.html'),
    os.path.join(base, 'templates', '401.html'),
    os.path.join(base, 'templates', 'checkout.html'),
]

# Link replacements
replacements = {
    'href="index.html"': 'href="/"',
    'href="about-us.html"': 'href="/about-us"',
    'href="courses.html"': 'href="/courses"',
    'href="community.html"': 'href="/community"',
    'href="instructors.html"': 'href="/instructors"',
    'href="contact-us.html"': 'href="/contact-us"',
}

for fpath in files_to_update:
    if not os.path.exists(fpath):
        print(f'Skipped (not found): {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {os.path.basename(fpath)}')
    else:
        print(f'No changes: {os.path.basename(fpath)}')

print('Done!')
