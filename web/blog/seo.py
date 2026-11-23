"""
Page metadata for search engines and social link previews.

Each view puts a `seo` dict (title, description, url, image, ...) and a list of
`structured_data` (schema.org JSON-LD) objects in its context; seo_meta.html
renders them into Open Graph, Twitter/X card and canonical tags. Open Graph
covers Facebook, LinkedIn, WhatsApp, Slack, Discord, Telegram, Pinterest and
most other platforms; X reads its own twitter:* tags.
"""
from django.conf import settings
from django.templatetags.static import static

NAME = "Victor Ng'eno"
JOB_TITLE = "Software Engineer"
LINKEDIN_URL = "https://www.linkedin.com/in/ngenovictor/"
SITE_DESCRIPTION = (
    "Victor Ng'eno is a Software Engineer and Geomatic Engineer skilled in web, mobile, "
    "GIS, AI integration, data pipelines and DevOps. Based in Nairobi, Kenya."
)
BLOG_DESCRIPTION = (
    "Technical blog by Victor Ng'eno: articles on software development, GIS, Python, "
    "Django, AI integration and more."
)
SHARE_IMAGE = "img/og-image.png"
SHARE_IMAGE_WIDTH = 1200
SHARE_IMAGE_HEIGHT = 630
SHARE_IMAGE_ALT = "Victor Ng'eno: Software Engineer and Geomatic Engineer"


def absolute_url(url):
    """Make a site-relative URL absolute against SITE_URL; leave absolute URLs alone."""
    if not url:
        return ""
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("//"):
        return "https:" + url
    return settings.SITE_URL + ("" if url.startswith("/") else "/") + url


def default_image():
    return {
        "url": absolute_url(static(SHARE_IMAGE)),
        "width": SHARE_IMAGE_WIDTH,
        "height": SHARE_IMAGE_HEIGHT,
        "type": "image/png",
        "alt": SHARE_IMAGE_ALT,
    }


def page_meta(*, title, description, path, og_type="website", image=None, robots="index, follow", **extra):
    return {
        "title": title,
        "description": description,
        "url": absolute_url(path),
        "og_type": og_type,
        "image": image or default_image(),
        "robots": robots,
        **extra,
    }


def person():
    return {
        "@type": "Person",
        "@id": settings.SITE_URL + "/#person",
        "name": NAME,
        "url": settings.SITE_URL + "/",
        "jobTitle": JOB_TITLE,
        "image": absolute_url(static(SHARE_IMAGE)),
        "address": {"@type": "PostalAddress", "addressLocality": "Nairobi", "addressCountry": "KE"},
        "knowsAbout": [
            "Web development", "Mobile development", "GIS", "AI integration",
            "Data pipelines", "DevOps", "Python", "Django", "Flutter", "PostgreSQL", "Docker",
        ],
        "sameAs": [LINKEDIN_URL],
    }


def website():
    return {
        "@type": "WebSite",
        "@id": settings.SITE_URL + "/#website",
        "name": NAME,
        "url": settings.SITE_URL + "/",
        "publisher": {"@id": settings.SITE_URL + "/#person"},
    }


def with_context(*items):
    """Wrap schema.org objects in a single JSON-LD graph."""
    return {"@context": "https://schema.org", "@graph": list(items)}


def post_image(post):
    if post.image:
        return {"url": absolute_url(post.image), "alt": post.title}
    return default_image()


def blog_posting(post):
    url = absolute_url(post.get_absolute_url())
    return {
        "@type": "BlogPosting",
        "@id": url + "#post",
        "headline": post.title,
        "description": post.summary,
        "image": post_image(post)["url"],
        "datePublished": post.date_created.isoformat(),
        "dateModified": post.date_updated.isoformat(),
        "url": url,
        "mainEntityOfPage": url,
        "author": {"@id": settings.SITE_URL + "/#person"},
        "publisher": {"@id": settings.SITE_URL + "/#person"},
    }
