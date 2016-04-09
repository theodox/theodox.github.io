Title: Wraptastic!
Date: 2015-07-12 14:34:00.003
Category: blog
Tags: , , , , 
Slug: Wraptastic!
Authors: Steve Theodore
Summary: pending

  

## [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#the-wrap-
up)The wrap up

The beauty of working with code, even really simple code, is that you can
build your own little universe out of bits and pieces contributed by thousands
of other people – all without paying a dime or even asking them for help. From
sharing a script off of CreativeCrash to downloading a huge open-source
behemoth like Apache, any reasonably plucky individual can today make stuff
that actually involves the work of thousands of anonymous others. It’s really
quite a remarkable evolution in human history that so many people voluntarily
give away their work for nothing, and (whatever else you can say about the
internet era) it’s something to be proud of participatng in.  
On the other hand…  
Well, Say you are an Amish farmer and all your neighbors showed up to help you
raise your barn, you’d certainly be grateful. But you might still be pretty
annoyed if Hans from next door hung your barn doors so they stuck in the
summer heat. Maybe old Hans worries more about keeping the barn warm than you
do, so he prefers a tight seal: but that’s small comfort when you’re heaving
on that handle in a muggy Pennsylvania morning.  
![barn raising](http://notonbluray.com/blog/wp-content/uploads/2014/04
/Witness-barn-raising-scene-Bluray-screenshot-3.png)  
  
The internet abounds in excellent – and, amazingly, free – tools to help make
your life easier. But they all started life as tools to make somebody else’s
life easier. If your needs don’t line up perfectly with the needs of the
original author, you’re likely to get a little _[gereizt](http://www.dict.cc
/deutsch-englisch/gereizt.html)_.  
  
The fact is that nobody writes all their own stuff: we all use other people’s
code all the time (and, as sharing becomes more and more ingrained in coding,
that’s only going to increase). All that sharing means that we constantly have
to work with libraries and APIs that are useful and free and for which we know
we should be grateful… but – like that sticky barn door – they drive us
absolutely bonkers.  

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#wrap-up)Wrap
up

Not surprisingly, almost everybody ends up writing _wrappers_: code to help
ease those nice-but-imperferct tools and API into a something that feels a
little more natural. If you spend a lot of time on [TAO](http://tech-
artists.org/) or coding forums where people swap tips and advertise their
wares you’ll see a huge variety of wrappers for all sorts of tasks: indeed,
the wrappers often seem to outnumber the actual functional bits. Whether you
call the job making things ‘more pythonic’ or ‘more functional’ or ‘cleaner’,
its something we all feel compelled to do (and to
[share](https://github.com/theodox/mGui)) from time to time.  
It’s also easy to get cynical about wrappers. You see so many – and so many of
them just taste-driven syntactic variations on each other – that veteran
coders often reflexively shrug and ignore them. This is particularly true in
Python land, where the malleability of the language encourages a certain
degree of experimentation and re-casting. Because you _can_ adapt Python to
suit your tastes, the temptation to do so even when it’s not actually getting
you much beyond style points is hard to resist.  
The net result of all this customization and adaptation is messier than
Christmas morning: wrappers everywhere. Whatever simplifications each
individual wrapper gives you, the aggregate effect of so many different extra
layers is overwhelming. At several times in the last decade I’ve sworn off
wrappers and vowed to stick with vanilla python, straight-up maya.cmds and
simple, linear code. A good code archaeologist could troll through my history
and find several repeated periods of growth and die-offs in the wrapper
ecosystem, like fossils trapped in shale.  
![where's pymel?](http://www.lparchaeology.com/prescot/images/156.jpg)  
_Where's pymel in there?_  

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#wraptors)Wra
ptors

Wrappers, though, never really die off like the dinosaurs: they, in fact, more
persistent as the cockroaches. And there’s a lesson in that.  
Consider a classic case of wrapper-iteis: a system for [making maya GUI less
of a pain](http://techartsurvival.blogspot.com/2014/02/rescuing-maya-gui-from-
itself.html). Everybody writes that one at some point in their TA career (I’ve
done it 4 times to my certain knowledge, not counting one-offs and half-assed,
abandonware). When somebody feels compelled to spruce something up that much
it’s a sign.  
Sure, most gui wrappers are just a reaction to the clunky, wordy way that Maya
expects us to pop up a window or make a button. And sure, most of those
wrappers (some of my own, I hasten to add) really aren’t much better: they’re
just shortcuts that cut down on the carpal-tunnel of
`cmds.textField(fieldname, q=True, text=True)`.  
Sure, saving keystrokes is nice, but over the life of a piece of code the time
spent typing is a tiny fraction of that spent reading, debugging and
refactoring: that you could (and probably should) just bit the bullet on. But
so many persistent, repeated efforts to fix a problemare a symptom that
something worse than wordiness is the problem. Wrapper-itis really runs
rampant when the toolkit that is simply not adequate to the job at hand. If
you have to spend a lot of time thinking about the implementation details
_instead_ of the problem you really want to solve you’re not just wasting
keystrokes: you’re wasting precious thought and time.  
So I’ve been trying to soften my anti-wrapper stance. Sometimes it’s better to
actually solve a recurring problem instead of papering it over; sometimes it’s
worth taking the time to be in a position to write the code you _need_ to
write instead of the code you’re _forced_ to write. Sometimes.  
Which of course raises the question of how you can identify those situations
and distinguish between a real need for better abstractions and a plain old
peevish desire to avoid boilerplate.  

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#wraptitude)W
raptitude

The prime way to distinguish between a ‘wrappable’ problem and a purely
syntactic one is to consider the needs of the person who’ll be picking through
your code after you’be been run over by a bus.  
![](http://i.ytimg.com/vi/y_PrZ-J7D3k/maxresdefault.jpg)  
When your replacement comes to look at your code, will they see something that
seems to clearly express the problems you were trying to solve? Or just code
that clearly expresses your preferences for a particular set of formatting
options and code idioms?  
Here’s a little bit of code that reads some information from a database in
order to add some ‘credits’ to a time account:  

    
    
    def replenish(user):  
        if user is None:  
            return False  
      
        with connect_db() as db:  
            repl = db.execute("SELECT replenished FROM users WHERE name LIKE ? AND DATE (replenished) <  DATE ('now')", (user,))  
            recent = repl.fetchone()  
      
            if recent:  
                daynum = db.execute("SELECT strftime ('%w', 'now')").fetchone()[0]  
                daynum = int(daynum)  
                repl_amount = db.execute(  
                    "SELECT sun, mon, tues, weds, thurs, fri, sat FROM replenish WHERE users_name LIKE ?", ( user,))  
                refresh = repl_amount.fetchone()[daynum]  
                cap_amount = db.execute("SELECT cap, balance FROM users WHERE name LIKE ?", (user,))  
                cap, balance = cap_amount.fetchone()  
                new_balance = min(cap, refresh + balance)  
      
                db.execute("UPDATE users SET balance = ? , replenished = DATE('now') WHERE name LIKE ?", (new_balance, user))  
            log(db, user, "replenished with %i credits" % new_balance)  
    

the basic logic is pretty simple. Stripped all the fluff, you merely need to:  

  * connect to the database
  * ask the database the last time the user was topped off
  * if the user hasn’t been replenished today, get the amount due
  * add the amount to the user’s account

  
That’s just four basic ideas. but it takes more than 20 lines to express them.  
Far worse, the key logical linkages of the operation are implied, not
stated.For the code to make real sense you need to know or deduce that the
_users_ table has a field called _replenished_ which stores the last day when
the user was topped off; that the ‘replenish’ table has seven fields
containing the top-off numbers, arranged Sunday throguh Saturday; and that the
user table stores both the maximum number of credits to store and the current
balance of credits. The implementation of our simple, 4-step idea only makes
sense with all of that special knowledge. It’s further obscured by time saving
shortcuts, like using the actual column index in a database table to check
today’s value. That may save a couple of lines but it renders the code even
harder to parse. And, of course, there are syntax quirks big and small,
particularly relating to the creation and formatting of the SQL.  
This code works fine; it’s even fairly economical and readable for what it
does (for a given value ‘economical’) But it’s not the kind of thing you’d
ever want to _inherit_; it makes sense to me, because I wrote it and I
remember (at least today) what I was thinking about when I did. But some
future inheritor (heck, even me a year from now) will have to think long and
hard about what really ought to be a simple process. The whole thing is bogged
down in implementation details that _obscure the intent_ of what’s going on.
Really good code often reads almost like pseudo-code. This does not.  
To illustrate what a good wrapper can do, here’s the same code using an
‘[object relational mapper](https://en.wikipedia.org/wiki/Object-
relational_mapping)‘ called [peewee](https://github.com/coleifer/peewee): it’s
a wrapper around the SQL backend that map database operations onto classes and
allows you to focus on the logic instead of the mechanics:  

    
    
    def replenish(user):  
        if user is None:  
            return  
        with connect_db().atomic():  
            today = datetime.now()  
            today_name = now.strftime("%A")  
      
            updatable_user = User.get(name=user, replenished  < today)  
            today_update = Replenish.get(name = user, today_name > 0)  
            if updatable_user and  today_update:  
                refresh = getattr(today_update, today_name)  
                new_balance = min(updatable_user.cap, refresh + updatable_user.balance)  
                updatable_user.balance = new_balance  
                Log.create(user= user,  message = "replenished with %i credits" % new_balance)  
    

That’s a significantly cleaner bit of code to read. It still requires some
outside knowledge but the intention is much more clearly expressed and the
message isn’t drowned out in quotes and parens. An ‘offscreen’ benefit, given
the way peewee is structured, is that backtracking to the `User` and
`Replenish` classes would tell the rest of the story pretty straightforwardly
without a ton of comments. Only a handful of lines are needed to munge data
into the right forms, and the code almost _reads_ like the summary.  
That’s a good example of how wrappers can help: saving keystrokes is nice but
clarifying the real _meaning_ of the code is priceless.  

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#wrapola)Wrap
ola

Well, maybe not exactly price-_less_. All wrapper code comes with a cost:
there are new rules to learn and, probably, new bugs to encounter. If the
wrapper uses odd conventions, unusual data formats or is simply slower than
hand rolled code it may still be a bad bargain. Nonetheless, this example
shows wrappers can be more than just a protest against awkward syntax and
API’s that don’t match your taste. Ultimately wrappers are a perfect microcosm
of what all coding is about: the search for a clearer understanding of the
problem you’re trying to solve.  
So if you’re thinking about writing a wrapper, ask yourself this: does the
code you want to write teach you something about the problem your solving? Or
does it just save you a few keystrokes? Typing is a pain, but you’ll spend a
lot more tine looking at your code than you ever will typing it. So don’t
focus on just counting lines or syntax: focus on whether the wrapper helps you
understand the problem better. If the wrapped code reads like a description of
your thought process, you’re on the right track. If it’s just getting you back
to [that TwitchTV stream](http://www.twitch.tv/undeadlabs) on your second
monitor a few minutes earlier it might not be worth your time.  

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#ps)PS

I used an ORM for my example because it provides such a powerful example of
code that’s not bogged down in syntactic complexities. There is, however, a
classic internet flame war about ORMs that I’m glossing over, with nerd rage
aplenty for friends and foes of ORMs. Background
[here](http://martinfowler.com/bliki/OrmHate.html) if you care.


