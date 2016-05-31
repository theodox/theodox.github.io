Title: Unity 5 announced
Date: 2014-03-18 11:14:00.001
Category: blog
Tags: unity 
Slug: unity_5_announced
Authors: Steve Theodore
Summary: Unity 5 has been announced

So it looks like Unity [is announcing Unity 5 a bit early](http://unity3d.com/5).   It's a bit premature, since they are not done with the much anticipated 4.6 release (I've been wrestling with the existing, awful Unitry GUI system for months and I **can't freaking wait** to push it over the gunwale!)   
  
[![](http://unity3d.com/profiles/unity3d/themes/unity/images/pages/unity5/slider/doll2.jpg)](http://unity3d.com/profiles/unity3d/themes/unity/images/pages/unity5/slider/doll2.jpg)  

##   Key points of interest:

#### They are integrating the realtime GI middleware [Enlighten ](http://www.geomerics.com/)  

This is an interesting choice on a couple of levels; for one thing, I'm not sure most platforms out there are quite ready for realtime GI yet -- while you can _do_ it, as Crytek has been doing for a couple of years, it's hard to do it in a real production environment with real assets and (more importantly) real performance constraints.  I wonder how many current Unity users really need this?  Given that Unity perf generally lags more traditional engines thanks to the C# layer switch costs and managed memory, I'm a bit surprised they took on something so high end.   They advertise this as 'mobile ready' - I'll believe it when I see it. [SkyShop ](https://www.marmoset.co/skyshop)makes gorgeous pictures on an iPad  \- at around 20 fps for one object on screen. 


That said, it does make really pretty demos.

#### Physically based shaders. 

This is very interesting, but the devil is in the details;  physically correct rendering is a very appealing idea, and is hard to beat when done right; but the mental and artistic adjustment costs can be pretty significant if you've been doing traditional anything-goes rendering for a decade or more.  Will be very interested to see if they manage to popularize this approach.

  


#### A 64 bit version of the editor.  

How will this play out with the notoriously flaky GUID system in unity? And honestly, I'd take a 32 bit version that [integrated better with source control](http://tech-artists.org/forum/showthread.php?4584-Studio-Switching-to-Perforce-need-good-introduction-ramp-up) and was better adapted to collaborative work environments.  And '[save my goddam prefab](http://forum.unity3d.com/threads/48088-Prefab-saving-question)' would also be nice.  
   
On the other hand it looks like they're also making the editor more multi-core friendly, which gives me another reason to buy that [Mac Pro](https://www.apple.com/mac-pro/) I've been dreaming of. 


#### More direct control over blend weights in Mecanim.  

The recent addition of `CrossFade()` and `Play()` is already a big step forward, but this seems like even more belated recognition that the original was too doctrinaire. Who, exactly, thought that an animation system that _didn't let you tell it what animations to play_ was a good idea?  
  
The most exciting bullet on animation though is a real headsmacking 'Oh of course' things: the ability to add behavior scripts directly to animation states. This should go a _long_ way to enabling much more interesting -- and comprehensible -- procedural animation code. I'm _very excited._


#### Forking the web player between the old plugin and WebGL

you'll be able to publish to the traditional web player plugin, or to WebGL. Interesting to see how that plays out - I wonder if it will affect security sandbox issues with the web player. I'm still wishing it was easier to write real 3-d tools that could be published on the web, ala [clara.o](http://clara.o/).  
  
Of course, once you get into _interesting _stuff, like shader work, "write once run anywhere" gets a little more difficult (I've been battling stencil shader difference between PC, IOS and Android for a while now, so I'm prejudiced).  Will this make it even dicier?  

#### A new audio system.  

Not my area, but given the complaints I've heard from audio guys any change is probably for the good.  


  


