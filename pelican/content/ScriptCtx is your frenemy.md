title: ScriptCtx is your frenemy
category: Blog
tags: blog, maya, python
date: 2014-03-01


You may have noticed the little poll I ran in the sidebar during   February and March: the question about `scriptCtx` in Maya.  

The poll was hardly scientific: with a sample size of 31 hardy souls it has even less statistical validity than the average re-tweeted infographic.  Still, it certainly jibes with what I’ve gotten in conversation, namely, _nobody knows what the damn thing does. _

Actually, _what_ it does is really simple. ScriptCtx is just a wrapper that allows you to collect sets of selections in series and then run a script on them.  It’s hardly rocket science… conceptually.  "Select 3 nurbs curves, then do this to them" or "select one polyFacet and one curve to do an extrusion."  We’ve all done it, just usually with buttons:  the job of `scriptCtx` is to make those sequences button-free.

Unfortunately this command is a  grand-prix champion in the incomprehensible design sweepstakes.  One look at the manual page is enough to scare away most TA’s: the fact that 86% of "survey" responsdents either have never heard of the command or don't use it.  

I’m not going to say folks are wrong to be turned off, because I  am morally (or at least aesthetically) outraged every time I sit down to look at the stupid thing.  However it does have its uses, and working through the giant mess one piece at a time is a good excersize in using Python to arm-wrestle Maya into submission.

## Basics

Here’s the example that comes straight from the Maya docs:

```python
cmds.scriptCtx( title='Attach Curve',    
		totalSelectionSets=1, fcs="select -r $Selection1; performAttachCrv 0 \"\"", 
		cumulativeLists=True, 
		expandSelectionList=True, 
		setNoSelectionPrompt='Select two curves close to the attachment points', 
		setSelectionPrompt='Select a second curve close to the attachment point', 
		setDoneSelectionPrompt='Never used because setAutoComplete is set', 
		setAutoToggleSelection=True, 
		setSelectionCount=2, 
		setAutoComplete=True, 
		curveParameterPoint=True )
```

That's a lot of verbiage for

``` python
# prompts the user to select two curves to attach.
```

But that's all it does.

Here's what really happens: 

1. `totalSelectionSets=1` tells the command we're going to pass only one selection group to the final command.
2. `fcs="select -r $Selection1; performAttachCrv 0 \"\""`  sets up a mel command to run when the selection is done
3. `cumulativeLists=True, expandSelectionList=True` tells the command to 
4. the `setSelectionPrompt` and `setNoSelectionPrompt` tell maya a message to print in the help line to nudge you in the right direction
5. The other flags tweak the behavior so that, in this case, the tool will complete itself once you select two ro more curves.

