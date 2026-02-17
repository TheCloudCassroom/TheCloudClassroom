"""Fix about-us.html to match production:
1. Uncomment the 'OUR STORY' button in hero
2. Remove 'Come and Visit Us' section
3. Merge 'Meet Our Founders' + 'Meet Our Team' into one unified 'Meet Our Team' section
   matching the production order of 9 members
"""
import re

filepath = "templates/about-us.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Uncomment the "OUR STORY" button
content = content.replace(
    '<!-- <a href="#Our-Story" class="button-secondary large w-button">Our Story</a> -->',
    '<a href="#Our-Story" class="button-secondary large w-button">Our Story</a>'
)

# 2. Remove the entire "Come and Visit Us" section 
# This section starts after the mission slider and ends before the Meet Our Team section
# Find and remove everything from the "Come and Visit Us" container to the divider after it
come_visit_start = content.find('<div data-w-id="081c0aac-b96f-7778-465c-c59646c494dd"')
# We want to remove from this div up to and including the closing </div> of the section
# The section ends at the commented-out CTA block
come_visit_end = content.find('<!-- <div data-w-id="458a3e47-e544-5eec-ffce-58aa64417b32"')
if come_visit_start > 0 and come_visit_end > come_visit_start:
    # Also need to remove up through the end comment of the CTA block
    cta_end = content.find('</div> -->', come_visit_end)
    if cta_end > 0:
        cta_end += len('</div> -->')
        # Remove the newline after too
        while cta_end < len(content) and content[cta_end] in '\r\n':
            cta_end += 1
        content = content[:come_visit_start] + content[cta_end:]

# 3. Replace the "Meet Our Founders" section AND "Meet Our Team" section with unified "Meet Our Team"
# Find the start of "Meet Our Founders" section
founders_start = content.find('<div data-w-id="081c0aac-b96f-7778-465c-c59646c49506"')
# Find the end of the "Meet Our Team" section - it ends at the divider before the footer
team_end_marker = '<div class="container-default-1209px w-container">\n    <div data-w-id="081c0aac-b96f-7778-465c-c59646c49526"'
team_end = content.find('data-w-id="081c0aac-b96f-7778-465c-c59646c49526"')
if team_end > 0:
    # Go back to find the enclosing div
    team_end = content.rfind('<div class="container-default-1209px w-container">', 0, team_end)

if founders_start > 0 and team_end > founders_start:
    # The unified Meet Our Team section matching production exactly
    # Production order: Elizabeth Zhao, Jessie Chen, Lero Wang, Ethan Hu, Tiana Wang, Jonathan Wang, Rena Wang, Omar Wahby, Ruikuan Zhu
    unified_team = '''<div data-w-id="081c0aac-b96f-7778-465c-c59646c49506" style="-webkit-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
    class="section">
    <div class="container-default-1209px w-container">
        <div data-w-id="081c0aac-b96f-7778-465c-c59646c49508" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
            class="top-content meet-our-teachers">
            <h2 class="heading-2">Meet Our Team</h2>
        </div>
        <div class="w-dyn-list">
            <div role="list" class="meet-our-teachers-grid w-dyn-items">
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/ez.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Elizabeth Zhao</h3>
                            </a>
                            <div class="teachers-work">Founder &amp; Chairwoman</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/jc.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Jessie Chen</h3>
                            </a>
                            <div class="teachers-work">Co-Founder &amp; President</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Lero Wang</h3>
                            </a>
                            <div class="teachers-work">Vice President of Community Service</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Ethan Hu</h3>
                            </a>
                            <div class="teachers-work">Vice President of Technology</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Tiana Wang</h3>
                            </a>
                            <div class="teachers-work">Co-Founder &amp; Vice President of Marketing</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Jonathan Wang</h3>
                            </a>
                            <div class="teachers-work">Regional Director, South East of USA</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Rena Wang</h3>
                            </a>
                            <div class="teachers-work">Co-Founder and College Advisor</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Omar Wahby</h3>
                            </a>
                            <div class="teachers-work">College advisor</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                    <div class="card teachers">
                        <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                            <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                <h3 class="title teachers">Ruikuan Zhu</h3>
                            </a>
                            <div class="teachers-work">Director of Technology Incubation</div>
                            <a href="#" class="button-secondary w-button">VIEW PROFILE</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''
    content = content[:founders_start] + unified_team + content[team_end:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("about-us.html fixed successfully!")
print("- Uncommented 'OUR STORY' button")
print("- Removed 'Come and Visit Us' section")
print("- Merged Founders + Team into unified 'Meet Our Team' (9 members, production order)")
