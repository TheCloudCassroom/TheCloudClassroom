"""Add missing team members (Lero Wang, Ethan Hu, Tiana Wang) to about-us.html."""
import os

filepath = os.path.join(os.path.dirname(__file__), 'templates', 'about-us.html')

with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

# New team member cards to insert
new_members = '''
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                        <div class="card teachers  ">
                            <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                                <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                    <h3 class="title teachers">Lero Wang</h3>
                                </a>
                                <div class="teachers-work">Vice President of Community Service</div>
                                <p class="paragraph teachers-text">Lero is dedicated to community service and leads Cloud Classroom's community outreach efforts.</p><a href="#" class="button-secondary w-button">View Profile</a></div>
                        </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                        <div class="card teachers  ">
                            <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                                <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                    <h3 class="title teachers">Ethan Hu</h3>
                                </a>
                                <div class="teachers-work">Vice President of Technology</div>
                                <p class="paragraph teachers-text">Ethan brings technical expertise to Cloud Classroom, leading the technology team to build and maintain our learning platform.</p><a href="#" class="button-secondary w-button">View Profile</a></div>
                        </div>
                </div>
                <div data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec08" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    role="listitem" class="teacher-card w-dyn-item">
                        <div class="card teachers  ">
                            <div class="teacher-card-wrapper"><img src="/static/images/Facetune_11-09-2020-22-32-35-2.JPG" alt="" class="image teachers">
                                <a data-w-id="128ea10a-6aac-921c-879c-98b5b7dfec0b" href="#" class="card-title-link teachers w-inline-block">
                                    <h3 class="title teachers">Tiana Wang</h3>
                                </a>
                                <div class="teachers-work">Co-Founder &amp; Vice President of Marketing</div>
                                <p class="paragraph teachers-text">Tiana co-founded Cloud Classroom and leads marketing efforts to spread our mission of accessible education.</p><a href="#" class="button-secondary w-button">View Profile</a></div>
                        </div>
                </div>'''

# Find the insertion point: after the last team member card (Ruikuan Zhu), before the closing </div>
# The grid ends with:  </div>\n            </div>  
# (closing for the w-dyn-items role="list" div and the w-dyn-list div)
marker = '<h3 class="title teachers">Ruikuan Zhu</h3>'
pos = c.find(marker)
if pos != -1:
    # Find the end of this card's parent div (the w-dyn-item div)
    # Looking for the closing: </div>\n            </div>  after the card
    # The card structure ends with: </div>\n                    </div>\n            </div>
    # Then next is: </div> (closing w-dyn-items)
    
    # Find the closing </div> tags after this marker
    # Each card ends with: </div>\n                    </div>\n            </div>
    search_from = pos
    # Find "View Profile</a></div>" which marks end of teacher-card-wrapper
    vp_pos = c.find('View Profile</a></div>', search_from)
    if vp_pos != -1:
        # After this, we have closing </div> for card teachers, then </div> for w-dyn-item
        # Let's find the pattern "            </div>\n            </div>"
        # Actually, let's count from vp_pos forward
        after_vp = c[vp_pos:]
        # Find 3rd </div> closing after "View Profile</a></div>"
        # "View Profile</a></div>" closes teacher-card-wrapper
        # Next </div> closes "card teachers"
        # Next </div> closes w-dyn-item
        close1 = after_vp.find('</div>', len('View Profile</a></div>'))
        if close1 != -1:
            close2 = after_vp.find('</div>', close1 + 6)
            if close2 != -1:
                insert_pos = vp_pos + close2 + 6
                # Insert the new members before the grid closing
                c = c[:insert_pos] + new_members + c[insert_pos:]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(c)
                print('OK: Added 3 missing team members (Lero Wang, Ethan Hu, Tiana Wang)')
            else:
                print('FAIL: Could not find second closing div')
        else:
            print('FAIL: Could not find first closing div')
    else:
        print('FAIL: Could not find View Profile after Ruikuan Zhu')
else:
    print('FAIL: Ruikuan Zhu marker not found')
