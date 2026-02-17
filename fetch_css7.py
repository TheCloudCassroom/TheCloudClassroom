import re

with open('prod_webflow.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find all occurrences of centered-container and gallery-grid-container
# and trace back to find which @media block they're in

def find_enclosing_media(css_text, pos):
    """Walk backwards from pos counting braces to find enclosing @media."""
    # Count curly braces backwards from pos
    depth = 0
    i = pos - 1
    while i >= 0:
        if css_text[i] == '}':
            depth += 1
        elif css_text[i] == '{':
            if depth > 0:
                depth -= 1
            else:
                # This { opens a block we're inside. Check if it's @media
                # Look backwards for @media
                pre = css_text[max(0, i-100):i].strip()
                if pre.endswith(')') or '@media' in pre:
                    # Find the @media start
                    media_start = pre.rfind('@media')
                    if media_start >= 0:
                        return pre[media_start:] + css_text[i]
                    return "(nested in unknown block)"
                else:
                    # This is a rule selector, not a media query
                    # We're at the top level
                    return "GLOBAL (no media query)"
        i -= 1
    return "GLOBAL (beginning of file)"

# Find each selector occurrence
selectors_to_find = [
    '.centered-container',
    '.gallery-grid-container',
    '.w-container',
    'h1',
    '.font-color-primary',
    '.container-default-1209px',
    '.w-embed-youtubevideo',
]

for sel in selectors_to_find:
    print(f"\n{'='*80}")
    print(f"Selector: {sel}")
    print(f"{'='*80}")
    # Escape for regex
    escaped = re.escape(sel)
    for m in re.finditer(escaped + r'\s*[\{,.]', css):
        pos = m.start()
        rule_start = pos
        # Get the full rule
        brace_open = css.find('{', pos)
        if brace_open < 0:
            continue
        brace_close = css.find('}', brace_open)
        if brace_close < 0:
            continue
        selector = css[pos:brace_open].strip()
        body = css[brace_open+1:brace_close].strip()
        media = find_enclosing_media(css, pos)
        print(f"\n  Media: {media}")
        print(f"  {selector} {{ {body} }}")
