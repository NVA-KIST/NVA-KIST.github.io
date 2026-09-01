#!/usr/bin/env python3
"""Sync the shared header/footer into every page.

The header and footer live once in _chrome/. This script renders them per page
(About link target, active nav item) and writes the result between marker
comments in each HTML file. Pages stay plain static HTML - nothing is rendered
at request time, so search engines still see the full navigation.

    python sync-chrome.py            # show what would change
    python sync-chrome.py --apply    # write it

The first run inserts the markers around the existing blocks.
"""
import io, os, re, sys

APPLY = '--apply' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

H_OPEN, H_CLOSE = '<!-- @chrome:header -->', '<!-- /@chrome:header -->'
F_OPEN, F_CLOSE = '<!-- @chrome:footer -->', '<!-- /@chrome:footer -->'

# page -> (About link target, href of the nav item to mark active)
PAGES = {
    'index.html':           ('#about',              '#about'),
    'Home.dc.html':         ('#about',              '#about'),
    'Members.dc.html':      ('Home.dc.html#about',  'Members.dc.html'),
    'Publications.dc.html': ('Home.dc.html#about',  'Publications.dc.html'),
    'Research.dc.html':     ('Home.dc.html#about',  'Research.dc.html'),
    'Board.dc.html':        ('Home.dc.html#about',  'Board.dc.html'),
    'Contact.dc.html':      ('Home.dc.html#about',  'Contact.dc.html'),
}

header_tpl = io.open('_chrome/header.html', encoding='utf-8').read().rstrip('\n')
footer_tpl = io.open('_chrome/footer.html', encoding='utf-8').read().rstrip('\n')


def render_header(about_href, active_href):
    s = header_tpl.replace('__ABOUT__', about_href)
    # Mark exactly one top-level nav link as current.
    needle = '<a href="%s">' % active_href
    if needle not in s:
        raise SystemExit('sync-chrome: no nav link with href %r' % active_href)
    s = s.replace(needle, '<a href="%s" class="nav-active" aria-current="page">'
                  % active_href, 1)
    return s


def find_div(s, start_marker):
    """(start, end) of the div opened at start_marker, including its close."""
    i = s.index(start_marker)
    depth, j = 0, i
    tag = re.compile(r'<div\b|</div>')
    while True:
        m = tag.search(s, j)
        if m is None:
            raise SystemExit('sync-chrome: unbalanced div at ' + start_marker)
        depth += -1 if m.group(0) == '</div>' else 1
        if depth == 0:
            return i, m.end()
        j = m.end()


def splice(s, body, open_tag, close_tag, bootstrap_span):
    """Replace an existing marked region, or wrap the raw block on first run."""
    if open_tag in s:
        a = s.index(open_tag) + len(open_tag)
        b = s.index(close_tag)
        return s[:a] + '\n    ' + body + '\n    ' + s[b:]
    a, b = bootstrap_span
    return (s[:a] + open_tag + '\n    ' + body + '\n    ' + close_tag + s[b:])


changed, boot = [], []
for page in sorted(PAGES):
    if not os.path.exists(page):
        continue
    about, active = PAGES[page]
    s0 = io.open(page, encoding='utf-8').read()
    s = s0

    header = render_header(about, active)
    if H_OPEN in s:
        span = None
    else:
        a, _ = find_div(s, '<div class="site-header-bar">')
        _, b = find_div(s, '<div class="site-header-rule">')
        span = (a, b)
        boot.append(page)
    s = splice(s, header, H_OPEN, H_CLOSE, span)

    footer = footer_tpl
    span = None if F_OPEN in s else find_div(s, '<div class="site-footer">')
    s = splice(s, footer, F_OPEN, F_CLOSE, span)

    if s != s0:
        changed.append(page)
        if APPLY:
            io.open(page, 'w', encoding='utf-8', newline='\n').write(s)

for p in changed:
    print('  %-24s synced%s' % (p, '  (markers inserted)' if p in boot else ''))
print('%d page(s) %s' % (len(changed), 'written' if APPLY else 'would change'))
if not APPLY:
    print('re-run with --apply to write')
