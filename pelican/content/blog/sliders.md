Title: Sliders!
Date: 2014-03-16 11:08:00.000
Category: blog
Tags: tools 
Slug: sliders
Authors: Steve Theodore
Summary: pending

Although GDMag is no more, I still occasionally get interesting press releases from PR flacks who haven't gotten the bad news. This morning,  one from [MakeHuman](http://www.makehuman.org/) caught my eye.  
  
[![](http://www.makehuman.org/sites/makehuman.org/files/images/3/img003_001.png)](http://www.makehuman.org/sites/makehuman.org/files/images/3/img003_001.png)  
---  
Now with realistic back flab!  
  
MakeHuman is a new open sourced parametric modeling / body morphing program written in Python.  The overall use case is similar to [Poser](http://poser.smithmicro.com/gallery.html) or [Daz3d](http://www.daz3d.com/).  It seems like it also incorporates some of the underlying ideas from the venerable [FaceGen](http://www.facegen.com/) \- particularly having a few high level sliders that correlate changes across many different aspects of a model. 
  


[![](http://2.bp.blogspot.com/-MDesUhTFBYM/UyXbys3vv1I/AAAAAAABH9o/PEIhdil6obE/s1600/makeh.png)](http://2.bp.blogspot.com/-MDesUhTFBYM/UyXbys3vv1I/AAAAAAABH9o/PEIhdil6obE/s1600/makeh.png)

  
  
  


### Prognathism += .05

The slider set that comes with MakeHuman is pretty good. I didn't do a count but I'd guess there are several hundred.  Unlike many similar programs you can get a decent variety of body types outside the Burne Hogarth / superhero range, with decent control over the high level feel of the model. 

  


[![](http://3.bp.blogspot.com/-OcSmU55zGkk/UyXt2tCPLvI/AAAAAAABH-Q/OQ70pbYgcwc/s1600/bodytypes.png)](http://3.bp.blogspot.com/-OcSmU55zGkk/UyXt2tCPLvI/AAAAAAABH-Q/OQ70pbYgcwc/s1600/bodytypes.png)

  


The high frequency details that you really wouild need to sell the model are still up to you, however - fat rolls, wrinkles, scars and so on are going to have to be painted on or hand modelled in a later step.

  


Like most slider-modeler programs it's easy to create really disturbing imagery, but the underlying slider set is pretty good, with a decent amount of anatomically based sliders for facial and body proportions.  Like all slider-modellers it suffers from the tension between local control and overall believability - it's easy to start noodling on a detail only to discover you've undermined the whole product.  
  


[![](http://2.bp.blogspot.com/-um2YWid2fNk/UyXm310LhaI/AAAAAAABH94/bmzSUhs80SY/s1600/lotsasliders.png)](http://2.bp.blogspot.com/-um2YWid2fNk/UyXm310LhaI/AAAAAAABH94/bmzSUhs80SY/s1600/lotsasliders.png)

  
  
As always with these kinds of things , you are teleported right to the bottom of the [Uncanny Valley](http://www.arts.rpi.edu/~ruiz/EGDFall08/postmortemreadings/Theodore%20Uncanny%20Valley.pdf) when you first start to twiddle things; the vacant stare can really get to you as you creep those sliders along (I will not speculate on which sliders _you _spend the most time creeping, but if you've looked at [Poser (NSFW) ](https://www.google.com/search?q=poser+models&safe=active&espv=210&es_sm=122&source=lnms&tbm=isch&sa=X&ei=Vt8lU7LwGoqDogS7q4CgBA&ved=0CAoQ_AUoAg&biw=1180&bih=974)I bet you can guess which one gets the most over-use. Makes you think:: _What a missed microtransaction opportunity!_).   
  


### Use Case

  
If you go into any slider-modeller expecting shippable characters with strong personalities to pop out the other end, you'll be disappointed.  That's not where these tools shine.  
  
One-button art is not really the point with these kinds of tools.  They are, however,  a fabulous way to kick off a ZBrush sculpt or play with ideas quickly.  The topology  on the base meshes that come with the package seems pretty good to me, although I'm sure plenty of artists will have their own preferences. However MakeHuman  allows you to provide alternate base meshes (another trick pioneered by FaceGen back in the day) so you could provide your own body meshes before hitting the sliders if you so desire.   
  
[![](http://3.bp.blogspot.com/-6Ju73PA4gS8/UyXnRjYcyII/AAAAAAABH-A/maJd8o1mGy0/s1600/hai.png)](http://3.bp.blogspot.com/-6Ju73PA4gS8/UyXnRjYcyII/AAAAAAABH-A/maJd8o1mGy0/s1600/hai.png)  
---  
The base topo and skinning aren't bad  
  
The program can also output ready-riigged characters witth a variety of skeletons to FBX and other intermediate formats.  As with the models, go in expecting to have to tweak the results - but again, its a huge accelerator for progress. The selection of hair, clothing and accessories is pretty small compared to what you'd get with the commercial alternatives, but adding your own is not too tough (an [example tutorial here](http://www.aversionofreality.com/blog/2014/1/30/project-maiko-creating-the-base-bodysuit))  
  
For TA's one of the most interesting aspects of the program is the fact that it's mostly written in Python, and that the source code is freely available. If you're interested in adding your own sliders, or new deformation algorithms, or more body data the way is open.  One thing that I'd liove to see more of in the program is a mode based on real world body scan data - one of the ways FaceGen was ahead of its time was its use of statistical models rather than the more obvious 'make bigger butt cheeks' sliders, which meant that randomly generated characters usually started from a more plausible place than the familiar monstrosities of, say, Oblivion:  
  
[![](http://cloud-4.steampowered.com/ugc/542932685069387623/92E24D6F77E61891EFC6A2FC9A077BB70E4C31A5/1024x768.resizedimage)](http://cloud-4.steampowered.com/ugc/542932685069387623/92E24D6F77E61891EFC6A2FC9A077BB70E4C31A5/1024x768.resizedimage)  
---  
yes, Oblivion, I'm talking about you.  
All in all, not bad for free-as-in-beer!   [Download it from here](http://www.makehuman.org/content/download.html)

