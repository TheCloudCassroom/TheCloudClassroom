import re

with open('prod_webflow.css', 'r', encoding='utf-8') as f:
    css = f.read()

# centered-container max-width 1200
pos = css.find('.centered-container {\n    max-width: 1200px;')
if pos == -1:
    pos = css.find('.centered-container {\n  max-width: 1200px;')

if pos >= 0:
    # Get back further
    search_back = css[max(0, pos-5000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        media_text = search_back[last_media.start():last_media.end()]
        print(f"centered-container max-width:1200px in: {media_text}")
    else:
        print("No media query found (global scope)")
else:
    print("centered-container max-width 1200 not found")

# gallery 1-col
pos = css.find('grid-template-columns: 1fr;\n    margin-left: 0;')
if pos >= 0:
    search_back = css[max(0, pos-5000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        media_text = search_back[last_media.start():last_media.end()]
        print(f"gallery 1-col in: {media_text}")

# gallery stretch
pos = css.find('.gallery-grid-container {\n    align-self: stretch;')
if pos == -1:
    pos = css.find('.gallery-grid-container {\n  align-self: stretch;')
if pos >= 0:
    search_back = css[max(0, pos-5000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        media_text = search_back[last_media.start():last_media.end()]
        print(f"gallery stretch in: {media_text}")

# gallery 2-col (1fr 1fr)
for m in re.finditer(r'\.gallery-grid-container\s*\{[^}]*1fr 1fr[^}]*\}', css):
    pos = m.start()
    search_back = css[max(0, pos-5000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        media_text = search_back[last_media.start():last_media.end()]
        print(f"gallery 2-col in: {media_text}")
    break

# centered-container text-align:left
pos = css.find('.centered-container {\n    text-align: left;')
if pos == -1:
    pos = css.find('.centered-container {\n  text-align: left;')
if pos >= 0:
    search_back = css[max(0, pos-5000):pos]
    media_matches = list(re.finditer(r'@media[^{]*\{', search_back))
    if media_matches:
        last_media = media_matches[-1]
        media_text = search_back[last_media.start():last_media.end()]
        print(f"centered-container text-align:left in: {media_text}")
