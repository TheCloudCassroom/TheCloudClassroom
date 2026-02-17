import requests
import re

r = requests.get('https://www.thecloudclassroom.org/community', timeout=15)
print(f"Status: {r.status_code}")

# Find all link tags with stylesheet
links = re.findall(r'<link[^>]*href="([^"]*)"[^>]*>', r.text)
for l in links:
    if 'css' in l.lower() or 'style' in l.lower():
        print(f"CSS: {l}")

# Also find inline style tags count
styles = re.findall(r'<style[^>]*>(.*?)</style>', r.text, re.DOTALL)
print(f"\nInline style blocks: {len(styles)}")

# Check for specific classes in HTML
for cls in ['centered-container', 'gallery-grid-container', 'w-embed-youtubevideo', 'font-color-primary']:
    count = r.text.count(cls)
    print(f"Class '{cls}' found {count} times in HTML")

# Save raw HTML for inspection
with open('prod_community_raw3.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print("\nSaved raw HTML to prod_community_raw3.html")
