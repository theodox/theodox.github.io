Title: The Dismal Science : Technical Debt For Technical Artists
Date: 2014-10-05 22:45:00.000
Category: blog
Tags: techart, programming, industry
Slug: _dismal_science
Authors: Steve Theodore
Summary: Technical debt for tech artists
From the estimable [+Paul Vosper](https://plus.google.com/105359351421932966635)  an excellent discussion of [technical debt](https://medium.com/@joaomilho/festina-lente-e29070811b84): the long term costs you incur by prioritizing the here-and-now demands of everyday life over technical and architectural needs.

[![](http://www.darwinsmoney.com/wp-content/uploads/2011/07/debt-slave.jpg)](http://www.darwinsmoney.com/wp-content/uploads/2011/07/debt-slave.jpg)

[Tech debt](http://martinfowler.com/bliki/TechnicalDebt.html) is a great subject any developer to ponder, but it's particularly relevant to TAs because so many of us are in roles that are fundamentally reactive rather than proactive - we fight fires, solve mysteries, and provide workarounds for broken systems.  Keeping our artists happy and productive gives us an endless series of demands: there is always another button or hotkey on the backlog, or another new feature to try to massage into some kind of workable shapes.
The demands of doing good customer service often leave us with little time or energy to look at our own infrastructure. It's can be hard to spend a week rebuilding the way you build menus in Maya or how your file naming system works when you have a pile of post-it's taped to your monitor with new feature requests and bugs to track down.

The more-or-less inevitable result is that a lot of TA code devolves into a rat's nest -- not only is old bad code lying around, impeding growth, but it's constantly inserting itself into your newer, better code, entrenching itself further and making it harder to rationalize and streamline your toolkit. This, of course, will gradually degrade your ability to respond to new requests in future, putting you farther and farther behind user wants and needs...  TA life involves a lot of firefighting, and relatively little room for planning ahead or even keeping the cobwebs off the darker recesses of the tool shed.
Tech debt - like real world debt - is always piling up. As with real world debt the choice is not between debt and a completely cash-on-hand lifestyle: it's between reasonable debts and crazy ones.  Getting a mortgage is an investment: financing your vacation on a credit card with a 17% APR is crazy.  If you want to survive, it's a good idea to try to distinguish different kinds of tech debt so you can make smarter choices that will pay off in the long run.

## Bad debts

When you're looking at an old piece of code and trying to figure out whether it needs to be overhauled, start by figuring out if where your reaction comes from.  There's a difference between rebuilding a system that works and is functional and rebuilding one that's buggy. Anybody who spends a lot of time with old code  knows that aesthetics do matter: sometimes an old routine or function just begs to be fixed, not because it doesn't work but because it's just ugly: the code is wordy, the variable names opaque, the algorithms too esoteric or too ad-hoc.  Every time you step through it you feel like you need to shower.  Some old code is positively painful to read, even if the hypothetical alternatives are no faster, more capable, or bug free.

Sad to say, fixing code _just_ for aesthetics is a luxury purchase - the kind you should not buy on credit. For one thing, the time spent replacing functional code with equally functional but less embarrassing code could be better spent upgrading stuff that is, you know, _actually busted. _Or in making existing code more robust and capable. Or adding new features. For another, no upgrade is really free: the new code will come with weaknesses and flaws of its own.  If you're doing things right it should be an improvement: but it's an investment which will take a while to mature. So you should be careful before you squander your precious time on an upgrade. Figure out the payoff!

Here's another way to think about it: If you spend a lot of time supporting artists, you occasionally run into to the ones who spend an inordinate amount of time on managing their scenes. Sometimes you'll be struck by the sheer beauty of the top-down view of a level, or the elegant simplicity of the outliner layout for a character. These are admirable things, no doubt. If you've spent a lot of time supporting artists you've probably also observed that those perfectly groomed files are not always the best art in the game. For artists, organization is a means to an end, not an end itself. For tech-artist coders, the same is true about spiffy new programming paradigms and modish idioms.  They can be helpful - but they're not a substitute for the actual work.

That doesn't mean that ugly old code should never get touched: if the code is actually creating problems then the ugliness is just a symptom of a more serious problem that needs addressing.  In a way that would make the ghost of John Keats smirk, it's often true that  ugliness is a symbol of something morally wrong... ok, let's say _technologically _wrong... in your code.
Here are a couple of tests that might help you distinguish the merely ugly from the must-be-eradicated.

### Does it work reliably and predictably?

Obviously, code that doesn't work at all is going to get reworked.  However the tricky judgement calls often involve code which _sort of _works. Which works for a given value of working. The payoff for replacing the code depends a lot on how well you understand that that given value really is.
Maybe it's a function with a hidden side effect that works the first time it runs but not afterwards. Maybe it's a module that can only handle some kinds of geometry but fails spectacularly on others. Or maybe it's just code that nobody can figure out how to use correctly - it seems to lead otherwise sane TAs to create bugs because it's got complex setup requirements, unexplained dependencies, or works only when run at midnight on Walpurgisnacht.

The obvious symptom of unreliability is that it generates superstition. If you don't know why things break you start to develop theories which become increasingly insane (one of my artists used to insist with complete seriousness that this Max install would not work properly when his keyboard was too close to his monitor).  You can spot the real troublemakers when you start doing things like repeating the same function three times in a row just to make sure that it works, or juggling import statements to create exactly the right set of useful side effects.
These are sure signs that something is really wrong, wrong-wrong and not just  "it offends my higher techie sensibilities" wrong. This kind of stuff is the going to drive you crazy over time. When  every invocation has to be swaddled in try blocks and holy water, that's a good reason to take said old code out behind the barn.  Or, as the investment bankers say, it's time to write down your non-performing assets.

## Is it built to last?

Sometimes bad code is not really _bad_, merely misunderstood.
If a particular module or function becomes too ambitious, it can get entrenched in the codebase and leveraged into positions where it really doesn't belong. You might have a perfectly serviceable module for, say, parsing a particular file format.   Somebody later finds that another file format can be parsed in a similar way, with a few text substitutions and syntax swaps, and some fileModuleX is now being used to read files Y, Z, and Q  \-- all with their own odd special cases and gotchas.   Each one may be fine - but collectively you've got a snarled nest of assumptions and shortcuts that can't survive any significant changes: tweak a single function in the original module and the whole edifice comes tumbling down like a tranche of sub-prime mortgages.

Equally bad are cases where a big complex module is being used for a minor side-effect or trivial information.   Activating a huge, complex geometry handling module because one of it's objects has a cheap call to collect names of bad UV channels may work, but that doesn't make it goods practice.  It's particularly tricky if you're relying on outside modules, since you'll be hard pressed to know all of the side effects that may come from importing hundreds or thousands of lines just to save yourself writing a few dozen of your own.

A good way to spot code that has grown too important for it's own good is to look for radical mismatches between the names of functions and classes and their actual jobs. When you find yourself calling get_topology_order as a fancy way to count UV shells, or creating an AnimationMorpher() object just to figure out how if there are any keys on a particular object -- those are good signs something has gone wrong.  Another symptom of danger is importing modules without using them, relying on setup actions and initializations to make things right for you.  This can work as long as you have rigid control over the order in which your imports happens -- which is rather like saying that juggling chainsaws can work as long as you don't miss one.


All TA's have a soft spot in their hearts for the _Righteous Hack_ \- the clever bit of lateral thinking that can quickly upend an apparently insoluble problem and solve it in a jiffy with inspired ingenuity and bit of better-to-ask-forgiveness-than-permission swagger.  That's part of the job, and something to be proud of.  That doesn't mean it's the right way to conduct business day-in and day-out.   Saving the day with a last minute miracle based on duct tape and genius is a grand thing.  But once the immediate crisis is past it's time to go back, clean up the mess, and put something more credible in place for the long haul. When you see evidence of deliberate misuse -- or just of insupportable mission creep -- it's time to think about refactoring the original code into smaller, more targeted chunks that do just one thing at at time, instead of relying on side-effects for important behavior.

## Can it grow?

The last big indicator that old code is really bad, and not merely unfashionable, is when you find it's holding you back in other areas. You might have a perfectly serviceable tool today that a year from now will feel like a straitjacket.  In our business nothing is ever "done": we constantly have to adapt to new situations, and our tools need to be able to do the same.
Stagnation can happen for a lot of reasons. You might have code that's too dependent on obsolescent third party pieces -- a  binary that can't be recompiled for next year's Maya, or an out of date module that ties you to an old version of Python.  Or, you may have tied yourself up in knots by entangling your core code and your UI so tightly that neither can be changed without unpredictable ramifications in the other. When you find yourself figuring out how to find a particular button by name in order to 'push' it in code, because the function you really want is buried so deep in the UI that it's impossible to set up any other way, that's a good indication that you should break out the hacksaw and start cutting the old tool down into nicely modular code that can be cleanly used in more than one setting.
Your toolkit is like a garden: it a little ecosystem that needs to be tended and nurtured. If any part of it dies in place, it's easy for rot to spread.  Be a vigilant gardener.

## Pay it forward
[![](http://www.businesskorea.co.kr/sites/default/files/field/image/lending%20and%20investment.jpg)](http://www.businesskorea.co.kr/sites/default/files/field/image/lending%20and%20investment.jpg)
>I know this image is supposed to encourage investment. But is that... manure? I mean, growth is a metaphor, but really?

Despite all this, caution is still appropriate. In a crazy business like ours, "If it ain't broke, don't fix it" still seems like a reasonable stance.  TA's (particularly the more grizzled among us) are usually all too familiar with the gap between optimistic plans and the messy realities of execution, particularly in a line of work where emergencies tend to appear without warning and large projects are rarely suffered to mature in peace.
Nonetheless, there really are times  \-- I've tried to sketch out a few -- when the long term costs of bad code are going to add up.

Your choice is not between change and stasis - it's between steady, rational maintenance and unplanned emergency overhauls that come about when some weak point in the system fails at the wrong moment.   A bug which used to be a minor annoyance can be a major productivity killer in a new version of your DCC tools.  A new project may demand an upgrade, forcing you to prune out elderly binaries and orphaned tools.   You might even have to upgrade to Windows 8 -- stranger things have happened.

Change is inevitable, so you should always be on the lookout for the weak spots in your toolkit.  Be willing to do regular maintenance so you will have fewer massive overhauls  \-- it's far cheaper to clean your gutters every fall than to have to replace your whole roof every five or six years. Just as with any other form of maintenance,  keeping a codebase healthy  never takes the form of a single heroic intervention that fixes all problems for all time.  Instead, it's a steady pitter-pat of small scale changes that keep old code growing and evolving healthily -- or sometimes sending it off to live on a farm.

If you prefer the debt metaphor, smart maintenance is sort of like periodically re-balancing your portfolio: you adjust for changing conditions,  trim out under performing assets, and embrace new opportunities as they come up -- always knowing that what's working today may need to be revisited tomorrow, when the software equivalent of the Federal Reserve changes policy and all your carefully assured positions look silly.  And (to run that metaphor right into the ground) you need to maximize your investments two ways: by looking for growth opportunities and by dumping laggards that are dragging your portfolio down.

Regardless of which similes you prefer, the basics are simple: keep your eyes open and look for small, low costs ways to improve things. When small fixes aren't enough, do some careful cutting and patch in higher quality code.  Except in extreme cases this won't involve much drama or even much technical brilliance: just good workmanship,  attention to detail, and an eye to keeping future maintenance costs as low as possible.

Fortunately a lot of modern development practice embraces the notion of constant change; as the always-on web development has become ubiquitous methodologies have evolved to keep the chaos at bay.  Here are few important tools that a modern TA can borrow from other kinds of programming to make to make the process of overhauling old code less intimidating and error-prone.

### Agility

_"Agile"_ is the most overused, least useful word in software (or at least, in software blogging).  It means too many things to too many people to be a reasonable answer to anything anymore: as a practice, it's so over-defined it's impossible to define.
As a goal, however, agility is an obviously good thing to strive for.  Don't make plans that stretch out into the indefinite future: focus on achievable goals in the short- and mid-term. Don't imagine fixing your code as a giant, ultra-complicated process that can be planned down to the tiniest detail. Instead, visualize it as doing just what we always do: dealing with whatever comes up, using the resources available, and working in small pieces that do clearly defined things well instead of grand systems that won't come together until the fabulous future arrives.

### Constant refactoring

In an agile world you're constantly correcting course - which means not just writing new code, but fixing the old as you go.  In a world that has become agile-obsessed, we can at least be glad that there are a wealth of tools designed  for cleaning up and rationalizing code: changing names, moving things around, and partitioning big ugly functions into neatly scoped smaller ones can all be done  efficiently with modern tools.

The debatable border line between code that's just ugly and code that's actually bad can be straightened out considerably by just cleaning up names and reorganizing the code into tighter scopes.  This is a Good Thing.  It's a direct attack on one of the biggest sources of code entropy: name drift.  As the old programmer's saw has it:
_Programming is easy._
_Naming things is hard._

If you haven't gotten familiar with the refactoring tools in your editor, you should.  If the whole concept is unfamiliar, [here's a pretty good little video showing how refactoring works in the Wing IDE](https://www.youtube.com/watch?v=OFIiFaBulHg).  There is similar functionality in [PyCharm](http://www.jetbrains.com/pycharm/) (my favorite),  [Eclipse/Pydev](http://pydev.org/), [PTVS](http://pytools.codeplex.com/), and [many others](https://wiki.python.org/moin/IntegratedDevelopmentEnvironments).  You can achieve the same thing with the [rope](http://rope.sourceforge.net/) library, although a good IDE seems to me like a great way to buy convenience for not much money.

### Test Driven Development

TDD, for those readers who haven't gotten the gospel from [+Rob Galanakis](https://plus.google.com/112207898076601628221), is a coding practice where you build up your codebase along side a set of tests: short programs which exercise your code to make sure it's doing everything it promises to do.  It's a classic programmery hot-potato topic, with some folks who swear by it, others who naysay, and a lot of folks in the middle who think it's an interesting idea but never quite run with it.

I'm way too lazy to take a big stand the _right_ way to do TDD, or whether or not TDD is_ the_ right way to do software; but I can make one statement with complete certainty: The more tests you have, the less scary it is to make changes to your code.

Most TA's are pretty smart folks, they anticipate and catch the obvious problems that come with any serious change to existing tools. The really scary stuff is the _unanticipated_ changes, because those are the ones which get you from behind.  Say you clean up some old file handling code and make sure that it always returns consistent slashes. You'll feel great -- tend that garden, baby ! -- right up until the day you find another function that counts left-slashes to test for path depth and now returns garbage.  Thats' the sort of thing that tests are far better at catching than even the most prudent bit of prior planning.

TDD is not  cure-all for bugs or a guarantee that nothing will ever go wrong in your code. It does, however,  make changes appreciably less scary and therefore it is a huge aid to maintaining your code base.   In the world of technical debt management, testing is a blue chip investment.

### Good release management

There's one  last precaution you need to be sure that tending your garden doesn't let loose too much havok on your users.  You need a clear and well defined release policy.

Nothing makes you more timid, more unwilling to fix problems, or more unpopular with your users than dropping every line of code you change directly into your artists' laps.  _You_ need the ability to experiment, make changes, and to use source control for your own sanity.  _They_ [need to be able to work without worrying that every sync could put an end to their working day.](http://tech-artists.org/forum/showthread.php?3752-Best-Way-to-Share-Your-Scripts)

At a minimum, this means you have some kind of staging area where TA's and maybe carefully select guinea pigs can work on bleeding edge code while the rest of the team goes on with safe, stable working tech.  If you've got a robust set of tests, you can automate the process by setting up a build system that tests and packages changes as you make them.  If you've got a big team you may even be able to enlist an actual tester to make sure that things are stable for the users every day. No matter how you approach it, you must have have a solid firewall between your efforts to keep the codebase happy and the users, who don't know or care about your technical balance sheet.

Circling back around to that damned financial metaphor, technical debt is not something to be embraced heedlessly, but neither is it something you should shun at all cost.  All your daily decisions have to be made with two different goals in mind: satisfying the necessities of the moment and staying solvent for the future,  Alas, much like managing money the only incontestable advice is the most banal: work hard, think ahead, don't take foolish risks but don't keep all your money under the mattress.   A solid working environment for your artists isn't an artifact you can create and forget; it's a dynamic system that grows and changes over time.  Its never "done."  Your main job is to keep it progressing.

Now, that all can be a bit frustrating, if you think of yourself as a problem solver who just 'solves' problems they way you solve a crossword puzzle - it's no fun to work your way through the Sunday Times while somebody's sneaking in and changing the clues as you move along.

 On the other hand, think of the job security!
