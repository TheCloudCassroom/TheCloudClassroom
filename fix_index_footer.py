"""Fix the footer-links-block in index.html by uncommenting it."""
import os

filepath = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')

with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

marker = '<!-- <div class="footer-links-block">'
start = c.find(marker)
if start != -1:
    end = c.find('-->', start + 5)
    if end != -1:
        end += 3
        commented = c[start:end]
        # Remove the opening <!-- and closing -->
        uncommented = commented[5:]  # remove '<!-- '
        uncommented = uncommented.rstrip()
        if uncommented.endswith('-->'):
            uncommented = uncommented[:-3].rstrip()
        c = c[:start] + uncommented + c[end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK: Footer-links-block uncommented in index.html')
    else:
        print('FAIL: End marker not found')
else:
    print('FAIL: Comment start not found')
