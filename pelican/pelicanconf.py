#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Steve Theodore'
SITENAME = u'theodox.com'
SITEURL = 'http://blog.theodox.com'
COPYRIGHT_YEAR = 2016

PATH = 'content'

TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

ROBOTS = 'index, follow'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = None #'atom/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
FEED_ALL_RSS = 'feeds/rss.xml'

ADDTHIS_PUBID = 'ra-575daf41c4afb207'
SLUGIFIY_SOURCE = 'basename'

ARTICLE_URL = '{date:%Y}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

STATIC_PATHS = ['pages/course', 'pages/cookbook', 'pages/publications']

MAIN_MENU = True
SINGLE_AUTHOR = True
AMAZON_STORE = 'http://astore.amazon.com/tecsurgui-20'
DISQUS_SITENAME = 'theodoxcom'

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = (
                ('About...', '/about'),
        ('Publications', '/pages/pub'),
        ('Tech-Art Book Store', AMAZON_STORE),
        ('Cookbook', '/pages/cookbook')
        )

# Blogroll
LINKS = (('home', 'index.html'))


# Social widget

SOCIAL = (
	('linkedin', 'https://www.linkedin.com/in/stevetheodore'),
        ('github', 'https://github.com/theodox'),
	('google', 'https://plus.google.com/u/0/+SteveTheodore480BC/posts'),
	('stack-overflow', 'http://stackoverflow.com/users/1936075/theodox'),
	)

DEFAULT_PAGINATION = 8
DEFAULT_HEADER_IMAGE = 'http://texturetaddka.com/wp-content/uploads/2011/09/DSC862.jpg'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
COLOR_SCHEME_CSS = 'zenburn.css'

THEME = "pelican-clean-blog"
DELETE_OUTPUT_DIRECTORY = True