import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from bs4 import BeautifulSoup, formatter

with open('prod_community_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("=" * 80)
print("=== SECTION ORDER (ALL HEADINGS) ===")
print("=" * 80)
headings = soup.find_all(['h1', 'h2', 'h3'])
for i, h in enumerate(headings):
    text = h.get_text(strip=True)
    if text and len(text) > 2:
        parent_classes = []
        p = h.parent
        depth = 0
        while p and depth < 5:
            if p.get('class'):
                parent_classes.append('.'.join(p.get('class')))
            p = p.parent
            depth += 1
        print(f"  {i}: <{h.name}> class={h.get('class','')} => \"{text}\"")
        print(f"       parent chain: {' > '.join(parent_classes[:3])}")

print()
print("=" * 80)
print("=== 1. COMMUNITY THROUGH THE LENS ===")
print("=" * 80)
# Find the heading
lens_heading = soup.find(string=lambda s: s and 'Community through the lens' in s)
if lens_heading:
    # Go up to find the containing section
    container = lens_heading.find_parent('div', class_=lambda c: c and 'container' in ' '.join(c) if c else False)
    if container:
        # Pretty print the section
        print(container.prettify()[:5000])
        print("... (truncated)" if len(container.prettify()) > 5000 else "")
    else:
        # Try different parent
        container = lens_heading.parent.parent.parent
        print(container.prettify()[:5000])

print()
print("=" * 80)
print("=== 1b. YOUTUBE VIDEOS IN 'THROUGH THE LENS' SLIDER ===")
print("=" * 80)
# Find all YouTube embeds in the slider
sliders = soup.find_all('div', class_='w-slider')
for idx, slider in enumerate(sliders):
    iframes = slider.find_all('iframe')
    slides = slider.find_all('div', class_='w-slide')
    print(f"Slider {idx}: {len(slides)} slides, {len(iframes)} iframes")
    for j, iframe in enumerate(iframes):
        print(f"  iframe {j}: src={iframe.get('src', 'N/A')}")
    for j, slide in enumerate(slides):
        yt_embed = slide.find('div', class_='w-embed-youtubevideo')
        if yt_embed:
            iframe = yt_embed.find('iframe')
            if iframe:
                print(f"  slide {j}: YouTube embed src={iframe.get('src', 'N/A')}")
        imgs = slide.find_all('img')
        for img in imgs:
            print(f"  slide {j}: img src={img.get('src', 'N/A')[:100]}")

print()
print("=" * 80)
print("=== 2. BROWSE CLASS RECORDINGS ===")
print("=" * 80)
recordings_heading = soup.find(string=lambda s: s and 'Browse Class Recordings' in s)
if recordings_heading:
    container = recordings_heading.find_parent('div', class_=lambda c: c and 'container' in ' '.join(c) if c else False)
    if container:
        print(container.prettify()[:8000])
        print("... (truncated)" if len(container.prettify()) > 8000 else "")

print()
print("=" * 80)
print("=== 2b. BROWSE CLASS RECORDINGS - ALL IFRAMES AND IMAGES ===")
print("=" * 80)
if recordings_heading:
    container = recordings_heading.find_parent('div', class_=lambda c: c and 'container' in ' '.join(c) if c else False)
    if container:
        iframes = container.find_all('iframe')
        imgs = container.find_all('img')
        lightboxes = container.find_all('a', class_=lambda c: c and 'lightbox' in ' '.join(c) if c else False)
        print(f"Total iframes: {len(iframes)}")
        for i, iframe in enumerate(iframes):
            print(f"  iframe {i}: src={iframe.get('src', 'N/A')}")
        print(f"Total images: {len(imgs)}")
        for i, img in enumerate(imgs):
            print(f"  img {i}: src={img.get('src', 'N/A')[:120]}")
            print(f"           alt={img.get('alt', 'N/A')}")
        print(f"Total lightboxes: {len(lightboxes)}")
        for i, lb in enumerate(lightboxes):
            scripts = lb.find_all('script')
            for s in scripts:
                print(f"  lightbox {i} script: {s.string[:200] if s.string else 'N/A'}")

print()
print("=" * 80)
print("=== 3. WHAT FAMILIES SAY ===")
print("=" * 80)
families_heading = soup.find(string=lambda s: s and 'What families say' in s)
if families_heading:
    container = families_heading.find_parent('div', class_=lambda c: c and 'container' in ' '.join(c) if c else False)
    if not container:
        container = families_heading.find_parent('section')
    if not container:
        container = families_heading.parent.parent.parent.parent
    if container:
        print(container.prettify()[:8000])
        print("... (truncated)" if len(container.prettify()) > 8000 else "")

print()
print("=" * 80)
print("=== 4. NEVER MISS ANOTHER EVENT (NEWSLETTER) ===")
print("=" * 80)
newsletter_heading = soup.find(string=lambda s: s and 'Never miss another event' in s)
if newsletter_heading:
    container = newsletter_heading.find_parent('div', class_=lambda c: c and ('section' in ' '.join(c) or 'newsletter' in ' '.join(c)) if c else False)
    if not container:
        container = newsletter_heading.find_parent('section')
    if not container:
        container = newsletter_heading.parent.parent.parent
    if container:
        print(container.prettify()[:5000])

print()
print("=" * 80)
print("=== 5. HACKPNW EVENT CARD ===")
print("=" * 80)
hackpnw = soup.find(string=lambda s: s and 'HackPNW' in s if s else False)
if hackpnw:
    card = hackpnw.find_parent('div', class_=lambda c: c and 'card' in ' '.join(c) if c else False)
    if card:
        print(card.prettify()[:5000])
