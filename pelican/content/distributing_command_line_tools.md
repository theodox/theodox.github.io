title: distributing_command_line_tools
category: Blog
tags: blog
date: 2015-01-01

It's pretty common for TA's to want some specialty command-line tools that for their own use, or to share with a select number of power users who aren't afraid of typing.  While python is great at making tools for this kind of one-off use, distributing and maintaing these kinds of scripts  requires jumping even more hoops than sending out artist tools (something covered in more detail [here](http://techartsurvival.blogspot.com/2014/06/save-environment.html) and [here](http://techartsurvival.blogspot.com/2014/07/save-environment-2-i-am-egg-man.html)). 

It's much easier for folders full of loose scripts to diverge among coders, who are likely to be tinkering with their contents, than it is among artists.  My usual answer to keeping the artists on the same page is to [distribute a complete environment in a single .zip file](http://techartsurvival.blogspot.com/2014/07/save-environment-2-i-am-egg-man.html), which has definitely cut my distribution headaches by an order of magnitude and simplified my management a great deal.

Lately one of my colleagues has been working on some command line tools and we realized that we can get many of the same benefits by using the same zip file as part of our command line arsenal.  This means we can write scipts that use our up-to-date in-house libraries (and also all of the path manipulation that gets done for our artist tools) without modification.

HED
===

The trick is really pretty simple. All you need to do is include a `__main__.py` in the zip file.  Any python zip with a `__main__.py` is treated by python as an executable script.  Here's a trivial example:

```python
# main.py
import sys
if __name__ == '__main__':
    arguments = sys.argv[1:]
    print "# I was called with", arguments
```

If you zip that file, you can execute it like so:

```python
python path/to/example.zip hello world
# I was called with hello world
```

Once you understand that, you can build a flexible command-line toolkit that uses your library quite simply.  You'll need to collect all of your path mongering into a single place, but that's a good idea in any case -- things get crazy pretty quick if every module can mess with `sys.path` on a whim.  I use a module that mimics `site` but works for zips as well as loose files:

```python
"""
zipsite
"""
import zipfile
import sys
import os


class SiteProcessor(object):
    def __init__(self, root):
        self.root = root

    def process(self):
        for root, contents in self.pth_files():
            self.read_pth_file(root, contents)

    def pth_files(self):
        # this gets overridden in derived classes
        # so that zips and loose files worh the same
        yield

    @staticmethod
    def read_pth_file(root, contents):
        for line in contents.readlines():
            if line.startswith('#'):
                continue
            if line.startswith("import"):
                exec (line.strip())
                continue
            new_path = "{0}/{1}".format(root, line.strip())
            if not new_path in sys.path:
                sys.path.append(new_path)


class FolderSiteProcessor(SiteProcessor):
    def pth_files(self):
        for roots, dirs, files in os.walk(self.root):
            for f in files:
                if f.endswith(".pth"):
                    clean_path = (roots + "/" + f).replace("\\", "/")
                    with open(clean_path, 'r') as handle:
                        yield roots, handle


class ZipSiteProcessor(SiteProcessor):
    def pth_files(self):
        archive = zipfile.ZipFile(self.root, 'r')
        all_names = archive.namelist()
        all_names.sort()
        pth_list = [p for p in all_names if p.endswith('.pth')]
        for pthfile in pth_list:
            local_pth = os.path.dirname(self.root + "/" + pthfile)
            contents = archive.open(pthfile, 'U')
            yield local_pth, contents


def addsitedir(*roots):
    """
    for every .pth file in or under each root, process the pth file
    in the same way as site.addsitedir()
    """
    for each_root in roots:
        if zipfile.is_zipfile(each_root):
            ZipSiteProcessor(each_root).process()
        else:
            FolderSiteProcessor(each_root).process()
```

As long as that's in my distribution zip, my `__main__` cam setup all the paths with a couple of lines:

```
import zipsite
import os
zipsite.addsitedir(os.path.normpath(__file__ + "/.."))
```

All the real work is delegated to the .pth files, which is a much simpler and less error prone method than letting the individual modules run rampant.
