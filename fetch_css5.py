import re

with open('prod_webflow.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find the media query that contains ".centered-container { max-width: 1200px }"
pos = css.find('.centered-container {\n    max-width: 1200px;')
if pos == -1:
    pos = css.find('.centered-container {\n  max-width: 1200px;')
if pos == -1:
    # Search for it differently
    for m in re.finditer(r'\.centered-container\s*\{[^}]*max-width', css):
        pos = m.start()
        break

if pos >= 0:
    # Walk backwards to find the opening @media
    search_back = css[max(0, pos-2000):pos]
    # Find the last @media
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        print(f"Media query: {search_back[last_media.start():last_media.end()]}")
        print(f"Context around: {search_back[last_media.start():last_media.start()+100]}")
    print(f"\nFull context around .centered-container max-width:")
    print(css[pos-100:pos+200])
else:
    print("Not found")

# Similarly check what media query the .gallery-grid-container { align-self: stretch } is in
print("\n\n" + "="*80)
pos = css.find('.gallery-grid-container {\n    align-self: stretch;')
if pos == -1:
    pos = css.find('.gallery-grid-container {\n  align-self: stretch;')
if pos >= 0:
    search_back = css[max(0, pos-2000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        print(f"gallery-grid-container stretch in Media: {search_back[last_media.start():last_media.end()]}")

# Check what media query .gallery-grid-container 1fr 1fr is in
print("\n")
pos = css.find('grid-template-columns: 1fr 1fr;')
if pos >= 0:
    search_back = css[max(0, pos-3000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        print(f"gallery 2-col in Media: {search_back[last_media.start():last_media.end()]}")

# Check what media query .gallery-grid-container 1fr (single col) is in
print("\n")
pos = css.find('grid-template-columns: 1fr;\n    margin-left: 0;')
if pos >= 0:
    search_back = css[max(0, pos-3000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        print(f"gallery 1-col in Media: {search_back[last_media.start():last_media.end()]}")
