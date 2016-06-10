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
FEED_ALL_ATOM = 'atom/%s_all.atom.xml'
CATEGORY_FEED_ATOM = 'atom/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = 'rss/%s.rss.xml'

MAIN_MENU = True
SINGLE_AUTHOR = True
MENUITEMS = (
		('book store', 'TA-Bookstore-page.html'),
		)

# Blogroll
LINKS = (('home', 'index.html'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget

SOCIAL = (
	('linkedin', 'https://www.linkedin.com/in/stevetheodore'),
        ('github', 'https://github.com/theodox'),
	('google', 'https://plus.google.com/u/0/+SteveTheodore480BC/posts'),
	('stack-overflow', 'http://stackoverflow.com/users/1936075/theodox')
	)

DEFAULT_PAGINATION = 8
DEFAULT_HEADER_IMAGE = 'http://texturetaddka.com/wp-content/uploads/2011/09/DSC862.jpg'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "pelican-chunk"

