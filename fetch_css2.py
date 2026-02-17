import requests
import re

# 1. Fetch the CSS
css_url = "https://assets-global.website-files.com/60306606d61c1d030823ec1e/css/cloudclassroom-d626d0982bf066fecbc76582.webflow.d737571b4.css"
r = requests.get(css_url, timeout=15)
css = r.text
print(f"CSS length: {len(css)} chars")

# Save CSS for reference
with open('prod_webflow.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Helper to extract CSS rule
def find_rules(css_text, selector_pattern):
    """Find CSS rules matching a selector pattern."""
    results = []
    # Find all rule blocks
    pattern = re.compile(r'([^{}]*)\{([^{}]*)\}')
    for m in pattern.finditer(css_text):
        selector = m.group(1).strip()
        body = m.group(2).strip()
        if re.search(selector_pattern, selector):
            results.append(f"{selector} {{\n  {body}\n}}")
    return results

print("\n" + "="*80)
print("1. .centered-container rules:")
print("="*80)
for rule in find_rules(css, r'\.centered-container'):
    print(rule)
    print()

print("\n" + "="*80)
print("2. .gallery-grid-container rules:")
print("="*80)
for rule in find_rules(css, r'\.gallery-grid-container'):
    print(rule)
    print()

print("\n" + "="*80)
print("3. .w-embed-youtubevideo rules:")
print("="*80)
for rule in find_rules(css, r'\.w-embed-youtubevideo'):
    print(rule)
    print()

print("\n" + "="*80)
print("4. .font-color-primary rules:")
print("="*80)
for rule in find_rules(css, r'\.font-color-primary'):
    print(rule)
    print()

print("\n" + "="*80)
print("5. .container-default-1209px rules:")
print("="*80)
for rule in find_rules(css, r'\.container-default-1209px'):
    print(rule)
    print()

print("\n" + "="*80)
print("6. .w-container rules:")
print("="*80)
for rule in find_rules(css, r'^\.w-container$'):
    print(rule)
    print()

print("\n" + "="*80)
print("7. h1 rules (checking for font-size):")
print("="*80)
for rule in find_rules(css, r'\bh1\b'):
    if 'font-size' in rule:
        print(rule)
        print()
