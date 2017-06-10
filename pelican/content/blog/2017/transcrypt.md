Title: How the other half lives
Date: 2017-06-09
Category: blog
Tags: python, web
Slug: transcrypt.md
Authors: Steve Theodore
Summary: An interesting way to get python into the browser
Status: Draft

Way back in 2013, when I was first getting this blog rolling, I spent some time investigating [different ways to get Python into the browser](blog/2013/Python_in_browsers).  In the intervening several years, Javascript has continued to spread its dark cloud of despair over the web like a digital Mount Doom, spewing depression and silent type conversions to every corner of Middle Earth.  

The much-hyped prospect of [WebAssembly](http://webassembly.org/) hasn't really panned out yet. There has been progress, and someday we'll probably get to the point where Python and other languages can be 'compiled' directly to WebAssembly -- but right now the tools and processes for doing it are too clunky and the performance of Python intepreters running in the browser remains unimpressive.  It's particularly tough because projects like [Pypy.js](http://pypyjs.org/) usually focus on recreating large parts of the entire Python ecosystem, which is great for familiarity but tends to impose a large startup cost -- you have to pay for all the things Python _might_ do, even if you're only using a fraction of them.  

One approach which has looked better in the last few years is the creation of dialects of Javascript which work around some of the language's quirks and syntax.  Effectively, you write in some _other_ language and then compile (or more precisely, "transpile") it into Javascript. This approach has two obvious benefits. First off, you get the universal applicability of Javascript -- once your code is transpiled, it's just another bit of JS so it will work in all those browsers without extra help.  Secondly, it's automatically interoperable with all the Javascript libraries out there, so you can tap into web ecosystem right off the bat. 

One of the first examples of this approach [CoffeeScript](http://coffeescript.org/), which looks and acts a lot like Ruby but gets turned into vanilla Javascript when compiled.  I did a couple of hobby projects with a more Python-ish transpiler called [RapydScript](http://www.rapydscript.com/).  For a lot of common cases Rapydscript really looks and acts like Python.  However if you're a moderately advanced Python programmer the two languages start to show increasing differences; the maintainer of RapydScript wants to optimize for raw Javascript performance, which means that many language constructs don't work quite the same way; the project's [list of "quirks"](https://github.com/atsepkov/RapydScript#quirks) ended up being a little long for my taste. 

THe most recent entry in the transpiler field is [Transcrypt](http://www.transcrypt.org/).  Like other transpilers it allows you to write "almost Python" (in this case, "almost Python 3.6") and compile it to Javascript.  For me, at any rate, it has a couple of interesting advantages to other entries in this space:

### Source maps
The most irritating part of using a Transpiler is debugging -- since there's not a 1:1 match between the code you wrote and the code that's being run, it can be a chore to understand how things have gone wrong.

Transcrypt makes this far less painful by generating [source maps](https://developers.google.com/web/tools/chrome-devtools/javascript/source-maps), which provide a map between the compiled code and the source. While this feature was created to support 'minified' JS (where all the whitespace is removed to allow for quicker downloads) Transcrypt does a good job of linking runtime problems in the JS version to the python source when debugging. In Chrome, at least, I can even get live preview of the values at a breakpoint:

![](screenshot showing source map)

For me this is a killer advantage over alternate transpilers, since I have to fix the problems in Python.  Occasionally the problems are in code that doesn't map easily to mine, in which case I see the Javascript debug code instead.  Transcrypt's JS is generally clean and readable, although (being Javascript) it still involves spooky scope magic that my brain refuses to process.

### Fine-grained control
There's a built-in tension in all transpiled projects.  A lot of core language features in Python have only approximate counterparts in Javascript; basic data types like lists (=JS Arrays) and dicts (= JS Objects) have subtly different behaviors. This forces the transpiler designer to choose between re-implementing the Python behavior in a custom JS object -- which is going to be slower than using the native JS types -- and creating false-friend code which confounds the user's expectations when run in the browser.  Rapydscript basically followed the designer's intuitions as to which behaviors to keep and which to diverge (perhaps not surprisingly, this has led to a rival [fork of the project](https://github.com/kovidgoyal/rapydscript-ng) from a developer who disagreed with some of those choices).  Transcrypt, by contrast, allows local control over the compilation strategy so you can opt in to the more expensive features using a compiler directive.  Which this puts some degree of burden on the developer it at least allows the choices to be made tactically.  So, for example, an ordinary Transcrypt function does not accept the `**kwards` syntax.  However you can enable it in functions where it's appropriate like this:

```

	def vanilla_function(*args):
		print ("*args are supported automatically")

	__pragma__('kwargs')

	def kwargs_function(*args, **kwargs):
		if kwargs['test']:
			print ("kwargs have to be enabled manually")

	__pragma__('nokwargs')

```

This is a bit cluttered, but at least its clear.

### Pythonic feel

This is subjective, but in general Transcrypt feels more "pythonic" than Rapydscript.  The compiler is actually written in Python and uses the native Python AST module, so it does not have to reinvent the semantics of the Python side of the language.  Most of the things that make Python a high-productivity environment (decorators, for example, and )


## Gotchas

* metaclass intance methds
* context managers
* hidden type conversions
* zip() bug

## Overall

I like Transcrypt pretty well so far.  It's not a complete web-ready Python.  However it's pretty good, and the code it makes is pretty speedy.  I banged out a version of Asteroids with Transcrypt and [three.JS](https://threejs.org/) which runs pretty smoothly on my phone with 3d graphics and all in a couple of nights.  Although the missing bits and pieces are irritating, I'm not altogether sure they're actually more irritating than the hassle of creating a working virtualenv with pyglet or pygame would be. And -- unlike pyglet or pygame -- once I've got my project compiled I can get it into lots o people's hands by simply popping it onto a web server without any of the [usual indignities of Python distribution]().  So it's not quite web-python Nirvana but it's pretty damn cool.

