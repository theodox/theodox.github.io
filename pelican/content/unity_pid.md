Title: A PID controller for Unity
Date: 2017-01-01
Category: unpublished
Tags: unity, programming
Slug: unity_pid
Authors: Steve Theodore
Summary: A quick introduction to the Proportional-Integral-Differential controller with a Unity implementation

Outside of work I've been toying a lot with [BrickPi](http://www.dexterindustries.com/site/?product_cat=brickpi-lego-for-raspberry-pi), which allows a Raspberry Pi to control [Lego Mindstorms](http://www.lego.com/en-us/mindstorms/?domainredir=mindstorms.lego.com) sensors and motors.  One of the neatest ideas I stumbled on in my reading is the Proportional Integral Differential Controller, or 'PID' for short. It's a nifty idea with a lot of possible applications in games, particularly in animation.

The PID algorithm is actually a pretty old trick - PID's were originally invented for automatic steering of steamships back in the 1890's (a helpful reminder, if you need one, that people were pretty damn clever even before the internet). Nowadays PIDs can be found  in all sorts of semi-automatic control systems from thermostats to autopilots to Segways.  Although the original implementations are mechanical, nowadays the overwhelming majority of PIDs are done in software, because if you take away all the fancy terminology they are just a tool for trying to fiddle some numbers to get other numbers to come out where you want them to be. Those numbers could be the temperature of your home being adjusted by the output of your air conditioner, the angle of a rudder on a ship trying to compensate for winds and current, or the force of a servo motor trying to keep a Segway from [doing something embarrassing](https://www.youtube.com/watch?v=F8oKJbU5MCQ). 

## PID Basics

In all of these cases, the basic facts are simple. There are only 3 numbers to understand:

* The **output signal** is the number that represents how things are right now: the heading of the ship, the angle of the segway, or the temperature in the bedroom.  The neat thing about PID controllers is they don't care *why* the number is off - they don't require any understanding of the mechanism that causes the output signal to change, only what the current state of the output it. This makes them a great general purpose tool.
* The **target** number represents how we want things to be: the way we should be heading or the right temperature or whatever. It's worth mentioning that the target and the output only make sense if they are measured in the same way  - the units could be degrees of angle or degrees Farenheit or miles per hour, but they need to be the same for the output and the target.
* The **error** is the difference between the output signal and the target.  If whatever we're trying to control is right on track -- the ship's heading straight or the room is a comfy 70 degrees -- the error is zero. Larger numbers mean bigger offsets. In most cases the error can be positive or negative - it can be too hot or too cold, and the value of the difference affects how we can try to correct it.

## Controlling the system

The PID controller's job is to track that error value and use it to nudge the process in the right direction. If the ship is heading too far to port, nudge the rudder starboard. If the room is too hot, turn down the furnace. If the Segway is falling over, have a good laugh at the poor joker who just fell off... er, _apply more torque_ to push it back toward equilibrium.

Now, it's easy to see how you could try to fix single-variable problems like ship heading or temperature with a really dumb algorithm like "if it's cold, turn up the heat -- if it's hot, turn it down."  However most complex systems don't work in a very linear fashion: ships get pushed off course by winds and waves; furnaces take a while to heat up and longer to cool down; Segways have to accomodate people of all different shapes and sizes.  This means that the same inputs might not make the same responses - adding 1 newton of torque to the Segway will produce very different results for Mike Tyson and Natalie Portman _I'd add, parenthetically, that googling [short celebs](https://www.google.com/search?q=short%20celebs) is a revealing experience. You're being **lied to** by the Hollywood machine. Wake up, sheeple!_


This is why the PID is so handy. It uses 3 different ways of compensating for the delta between the current output and the target. These work together to produce stronger corrections when whatever you're controlling is way out of line, but gradually diminish the correction in order to damp down the wild swings which would come from over-correcting.  The balance between the three factors is very important to the behavior of the system (in the commercial world, it's a whole specialized math discipline of its own). Luckily they are based on fairly simple concepts so they can be managed without a math PhD.

The Proportional Integral Differential controller has three basic correction types, known (surprise) as the proportional, integral and differential components.  Here's what they do:

The **proportional component** is based only on how large the current error is. If you have an error value of X, it wants to apply a correction of -X to the result.  When the proportional control is cranked very high, the output will be clamped very tightly to the target. Unfortunately this is not usually what you want in games - it's trivial to simple position-constrain one object to another or set a number. 

The **integral component,** on the other hand, applies its fix based on how long the signal has been off. This means integral fix will be more powerful if the signal has been away from the target for long times - think of a ship that has been pushed off course by a strong wind - if it's been heading the wrong way for a while it will need to correct far more.

The **differential component** applies a fix which scales based on how quickly the error is diminishing - if the signal and target are converging fast, the differential will fade out; if they are diverging fast it ramps up. The differential control is useful for preventing overshoots. It also provides a little bit of anticipation: the proportional and integral corrections only know that you are off-target _right now_, where the differential essentially predicts that you will be on target soon, so maybe you can relax a bit.

The interaction between these three systems is far more subtle and interesting than this simple, bald description conveys. Despite the incredible simplicity of the algorithm (see below) the behavior can be rigidly mechanical or lazily organic, highly reactive or ponderously slow. Plus - unlike more complex control mechanisms - PIDs work on a huge range of different applications with no special knowledge.  The three components allow this fairly dumb bit of code to react to the present (the proportional), the past (the integral), and to some degree the future (the differential). Not bad for a dozen or so lines!

I got interested in PIDs for making self-balancing robots in Unity, using them to control joint motors. However they are also an interesting option for animation, and at some point in the future I'd be interested porting this code to Python to see what I can do with it as an animation rigging component. The genius of the PID algorithm is that it doesn't care what the numbers _mean_ - the error value could be revenue numbers and the response could be controlling the discount on your Steam sales, or it could be measuring joint angles and controlling physics forces, or it could be adjusting the twist on a shoulder fixup joint to avoid pinches. The trick is simply to find a consistent way to measure the difference between what you want and what you've got. 

##Basic code

I've put the basic code for the PID controller up on GitHub.  Since it's in C# it's fairly self-explanatory, but here's some highlights of how it's put together.

The MonoBehavior component itself is called Follower, and it's really just example of how a PID controller could be rather than a complete system in it's own right.  All this one does is to follow a target transform, trying to match it's Y component. The Follower MonoBehavior is really just a wrapper around a modular PIDController class : it feeds in the Y-axis delta to the PID as an an error value, and uses the response coming back from the PID to add or remove thrust. In a real application would probably be used to drive joint motors or physics impulses, but I kept it simple so as not to distract from the PID code. 

It's the PIDController class which does all the real work. It has 3 important public fields which control the relative power of the three correction techniques (in the reference these are usually called the _gain_ or _coefficients_). The algorithm itself (stripped of all those impressive calculus symbols in the [Wikipedia article](http://en.wikipedia.org/wiki/PID_controller) is as simple as:

1. **Get the error** the difference between where the input is and where we want it to be. In the code that's calculated by the Follower class and just passed to the PID. This version includes an optional term called 'Droop', which introduces a user-controlled amount of randomness to keep the solution from oscillating when the error and the integral get into lockstep.  
2. **Add the error** to the accumulated error value stored in `_integral`. 
3. **Check how quickly the error is changing** by comparing the new error value with the last two (stored in `_backOne` and `_backTwo`).

Once you've got all three kinds of error you just multiply each one by the corresponding gain value and return the result (known as the `_Response`). 

Clearly, the whole thing is simple -- so simple that it falls below my mildy-comic-metaphor threshold.  However there's one subtlety which drove me crazy for a while and is worth pointing out.  **Error** has to be a **signed** value - that is, you have to be able to have *negative* error, or overshoot of the target, as well as the obvious undershoot errors.  If you don't have both positive and negative error values flowing in, your integral component will shoot off to infinity pretty quickly!  In this example, just measuring the distance between the follower and the target wouldn't work - that's why the example uses the difference on the Y axis rather than just measuring the distance.  In a real application, you'd need to figure out what 'error' means: it could be over/under-steering, going to fast or going too slow, or some other measure of 'correctness.' 



