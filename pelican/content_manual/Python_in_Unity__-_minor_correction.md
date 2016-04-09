Title: Python in Unity  - minor correction
Date: 2013-12-22 09:53:00.001
Category: blog
Tags: , , , 
Slug: Python-in-Unity----minor-correction
Authors: Steve Theodore
Summary: pending

Going over the last post about [Python +
Unity](http://techartsurvival.blogspot.com/2013/12/embedding-ironpython-in-
unity-tech-art.html), I did a clean install to make sure the steps I was
describing were working correctly and it reminded me about an inportant bit
I've left out: how to get the Python stdlib into your Unity IronPython  
  
Because Microsoft was the sponsor of the original IronPython project, versions
that Microsoft released (including the 2.6.2 that i linked to in the last
post) **don't include the stdlib**, which comes with it's own license that
clashes in some mysterious way with MS's licensing terms (even though both MS
and the Python Foundation are giving the stuff away for free... _*_sigh*). So
to dance around that, they did not include the stdlib  \-- the 'batteries
included' -- with base install.  
  
The remedy is simple - grab a copy of the regular python stdlib from a python
2.6 series install and copy it into the /Lib folder next to the location of
your IronPython DLL.  I found it simplest to grab the Python26.zip folder from
my Maya install and to expand that into the folder.  I did leave the 3 or 4
files that IPy had installed there on its own intact, I believe -- on pure
intuition -- that they are different from the corresponding files in the
standard python lib.  
  

##  Caveat emptor

  
  
FWIW, this is a good place to point out that some small percentage of stdlib
modules don't work under IronPython (an unfortunate example being the handy
_csv_ module for reading comma-delimited data files).  AFAIK there is no
authoritative list of which modules do and don't work under Ipy. The good news
is that, for this application , there is almost always a dotnet native
solution to use as an alternative without having to install anything else.  
  


