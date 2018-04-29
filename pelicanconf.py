#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Steve Theodore'
SITENAME = u'Chimeras & Manticores'
SITESUBTITLE = 'technical art, python, the games business, and obscurantism'
SITEURL = 'https://theodox.github.io'
COPYRIGHT_YEAR = 2018

PATH = 'content'

TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'
ROBOTS = 'index, follow'


PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'sitemap', 'summary', 'tag_cloud']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = None  # 'atom/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
FEED_ALL_RSS = 'feeds/rss.xml'
ADDTHIS_PUBID = 'ra-575daf41c4afb207'
SLUGIFIY_SOURCE = 'basename'

ARTICLE_URL = '{date:%Y}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

STATIC_PATHS = ['pages/course', 'pages/cookbook', 'pages/publications', 'images', 'extra']
ARTICLE_EXCLUDES = ['extra']


MAIN_MENU = True
SINGLE_AUTHOR = True
AMAZON_STORE = 'http://astore.amazon.com/tecsurgui-20'
DISQUS_SITENAME = 'theodoxcom'

SUMMARY_END_MARKER = "<!---jump--->"

#SHOW_FULL_ARTICLE = True
SHOW_SITESUBTITLE_IN_HTML = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [
    ('About...', '/about'),
    ('Publications', '/pages/pub'),
    ('Cookbook', '/pages/cookbook')
]

# Blogroll
LINKS = [('home', 'index.html'), ('tech-artists.org', 'https://tech-artists.org')]


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
CSS_OVERRIDE = 'theme/css/theodox.css'
TYPOGRIFY = True
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'


THEME = "../pelican-themes/svbtle"
DELETE_OUTPUT_DIRECTORY = True
