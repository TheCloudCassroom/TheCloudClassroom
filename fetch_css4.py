import re

with open('prod_webflow.css', 'r', encoding='utf-8') as f:
    css = f.read()

# The CSS is minified, let's find the context around our selectors within media queries
# First, let's find all media query blocks and parse them

# Find centered-container occurrences with surrounding context
print("="*80)
print("ALL .centered-container occurrences with context (200 chars around):")
print("="*80)
for m in re.finditer(r'\.centered-container', css):
    start = max(0, m.start() - 200)
    end = min(len(css), m.end() + 300)
    context = css[start:end]
    # Check if inside a media query
    print(f"\n--- Position {m.start()} ---")
    print(context)
    print()

print("\n" + "="*80)
print("ALL .gallery-grid-container occurrences with context:")
print("="*80)
for m in re.finditer(r'\.gallery-grid-container', css):
    start = max(0, m.start() - 200)
    end = min(len(css), m.end() + 400)
    context = css[start:end]
    print(f"\n--- Position {m.start()} ---")
    print(context)
    print()

# Find .w-container rules with context to see media query context
print("\n" + "="*80)
print("ALL .w-container (exact) occurrences with context:")
print("="*80)
for m in re.finditer(r'\.w-container\s*\{', css):
    start = max(0, m.start() - 200)
    end = min(len(css), m.end() + 300)
    context = css[start:end]
    print(f"\n--- Position {m.start()} ---")
    print(context)
    print()
