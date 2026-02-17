"""Fix community.html to match production:
1. Uncomment "Upcoming events" section with HackPNW event
2. Change hero heading to "Upcoming events" instead of "Cloud Classroom Through The Lens"
3. Remove "School Ambassadors" section (not on production)
4. Remove "Students Geo Distribution" section (not on production)
5. Add "Community through the lens" photo section
6. Update "Browse Class Recordings" with YouTube links instead of local videos
7. Change "What students say" to "What families say" with real testimonial
8. Fix newsletter section text
"""
import re

filepath = "templates/community.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# The community page needs a major rewrite of the body content.
# Let's find the main content area and replace it.

# Find the start of the main content after the nav
# The content starts after the header closing div
header_end = content.find('<div class="section community">')
if header_end < 0:
    print("ERROR: couldn't find section community start")
    exit(1)

# Find the footer
footer_start = content.find('<footer data-w-id="5d3def44-2af0-a39e-d268-cb5e4a46cda3"')
if footer_start < 0:
    print("ERROR: couldn't find footer")
    exit(1)

# New body content matching production structure
new_body = '''<div class="section community">
            <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8759" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                class="container-medium-727px text-center w-container">
                <h1 class="special-2">Upcoming <span class="font-color-primary">events</span>.</h1>
                <p class="paragraph events">Explore and sign up for Cloud Classroom sponsored events.</p>
            </div>
            <div class="container-default-1209px w-container">
                <div class="w-dyn-list">
                    <div role="list" class="events-grid w-dyn-items">
                        <div data-w-id="55cd279d-65f1-1f8d-20fe-77100a429ba9" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                            role="listitem" class="w-dyn-item">
                            <div class="card events">
                                <a href="#" class="card-image-link events w-inline-block"><img src="https://cdn.prod.website-files.com/60306606d61c1dfb1923ec1f/63d4f119a9e7e71ee259ba2c_HackPNW%20(1).png" alt="HackPNW" class="image card-events"></a>
                                <div class="card-content events">
                                    <a href="#" class="card-title-link w-inline-block">
                                        <h3 class="title card-event">HackPNW</h3>
                                    </a>
                                    <p>HackPNW is a two day highschool hackathon @Microsoft Reactor, Redmond Washington. We encourage highschool students from around the Pacific Northwest to come and compete for fortune and glory! There will be code, There will be prizes, and most of all there will be lots of fun! Best of all it&#x27;s entirely free (including food)!</p>
                                    <div class="divider card-events"></div>
                                    <div class="card-event-details-wrapper">
                                        <div class="event-date-wrapper">
                                            <div class="event-date"><img src="/static/images/icon-event-01-academy-template.svg" alt="" class="event-icon">
                                                <div class="event-details-text">February 4, 2023</div>
                                            </div>
                                            <div class="event-time"><img src="/static/images/icon-event-02-academy-template.svg" alt="" class="event-icon">
                                                <div class="event-details-text">9:00 am</div>
                                            </div>
                                        </div>
                                        <div class="event-location-wrapper"><img src="/static/images/icon-event-03-academy-template.svg" alt="" class="event-icon location">
                                            <div class="event-location-text">Microsoft Reactor, Redmond Washington.</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section community">
            <div data-w-id="2d20106d-2a09-044a-b62e-a1e40a8cd635" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                class="container-medium-727px text-center w-container">
                <h2>Community through the lens</h2>
                <p class="paragraph events">Meet students and teachers from Cloud Classroom instructors.</p>
            </div>
        </div>
        <div class="section community">
            <div class="container">
                <div data-w-id="78e47083-7b8b-2ed1-0906-7e1b7e06f4b2" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                    class="container-medium-727px text-center w-container">
                    <h1 class="special-2">Browse Class <span class="text-span">Recordings</span>.</h1>
                    <p class="paragraph events">View clip recordings of past classes taught by Cloud Classroom instructors.</p>
                </div>
                <div class="container-default-1209px w-container"></div>
                <div>
                    <div class="class-columns w-row ys">
                        <div class="w-col w-col-4">
                            <div class="w-embed-youtubevideo youtube-class" style="padding-bottom: 56.25%; position: relative; width: 100%;">
                                <iframe src="https://www.youtube.com/embed/videoseries?list=UUSZOOzOIdGPin_9jkMeqy1Q" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" allow="autoplay; encrypted-media" allowfullscreen="" frameborder="0"></iframe>
                            </div>
                        </div>
                        <div class="w-col w-col-4">
                            <div class="w-embed-youtubevideo youtube-class" style="padding-bottom: 56.25%; position: relative; width: 100%;">
                                <iframe src="https://www.youtube.com/embed/videoseries?list=UUSZOOzOIdGPin_9jkMeqy1Q" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" allow="autoplay; encrypted-media" allowfullscreen="" frameborder="0"></iframe>
                            </div>
                        </div>
                        <div class="w-col w-col-4">
                            <div class="w-embed-youtubevideo youtube-class" style="padding-bottom: 56.25%; position: relative; width: 100%;">
                                <iframe src="https://www.youtube.com/embed/videoseries?list=UUSZOOzOIdGPin_9jkMeqy1Q" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" allow="autoplay; encrypted-media" allowfullscreen="" frameborder="0"></iframe>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="div-block-4"><a href="https://www.youtube.com/channel/UCSZOOzOIdGPin_9jkMeqy1Q/featured" target="_blank" class="button-primary community-buttons small-mobile w-button">VIEW ALL ON YOUTUBE</a></div>
                <div class="card"></div>
            </div>
        </div>
        <div class="section community">
            <div data-w-id="3867e0ad-8a50-b1da-d0cc-7046e6faf820" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                class="container-medium-727px text-center w-container">
                <h1 class="special-2">What <span class="font-color-primary">families </span>say.</h1>
                <p class="paragraph events">Read student and parent testimonials here.<br>Have a story to tell? <a href="#">Share it with us!</a></p>
            </div>
            <div class="container-default-1209px w-container"></div>
            <div data-animation="slide" data-duration="500" data-infinite="1" class="slider-2 w-slider">
                <div class="mask w-slider-mask">
                    <div class="slide-3 w-slide">
                        <div class="testimonial-quote-block">
                            <blockquote class="block-quote-2">My daughter absolutely loves the courses we&#x27;ve taken! Her instructors are a great encouragement and the academic program is great.</blockquote>
                            <div class="testimonial-quote-student">- Millie M, parent</div>
                        </div>
                    </div>
                </div>
                <div class="w-slider-arrow-left">
                    <div class="icon w-icon-slider-left"></div>
                </div>
                <div class="w-slider-arrow-right">
                    <div class="w-icon-slider-right"></div>
                </div>
                <div class="slide-nav-2 w-slider-nav w-round"></div>
            </div>
        </div>
                <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8768" style="-webkit-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 48PX, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
            class="section newsletter-events">
            <div class="container-default-1209px w-container">
                <div class="newsletter-events-wrapper">
                    <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd876b" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        class="split-content newsletter-events-left">
                        <h2 class="title newsletter-events">Never miss another event!</h2>
                        <p class="paragraph newsletter-events">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Odio quisque integer elementum egestas aliquet tincidunt.</p>
                    </div>
                    <div data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8770" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        class="split-content newsletter-events-right">
                        <div class="form-block newsletter w-form">
                            <form id="wf-form-Event-Newsletter" name="wf-form-Event-Newsletter" data-name="Event Newsletter" class="form-newsletter"><input type="email" class="input newsletter-events w-input" maxlength="256" name="Email" data-name="Email" placeholder="Enter your email" id="Email" required=""><input type="submit" value="Subscribe" data-wait="Please wait..."
                                    class="button-secondary cta newsletter w-button"></form>
                            <div class="success-message newsletter w-form-done">
                                <div>Thank you! You are now subscribed!</div>
                            </div>
                            <div class="error-message w-form-fail">
                                <div>Sorry, something went wrong!</div>
                            </div>
                        </div>
                        <div class="newsletter-events-text">We&#x27;ll never send you spam.</div>
                    </div><img src="/static/images/circle-shape-newsletter-events-04-academy-template.svg" data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd877d" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        alt="" class="circle-shape-newsletter-events _4"><img src="/static/images/circle-shape-newsletter-events-03-academy-template.svg" data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd877e" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        alt="" class="circle-shape-newsletter-events _3"><img src="/static/images/circle-shape-newsletter-events-02-academy-template.svg" data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd877f" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        alt="" class="circle-shape-newsletter-events _2"><img src="/static/images/circle-shape-newsletter-events-01-academy-template.svg" data-w-id="a64e4142-528b-f7eb-06ea-9629c3dd8780" style="-webkit-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(0.97, 0.97, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);opacity:0"
                        alt="" class="circle-shape-newsletter-events _1"></div>
            </div>
        </div>
        '''

content = content[:header_end] + new_body + content[footer_start:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("community.html fixed successfully!")
print("- Added 'Upcoming events' section with HackPNW event card")
print("- Added 'Community through the lens' section")
print("- Replaced local videos with 'Browse Class Recordings' YouTube embeds")
print("- Changed 'What students say' to 'What families say' with real testimonial (Millie M)")
print("- Removed 'School Ambassadors' section")
print("- Removed 'Students Geo Distribution' section")
print("- Updated 'VIEW ALL ON YOUTUBE' link to actual YouTube channel")
print("- Kept 'Never miss another event!' newsletter section")
