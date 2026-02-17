"""Update nav in all template files to add Volunteers and Contact tabs."""
import re

import os
base = os.path.dirname(os.path.abspath(__file__))
files_to_update = [
    os.path.join(base, 'templates', 'about-us.html'),
    os.path.join(base, 'templates', 'courses.html'),
    os.path.join(base, 'templates', 'detail_product.html'),
    os.path.join(base, 'templates', 'community.html'),
    os.path.join(base, 'templates', 'index.html'),
]

for fpath in files_to_update:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace the logo/brand link and srcset image
    content = re.sub(
        r'<a href="index\.html"[^>]*class="brand w-nav-brand[^"]*"><img[^>]+class="header-logo"[^>]*></a>',
        '<a href="/" class="brand w-nav-brand"><img alt="" src="https://cdn.prod.website-files.com/60306606d61c1d030823ec1e/6030af958678e259c6e94f21_logo.png" class="header-logo"/></a>',
        content
    )

    # 2. Replace mega menu content - remove old links, add clean ones
    content = re.sub(
        r'<div class="menu-2-columns">.*?</div>\s*</div>\s*<div class="mega-menu-column-4">.*?</div>',
        '<div class="menu-2-columns">\n                          <div class="mega-menu-column-1"><a href="/" class="mega-menu-link">Home</a><a href="/about-us" class="mega-menu-link">About</a><a href="/courses" class="mega-menu-link">Courses</a></div>\n                          <div class="mega-menu-column-3"><a href="/community" class="mega-menu-link">Events</a><a href="/instructors" class="mega-menu-link">Teachers</a></div>\n                          <div class="mega-menu-column-3"><a href="/contact-us" class="mega-menu-link">Contact</a></div>\n                        </div>\n                      </div>',
        content,
        flags=re.DOTALL
    )

    # 3. Replace the nav links after the dropdown (About, Community -> About, Community, Volunteers, Contact)
    content = re.sub(
        r'</div><a href="about-us\.html"[^>]*class="nav-link[^"]*">About</a><a href="community\.html"[^>]*class="nav-link[^"]*">Community</a></nav>',
        '</div><a href="/about-us" class="nav-link">About</a><a href="/community" class="nav-link">Community</a><a href="/instructors" class="nav-link">Volunteers</a><a href="/contact-us" class="nav-link">Contact</a></nav>',
        content
    )

    # 4. Replace Home nav link
    content = re.sub(
        r'<a href="index\.html"[^>]*class="nav-link[^"]*">Home</a>',
        '<a href="/" class="nav-link">Home</a>',
        content
    )

    # 5. Replace Courses button + SIGN IN
    content = re.sub(
        r'<a href="(?:courses\.html|#)" class="button-primary header-button w-button">Courses</a><a href="#" class="link-2">SIGN\s+IN</a>',
        '<a href="/courses" class="button-primary header-button w-button">Courses</a>',
        content
    )

    # 6. Also fix standalone courses.html link
    content = re.sub(
        r'<a href="courses\.html" class="button-primary header-button w-button">Courses</a>',
        '<a href="/courses" class="button-primary header-button w-button">Courses</a>',
        content
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {fpath}')
    else:
        print(f'No changes: {fpath}')

print('Done!')
