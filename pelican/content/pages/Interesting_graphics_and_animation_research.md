Title: Interesting graphics and animation research
Date: 2016-03-06 11:40:00.000
Category: pages
Tags: cg, industry
Slug: research
Authors: Steve Theodore
Summary: A new permanent page of interesting academic research

This page is a list of interesting,  maybe not-quite-ready-real time graphics and animation tech that I'm keeping an eye on. Should be growing over time.

### Rendering

Anybody in games should be interested in the fate of [Ptex](http://ptex.us/), the no-uvs, variable resolution texturing system from Disney and used in, for example, [Mari](http://www.thefoundry.co.uk/products/mari/).  So far, it's not ready for runtime graphics. but [this Nvidia slideset](https://developer.nvidia.com/sites/default/files/akamai/gamedev/docs/Borderless%20Ptex.pdf) discusses a realtime implementation.  It claims to be only 15% slower than a UV mapped alternative - while saving about 18% of texture memory.  I'll believe it when I see it, but i _want_ to believe. ( **Update: **_I went over this with our residence graphics genius and he doesn't think it'll fly, even on XBone / PS4 class hardware)_

A [GPU Gem](http://diglib.eg.org/EG/DL/PE/VMV/VMV12/063-070.pdf.abstract.pdf;internal&action=action.digitallibrary.ShowPaperAbstract) on doing hardware aging of materials using GPU particles. Can't wait to see this get out from behind the paywall!

[Joint Importance Sampling](http://www.disneyresearch.com/project/joint-importance-sampling/): a paper from Disney on a better way to render path-traced media like fog or water.  Claims to increase render times 1000x for little change in quality! And it's _still_ too slow for games :)

A [new(ish) paper](http://ppsloan.org/publications/mrtSA.pdf) from [Peter-Pike Sloan](http://ppsloan.org/) proposing a method for low-res, realtime friendly pseudo gi lighting.  The new hardware generation is not going to make realtime GI happen with [the current techniques,](http://cg.ibds.kit.edu/publications/p2011/DGIWTCLPV_Kaplanyan_2011/DGIWTCLPV_Kaplanyan_2011.html) so new ways of looking at GI are important.

Also from PPS and Bungie, a review of the [hardware-based AO bake system used on Destiny](http://ppsloan.org/publications/BungieBake.pdf).  Note that in this example "AO" is "ambient obscurance" rather than "ambient occlusion" - obscurance accounts for distance to light sources, where as tradtional occlusion is dimensionless.

A neat paper from Sebastian Lagarde on [rendering wet surfaces in a physically based environment](http://seblagarde.wordpress.com/2012/12/10/observe-rainy-world/).  [Seb's blog](http://seblagarde.wordpress.com/) is a top-notch reference for anybody doing Physically based rendering (which means most of us by about 2015)

---

### Animation

[Motion fields](http://grail.cs.washington.edu/projects/motion-fields/motion-fields.pdf)  "Motion graphs" - basically efficiently seaming together  a desired set of Mocap data  \- has been a big deal in academia for a long time, but it's never caught on in games due to the Prince of Persia problem: it's too realistic and thus not responsive enough. This work from the graphics group at UW is an interesting slant on making this more reactive.  Unfortunately @ZoranPopovic has largely moved on to education from animation, but his [group's page at UW ](http://homes.cs.washington.edu/~zoran/)has a lot of interesting work from the last 5-6 years.

I'm a huge fan of Kevin Wampler's work on procededural animation. [This paper](http://grail.cs.washington.edu/projects/animal-morphology/s2009/) from 2009 describes a (slow, offline, but _cool) _process for generating decent gaits for arbitrarily shaped creatures. Check out the [videos](http://grail.cs.washington.edu/projects/animal-morphology/s2009/movs/morphology.avi) (note: big download, requires divx).  [This one](http://www.staff.science.uu.nl/~geijt101/papers/SA2013/) from the Netherlands is a similar optimization based approach to bipeds only - the big wrinkle being that everything in this one runs on simulated muscle networks rather than pure joint motors. Fun stuff!

This is an [interesting paper from Karen Liu's group at Georgia Tech](http://www.cc.gatech.edu/~jtan34/project/softBodyLocomotion.html), featuring soft body simulation done with a combination of finite element modeling and a muscle fiber system. Soft body animation remains a pretty black art, it would be great if it catches on in realtime-friendly ways. Not holding my breath, alas.

[This talk from the developer of Overgrowh ](http://aigamedev.com/open/access/overgrowth/)is an interesting look at hybrid physical-kinematic animations, a sort of  'Euphoria Lite'.  Some related references from [AIGameDev](http://aigamedev.com/open/editorial/animation-revolution/).  Also related is [Rick Lico's talk from GDC 2014](http://www.gdcvault.com/search.php#&category=free&firstfocus=&keyword=lico&conference_id=) about the Destiny animation system (GDC vault paywall).

### Procedural worlds

I'm very interested in procedural worlds for [obvious reasons](http://www.ign.com/articles/2013/04/16/4-hours-in-state-of-decays-open-world-zombie-nightmare).  It's an area that's got enornous potential but has been moving very slowly in the game side of things.

[The early chapters of this dissertation](http://hss.ulb.uni-bonn.de/2013/3124/3124.pdf) provides a decent overview of lots of the terminology and existing work in the field

There's [CityEngine, ](http://www.esri.com/software/cityengine) which looks good if you're looking at city size data sets (and it [supports python](http://www.esri.com/software/cityengine/features)!)  There are a lot of nice procedural terrain packages but they all look very fractal-y to me  nowadays; it was impressive in _Wrath of Khan_ but hasn't moved on much since. The most interesting terrain paper I've seen in a while is [this one](http://hpcg.purdue.edu/?page=publication&id=170), which uses rivers as the structural basis for terrain generation..

A [collection of papers from Purdue](https://www.cs.purdue.edu/cgvlab/urban/urban-procedural-modeling.html) on procedural land use - thing like zoning and road layout. Some of this looks pretty handy.   If it gets scary, just remember 'markov chain'  is math-speak for 'state machine', more or less.  The other fun aspect is their efforts to  'inverse model' the stuff they study - to turn real data into the data their model uses.

---

### Meshes, models, and surfaces

[This paper from Columbia](http://www.cs.columbia.edu/~keenan/Projects/GloballyOptimalDirectionFields/paper.pdf) promises an optimal way of establishing surface flow across arbitrary surfaces. This is interesting for a couple of reasons - it might be an interesting improvement to mesh-based navigation, and it might also lead to alternate methods of automatic UV generation.

A [decent roundup of mesh parameterization techniques](http://www.cs.berkeley.edu/~jrs/meshpapers/ShefferPraunRose.pdf)

