Title: A PID controller for Unity
Date: 2014-10-27 23:01:00.002
Category: blog
Tags: 
Slug: A-PID-controller-for-Unity
Authors: Steve Theodore
Summary: pending

Outside of work I've been toying a lot with [BrickPi](http://www.dexterindustries.com/BrickPi/), which allows a [Raspberry Pi](http://www.raspberrypi.org/) to control [Lego Mindstorms](http://www.lego.com/en-us/mindstorms/?domainredir=mindstorms.lego.com) sensors and motors.  One of the neatest ideas I stumbled on in my reading is the [Proportional Integral Differential Controller](http://en.wikipedia.org/wiki/PID_controller#Droop), or 'PID' for short. It's a nifty idea with a lot of possible applications in games, particularly in animation.  
  
A PID is an algorithm for adjusting a process so that it converges on a desired outcome: imagine a thermostat, for example, that controls heaters and air conditioners to keep a constant temperature.  PID's were originally invented for automatic steering of ships; nowadays they are in all sorts of semi-automatic control systems from thermostats to autopilots to [Segways](http://www.chrismarion.net/index.php?option=com_content&view=article&id=122:the-segway-theory&catid=44:robotics).  
  
Here's [a great video on the background theory ](https://www.youtube.com/watch?v=XfAt6hNV8XM)of PID controllers.  But on a high level here's how it works:  
  
The PID controller uses three different strategies simultaneously try to nudge a process in the right direction.  


  1. The **proportional** component applies a direct fix to the process; the strength of the correction is proportional to how far off the signal is from the target value.(need correct names) 
  2. The **integral** component applies a fix based on how long the signal has been off. Essentially the integral fix will be more powerful if the signal has been away from the target for long times.  
  3. The **differential ** component applies a fix which scales based on how quickly the error is diminishing. It's useful for preventing overshoots: as the corrections take hold and the signal approaches the target more quickly, the correction will scale down.



### Basic code

I've put the basic code for the PID controller [up on GitHub](https://gist.github.com/theodox/3c956ccffd3d5d060b15).  Since it's in C# it's fairly self-explanatory, but here's some basic highlights of how it's put together.

  


The Monobehavior component itself is called **Follower**, and it's really just example of how a PID controller could be rather than a complete system in it's own right. When applied to a game object, a Follower will try to 

