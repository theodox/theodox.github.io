Title: Multiple MayaPy Management Mania
Date: 2014-05-11 14:03:00.000
Category: blog
Tags: , , , , 
Slug: Multiple-MayaPy-Management-Mania
Authors: Steve Theodore
Summary: pending

Lately I've been re-factoring the build system I use to distribute my python
tools to users.  The things which has been driving me crazy is the need to
start supporting multiple versions of Maya at the same time.  
  

[![](http://www.opensrs.com/images/wordpress/uploads/2007/04/email-service-1
/it-worked-on-my-
machine.jpg)](http://www.opensrs.com/images/wordpress/uploads/2007/04/email-
service-1/it-worked-on-my-machine.jpg)

  
  
Besides the general hassle involved, supporting multiple Maya versions and
multiple projects at the same time is a nightmare for doing good testing and
QA.  With so many different configurations it becomes increasingly easy for
something to slip through the cracks.  You might have a bit of Python 2.7
syntax which you wrote in Maya 2014 sneaking into a tool used in Maya 2011.
You might have tools that rely on an external dll that is correctly set up in
your Maya 2011 tools but not in the outsourcer version of your 2012 setup....
The possibilities for shooting yourself in the foot are endless.  
  
So, in an effort to clean this up, I've cooked up a simple module designed to
create and run instances of MayaPy.exe with precise control over the paths and
environment variables.  You can use it to run tests or automatic processes in
isolation, knowing that only the paths and settings you're using will be live.  
  
The actual code is not super complex -[ it's up on
gitHub](https://gist.github.com/theodox/2c712a91155c7e1c4c15), as usual free-
to-use under the MIT license.  Comments / questions/ feedback and especially
bug fixes all welcome! Code also here after the jump  
  
  
  
  
  
  
  


