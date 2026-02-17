import re

with open('prod_community_raw3.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all w-embed-youtubevideo elements and their padding-top
print("="*80)
print("YouTube embed elements with inline styles:")
print("="*80)
# Find divs with w-embed-youtubevideo
pattern = re.compile(r'<div[^>]*class="[^"]*w-embed-youtubevideo[^"]*"[^>]*>', re.DOTALL)
for m in pattern.finditer(html):
    elem = m.group(0)
    # Extract style
    style_match = re.search(r'style="([^"]*)"', elem)
    if style_match:
        print(f"Style: {style_match.group(1)}")
    else:
        print(f"No inline style: {elem[:200]}")
    print()

# Find the gallery-grid-container HTML section
print("="*80)
print("Gallery grid container HTML snippet:")
print("="*80)
idx = html.find('gallery-grid-container')
if idx >= 0:
    snippet = html[max(0, idx-100):idx+2000]
    print(snippet[:3000])

print("\n" + "="*80)
print("Centered container HTML context:")
print("="*80)
idx = html.find('centered-container')
if idx >= 0:
    snippet = html[max(0, idx-200):idx+500]
    print(snippet)

# Check for h1 with font-color-primary
print("\n" + "="*80)
print("h1 with font-color-primary:")
print("="*80)
pattern = re.compile(r'<h1[^>]*class="[^"]*font-color-primary[^"]*"[^>]*>.*?</h1>', re.DOTALL)
for m in pattern.finditer(html):
    print(m.group(0)[:300])
    print()
