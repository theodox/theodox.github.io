Title: SIGGRAPH 2014 Short Review
Date: 2014-08-20 12:28:00.002
Category: blog
Tags: 
Slug: SIGGRAPH-2014-Short-Review
Authors: Steve Theodore
Summary: pending

It's been [crazy times at Undead Labs](http://moonrise-game.com/) as we [get
ready for Pax](http://undeadlabs.com/2014/08/news/pinny-arcade-now-featuring-
moonrise-pin/).  I did sneak in a lightning visit to SIGGRAPH, since it drive-
able in Vancouver, but I had to cut it pretty short.  
  
The highlight of the show was the [TA beer night at the Butcher and
Bullock](http://tech-artists.org/forum/showthread.php?4885-Siggraph-2014-TA-
Meetup)  \-- hats off to [+Robert
Butterworth](https://plus.google.com/116275833090172173559)  for putting
together -- but there was some other stuff going on as well. Here's a very
partial and completely unscientific brain dump of what I saw. The important
caveat here is that my limited schedule kept me on a very short leash:  I
spent all day Monday in the _Advances in Real Time Graphics_ course, which I'm
pleased to say has become a SIGGRAPH institution (go Natasha!) and then all
day Tuesday talking to vendors, so I'm 100% certain to have missed a lot of
cool and interesting stuff. This was an all business visit, so most of what I
have to report is general impressions rather than new cutting edge research.
My impressions are after the jump...  
  
  

## Have a PBR!

The trend towards [physically based
rendering](http://www.marmoset.co/toolbag/learn/pbr-theory) is getting even
more pronounced: I think there's no question this will be this year's buzzword
of the year, at least in games.  I've been working with PBR renderers at work
(mostly, but not only Marmoset) and it really is a better way to work, at
least if your working with realistic subject matter.  I've got an article in
the works for 3D World about exactly this - lost somewhere in the labyrinth
that is print production - and the takeaway is that it's a good thing for
anybody in game art to be boning up on.  
  
 The standard textbook, [Physically Based Rendering, Second Edition: From
Theory To Implementation](http://www.amazon.com/gp/product/0123750792/ref=as_l
i_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0123750792&linkCode=as2&ta
g=tecsurgui-20&linkId=HDVQMGQOD6MKGOCB)![](http://ir-na.amazon-
adsystem.com/e/ir?t=tecsurgui-20&l=as2&o=1&a=0123750792), is a bit of a slog.
It has great info but very coder-centric. The Marmoset site linked above has
some great intro level material.  For a deeper dive there's [this post from
Sebastian Lagarde](http://seblagarde.wordpress.com/2011/08/17/feeding-a
-physical-based-lighting-mode/). There's also a couple of decent video
intros:|  
---|---  
Hat tip : +Robert-Jan Brems  
I think there's a near-future blog post in all this somewhere :)  
  
One side note: the need for high quality specular light samples - usually
cubemaps - in a PBR pipeline has the nice side-effect that you can usually
count on a reflection map for lots of areas which might not have gotten one
traditionally. Combine with depth buffer reflections for fun and profit!
There were good talks from the _Killzone_ and _Thief _teams about real-time
depth buffer reflections which I think are going to make a noticeable
difference in tone from last gen graphics as it becomes more common.  

## Free samples

  
One of the side effects of the new console generation is that everybody is
revisiting antialiasing and sampling.  From 720p to 1080p means pushing more
than 2X the pixels. This makes MSAA a worrisome burden: you've to do a lot of
sampling at that res.  
  
Not surprisingly there was a lot of interest in alternatives to brute force
antialiasing at this year's graphics course. I particularly liked the paper
from Michel Drobot of Guerilla on 'Hybrid Reconstructive AA', which to my
less-than-wizardly ears sounded like a variant of temporal AA (in which you
accumulate AA over a few frames by varying the precise sampling point in the
3d world a little bit on each render) spiced up by oversampling just the
coverage buffer of the graphics card to get enough data to do higher quality
sample weighting on the AA for edges. ~~ I know that's kind of a sketchy
description, unfortunately the paper is not up yet for linking so I can't go
through it more academically;  however it will eventually show up on the
course website at ~~  The slide with all the gory details are now up at
[advances.realtimerendering.com](http://advances.realtimerendering.com/).  

## Fabric 50

What does it say about me in my old age that one of the pulse-pounders of the
show was a change in licensing terms? The [Fabric 50
program](http://fabricengine.com/fabric50/) is a new idea from the makers of
the [Fabric Engine](http://fabricengine.com/). Fabric is a high performance,
highly parallel computing engine that is intended to be used inside DCC tools
like Maya or as the core of a standalone app. The key goal is to put lots and
lots of power in a package that is usable by mortals so you can write a pretty
beefy tool without having to go back to school and learn all the dark arts of
multiprocessing and parallelism. The 50 program allows studios up to 50
licenses for free in an effort to get more tool makers using and evangelising
for the tech. I'm pretty sure I'll be dropping this one on my tech director's
desk soon.  

## The Dismal Science

Business-wise this felt like a slow year to  me. Not sure how much of that
comes from the size of the venue, how much comes from Hollywood types skipping
out on the cross-border travel, and how much is the result of the slow
implosion of the big-budget FX industry but the overall vibe among vendors was
fairly mellow.  
  
The advances in capture and acquisition tech are kind of like those in cell
phones: we're so jaded that we don't even notice the miracles anymore. I saw a
lot of mocap demos - it's the siggraph show floor, so ball suits abound - and
I was struck by how clean and lag-less the captured images were all round;
even the bargain stuff looks pretty damn good these days.  

  

There's no big 3d application booths anymore - the market has gotten so mature
(or monopolized, depending on your mood) that big stage shows and high power
demos you used to see are gone - the Autodesk booth was literally a 10 foot
cube featuring primarily  abstract artwork.  
  
One 3d app demo I did catch was a [Modo
801](http://www.thefoundry.co.uk/products/modo/latest-version/) animation
demo. I've been ambivalent about Modo's efforts to compete head on with the
Max/Maya juggernaught, but I was quite impressed by their animation workflow
(here's a video from their site, which covers a lot of the ground I saw in a
more bullet-pointy fashion:)  
  
  
I'm usually a bit suspicious of efforts to port the pen-and-paper workflow to
CG, since I don't see the point in mimicking the artifacts of one medium in
another. However the timing chart workflow is a fresh take on an aspec of
animation which has been badly overshadowed by the minutia of rigging, and I
hope it inspires everybody to kickstart the moribund business of animation
software. Speaking of which, I had an interesting talk with the founder of
French startup [Nukeygara](http://www.nukeygara.com/), who was showing an
interesting and unconventional standalone animation package called Akeytsu
(no, I'm not sure how to pronounce it either. It's _French_. Just roll with
it!) This vid gives a pretty good idea where this is going:  
    
  
I'm very curious to see how this one works out: I'm still waiting for somebody
-- please! -- to shake up animation the way Zbrush has (and continues to)
shake up modelling. Like recent GDC's it seemed like schools and training
programs took up as much floor space as vendors, which is a little scary: call
me selfish but I kind of miss the days when  our skills were rare and
esoteric.  Of course, the kids coming out of these programs are all waaaay
more sophisticated technically and artistically than I was at the same point
in my career, so it's good for the art form I suppose.  
  
Not for my ego, though.  

## The Meet Market

 The Job fair was a tad small this year -- like the show floor, it might just
be the distance from LA, but I'd say there were only about two dozen booths.
Many of these seemed to be BC based VFX houses as well: the hurly burly of the
old days with 4 hour lines at ILM and Pixar was not much in evidence, at least
not while I was there. I saw a handful of game companies (biggies like
Blizzard and smaller ones) but things seemed a bit subdued. Here's hoping
that's just an artifact of the time and place of the show.  Maybe there was
more action in private suites and hotel rooms, perhaps the internet has taken
some of the flesh-pressing out of the process. Still, a bit worrisome.  
  
  
  
  


