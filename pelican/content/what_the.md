Title: What The...?
Date: 2015-02-05 22:57:00.001
Category: blog
Tags: maya, python, ls
Slug: ls_float3
Authors: Steve Theodore
Summary: A nice little trick for filtering components in Maya using `cmds.ls()`

Like many Maya heads I have long wrestled with the problem of filtering lists to get what I'm interested in.  You're probably familiar with the use of  the **type** flag in cmds.ls() to filter on types: for example this will give you only the transforms in your current selection:

    cmds.ls(sl=True, type = 'transform')

This works for any node type (the list is quite long: it's basically the whole maya node class hierarchy) and is a handy way to find only once class of objects.  However there's no equivalent command for components: so if you've got a mixed list of objects and components it's hard to extract just the components without resorting to cumbersome string processing.

However I just found a partial workaround today that helps with component selections.  For some reason known only to [Xibalba](https://en.wikipedia.org/wiki/Xibalba),  Maya 2014+ seems to treat faces, edges and vertices as if they were nodes of a "float3" type (uv's are "float2"s) .  This means you can get the components from a mixed selection with:

    cmds.ls(sl=True, type = 'float3')

Not the most earth-shattering discovery of the 21st century, but handy nonetheless.

  


