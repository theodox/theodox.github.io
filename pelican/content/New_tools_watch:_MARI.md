Title: New tools watch: MARI
Date: 2014-03-25 09:30:00.000
Category: blog
Tags: , , , , , 
Slug: New-tools-watch:-MARI
Authors: Steve Theodore
Summary: pending

Lately - particularly since the demise of the [late, lamented XSI](http://techartsurvival.blogspot.com/2014/03/sigh.html), I've been increasingly worried about getting too locked in to any one vendor for my tools.  I go way back with Photoshop - I once emailed a bug report directly to [John Knoll](http://en.wikipedia.org/wiki/John_Knoll) on my [Compuserve ](http://arstechnica.com/tech-policy/2009/07/goodbye-compuserve-we-thought-you-had-already-died/)(!!) account.  I was in the audience for the Maya launch at SIGGRAPH in, I think it was 1997.   
  
Jeez, I'm really fricking _old._ But I digress.  
  
The point is, I love those tools. They've been part of my life for a long time. But I don't like being too beholden to anybody, especially not an anybody who's a big public company that has to answer to shareholders and analysts and is not particularly worried about competition.  
  
For that reason I'm actively looking for alternatives to supplement or even supplant the old standbys.  And this GDC gave me some up-close and personal time with a very promising one: [Mari](http://www.thefoundry.co.uk/products/mari/), the 3-d painting app from [the Foundry](http://www.thefoundry.co.uk/).  
  
[![](http://www.cgsociety.org/stories/2010_05/mari/banner01.jpg)](http://www.cgsociety.org/stories/2010_05/mari/banner01.jpg)  
---  
Lots of Mari work on _Avatar_  
  
More after the jump.  
  
Caveat: this is _not_ a real review; it's a quick rundown of what I learned from a demo and some conversations with the devs.  If I write a real review, I'll mark it as such. This is more of a scouting report.  
  
Mari is a 3d paint package.  A very cool one.  
  
There have been 3d paint packages for a long time, since the SGI days, but they've never been a highly competitive area outside of the film business. The best software used to be confined to high-end workstations.  The most popular PC 3d painter, [Body Paint](http://www.maxon.net/products/new-in-cinema-4d-r15/overview.html), has never become a mainstream tool (at least in the US), perhaps since it's most closely aligned with [Cinema4D](http://www.maxon.net/products/cinema-4d-prime/who-should-use-it.html), which remains an outsider choice over here.  Although it does a pretty good job, it hasn't gotten a huge fan base -- it may be that the overlap with the free, built-in [PaintFX/Artisan](http://download.autodesk.com/global/docs/maya2014/en_us/index.html?url=files/3D_Paint_Tool_Paint_Textures_on_3D_objects.htm,topicNumber=d30e383981) tools in Maya kept it from gaining a lot of momentum.  PaintFX itself is -- well, it's free, it works OK if you have basic needs and good UVs, and I don't know a lot of folks who rely on it for much more than basic masks or blocking in broad strokes to be filled out in Photoshop.  The lack of layering, oddball texture handling, and finicky paint projection have all made it a feel like an afterthought: the MS paint of 3d paintng. Sure, it works... but, you know...  
  
So against this background I was a little skeptical when I went for my demo. I've run trial versions of Mari before, and the older version I have played with suffered from a somewhat idiosyncratic interface.  Mari originated at WETA Digital as an in-house tool and its roots in a very particular pipeline used to be very apparent.  The newest version (I believe I was shown 2.6, the website touts 2.5 as the latest) has a much more comprehensible feel.  
  
Like BodyPaint, but unlike PaintFX/Artisan, Mari supports layers. However it takes the concept of layering and runs with it way past where, say, Photoshop has to stop and catch it's breath.  Its has more in common with a node-graph based compositing tool (say, [Flame ](http://www.autodesk.com/products/autodesk-flame-family/features/flame-premium-products/all/gallery-view)or [Nuke](https://www.thefoundry.co.uk/products/nuke-product-family/nuke/features/))  than a joe-blow paint layer system. You can re-route channels from one map to another non-destructively. For example you could use a crisped up, high-contrast version of your diffuse texture as a spec mask - and be able to flow changes forward from the diffuse texture as you kept woirking while also adding new detail on top of the spec channel : each map gets its own stack of layers. Here's a video from the 2.0 version which touches on the concept:  
  
  
You can even put layers _on your layer masks_, which is extremely powerful and should be picked up by everybody else in painting soon. Plus you can make procedural layers (which can themselves be layer masks...). Even without the 3-d ness this would be a pretty compelling painting technology. Combined with the ability to paint specular or ambient occlusion masks directly in real time, its extra cool. Add in a nifty filter that lets you paint onto normal maps (again, real-time) while keeping your normals normalized and it's really, really cool.  
  
The 3D painting itself looked really smooth, with a good brush engine and pretty impressive performance (the demo was running on a Macbook Retina 15 laptop, so a very good but not firebreathing machine).  The most surprising bit was the resolutions that were possible: painting on multiple 4-k textures at once did not seem to faze the program (caveat: it's a demo. I'd assume they are pretty careful to pick subject matter that makes them look good).   
  
The extra high resolution is handy because the program also does a really nice job transferring textures to meshes with different UVs. Evidently they do it using a very dense color point cloud, rather than the more common raycast solutions that you see in, eg, Maya's transfer maps toolset.  The results looked pretty good even on pretty crummy auto-generated UV sets; this makes it easy to imagine painting big textures on high res models and transferring them to game-res as a final step, instead of committing to the low-res model and textures early on -- a workflow I've been championing for a long time.  
  
The last big plus for me was a built-in Python interpreter (looked like a 2.6 series). This should make it a much better citizen of the pipeline than some other painting programs I could mention, which require you to [reinvent network communications](http://techartsurvival.blogspot.com/2014/01/talking-to-photoshop-via-tcp.html) if you want to get anything done script-wise.  
  
Other good things:  
* [Support for PTex, the no-uv texturing system](http://www.digitaltutors.com/tutorial/743-Creating-Ptex-Textures-in-MARI). I'm not clear, though, on how to convert a PTex painted object to UVs.  
* Linear color workflow  
* A nice image-based lighting / physically based renderer preview (think [SkyShop or Toolbag](http://www.marmoset.co/))  
* Programmable shaders for the viewport, so you could paint directly into your game shaders  
  
All in all, this was a great first impression. As I said, it was a demo not a hands on, so I'm reporting what I saw which I expect was chosen well. However I'll write more when I've had a chance to grab a demo and actually use it myself.  In the meantime here's [a link to the Foundry's YouTube Channel ](http://www.youtube.com/playlist?list=PLi2GhhsPL-RqCYZy6THx-nveDPadoeORB)if you want to see more.

