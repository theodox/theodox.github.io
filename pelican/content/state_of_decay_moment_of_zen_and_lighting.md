Title: State of Decay moment of zen  (and lighting)
Date: 2014-01-07 10:00:00.000
Category: blog
Tags: , , , 
Slug: _state_of_decay_moment_of_zen_and_lighting_
Authors: Steve Theodore
Summary: pending

[![](http://1.bp.blogspot.com/-Y1CcBO5iyig/UsujMjcxTRI/AAAAAAAAPCc/dIyL6T-pZQY/s1600/home_07.png)](http://1.bp.blogspot.com/-Y1CcBO5iyig/UsujMjcxTRI/AAAAAAAAPCc/dIyL6T-pZQY/s1600/home_07.png)  
---  
Pastor Will found the Super Fudge Chunk.    
The whole scene (except for that one spot of sunlight and the window) is lit entirely by ambient lighting with some vertex lighting and (small) point lights in the windows. What a nightmare - whatever we do in the next game, it won't be this!  
  
There's no lightmapping, thanks to a 24 hour continuous time of day cycle.  The houses could also be placed at any orientation, so the vertex lighting has to be pretty gentle - we shot basically ran a very smoothed out hemsipherical dome light outside the house, once with Final Gather and once with a dome of stochastically placed Maya point lights to create the illusion of darker interiors and lighter areas near windows). The final gather provided some bounce light look and the point lights provided a smooth gradient; blending the two helped eliminate hard artifacts and cut down on the frequency since we didn't want real shadows which would be wrong as the sun moved.   We also ran a similar omnidirectional vert light pass on all the props to add depth to things like cabinets and shelving. I also did a little tool to try to do some vertex decimation on the lit meshes -- we tended to subdivide the big planar areas heavily before lighting and then trim down verts which didn't hold much light or shading information (again, the smoother interior gradients helped a lot on memory here).   
  
A handy trick - thanks to a suggestion from [+Wolfgang Engel](https://plus.google.com/113049613359148049737)  \- was small point lights in the windows and doors to add a boost to exterior areas and to make it look as if the characters move from light to shadow, which isn't really true.  These had to be very small - much smaller than I wanted - to keep the overdraw costs low in the Crytek deferred renderer. Every house had a handful of somewhat larger lights right near the floor. They watched the sun direction and lit up when the room was facing the sun to provide the illusion of bounce lighting (this wasn't really checking the sun, it was checking the orientation of the light (and the house) against a precalculated table of sun positions and elevations so you could figure out how bright a given vector should be at a given time. Would have been much nicer to really sample the sun , but the perf environment was brutal  
  
The ambient lighting comes from an HDR cube map -  only one per building, alas, and they didn't orient with the placement.  In the end I hand painted abstract ones.  The 'faces' of the cube are color biased to help pick out the planes of the architecture so it doesn't all collapse into mono-color mush.   
  
Thank God for screen space ambient occlusion, which adds a lot of edge definition.   
  
And for Super Fudge Chunk.  
  
PS: Who has seen the bug where Pastor Will flips out on somebody back at base and threatens to "Cut you like a prison bitch"?  We heard about it from a tester and unanimously voted it "Won't Fix".  
  
  


