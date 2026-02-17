import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from bs4 import BeautifulSoup

with open('prod_community_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# === BROWSE CLASS RECORDINGS ===
print("=" * 80)
print("=== BROWSE CLASS RECORDINGS - FULL SECTION ===")
print("=" * 80)
# Find ALL centered-container
for div in soup.find_all('div', class_='centered-container'):
    h1 = div.find('h1')
    if h1 and 'Browse Class Recordings' in h1.get_text():
        print(div.prettify()[:12000])
        break

# Try broader search
recordings_h1 = soup.find('h1', string=lambda s: s and 'Browse Class Recordings' in s)
if recordings_h1:
    print("\n--- Found heading, walking up ---")
    parent = recordings_h1.parent
    for i in range(8):
        cls = parent.get('class', [])
        tag = parent.name
        print(f"  Level {i}: <{tag}> class={cls}")
        if 'section' in tag or ('community' in ' '.join(cls) if cls else False):
            print(f"\n--- Section found at level {i} ---")
            print(parent.prettify()[:15000])
            break
        parent = parent.parent

print()
print("=" * 80)
print("=== WHAT FAMILIES SAY - FULL SECTION ===")
print("=" * 80)
families_h1 = soup.find('h1', string=lambda s: s and 'families say' in s.lower() if s else False)
if not families_h1:
    # Try h2
    families_h1 = soup.find('h2', string=lambda s: s and 'families say' in s.lower() if s else False)
if not families_h1:
    # Try searching all text
    for tag in soup.find_all(True):
        text = tag.get_text(strip=True)
        if 'families say' in text.lower() and tag.name in ['h1','h2','h3','h4']:
            families_h1 = tag
            print(f"Found via text search: <{tag.name}> {tag.get('class','')} => {text[:50]}")
            break

if families_h1:
    print(f"Found: <{families_h1.name}> {families_h1.get('class','')}")
    parent = families_h1.parent
    for i in range(8):
        cls = parent.get('class', [])
        tag = parent.name
        print(f"  Level {i}: <{tag}> class={cls}")
        parent = parent.parent
    
    # Find section-14 which was in the parent chain
    section14 = families_h1.find_parent('div', class_='section-14')
    if section14:
        print("\n--- section-14 found ---")
        print(section14.prettify()[:12000])
    else:
        # Find nearest section
        section = families_h1.find_parent('section')
        if section:
            print("\n--- section found ---")
            print(section.prettify()[:12000])
        else:
            # Just get container
            container = families_h1.find_parent('div')
            # Go up to a reasonable level
            p = families_h1
            for _ in range(6):
                p = p.parent
            print(f"\n--- 6 levels up: <{p.name}> class={p.get('class','')} ---")
            print(p.prettify()[:12000])
else:
    print("NOT FOUND - searching differently")
    # Maybe it's split across elements
    for tag in soup.find_all(string=lambda s: s and 'families' in s.lower() if s else False):
        par = tag.parent
        if par.name in ['h1','h2','h3','h4','span']:
            print(f"  Possible: <{par.name}> {par.get('class','')} => {tag.strip()[:80]}")

print()
print("=" * 80)
print("=== HACKPNW - FULL EVENT CARD ===")
print("=" * 80)
hackpnw_h3 = soup.find('h3', string=lambda s: s and 'HackPNW' in s if s else False)
if hackpnw_h3:
    # Find parent card
    parent = hackpnw_h3
    for i in range(8):
        parent = parent.parent
        cls = parent.get('class', [])
        if cls and 'card' in ' '.join(cls):
            print(parent.prettify()[:5000])
            break
    else:
        # Go up to w-dyn-item
        dyn_item = hackpnw_h3.find_parent(class_='w-dyn-item')
        if dyn_item:
            print(dyn_item.prettify()[:5000])
        else:
            parent = hackpnw_h3
            for _ in range(5):
                parent = parent.parent
            print(parent.prettify()[:5000])

print()
print("=" * 80)
print("=== TESTIMONIAL SLIDER (Slider 1) ===")
print("=" * 80)
sliders = soup.find_all('div', class_='w-slider')
if len(sliders) > 1:
    slider = sliders[1]
    print(slider.prettify()[:12000])

print()
print("=" * 80)
print("=== ALL GALLERY/LIGHTBOX ELEMENTS ===")
print("=" * 80)
gallery_grid = soup.find('div', class_='gallery-grid-container')
if gallery_grid:
    print(gallery_grid.prettify()[:15000])
else:
    print("No gallery-grid-container found")
    # Search for lightbox elements
    lightboxes = soup.find_all('a', class_=lambda c: c and any('lightbox' in x for x in c) if c else False)
    print(f"Found {len(lightboxes)} lightbox links")
    for i, lb in enumerate(lightboxes):
        imgs = lb.find_all('img')
        scripts = lb.find_all('script')
        print(f"  Lightbox {i}: imgs={len(imgs)}, scripts={len(scripts)}")
        for img in imgs:
            print(f"    img: src={img.get('src','N/A')[:120]}")
        for s in scripts:
            if s.string:
                print(f"    script: {s.string[:300]}")
