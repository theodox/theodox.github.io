title: mtasks
category: Blog
tags: blog
date: 2014-01-01

Maya is coming up on its twentieth birthday this year.  That's an impressive run for a piece of software, and it definitely validates some of the key design decisions made back in the 90's.  

However, the old gray mare is a little long in the tooth these days.  Many of the key changes in computing that have take place since the days of Windows 95 are not fully integrated into the Maya ecosystem. In particular, the core of Maya remains single-threaded:  only the main Maya thread can touch your maya scenes.  

If you've ever tried to run multiple tasks simultaneously in Maya using Python threads, you know it's a giant pain in the proverbial patootie.  If you don't obsessively wrap every call to `maya.cmds` or PyMel with `utils.executeDeferred()` you will be plagued with mysterious, inconsistent bugs - when you're not actually just hard-crashing your machine. Sometimes -- like when you've got a big long-running task you need to kick off and monitor -- the pain is worth it it.  There are a lot of little jobs -- particularly things where a bit of concurrency would make your users' experience a bit smoother, such as flashing messages in a gui window -- where the hassle doesn't justify the extra work and increased risk of bugs.
