Title: Talking to Photoshop via TCP
Date: 2014-01-29 02:04:00.000
Category: blog
Tags: python, programming, photoshop
Slug: talking_to_photoshop_via_tcp
Authors: Steve Theodore
Summary: Simple Photoshop scripting via tcp/ip

A recent [thread on TAO](http://tech-artists.org/forum/showthread.php?4481-Communicating-between-Photoshop-and-Maya-\(Python\)) got me thinking about communicating with Photoshop from Python. In the past I've done this [Adam Plechter-style](http://techarttiki.blogspot.com/2008/08/photoshop-scripting-with-python.html) using COM ( from both C# and Python) and it's worked for me, but I know some people have problems with COM for a variety of reasons relating to windows versions and DLL hell.  

And using COM always makes me feel like Mr. Yuk.

[![](http://www.calebsimpson.com/wp-content/uploads/2013/11/YuckFace.gif)](http://www.calebsimpson.com/wp-content/uploads/2013/11/YuckFace.gif)

Since I had to learn a few JavaScript tricks back when I started [looking into Python web development](and_i_thought_we_had_it_bad.html), I thought it might be worth investigating what could be done to cut out COM.  It turns out that ExtendScript - the JavaScript flavor that comes with Adobe products (at least since CS 5, and I think earlier) includes a socket object which allows for TCP communication.  That's not kosher in 'real' browser based JS - but ExtendScript cheats a little (that's also why it allows you to do things like hit the local file system, another JS no-no).


The[ Adobe docs](https://wwwimages2.adobe.com/content/dam/Adobe/en/products/indesign/pdfs/JavaScriptToolsGuide_CS5.pdf) have an example (around page 196) which shows how you can implement a chat server or a web server running inside Photoshop. That might not be practical but it provides a simple framework you can hijack to turn Photoshop into a remote procedure call server.  Here's an example of a super-simple server that can be run inside Photoshop:

    :::javascript
    // requires photoshop CS5+
     
    // create a new socket
    conn = new Socket();
     
    var keep_serving = true;
    // sample functions. In a real application you'd have handler functions that could accept  more complex inputs
    var alrt = alert;                                                                                           // pop a dialog
    var newLayer = function () { return app.activeDocument.artLayers.add(); };      // make a layer
    var stop = function () { keep_serving = false; };                                           // stop the server
     
    // 'register' the commands by putting them into a dictionary
    var known_cmds = { 'alert': alrt, 'stop': stop, 'newLayer': newLayer };
     
    while (keep_serving) {
        if (conn.listen(8789))  // ... you'd probably want to make this configurable
        {
            // wait forever for a connection
            var incoming;
            do incoming = conn.poll();
            while (incoming == null);
     
            // grab the next non-null communication
            new_cmd = incoming.read();
            try {
                // split the incoming message into cmd on spaces (shell style)
                var command_text = new_cmd.split(" ", 1);
                var args = new_cmd.slice(command_text[0].length + 1, 999).split(" ");
                var requested = known_cmds[command_text];
     
                if (null != requested) {
                    result = requested(args);
                    incoming.writeln(result + "\nOK\n");
                }
                else {
                    incoming.writeln("unknown command\nFAIL\n");
                }
     
            }
            catch (err) {
                incoming.writeln(err + "FAIL\n");
                incoming.close();
                delete incoming;
            }
        } // end if 
    } // -- end while

_Note: You'll need to save the file as a .JSX (not .JS!) for Photoshop to allow the ExtendScript functionality which makes the socket objects work._  

  
This example is very bare bones, but it is easy to extend - just create function objects and add them to `known_commands` dictionary and then send them over the socket. The way it's written here the commands and arguments are split on spaces (similar to the way a shell command works) -- if you need to get at them in your JS functions you can [get at them using the arguments() keyword:](http://stackoverflow.com/a/2141530/1936075).  For serious work I'd probably use the ExtendScript XML object and send the commands and responses as xml since that gets you out of having to worry about stuff like 'what if I want to send an argument with a space in it' -- however this purpose of this excersize is just to demonstrate what's possible.  
  
I should note that while the server is running, Photoshop is locked into the wait loop so it will not be accessible interactively -- like a Maya running a long script, the main thread is just waiting for the script to continue. For the typical 'remote control' application that's what you'd expect, but it may not answer for all purposes - so be warned.  
  
If you're trying to talk to Photoshop from Python, it's incredibly simple:  

    :::python
    import socket
    HOST = '127.0.0.1'
    PORT = 8789

    def send_photoshop(msg):
    '''
    Expects a photoshop instance running a tcp server on HOST:PORT
    '''
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST,PORT))
        conn.send(msg)
        r = conn.recv(4096)
        conn.close()
        return r

    send_photoshop("alert hello_from_python")       #show a dialog
    send_photoshop("newLayer")                      #create a layer
    send_photoshop("stop")                          #stop the server

  
That's all there is to it - of course, the _real _problem is getting useful work done in the clunky Photoshop API -- but that's going to be the same no matter whether you talk to PS via COM or TCP/IP.  Anecdotally, I've heard the PS scripts are faster in JavaScript than when using COM or AppleTalk or VB, so perhaps this method will be competitive on speed as well.  For small tasks it's certainly a simpler and less irritating way to send a squirt to and from PS 

