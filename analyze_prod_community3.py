import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from bs4 import BeautifulSoup

with open('prod_community_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# The "What families say" heading uses spans - search for the section-14 class directly
print("=" * 80)
print("=== WHAT FAMILIES SAY (section-14) ===")
print("=" * 80)
section14 = soup.find('div', class_='section-14')
if section14:
    print(section14.prettify()[:10000])
else:
    print("section-14 not found, trying alternatives...")
    # Search for the testimonial-quote-block
    tqb = soup.find('div', class_='testimonial-quote-block')
    if tqb:
        # Go up several levels
        p = tqb
        for _ in range(10):
            p = p.parent
            if p.name == '[document]':
                break
        print(p.prettify()[:10000])

print()
print("=" * 80)
print("=== HACKPNW - FULL w-dyn-item CARD ===")
print("=" * 80)
dyn_items = soup.find_all(class_='w-dyn-item')
for item in dyn_items:
    if item.get_text() and 'HackPNW' in item.get_text():
        print(item.prettify()[:5000])
        break

print()
print("=" * 80)
print("=== UPCOMING EVENTS - FULL SECTION (section community) ===")  
print("=" * 80)
# Find the first section.community (Upcoming events)
sections = soup.find_all('div', class_='section')
for s in sections:
    if s.find('h1', string=lambda t: t and 'Upcoming' in t if t else False):
        # Just print the event date/location details
        event_details = s.find_all('div', class_=lambda c: c and 'event' in ' '.join(c).lower() if c else False)
        print(f"Found section with {len(event_details)} event-related divs")
        # Print just the card portion
        cards = s.find_all('div', class_='card')
        for card in cards:
            if 'HackPNW' in card.get_text():
                print(card.prettify()[:5000])
        break

print()
print("=" * 80)
print("=== WHAT FAMILIES SAY - heading structure ===")  
print("=" * 80)
# Find spans with 'families'
for span in soup.find_all('span'):
    text = span.get_text(strip=True)
    if 'families' in text.lower():
        print(f"<span> class={span.get('class','')} => '{text}'")
        parent = span.parent
        for i in range(3):
            print(f"  parent {i}: <{parent.name}> class={parent.get('class','')}")
            parent = parent.parent

# Find the h1 that contains "What families say" - it may be split across child elements
for h1 in soup.find_all('h1'):
    full_text = h1.get_text(strip=True)
    if 'families' in full_text.lower():
        print(f"\nFound h1: class={h1.get('class', '')} => '{full_text}'")
        print(h1.prettify())

print()
print("=" * 80)
print("=== What families say - subtitle/description ===")
print("=" * 80)
# Look at what's right after that heading
for h1 in soup.find_all('h1'):
    full_text = h1.get_text(strip=True)
    if 'families' in full_text.lower():
        # Get next siblings
        for sibling in h1.find_next_siblings():
            if sibling.name == 'p':
                print(f"<p> class={sibling.get('class','')} => '{sibling.get_text(strip=True)}'")
                break
        # Find description
        container = h1.parent
        print(f"\nParent container: <{container.name}> class={container.get('class','')}")
        print(container.prettify()[:3000])
        break

print()
print("=" * 80)
print("=== VIEW ALL ON YOUTUBE button ===")
print("=" * 80)
for a in soup.find_all('a', class_='button-primary'):
    text = a.get_text(strip=True)
    if 'youtube' in text.lower():
        print(f"<a> class={a.get('class','')} href={a.get('href','')} => '{text}'")
        parent = a.parent
        print(f"  parent: <{parent.name}> class={parent.get('class','')}")
        print(a.prettify())
