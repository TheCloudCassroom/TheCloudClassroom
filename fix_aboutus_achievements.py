"""Fix the achievements section in about-us.html by uncommenting it."""
import os

filepath = os.path.join(os.path.dirname(__file__), 'templates', 'about-us.html')

with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

# The achievements section is commented with <!-- ... -->
marker = '<!-- <div data-w-id="081c0aac-b96f-7778-465c-c59646c49486"'
start = c.find(marker)
if start != -1:
    # Find the closing --> for this comment
    # It closes with   </div> -->
    end_marker = '</div> -->'
    end = c.find(end_marker, start)
    if end != -1:
        end += len(end_marker)
        commented = c[start:end]
        # Remove <!-- at start and --> at end
        uncommented = commented[5:]  # Remove '<!-- '
        uncommented = uncommented.rstrip()
        if uncommented.endswith('-->'):
            uncommented = uncommented[:-3].rstrip()
        c = c[:start] + uncommented + c[end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK: Achievements section uncommented in about-us.html')
    else:
        print('FAIL: End marker not found')
else:
    print('FAIL: Comment start not found')
