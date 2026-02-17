"""
Comprehensive crawl & diff: local vs production Cloud Classroom site.
Compares every page, section, element, image, link, header, footer, etc.
"""
import urllib.request
import re
import json
from html.parser import HTMLParser
from collections import OrderedDict

LOCAL = "http://127.0.0.1:5000"
PROD  = "https://www.thecloudclassroom.org"

PAGES = [
    ("/", "Home"),
    ("/about-us", "About Us"),
    ("/courses", "Courses"),
    ("/community", "Community"),
    ("/instructors", "Instructors/Volunteers"),
    ("/contact-us", "Contact Us"),
]


def fetch(url):
    """Fetch a URL and return the HTML."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"FETCH_ERROR: {e}"


class HTMLAnalyzer(HTMLParser):
    """Parse HTML and extract structured data for comparison."""

    def __init__(self):
        super().__init__()
        self.sections = []
        self.images = []
        self.links = []
        self.scripts = []
        self.stylesheets = []
        self.headings = []
        self.nav_links = []
        self.footer_links = []
        self.forms = []
        self.iframes = []
        self.meta_tags = []
        self.title = ""
        self.classes_used = set()

        # State tracking
        self._tag_stack = []
        self._in_nav = False
        self._in_footer = False
        self._in_title = False
        self._title_buf = ""
        self._current_text = ""
        self._heading_tag = None
        self._heading_buf = ""
        self._section_classes = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")

        if cls:
            for c in cls.split():
                self.classes_used.add(c)

        self._tag_stack.append(tag)

        if tag == "title":
            self._in_title = True
            self._title_buf = ""

        if tag == "nav" or (tag == "div" and "w-nav-menu" in cls):
            self._in_nav = True

        if tag == "footer":
            self._in_footer = True

        if tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self.images.append({"src": src, "alt": alt, "class": cls})

        if tag == "a":
            href = attrs_dict.get("href", "")
            link_info = {"href": href, "class": cls}
            self.links.append(link_info)
            if self._in_nav:
                self.nav_links.append(link_info)
            if self._in_footer:
                self.footer_links.append(link_info)

        if tag == "script":
            src = attrs_dict.get("src", "")
            if src:
                self.scripts.append(src)

        if tag == "link" and attrs_dict.get("rel") == "stylesheet":
            href = attrs_dict.get("href", "")
            if href:
                self.stylesheets.append(href)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_tag = tag
            self._heading_buf = ""

        if tag == "meta":
            name = attrs_dict.get("name", attrs_dict.get("property", ""))
            content = attrs_dict.get("content", "")
            if name and content:
                self.meta_tags.append({"name": name, "content": content})

        if tag == "form":
            self.forms.append({
                "id": attrs_dict.get("id", ""),
                "action": attrs_dict.get("action", ""),
                "name": attrs_dict.get("name", ""),
            })

        if tag == "iframe":
            self.iframes.append({
                "src": attrs_dict.get("src", ""),
                "class": cls,
            })

        # Track sections
        if tag == "div" and ("section" in cls.split() or "w-section" in cls.split()):
            self._section_classes.append(cls)
            self.sections.append(cls)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = self._title_buf.strip()

        if tag == "nav" or (tag == "div" and self._in_nav):
            # Simplified nav end detection
            pass

        if tag == "footer":
            self._in_footer = False

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and tag == self._heading_tag:
            self.headings.append({"level": tag, "text": self._heading_buf.strip()})
            self._heading_tag = None

        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._in_title:
            self._title_buf += data
        if self._heading_tag:
            self._heading_buf += data


def analyze_html(html_str):
    """Analyze HTML and return structured data."""
    analyzer = HTMLAnalyzer()
    try:
        analyzer.feed(html_str)
    except Exception:
        pass
    return analyzer


def normalize_url(url, is_local=True):
    """Normalize URLs for comparison."""
    if not url:
        return ""
    # Strip common prefixes for comparison
    url = url.strip()
    # Remove trailing slashes
    url = url.rstrip("/")
    # Normalize local paths
    if is_local:
        url = url.replace("http://127.0.0.1:5000", "")
        url = url.replace("/static/images/", "/STATIC/")
        url = url.replace("/static/", "/STATIC_ROOT/")
    else:
        url = url.replace("https://www.thecloudclassroom.org", "")
        url = url.replace("https://cdn.prod.website-files.com/60306606d61c1d030823ec1e/", "/CDN/")
        url = url.replace("https://assets-global.website-files.com/60306606d61c1d030823ec1e/", "/CDN/")
    return url


def compare_pages(local_html, prod_html, page_name):
    """Compare local and production HTML for a single page."""
    diffs = []

    local = analyze_html(local_html)
    prod = analyze_html(prod_html)

    # --- Title ---
    if local.title != prod.title:
        diffs.append({
            "category": "Page Title",
            "severity": "minor",
            "detail": f"Local: '{local.title}' | Prod: '{prod.title}'"
        })

    # --- Navigation Links ---
    local_nav = [l["href"] for l in local.nav_links if l["href"] and l["href"] != "#"]
    prod_nav = [l["href"] for l in prod.nav_links if l["href"] and l["href"] != "#"]
    local_nav_normalized = set(normalize_url(u, True) for u in local_nav)
    prod_nav_normalized = set(normalize_url(u, False) for u in prod_nav)

    nav_only_local = local_nav_normalized - prod_nav_normalized
    nav_only_prod = prod_nav_normalized - local_nav_normalized
    if nav_only_local or nav_only_prod:
        diffs.append({
            "category": "Navigation",
            "severity": "medium",
            "detail": f"Only in local nav: {nav_only_local or 'none'} | Only in prod nav: {nav_only_prod or 'none'}"
        })

    # --- Headings ---
    local_headings = [(h["level"], h["text"]) for h in local.headings if h["text"].strip()]
    prod_headings = [(h["level"], h["text"]) for h in prod.headings if h["text"].strip()]

    # Find headings only in one version
    local_h_texts = set(h[1].strip().lower() for h in local_headings)
    prod_h_texts = set(h[1].strip().lower() for h in prod_headings)

    only_local_h = local_h_texts - prod_h_texts
    only_prod_h = prod_h_texts - local_h_texts

    if only_local_h:
        diffs.append({
            "category": "Headings",
            "severity": "medium",
            "detail": f"Headings only in LOCAL: {only_local_h}"
        })
    if only_prod_h:
        diffs.append({
            "category": "Headings",
            "severity": "medium",
            "detail": f"Headings only in PROD: {only_prod_h}"
        })

    # --- Images ---
    local_imgs = set()
    for img in local.images:
        src = img["src"]
        if src and not src.startswith("data:"):
            # Extract filename
            fname = src.split("/")[-1].split("?")[0]
            local_imgs.add(fname.lower())

    prod_imgs = set()
    for img in prod.images:
        src = img["src"]
        if src and not src.startswith("data:"):
            fname = src.split("/")[-1].split("?")[0]
            prod_imgs.add(fname.lower())

    only_local_imgs = local_imgs - prod_imgs
    only_prod_imgs = prod_imgs - local_imgs
    if only_local_imgs:
        diffs.append({
            "category": "Images",
            "severity": "medium",
            "detail": f"Images only in LOCAL ({len(only_local_imgs)}): {sorted(only_local_imgs)[:10]}"
        })
    if only_prod_imgs:
        diffs.append({
            "category": "Images",
            "severity": "medium",
            "detail": f"Images only in PROD ({len(only_prod_imgs)}): {sorted(only_prod_imgs)[:10]}"
        })

    # Image count
    if abs(len(local.images) - len(prod.images)) > 2:
        diffs.append({
            "category": "Images",
            "severity": "info",
            "detail": f"Image count: Local={len(local.images)}, Prod={len(prod.images)}"
        })

    # --- CSS Classes ---
    # Check for important structural classes in prod that are missing locally
    important_classes = {
        "founder-card", "founder", "image-3", "image-5", "text-block",
        "columns", "w-row", "w-col", "w-col-4", "section", "cta",
        "teacher-card", "card", "meet-our-teachers-grid"
    }
    prod_important = important_classes & prod.classes_used
    local_important = important_classes & local.classes_used
    missing_classes = prod_important - local_important
    extra_classes = local_important - prod_important
    if missing_classes:
        diffs.append({
            "category": "CSS Classes",
            "severity": "medium",
            "detail": f"Prod classes missing in local: {missing_classes}"
        })
    if extra_classes:
        diffs.append({
            "category": "CSS Classes",
            "severity": "info",
            "detail": f"Local classes not in prod: {extra_classes}"
        })

    # --- Sections ---
    if local.sections != prod.sections:
        only_l = [s for s in local.sections if s not in prod.sections]
        only_p = [s for s in prod.sections if s not in local.sections]
        if only_l or only_p:
            diffs.append({
                "category": "Sections",
                "severity": "medium",
                "detail": f"Section classes only in local: {only_l[:5]} | only in prod: {only_p[:5]}"
            })

    # --- Footer Links ---
    local_footer = set(l["href"] for l in local.footer_links if l["href"] and l["href"] != "#")
    prod_footer = set(l["href"] for l in prod.footer_links if l["href"] and l["href"] != "#")
    if local_footer != prod_footer:
        only_lf = local_footer - prod_footer
        only_pf = prod_footer - local_footer
        if only_lf or only_pf:
            diffs.append({
                "category": "Footer",
                "severity": "minor",
                "detail": f"Footer links only in local: {only_lf or 'none'} | only in prod: {only_pf or 'none'}"
            })

    # --- Iframes ---
    if len(local.iframes) != len(prod.iframes):
        diffs.append({
            "category": "Iframes/Embeds",
            "severity": "medium",
            "detail": f"Iframe count: Local={len(local.iframes)}, Prod={len(prod.iframes)}"
        })

    # --- Forms ---
    local_forms = set(f["id"] or f["name"] for f in local.forms)
    prod_forms = set(f["id"] or f["name"] for f in prod.forms)
    if local_forms != prod_forms:
        diffs.append({
            "category": "Forms",
            "severity": "minor",
            "detail": f"Local forms: {local_forms}, Prod forms: {prod_forms}"
        })

    # --- Stylesheets ---
    if len(local.stylesheets) != len(prod.stylesheets):
        diffs.append({
            "category": "Stylesheets",
            "severity": "info",
            "detail": f"Stylesheet count: Local={len(local.stylesheets)}, Prod={len(prod.stylesheets)}"
        })

    # --- Scripts ---
    if abs(len(local.scripts) - len(prod.scripts)) > 1:
        diffs.append({
            "category": "Scripts",
            "severity": "info",
            "detail": f"Script count: Local={len(local.scripts)}, Prod={len(prod.scripts)}"
        })

    return diffs


def deep_content_compare(local_html, prod_html, page_name):
    """Do deeper text-level comparison for key content blocks."""
    diffs = []

    # Extract visible text blocks (simplified)
    def extract_text_blocks(html):
        # Remove script/style content
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', clean)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    local_text = extract_text_blocks(local_html)
    prod_text = extract_text_blocks(prod_html)

    # Check for specific production content missing locally
    # Extract unique phrases from production (5+ word phrases)
    prod_sentences = set()
    for match in re.finditer(r'[A-Z][^.!?]*[.!?]', prod_text):
        sentence = match.group().strip()
        if len(sentence.split()) >= 5:
            prod_sentences.add(sentence[:100])

    local_lower = local_text.lower()
    missing_content = []
    for sentence in sorted(prod_sentences):
        # Check if first 30 chars of sentence exist in local
        snippet = sentence[:30].lower()
        if snippet not in local_lower and len(snippet) > 15:
            missing_content.append(sentence[:80])

    if missing_content:
        diffs.append({
            "category": "Content",
            "severity": "medium",
            "detail": f"Prod text not found locally ({len(missing_content)} snippets): {missing_content[:5]}"
        })

    # Check for specific structural elements
    # Detect map/widget elements
    prod_has_map = 'TCC%20Map' in prod_html or 'TCC Map' in prod_html
    local_has_map = 'TCC%20Map' in local_html or 'TCC Map' in local_html
    if prod_has_map and not local_has_map:
        diffs.append({
            "category": "Map Widget",
            "severity": "high",
            "detail": "Production has TCC Map image but local does not"
        })

    # Check for QR codes in instructor cards
    if page_name == "Instructors/Volunteers":
        prod_qr = prod_html.count('qrcode')
        local_qr = local_html.count('qrcode')
        if prod_qr != local_qr:
            diffs.append({
                "category": "QR Codes",
                "severity": "medium",
                "detail": f"QR code references: Local={local_qr}, Prod={prod_qr}"
            })

    # Check YouTube embeds
    prod_yt = len(re.findall(r'youtube\.com/embed', prod_html))
    local_yt = len(re.findall(r'youtube\.com/embed', local_html))
    if prod_yt != local_yt:
        diffs.append({
            "category": "YouTube Embeds",
            "severity": "medium",
            "detail": f"YouTube embeds: Local={local_yt}, Prod={prod_yt}"
        })

    # Check Common Ninja or other third-party widgets
    for widget in ['commonninja', 'common-ninja', 'commoninja']:
        prod_w = widget.lower() in prod_html.lower()
        local_w = widget.lower() in local_html.lower()
        if prod_w and not local_w:
            diffs.append({
                "category": "Third-party Widgets",
                "severity": "medium",
                "detail": f"Production uses '{widget}' widget not found in local"
            })

    # Check for Snipcart / e-commerce
    prod_snipcart = 'snipcart' in prod_html.lower()
    local_snipcart = 'snipcart' in local_html.lower()
    if prod_snipcart != local_snipcart:
        diffs.append({
            "category": "E-commerce",
            "severity": "info",
            "detail": f"Snipcart: Local={'yes' if local_snipcart else 'no'}, Prod={'yes' if prod_snipcart else 'no'}"
        })

    return diffs


def specific_element_checks(local_html, prod_html, page_name):
    """Check for specific elements per page."""
    diffs = []

    if page_name == "Home":
        # Check hero section, stats, courses grid, testimonial
        for keyword in ['1,300+', '20+', '300+', '30+']:
            if keyword in prod_html and keyword not in local_html:
                diffs.append({"category": "Stats", "severity": "medium",
                              "detail": f"Stat '{keyword}' in prod but not in local"})

    if page_name == "About Us":
        # Check team members
        team_names = ['Elizabeth Zhao', 'Jessie Chen', 'Lero Wang', 'Ethan Hu',
                      'Tiana Wang', 'Jonathan Wang', 'Rena Wang', 'Omar Wahby', 'Ruikuan Zhu']
        for name in team_names:
            in_local = name in local_html
            in_prod = name in prod_html
            if in_prod and not in_local:
                diffs.append({"category": "Team Members", "severity": "high",
                              "detail": f"'{name}' missing from local"})

        # Check founder-card structure
        prod_founder_cards = prod_html.count('founder-card')
        local_founder_cards = local_html.count('founder-card')
        if prod_founder_cards != local_founder_cards:
            diffs.append({"category": "Team Structure", "severity": "medium",
                          "detail": f"founder-card count: Local={local_founder_cards}, Prod={prod_founder_cards}"})

        # Check for CDN images vs local placeholders
        local_facetune = local_html.count('Facetune_11-09-2020-22-32-35-2.JPG')
        if local_facetune > 0:
            diffs.append({"category": "Team Images", "severity": "high",
                          "detail": f"Local still uses placeholder Facetune image {local_facetune} times"})

        # Check Our Story button
        if 'OUR STORY' in prod_html:
            if 'OUR STORY' not in local_html:
                diffs.append({"category": "Buttons", "severity": "medium",
                              "detail": "Prod has 'OUR STORY' button, local doesn't"})

    if page_name == "Community":
        # Check for events, YouTube, testimonials
        if 'HackPNW' in prod_html and 'HackPNW' not in local_html:
            diffs.append({"category": "Events", "severity": "medium",
                          "detail": "Prod has HackPNW event, local doesn't"})

    if page_name == "Instructors/Volunteers":
        # Count instructor cards
        prod_cards = prod_html.count('teacher-card w-dyn-item')
        local_cards = local_html.count('teacher-card w-dyn-item')
        if prod_cards != local_cards:
            diffs.append({"category": "Instructor Cards", "severity": "medium",
                          "detail": f"Card count: Local={local_cards}, Prod={prod_cards}"})

        # Check for "Become a volunteer" CTA
        prod_cta = 'Become a volunteer' in prod_html or 'Get In Touch' in prod_html
        local_cta = 'Become a volunteer' in local_html or 'Get In Touch' in local_html
        if prod_cta and not local_cta:
            diffs.append({"category": "CTA", "severity": "medium",
                          "detail": "Prod has 'Become a volunteer' CTA, local doesn't"})

    if page_name == "Contact Us":
        # Check for map iframe or contact form
        prod_form = 'contact' in prod_html.lower() and 'form' in prod_html.lower()
        local_form = 'contact' in local_html.lower() and 'form' in local_html.lower()
        if prod_form and not local_form:
            diffs.append({"category": "Contact Form", "severity": "medium",
                          "detail": "Prod has contact form, local doesn't"})

    return diffs


def generate_report(all_results):
    """Generate a comprehensive markdown report."""
    lines = []
    lines.append("=" * 80)
    lines.append("COMPREHENSIVE SITE COMPARISON REPORT")
    lines.append(f"Local: {LOCAL}  |  Production: {PROD}")
    lines.append("=" * 80)

    total_diffs = 0
    high_count = 0
    medium_count = 0
    minor_count = 0
    info_count = 0

    for page_path, page_name, diffs in all_results:
        lines.append(f"\n{'─' * 80}")
        lines.append(f"PAGE: {page_name} ({page_path})")
        lines.append(f"{'─' * 80}")

        if not diffs:
            lines.append("  ✓ No differences found")
            continue

        # Group by category
        by_category = OrderedDict()
        for d in diffs:
            cat = d["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(d)

        for cat, items in by_category.items():
            lines.append(f"\n  [{cat}]")
            for item in items:
                sev = item["severity"].upper()
                icon = {"HIGH": "🔴", "MEDIUM": "🟡", "MINOR": "🔵", "INFO": "⚪"}.get(sev, "⚪")
                lines.append(f"    {icon} [{sev}] {item['detail']}")
                total_diffs += 1
                if sev == "HIGH": high_count += 1
                elif sev == "MEDIUM": medium_count += 1
                elif sev == "MINOR": minor_count += 1
                else: info_count += 1

    lines.append(f"\n{'=' * 80}")
    lines.append("SUMMARY")
    lines.append(f"{'=' * 80}")
    lines.append(f"Total differences found: {total_diffs}")
    lines.append(f"  🔴 HIGH:   {high_count}")
    lines.append(f"  🟡 MEDIUM: {medium_count}")
    lines.append(f"  🔵 MINOR:  {minor_count}")
    lines.append(f"  ⚪ INFO:   {info_count}")
    lines.append(f"{'=' * 80}")

    return "\n".join(lines)


def main():
    all_results = []

    for path, name in PAGES:
        print(f"Crawling {name} ({path})...")
        local_url = LOCAL + path
        prod_url = PROD + path

        local_html = fetch(local_url)
        prod_html = fetch(prod_url)

        if local_html.startswith("FETCH_ERROR"):
            print(f"  ERROR fetching local: {local_html}")
            all_results.append((path, name, [{"category": "Fetch", "severity": "high", "detail": f"Could not fetch local: {local_html}"}]))
            continue

        if prod_html.startswith("FETCH_ERROR"):
            print(f"  ERROR fetching prod: {prod_html}")
            all_results.append((path, name, [{"category": "Fetch", "severity": "high", "detail": f"Could not fetch prod: {prod_html}"}]))
            continue

        print(f"  Local: {len(local_html)} chars, Prod: {len(prod_html)} chars")

        diffs = []
        diffs.extend(compare_pages(local_html, prod_html, name))
        diffs.extend(deep_content_compare(local_html, prod_html, name))
        diffs.extend(specific_element_checks(local_html, prod_html, name))

        print(f"  Found {len(diffs)} differences")
        all_results.append((path, name, diffs))

    report = generate_report(all_results)
    print("\n" + report)

    # Also save to file
    with open("site_comparison_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to site_comparison_report.txt")


if __name__ == "__main__":
    main()
