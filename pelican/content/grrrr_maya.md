Title: Grrrr..... Maya!!!
Date: 2015-10-27 22:43:00.000
Category: blog
Tags: maya, bugs, programming,techart
Slug: grrrr_maya
Authors: Steve Theodore
Summary: A really annoying, and really old bug in Maya relating to materials.

Some kinds of pain are just occasional: you stub your toe or bump your head, ouch, and then its over. 

Other kinds of pain aren't as sharp or as sudden... but they're chronic.  That persistent twinge in your lower back may not hurt as much as a twisted ankle - but it's going to be there forever (at least unless you get into Power Yoga, or so my wife claims).  

Maya is old enough to have a few of those chronic pains, and I just ran in to one which -- once we debugged it and figured it out -- I realized has been a persistant irritant for at least the last decade; if my creaky old memory does not lie it's been a distinct pain in the butt since at least 2002 and it may very well go back all the way to Maya 1.0. 

In another context I might even have been able to diagnose it but instead we spent a ton of time and energy working around an unexpected behavior which is, in fact, purely standard Maya. It's _stupid_ Maya, but it's standard too.  Maya, alas, is **double plus ungood** about mixing per-face and per-object material assignments. So, I figured I'd document this here for future sufferers: it might not ease the pain much, but at least you'll know you're not crazy.  

The basic problem is that assigning materials to faces and to objects use slightly different mechanisms. If you check your hypergraph you'll see that per-face assignments connect to their shadingGroup nodes through the `compInstObjectGroups[]` attribute while object-level assigmemts go through the similar-but-not-identical `instObjectGroups` attribute (if you're looking for these in the docs, the component cone is inherited from the [`geometryShape`](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/Nodes/geometryShape.html) class and the object version comes from [`dagNode`](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/Nodes/dagNode.html)).  

As long as you're working with one object at a time this isn't a problem. However, if you're duplicating or copy-pasting nodes, there's a gotcha:  If you ever try to merge meshes which have a mix of per-face and per-object assignments, Maya will magically "remember" old per-face assigments in the combined mesh.  If you're a masochist, here's the repro:  

1. create a object, give it a couple of different materials on different faces
2. duplicate it a couple of times
3. assign a per-object material to the duplicates, overriding the original per-face assignments
4. combine all the meshes.
5. _Et voîla!_ The cloned meshes revert to their original assignments

[![](http://3.bp.blogspot.com/-WHA-mYamWSw/VjBfoXDF_4I/AAAAAAABMuY/BtrR34QPRhM/s640/pasted_image_at_2015_10_23_05_32_pm_720.png)](http://3.bp.blogspot.com/-WHA-mYamWSw/VjBfoXDF_4I/AAAAAAABMuY/BtrR34QPRhM/s1600/pasted_image_at_2015_10_23_05_32_pm_720.png)

What appears to happen is that those `compInstObjectGroups` connections are driven by hidden `groupID` nodes which don't get deleted when the per-face assignments are overridden by the per-object ones in step (3) .  They stick around even though they aren't being used, and when the mesh is combined they step right back into their original roles.  
  
If you're doing this interactively it's an annoyance. If you're got tools that do things like auto-combine meshes to cut down on transform load in your game.... well, it's a source of some surprising bugs and equally surprising bursts of profanity.  But at least it'ss predictable.

The workaround:  Before doing any mesh combination first delete the existing history then add something harmless to meshes you're about to combine. (I use a triangulate step, since this happens only at export time). That kills the rogue `groupID` nodes and keeps the combined mesh looking the way you intended.

Sheesh. What a way to make a living.

  


