Title: Earth calling maya.standalone!
Date: 2014-04-05 11:17:00.000
Category: blog
Tags: , , , 
Slug: Earth-calling-maya.standalone!
Authors: Steve Theodore
Summary: pending

Somebody on Tech-artists.org was [asking about how to control a
maya.standalone instance remotely](http://tech-
artists.org/forum/showthread.php?4642-Python-Maya-Open-commandPort-for-
Mayapy&p=24225#post24225).  In ordinary Maya you could use the commandPort,
but the commandPort doesn't exist when running under standalone - apparently
it's part of the GUI layer which is not present in batch mode.  
  
So, I whipped up an uber-simple JSON-RPC-like server to run in a maya
standalone and accept remote commands. In response to some queries I've
polished it up and [put it onto
GitHub](https://github.com/theodox/standaloneRPC).  
  
It's an ultra-simple setup. Running the module as a script form mayapy.exe
starts a server:  

    
    
        mayapy.exe   path/to/standaloneRPC.py

  
  
To connect to it from another environment, you import the module, format the
command you want to send, and shoot it across to the server. Commands return a
JSON-encoded dictionary. When you make a successful command, the return object
will include a field called 'results' containg a json-encoded version of the
results:  

    
    
                 
            cmd = CMD('cmds.ls', type='transform')  
            print send_command(cmd)  
            >>> {success:True, result:[u'persp', u'top', u'side', u'front'}  
     

  
For failed queries, the result includes the exception and a traceback string:  

    
    
                 
            cmd = CMD('cmds.fred')  # nonexistent command  
            print send_command(cmd)  
            >>> {"exception": "",   
                 "traceback": "Traceback (most recent call last)... #SNIP#",  
                 "success": false,   
                 "args": "[]",   
                 "kwargs": "{}",   
                 "cmd_name": "cmds.fred"}  
     

  
It's a single file for easy drop. Please, **please** read the notes - the
module includes no effort at authentication or security, so it exposes any
machine running it to anyone who knows its there. Don't let a machine running
this be visible to the internet!


