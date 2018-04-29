Title: Command and Conquer
Category: blog
Authors: Steve Theodore
Tags: maya, python, distribution
Slug: cli_zip
Date: 2016-06-16
Summary: A handy hack for distributing Python command line tools with predictable execution environments.
header_cover: http://www.wsgf.org/f/u/imagecache/node-gallery-display/contrib/dr/203/ingame_16x9.jpg

It's pretty common for TA's to want some specialty command-line tools that for their own use, or to share with a select number of power users who aren't afraid of typing.  Python is great at making tools for this kind of one-off use, distributing and maintaing these kinds of scripts  requires jumping even more hoops than sending out artist tools (something covered in more detail [here](blog/2014/save_the_environment) and [here](blog/2014/egg_man)). 

It's much easier for folders full of loose scripts to diverge among coders, who are likely to be tinkering with their contents, than it is among artists.  For keeping the artists on the same page, I [distribute a complete environment in a single .zip file](/blog/2014/egg_man), which has definitely cut my distribution headaches by an order of magnitude and simplified my management a great deal.  But until fairly recently the techies had to muddle along the old fashioned way.

However, once we started getting in to command line tools on a larger scale,  we realized that we can get many of the same benefits by using the same zip file as part of our command line arsenal.  This means we can write scipts that use our up-to-date in-house libraries (and also all of the path manipulation that gets done for our artist tools) without modification.

![](http://static2.gamespot.com/uploads/scale_super/gamespot/images/2006/043/reviews/712537-930763_20060213_001.jpg)
>  Forget CLI tools, bring on the FMV tools and party like its 1996

# Just a NOD

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

Once you understand that, you can build a flexible command-line toolkit that uses your library quite simply.  You'll need to collect all of your path mongering into a single place, but that's a good idea in any case -- things get crazy pretty quick if every module can mess with `sys.path` on a whim.  

I use a module that mimics `site` but works for zips as well as loose files:

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

![](http://s3.amazonaws.com/bronibooru/a5fcec9d4f6a844d7222954ada743cf5.jpg)
> I.... I just don't know what to say... I mean...   But it **is** the least problematic search result for 'Command and Conquerer Red Alert characters'

# Red Alert

Of course, this is only a little bandaid on the big, nasty psoriasis that is Python tools distribution.  I was very hopeful when I stumbled across this PyCon talk on YouTube:

<iframe width="560" height="315" src="https://www.youtube.com/embed/5BqAeN-F9Qs" frameborder="0" allowfullscreen></iframe>

Alas, however, the talk mostly served to reinforce my feeling that Python distribution is badly busted (and that `pip install` is not how to fix it).  For the meantime it's at least comforting to know there's fairly easy way to pop out an uncomplicated, repeatable toolkit with no external dependencies even if it costs you some disk space.


