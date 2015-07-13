import bleach
from urlparse import urlparse

def filter_iframe(name, value):
    if name in ('frameborder', 'height', 'width', 'allowfullscreen'):
        return True
    if name == 'src':
        parsed_url = urlparse(value)
        if parsed_url.netloc == 'www.youtube.com' and parsed_url.params == '' and parsed_url.query == '':
            return True
    return False

RICH_ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'br',
    'code',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'i',
    'iframe',
    'img',
    'li',
    'ol',
    'p',
    'pre',
    'span',
    'strike',
    'strong',
    'tbody',
    'table',
    'tr',
    'td',
    'ul',
    'u',
]

RICH_ALLOWED_STYLES = [
    'text-align',
    'font-size',
    'font-family',
    'color',
    'margin-left',
]

RICH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel', 'data-fr-link'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['alt', 'src', 'title'],
    '*': ['style', 'class'],
    'span': ['contenteditable'],
    'iframe': filter_iframe,
    'table': ['width']
}

def clean_rich_html(text):
    clean_html = bleach.clean(text, tags=RICH_ALLOWED_TAGS, attributes=RICH_ALLOWED_ATTRIBUTES,
                              styles=RICH_ALLOWED_STYLES, strip=True, strip_comments=True)

    return clean_html


SIMPLE_ALLOWED_TAGS = [
    'p',
]

SIMPLE_ALLOWED_STYLES = []

SIMPLE_ALLOWED_ATTRIBUTES = {}

def clean_simple_html(text):
    clean_html = bleach.clean(text, tags=SIMPLE_ALLOWED_TAGS, attributes=SIMPLE_ALLOWED_ATTRIBUTES,
                              styles=SIMPLE_ALLOWED_STYLES, strip=True, strip_comments=True)

    return clean_html
