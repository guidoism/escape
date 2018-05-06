---
layout: default
title: Proposal 3 — A Soft Gooey Center
---

The heart of a computer should be friendly and playful -- A place for experimentation.
A place with no thorns!

One should have something like a REPL and Browser to dive into tables, objects, and stuff.
Everything should start from here. Only after I'm happy with something I've done will I commit it.
I can't accidentally ruin my good state in my soft gooey center -- That should give me
the confidence to experiment. If I screw up my display or input I should always be able to get back
to a known good state. This should be hard-wired with a dedicated button. 

Let's tease apart the good parts of web browsing from the obese blob that we're used to dealing with
and exile that part to a proxy in a datacenter. This proxy will act as my agent. It will handle the
many connections to get resources for a webpage, keep them for eternity, because, you know, why not?...
And then construct a stream of bytes to construct a webpage and send that down to my computer. My
computer never needs to dirty itself with the messiness of the modern web. My proxy will also opportunistically
follow links and construct the pages ahead of time and do it on a schedule for sites I visit regularly. 
