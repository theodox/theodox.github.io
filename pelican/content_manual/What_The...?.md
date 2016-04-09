Title: What The...?
Date: 2015-02-05 22:57:00.001
Category: blog
Tags: , , 
Slug: What-The...?
Authors: Steve Theodore
Summary: pending

Like many Maya heads I have long wrestled with the problem of filtering lists
to get what I'm interested in.  You're probably familiar with the use of  the
**type** flag in cmds.ls() to filter on types: for example this will give you
only the transforms in your current selection:

  

**cmds.ls(sl=True, type = 'transform')**

  

This works for any node type (the list is quite long: it's basically the whole
maya node class hierarchy) and is a handy way to

  

However I just noticed today that this works _a little_ for component
selections as well.  For some reason Maya 2014+ seems to treat faces, edges
and vertices as if they were nodes of a "float3" type (uv's are "float2"s) .
This means you can get the components from a mixed selection with:

  

**cmds.ls(sl=True, type = 'float3')  **

  

Not the most earth-shattering discovery of the 21st century, but handy
nonetheless.

  


