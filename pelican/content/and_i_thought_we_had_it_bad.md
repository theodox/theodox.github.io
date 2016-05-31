Title: ...And I thought we had it bad...
Date: 2013-12-12 20:37:00.000
Category: blog
Tags: python, programming, web
Slug: _and_i_thought_we_had_it_bad
Authors: Steve Theodore
Summary: A tech artist looks at web development, recoils in horror

Bitching about all the random stuff you have to wire together is the key rituals of the tech-art faith.  You inherit all sorts of crazy decisions from Max, Maya, plugin authors, game engine teams, and random tools you find lying around and then some how have to lash it all together into a [Rube Goldberg contraption](http://www.rubegoldberg.com/gallery#) that (hopefully) hides the wackiness from your users  
  

[![](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_2001285523_lr.jpg)](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_2001285523_lr.jpg)
  
Of course, this is a huge pain in the butt  
  

[![](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_1673126806_lr.jpg)](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_1673126806_lr.jpg)

  
But I never realized that we have it _easy. _Until I sat down to write a web app.  
  
After lots of fruitless searching for commercial asset management system that would help us manage versions, review status and so on for our assets I finally broke down and decided to write my own. While [Shotgun](http://www.shotgunsoftware.com/) has gotten much slicker over the last year and [Tactic](http://www.southpawtech.com/) is both open-source and Python-based, neither works well with Perforce (Tactic has been promising P4 integration for over a year, with no public release that I've been able to find) and both are very heavy on the kind of features you need to handle a huge Hollywood-style team with hundreds of Anonymous Drones.  Our tiny team doesn't need pretty gantt charts and time-stamped hourly activity reports.  


[![](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_2039295957_lr.jpg)](http://users_v2.section101.com/memberdata/ru/rubegoldberg/photos/rubegoldberg_photo_gal_4152_photo_2039295957_lr.jpg)

  


## Web Dev 0.1B

  
The basic plan of attack is quite simple. Luckily the problem that usually damns these kinds of setups -- making sure that the database and the game are actually in sync on things like, say, texture size or polycount -- isn't a big problem since all of that is, blessedly, available in Unity with minimal work. The real goal of this system is to make sure people know what's placeholder art, what's work in progress, what has bugs, and so on..  To that, I've got a MySQL database sitting in our data center and some tools in the Unity editor that can collect and forward info to the database.  In Unity I've also hacked the editor so that the current status of the asset is displayed over the asset thumbnail in the project view so the users can see where they stand without going out to another tool.  
  
I love Unity to death, but even I can't convince myself to like Unity's built in procedural GUI language; it's clunky and formulaic -- and because it's orientation is so procedural it is extremely slow for anything with lots of controls.  Big Data -- spreadsheets, long lists, or fancy MVVM views are just not happening in the Unity Editor UI layer.  So -- to return at long last to the original seed of this post - I decided to write a web app to provide the producers and artists with the kind of overview data they'd need to see how things were progressing all across the project, rather than just the status of individual assets.  
  


## The Devil You Know

  
I did a bunch of research trying to figure out how to do this without having to start a whole new career as a web developer. In all honesty I was mostly hoping to avoid having to escape from the comfy confines of Python and C# (I can't really call SQL 'comfy' but at least it's _familiar_).  In particular my limited experiments with JavaScript (the real kind, not the beefed up Unity version) have been so uniformly unpleasant that I was desperate to avoid tangling with it at all costs.  I played with browser Pythons such as [Brython](http://www.brython.info/) , [Skulpt](http://www.skulpt.org/), and the [IronPython DLR host](http://jimmy.schementi.com/2010/03/pycon-2010-python-in-browser.html).  There's also projects like [PyJS ](http://pyjs.org/)and [RapydScript](https://bitbucket.org/pyjeon/rapydscript), which compile Python (or in the case of RapydScript a 'pythonalike') to Javascript.   
  
All of which are really cool - but none of which are tightly integrated into the bewildering complexity of modern web development. If all I wanted to do was _program_in the browser, I could stick with Python, take the speed hit and be done.  After more obsessive reading, however, I sadly concluded that the HTML-verse too crazy a place for any tacked-on, ex-post-facto solution -- even one as fricking cool as a complete Python interpreter written in Javascript.  The real hard part is not the programming, which is mostly UI level stuff -- hide this! highlight that! -- it's controlling the infinite number of stylistic choices that are involved in designing a functional and attractive layout in HTML.  The more I looked at it the more I felt like I needed to follow the herd and do what the 'real' web developers do -- which means not only learning HTML itself, but also CSS -- the language that defines style sheets for different graphic elements -- a language which is not the same as HTML - or the same as Javascript. ( Remember I said tech artists have it pretty good compared to web programmers? Imagine having to learn Mel, Python and Maxscript _all at the same time_ just to get started as a TA.  There but for the grace...)  
  
This could be worse. Thank heavens a friend at work pointed me at [Bootstrap](http://getbootstrap.com/), which is Twitter's clean and relatively simple to learn web gui framework. It lets you create nicely formatted modern looking pages without knowing too much about what really goes on in the tangled jungle of curly braces that define your CSS.  It still takes some doing to handle the GUI glue "do this when I push the button" stuff but its less annoying than, say, QT or WPF.  
  
 It's still incredibly annoying to write scads of parentheses and curlies for even the most trivial task  
  
`numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`  
`evens = [x for x in numbers if x % 2 == 0]`  
  
Is aesthetically and morally superior to  
`  
``numbers=[1,2,3,4,5,6,7,8,9,10];  
evens=new Array;  
var _$tmp1_data=_$pyva_iter(numbers);`  
`var _$tmp2_len=_$tmp1_data.length;`  
`for(var _$tmp3_index=0;_$tmp3_index<_$tmp2_len;_$tmp3_index++)`  
`    {`  
`    x=_$tmp1_data[_$tmp3_index];  
    if((_.isEqual((x % 2),0)))`  
`        {  
        evens.append(x);`  
`        }  
     }`  
`  
`But on the other hand you get lots of nice graphical goodies to soften the pain. I'm experimenting with [CoffeeScript](http://coffeescript.org/), which has Pythonic brevity and clarity -- but it's not Python and if you go in thinking it is (as I have on a few occasions) you'll get your knickers in a twist.   
  


## The backside

  
Fortunately, the server side code is actually much less of a hassle than I had feared. Given the nature of the problem -- selecting and filtering data from a database and then spitting it out to users -- the natural choice for me was [Django](https://www.djangoproject.com/), which has several advantages:  


  1. A great object-relational mapper (ie, you get to program with nice objects instead of gnarly SQL queries, cursors, and rows
  2. A decent templating language. When I wrote the first Python build server for [the lab](http://undeadlabs.com/) I did this all by myself with string.Template, and it was a pain in the pants.
  3. Hardly a curly bracket in sight
  4. Lots of documentation and tutorials on the web, which is comforting for the terrified novice (= me).



After all of the consternation I went to researching web client stuff, this was a snap choice. And then the fun began.  
  
The server is going to be running on a Mac (the tech art mac that we use for builds) so it will be ready to migrate to a Linux host later.  No problem, I use a mac laptop and do a fair amount of python on the mac already.,  So we want to install Django on the mac.  
  
We need to install easy-setup (not sure why that doesn't come with the default mac python install)  
....So we can install pip  
.......So we can install Django  
...... which needs MySQLdb  
.......... which needs MySQL  
..............which [doesn't install correctly on OSX the way it is supposed to](http://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x)  
.................so we need to install a Ruby package manager that can install MySql and MysqlDb  
....................so we install [Homebrew](http://brew.sh/)  
.........................which needs Xcode  
............................which requires you to accept the Xcode license after updates  
..............................and then to install the Xcode commmand line tools  
...........................so we can properly rebuild and install MySQL  
........................so we can install MySQLdb  
.....................so we can point Django at MySQL  
  
_Eh voila! _We're done!  It's a good thing Mac's are the elegant operating system for people who don't go in for all that techie stuff.  
  
Evidently. though,  this sort of thing is just business as usual for the real web developers. I guess I'll stop bitching about Autodesk's lousy license manager from now on.  The theme of this project is learning to appreciate just how good we've got it :)  
  
So, with all that done, I grabbed a trial of [PyCharm ](http://www.jetbrains.com/pycharm/). As an IDE I find it a bit clunky, but it's got good Django integration. Off to the races  
  


## SQLitis

_In this next bit I'm going to touch lightly on how Django does and doesn't make it easy to work with a database using familiar python techniques. The TL;DR is that it works pretty well, with gotchas. If you're unfamiliar with SQL terminology, databases, etc, you may want skim (and if you're an expert, you'll probably roll your eyes).  This isn't a how-to or tutorial - there are [great ones](http://gettingstartedwithdjango.com/) out there.  It's just a quick glance at something that many TA's may find useful in coming years._  
  
The nice part of the Django workflow is that you can get Django to generate your data models for you by analysing your existing database.  Running  
  
`python django-admin.py inspectdb`  
  
On your database will spit out the Python class definitions for your data models to stdout, where you can cut and paste them into your code.  I already had a decent database schema (I took most of my n00b lumps with that sort of thing building a bug tracking database for [SOD](http://undeadlabs.com/about-state-of-decay/)) and getting the object models built took about half an hour from 'starting to look at the docs' to 'done'. The little GUI that PyCharm gives you for django-admin is particularly helpful here.  
  
There are a couple of hitches.   
  
Django could be smarter about tables which don't use numerical ID columns as their primary keys -- which bugs my inner [Joe Celko](https://www.simple-talk.com/sql/t-sql-programming/a-tale-of-identifiers/) \-- and I ended up having to add numeric ID columns to some of my tables in order to placate Django. Evidently there are ways to get in under the hood an tweak the actual sql that is emitted from your models to get around this but I've got other things to worry about.   
  
It's also a bit tricky to get exactly the info you want.  For simple queries of the _get everything in this table named 'foo' _ variety Django works fine.  You can even do [SQL joins](http://www.w3resource.com/sql/joins/using-a-where-cluase-to-join-two-tables-related-by-a-single-column-primary-key-or-foriegn-key-pair.php), where you create a new pseudo table by picking entries from a set of tables with common keys - in Django you can trace back through a chain or table to table relationships just by following a  set of properties on your data objects.  In my case I have a table of assets (which describes the assets' names, location, and so on) and another table of asset types which is basically an Enum describing all the asset types - models, textures, animations and whatnot.  In SQL you'd connect them up using a [foreign key ](http://www.w3schools.com/sql/sql_foreignkey.asp)  to make sure that all the links were valid, and then use a JOIN statement to produce a combined result.  For example I have two tables somewhat like this:  
  
  
####Assets table  
|   |   |
|---|---|  
| Asset| String|  
|Thumbnail| Image|  
|Path| String|  
|Type| Int |

####Asset type table
|    |    |
|---|---  |
| ID| Int  |
|Description| String | 
|Name| String  |
  
And if I want to grab a combined view that shows the assets along with their types I might do something like  
  
    SELECT assets.asset, assets.path, asset_types.name  
    FROM assets  
    INNER JOIN asset_types  
    ON asset_types.id = assets.type  
      

Which seems kind of funky and 1970's to read, but it's a very powerful technique - this would give back all of the assets and their types without any tedious loop writing on the receiving end.  Django handles this for you nicely in its object model: as long as I made sure to let Django know that the 'type' I want comes from the asset types table and the 'asset' comes from the assets table, I can just grab it with  
  
    asset_list = Assets.objects.all()  # collect all the assets  
    for each_asset in asset_list:  
      print asset.type.name  

This is fine and dandy for many cases, but it does have some pitfalls. One of the great things about joins is that you can use them to substitute for conventional if-then logic. For example, in my case the I have a table of 'history' entries, which record changes in status (say from 'ready for review' to 'approved') along with times, dates and comments so we can see when things were OK'd for use in the game.  To get the current status of the object  I join the history table to itself:  
  
    SELECT  
    h1.idhistory, h1.asset, h1.changed  
    FROM (history h1 left join history h2  
          ON  
         (h1.asset = h2.asset and  h2.changed > h1.changed)  
         )  
          WHERE isnull(h2.asset)  
    ORDER BY h1.asset  

The LEFT JOIN tries to run all combinations of dates in h2 against matching assets/date combinations in h1.  In all but one cases these will succeed (since the last date will be larger than all but the latest date). By looking for the failed join (with "isnull (h2.assets)") we can grab the latest entry.  This seems like a lot of work but it's way faster than a conventional loop-through-them-all-and-pick-the-latest-one approach; plus it is done in the server, in highly optimized C code, instead of on the client in (slow) Python.  
  
Unfortunately this is a tricky one to get right with Django - at least, in my current (4 days and counting) aquaintance with Django.  I ended up having to work around it by creating a SQL view - basically a stored query - and grabbing just the id's of the history entries I wanted from their, and then doing a separate query to get the 'real' assets using the object technique I outlined earlier. Works fine but it is two server hits where one would do. C'est la vie.  
  

## Last words

  
So, it's been a mixed bag getting this thing off the ground.  Django is pretty cool - one of the nice things about working with web tech is that itt has several orders of magnitude more users than typical TA tech - the  speed with which things evolve in this space is pretty dizzying if you're used to the typical lackadaisical pace of tech advances from ADSK.  Web tools are clearly going to be a Big Thing in the coming years - the ease of distribution and graphical panache you can get makes the old school batch-file and script world seem pretty pokey.  On the other hand, web tech  really is a Rube Goldberg machine - it's made up of technologies that have vastly outgrown their original purposes, and is plagued by competing vendors and developer faddism.  Javascript is icky, and the idea of having to learn at least 3 different languages ( JS, CSS, and HTML) just to get anything done is pretty irritating.  
  
Fortunately the core of the TA personality is pure stubbornness.  We have our jobs because we don't like to rest until we figure out what the hell is going on. It's a very, very valuable trait to have if you're getting into web tools :)  
  
  
  
  


