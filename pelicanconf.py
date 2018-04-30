#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Steve Theodore'
SITENAME = u'Chimeras & Manticores'
SITESUBTITLE = 'a blog about technical art, python, the games business, and obscurantism'
SITEURL = 'https://theodox.github.io'
COPYRIGHT_YEAR = 2018

PATH = 'content'

TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'
ROBOTS = 'index, follow'


PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'sitemap', 'summary', 'tag_cloud', 'representative_image']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = None  # 'atom/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
FEED_ALL_RSS = 'feeds/rss.xml'
ADD_THIS_ID = 'ra-575daf41c4afb207'
SLUGIFIY_SOURCE = 'basename'

ARTICLE_URL = '{date:%Y}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

STATIC_PATHS = ['pages/course', 'pages/cookbook', 'pages/publications', 'images', 'extra', 'tipue-search']
ARTICLE_EXCLUDES = ['extra']


MAIN_MENU = True
SINGLE_AUTHOR = True
DISQUS_SITENAME = 'theodoxcom'

SUMMARY_END_MARKER = "<!---jump--->"

#SHOW_FULL_ARTICLE = True
SHOW_SITESUBTITLE_IN_HTML = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [
    ('About...', '/about'),
    ('Publications', '/pages/pub'),
    ('Cookbook', '/pages/cookbook'),
    ('By date', '/archives'),
    ('By subject', '/tags')
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Blogroll
LINKS = [   ]



# tag cload
TAG_CLOUD_STEPS = 4  # tag step 4 is suppressed in the style sheet
TAG_CLOUD_SORTING = 'alphabetically'
TAG_CLOUD_BADGE = True

# Social widget
SOCIAL = [
    ('linkedin', 'https://www.linkedin.com/in/stevetheodore'),
    ('github', 'https://github.com/theodox'),
    ('google', 'https://plus.google.com/u/0/+SteveTheodore480BC/posts'),
    ('stack-overflow', 'http://stackoverflow.com/users/1936075/theodox'),
]

DEFAULT_PAGINATION = 8
DEFAULT_HEADER_IMAGE = 'http://texturetaddka.com/wp-content/uploads/2011/09/DSC862.jpg'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
COLOR_SCHEME_CSS = 'zenburn.css'
USE_LESS = True
TYPOGRIFY = True
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'


THEME = "theme"
PYGMENTS_STYLE = "native"

DELETE_OUTPUT_DIRECTORY = True
