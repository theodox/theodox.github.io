Title: Some fixups for sfx
Date: 2016-01-29 00:52:00.001
Category: blog
Tags: sfx, programming, maya 
Slug: some_fixups_for_sfx
Authors: Steve Theodore
Summary: pending

I've posted [a couple of fixes](https://github.com/theodox/sfx/commits/master) to the code for the [shaderfx module](http://techartsurvival.blogspot.com/2016/01/first-module-of-year.htmlDone) I posted a little while ago.  [+Sophie Brennan](https://plus.google.com/116374315761191190711) spotted a problem with the way that module handled some kinds of nodes -- which I had assumed were just plain old objects but which were in fact buttoned-up group nodes.  Since they didn't use the same method to report their outputs as the rest of shaderfx they could not easily be created or connected using the module.  
  
Luckily  [+Kees Rijnen](https://plus.google.com/115746724358684308496), the main author of shaderfx, noticed the blog post and helpfully  pointed me at the source of the problem which I've included in a fix.   
  
If you are using the original version of the code this may be a breaking change.  To unify the way that individual nodes and groups are connected,  I changed the connect() and disconnect() methods to take only two arguments where they previously took 4.  In the first pass you would write  
  

    
    
    network.connect( node1, node1.outputs.xyz, node2, node2.inputs.rgb)  
      
    

which was needlessly wordy.  So connect() and disconnect() now sport the cleaner, simpler syntax  
  

    
    
    network.connect(node1.outputs.xyz,   node2.inputs.rgb)  
      
    

As always, comments and pulls are encouraged!

