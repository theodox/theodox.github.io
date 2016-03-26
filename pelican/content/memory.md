title: memory
category: Blog
tags: blog, ta, programming
date: 2015-03-15
	

We tend to be the kind of people who throw themselves into things -- we live for the joy of problem solving. So when we're really grappling with the intricacies of todays disaster, we immerse ourselves in it.  We tear it apart and inspect all the little moving pieces till we understand it well enought to duct-tape it back together again. 

Along the way, that attention to detail and mastery of nuance tends to make us think we know it all.  But -- a shock, I know -- we don't.  More to the point, we might now it all _for the moment_.  But we'll dump that knowledge to make sure we have room for our encyclopedic knowledge of tomorrow's problem. And next week's. And next months.

In short, we're constantly flushing our caches.  Unless you're stuck in a rut, doing the same thing every day, you're constantly learning new little things for your current problem and silently shelving the knowledge you aquired for your last.

This is one reason why good code comments are so important. Sure, comments rot just like code.  But a couple of well-placed notes about how and why the code looks the way it does can save future you a lot of time when many layers of memory recycling have left you completeley oblivious about what the hell past you was up to.  I can easily think of a couple of embarrassing occasions where I've literally chased my own tail -- done something non-obvious because of a wierd maya bug, then come back six month later to 'clean up' my 'ugly code' and of course hit the exact same bug again.  

Of course, good comments don't have to have high literary quality, they don't need to cover every variable and for loop, and they certainly don't need to be overwhelming: what they should be is notes to future-self that will help him or her revive all the fading memories which seem so obvious today but which will be utterly erased before the next season of _Silicon Valley_ is released.

Which brings me, by a _very_ roundabout route, to what I actually set out to talk about: a perfect case in point.  I was noodling around with a system that needed to fire events for maya attribute changes: basically, a way to make `attributeChanged` scriptJobs that were easy to start, stop and restart.  So I did a little googling and... 

Yep. I'd already written it. I'd even [put it up on Github](https://github.com/theodox/attributeEvents).

In my defense, I realized in retrospect that I had cancelled the project at work that made it necessary the first time: I did the work on the system, got it ready to go, and then decided that there was a simpler way to solve the problem without all those attribute-change scripts anyway. Nonetheless it's a perfect illustration of how thoroughly one's short-term memory cache gets flushed -- and of the importance of leaving good comments. At least when I found the damn thing the readme that Github makes you put up reminded me how it was supposed to work (as an aside, it's a great reason for putting your stuff up on GitHub or similar forums: knowing that other people will be looking at it forces you to clean up and document more than you would if you just decided to shelve a project).

So there you have it: an object lesson in the importance of clarity in tools development _and_ a free module for messing around with AttributeChange scriptJobs!


