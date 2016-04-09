Title: Talking to Photoshop via TCP
Date: 2014-01-29 02:04:00.000
Category: blog
Tags: , , , , , , 
Slug: Talking-to-Photoshop-via-TCP
Authors: Steve Theodore
Summary: pending

A recent [thread on TAO](http://tech-artists.org/forum/showthread.php?4481
-Communicating-between-Photoshop-and-Maya-\(Python\)) got me thinking about
communicating with Photoshop from Python. In the past I've done this [Adam
Plechter-style](http://techarttiki.blogspot.com/2008/08/photoshop-scripting-
with-python.html) using COM ( from both C# and Python) and it's worked for me,
but I know some people have problems with COM for a variety of reasons
relating to windows versions and DLL hell.  

Using COM always makes me feel like Mr. Yuk.

  

[![](http://www.calebsimpson.com/wp-
content/uploads/2013/11/YuckFace.gif)](http://www.calebsimpson.com/wp-
content/uploads/2013/11/YuckFace.gif)

  

Since I had to learn a few JavaScript tricks back when I started [looking into
Python web development](http://techartsurvival.blogspot.com/2013/12/and-i
-thought-we-had-it-bad.html), I thought it might be worth investigating what
could be done to cut out COM.  It turns out that ExtendScript - the JavaScript
flavor that comes with Adobe products (at least since CS 5, and I think
earlier) includes a socket object which allows for TCP communication.  That's
not kosher in 'real' browser based JS - but ExtendScript cheats a little
(that's also why it allows you to do things like hit the local file system,
another JS no-no).

  

The[ Adobe docs](https://wwwimages2.adobe.com/content/dam/Adobe/en/products/in
design/pdfs/JavaScriptToolsGuide_CS5.pdf) have an example (around page 196)
which shows how you can implement a chat server or a web server running inside
Photoshop. That might not be practical but it provides a simple framework you
can hijack to turn Photoshop into a remote procedure call server.  Here's an
example of a super-simple server that can be run inside Photoshop:

_Note: You'll need to save the file as a .JSX (not .JS!) for Photoshop to
allow the ExtendScript functionality which makes the socket objects work._  

  
This example is very bare bones, but it is easy to extend - just create
function objects and add them to **known_commands **dictionary and then send
them over the socket. The way it's written here the commands and arguments are
split on spaces (similar to the way a shell command works) -- if you need to
get at them in your JS functions you can [get at them using the arguments()
keyword:](http://stackoverflow.com/a/2141530/1936075).  For serious work I'd
probably use the ExtendScript XML object and send the commands and responses
as xml since that gets you out of having to worry about stuff like 'what if I
want to send an argument with a space in it' -- however this purpose of this
excersize is just to demonstrate what's possible.  
  
I should note that while the server is running, Photoshop is locked into the
wait loop so it will not be accessible interactively -- like a Maya running a
long script, the main thread is just waiting for the script to continue. For
the typical 'remote control' application that's what you'd expect, but it may
not answer for all purposes - so be warned.  
  
If you're trying to talk to Photoshop from Python, it's incredibly simple:  
  
  
That's all there is to it - of course, the _real _problem is getting useful
work done in the clunky Photoshop API -- but that's going to be the same no
matter whether you talk to PS via COM or TCP/IP.  Anecdotally, I've heard the
PS scripts are faster in JavaScript than when using COM or AppleTalk or VB, so
perhaps this method will be competitive on speed as well.  For small tasks
it's certainly a simpler and less irritating way to send a squirt to and from
PS


