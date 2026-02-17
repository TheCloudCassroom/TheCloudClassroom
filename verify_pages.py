"""Verify all key content elements are present in the rendered pages."""
from app import app
client = app.test_client()

def check(name, result):
    print(f"  {name}: {'PASS' if result else 'FAIL'}")

# Check about-us
html = client.get('/about-us').data.decode()
print('=== about-us.html ===')
check('OUR STORY button', 'button-secondary large w-button' in html and 'Our Story' in html)
check('Meet Our Team heading', 'Meet Our Team' in html)
check('No Meet Our Founders', 'Meet Our Founders' not in html)
check('No Come and Visit Us', 'Come and Visit Us' not in html)
check('Elizabeth Zhao first', html.index('Elizabeth Zhao') < html.index('Jessie Chen'))
check('All 9 members', all(n in html for n in ['Elizabeth Zhao','Jessie Chen','Lero Wang','Ethan Hu','Tiana Wang','Jonathan Wang','Rena Wang','Omar Wahby','Ruikuan Zhu']))
check('Founder & Chairwoman', 'Founder &amp; Chairwoman' in html)
check('Co-Founder &amp; President', 'Co-Founder &amp; President' in html)
check('VP of Technology', 'Vice President of Technology' in html)

# Check community
html = client.get('/community').data.decode()
print('=== community.html ===')
check('Upcoming events', 'Upcoming' in html and 'events' in html)
check('HackPNW event', 'HackPNW' in html)
check('Feb 4 2023', 'February 4, 2023' in html)
check('Community through lens', 'Community through the lens' in html)
check('Browse Class Recordings', 'Browse Class' in html)
check('YouTube embed', 'youtube.com/embed' in html)
check('What families say', 'families' in html)
check('Millie M testimonial', 'Millie M' in html)
check('No School Ambassadors', 'School Ambassadors' not in html)
check('No Students Geo', 'Students Geo' not in html)
check('Never miss event', 'Never miss another event' in html)
check('VIEW ALL ON YOUTUBE', 'VIEW ALL ON YOUTUBE' in html)

# Check instructors
html = client.get('/instructors').data.decode()
print('=== instructors.html ===')
check('Map locations', all(c in html for c in ['Sydney, Australia','Seattle, United States','Zanzibar, Tanzania','Shanghai, China']))
check('Google Maps directions', 'google.com/maps/dir' in html)
check('Sydney image', 'sydney-opera-house' in html)
check('CTA section', 'never too early to learn' in html)
check('Become volunteer', 'Become a volunteer' in html)

# Check homepage
html = client.get('/').data.decode()
print('=== index.html ===')
check('Cloud Classroom title', 'Welcome to' in html and 'Cloud Classroom' in html)
check('Our Courses section', 'Our Courses' in html)
check('Volunteers nav link', 'Volunteers' in html)
check('Contact nav link', 'Contact' in html)
check('Footer links', 'footer-links-block' in html)

# Check courses
html = client.get('/courses').data.decode()
print('=== courses.html ===')
check('Course cards', 'course-card' in html or 'card product' in html or 'w-dyn-item' in html)
check('VIEW ALL COURSES', 'VIEW ALL COURSES' in html or 'ALL COURSES' in html or 'all-courses' in html)

print("\nAll tests complete!")
