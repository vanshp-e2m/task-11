"""Semantic HTML for the About Us page (Figma 1:161), used as DevConnect's `dev/convert-html` input (the DevConnect draft).
Copy is verbatim from the Figma file (pages/_figma/file.json). Image URLs = the WP media uploaded via DevConnect (wp-media.json).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = {k: v["url"] for k, v in json.load(open(os.path.join(ROOT, "pages/about-us/figma/images/wp-media.json"))).items()}
M["about-hero-portrait"] = "http://task-11.local/wp-content/uploads/2026/09/about-hero-portrait.jpg"

TEAM = [("yamamura", "Dean Yamamura", "President and COO"), ("delaney", "William Delaney", "Vice-President – Sales"),
        ("todd", "Bob Todd", "Regional Business Manager – Central"), ("mccart", "Chris McCart", "Regional Business Manager – West"),
        ("wilson", "Chris Wilson", "Regional Business Manager – South"), ("kritt", "Steve Kritt", "Regional Business Manager – Northeast"),
        ("hanson", "Russ Hanson", "Business Development Manager"), ("rivera", "Odriel Rivera", "Manager of Neuro Latin America Sales")]
YEARS = ["1919", "1939", "1959", "1968", "1976", "1993", "2002", "2007", "2008", "2010", "2019", "2020", "2022", "2025"]
COLLABS = [
    ("lawton", "Michael T. Lawton, MD", "President and CEO,<br>Barrow Neurological Institute<br>Professor and Chair, Neurosurgery<br>Chief, Neurovascular Surgery",
     "LawtonElite Series, an intricately crafted, comprehensive micro instrumentation series for neurovascular and skull base procedures"),
    ("evans", "James J. Evans, MD", "Professor, Neurological Surgery &amp; Otolaryngology<br>Division Chief, Brain Tumor and Stereotactic Radiosurgery Division<br>Director, Cranial Base and Pituitary Surgery<br>Director, Cranial Base and Endoscopic Surgery Fellowship",
     "E3 Evans Elite Endoscopic Instruments, designed as a comprehensive set for endoscopic and minimally invasive procedures, featuring malleable instruments and suctions to provide versatility; and E3 Mithras Bipolar—instrumentation for minimally invasive endonasal surgery"),
    ("youssef", "A. Samy Youssef, MD, PhD", "Professor &amp; Vice Chairman for Education<br>Departments of Neurosurgery &amp; Otolaryngology<br>Director of Skull Base Surgery<br>University of Colorado School of Medicine",
     "Dr. Youssef’s Cranial Nerve Dissection Set, a comprehensive, high-quality, specialized set for nerve dissection"),
]

team_html = "".join(f'<figure><img src="{M["team-" + k]}" alt="{n}"><figcaption><strong>{n}</strong><br>{r}</figcaption></figure>' for k, n, r in TEAM)
collab_html = "".join(f'<article><img src="{M["about-collab-" + k]}" alt="{n}"><h3>{n}</h3><p>{role}</p><p><strong>Collaboration:</strong><br>{c}</p></article>' for k, n, role, c in COLLABS)
years_html = "".join(f"<li>{y}</li>" for y in YEARS)

HTML = f"""<section id="about-hero"><h1>About us</h1>
<img src="{M['about-hero-PLACEHOLDER']}" alt="Surgeons in an operating room"><img src="{M['about-hero-portrait']}" alt="Erol Veznedaroglu, MD">
<blockquote><p>“About a decade ago I designed a clip and worked in conjunction with Mizuho because I saw a need for my practice.”</p>
<p>Erol Veznedaroglu, MD, FACS, FAANS, FAHA<br>President and CEO, Global Neuroscience Institute<br>Professor, Robert A. Groff Chair, Department of Neurosurgery<br>Drexel University College of Medicine</p></blockquote></section>
<section id="about-intro"><h2>Advanced Neurosurgical tools. Enhanced customer care.</h2>
<p>That’s why so many neurosurgeons choose Mizuho America. We’ve built our reputation on high-quality, handcrafted products with patented features backed by exceptional support. We’ve accomplished this through:</p>
<ul><li>Collaborations with neurosurgical experts to help fill unmet instrumentation needs in the neurosurgery OR</li><li>High-performance tools that meet rigorous quality protocols—with no generic designs or mass-production assembly lines</li><li>A personalized, dedicated partnership with our customers before, during, and after the sale</li></ul>
<div><h3>1993</h3><p>Mizuho America, Inc. established in Boston, MA (relocated to Union City, CA, in 2010)</p></div>
<div><h3>1,800+</h3><p>neurosurgical products, including head-holding systems, instruments, microsurgery tables, and vascular management</p></div>
<div><h3>ISO 13485</h3><p>for patient safety, regulatory compliance, traceability &amp; documentation, risk management, and supplier control</p></div>
<div><h3>1,000+</h3><p>hospitals served</p></div>
<p>We’re a global leader in neurosurgery tools, and we’ll continue to maintain the high standards that have earned us the trust of the neurosurgical community. Because we share your same goal: achieving the best outcomes for patients.</p>
<a href="#clinical-collaborators">Hear from our clinical collaborators</a></section>
<section id="about-mission"><h2>Our mission</h2>
<p><em>“Collaborate with surgeons to provide high-quality neurosurgical devices in order to help advance surgical techniques to benefit patient health</em>.”</p>
<p>Message from <strong>Hiroshi Nemoto</strong>, Representative Director President &amp; CEO, Mizuho Global Headquarters</p>
<h3>Our corporate creed</h3><ul><li><img src="{M['creed-honesty']}" alt="">Honesty</li><li><img src="{M['creed-contribution']}" alt="">Contribution</li><li><img src="{M['creed-solidarity']}" alt="">Solidarity</li></ul>
<h3>Our guiding principles</h3><ul><li><img src="{M['principle-customer']}" alt="">Customer-focused</li><li><img src="{M['principle-innovative']}" alt="">Innovative</li><li><img src="{M['principle-professional']}" alt="">Professional</li></ul>
<h2>Mizuho-America sales team—putting our core values into action</h2>{team_html}</section>
<section id="about-heritage"><h2>A heritage of excellence</h2>
<p>Founded more than 100 years ago, Mizuho Corporation—Mizuho America’s parent company—has grown into a respected global powerhouse because of its unceasing commitment to provide dependable, sophisticated, and time-tested technology for healthcare professionals.</p>
<p>Established in 1993, Mizuho America reflects that commitment, becoming a trusted leader in neurosurgery devices that you can rely on to help deliver the performance you need for your high-stakes procedures. Our expert-driven solutions were designed to overcome barriers and facilitate a high level of surgical precision, helping to give you greater freedom and power to evolve surgical techniques for optimal outcomes.</p>
<a href="#products">Explore our advanced neurosurgical products</a>
<h2>100+ years of making a difference</h2><p>Milestones that paved the way for Mizuho America today</p>
<p>Mizuho Corporation</p><p>Mizuho America</p><ul>{years_html}</ul>
<p>Mizuho America, Inc. is established in Boston, Massachusetts, as a sales company for neurosurgical products</p>
<p>Our past</p><p>Our future</p><a href="#procedures">Browse the many neurosurgical procedures we support</a></section>
<section id="about-collaborations"><h2>Collaborations that have helped advance instrumentation</h2>
<p>No one knows the unique demands of neurosurgery better than neurosurgeons. That’s why we’ve partnered with renowned leaders in the field to design and develop handcrafted, expertly engineered tools specially tailored to support control, efficiency, and workflow during your exacting procedures.</p>
<p><strong>It all started in 1976 with Dr. Kenichiro Sugita</strong><br>That’s when this acclaimed neurosurgeon worked with Mizuho Corporation to develop the famous Sugita Clip for cerebral aneurysm. This breakthrough product went on to become a gold standard and continues to be used in countless ORs worldwide.</p>
<p>Dr. Sugita continued partnering with Mizuho Corporation, and today Mizuho America proudly offers a full line of Sugita products.</p>
<figure><img src="{M['about-sugita']}" alt="Dr. Kenichiro Sugita"><figcaption>Dr. Kenichiro Sugita</figcaption></figure>
<h2>Mizuho America’s expert collaborators include:</h2>{collab_html}<a href="#request-a-demo">Request a product demo</a></section>
<section id="about-global"><img src="{M['about-map']}" alt="Mizuho locations worldwide">
<h2>We’re proud to be an agile, forward thinking company in a trailblazing global organization</h2><p>Mizuho Corporation, founded and headquartered in Japan, has a worldwide presence</p>
<div><h3>15+</h3><p>sales dealers in the United States</p></div><div><h3>15+</h3><p>distributors in Latin America</p></div><div><h3>65+</h3><p>distributors in Europe, the Middle East, and Africa</p></div><div><h3>35+</h3><p>distributors in Asia-Pacific</p></div></section>
<section id="about-closing"><blockquote><p>“Better instruments help you get the best patient outcome. And that’s really the name of the game is to try and find things, tools, that make you a better surgeon.”</p><p>– Michael Lawton, MD</p></blockquote>
<a href="#products">Discover our wide range of products</a><a href="#video-testimonials">Watch video testimonials</a><a href="#product-brochures">Download product brochures</a></section>"""

out = os.path.join(ROOT, "pages/about-us/html/about.html")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(HTML)
print(len(HTML), "chars ->", out)
