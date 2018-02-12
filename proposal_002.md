---
layout: default
title: Proposal 2 — A Language
---

Here I propose a language by way of a garden path by describing Forth
(as I learn it for real), and **APL**, **LISP**, **REBOL**, Smalltalk,
and other cool languages that aren't quite as mainstream as I'm used
to. I don't care that I'm not adding anything original to this
language. I'm going to steal steal steal good ideas from others as
much as possible.

## Forth

Forth is an interesting language because it's both low level and high
level at the same time. It's mind bending that a system that can serve
as an assembly language can also be used for **AI** research. I love
seeing examples of people starting off with a Forth prompt on a
computer with nothing else, not even an operating system, and building
a usable system from it.

I'm also sure that nostalgia has something to do with my interest in
it. I started programming in the 1980s and Forth, as far as I
remember, had a reputation of being the hacker's language. When I
think of Forth I think of a black/green **CRT** with a blinking cursor
in a dark room. 

I think also the whole nip/tuck constrained puzzle nature of the
language is intriguing to me.

And one doesn't start off by talking about Forth's grammar, as there
really isn't one. The interpreter essentially just handles each
whitespace-delimited token individually, executing the token if it's
defined in the *word dictionary*, and pushing it onto the stack if
it's not.

The language essentially just starts out with a linked list used
as the dictionary and a few built-in words. Everything else can be
built from that. Using the wonderful
[jonesforth](https://github.com/nornagon/jonesforth/blob/master/jonesforth.S)
as a starting place, let's describe some build-in words.

- **DROP** -- Drop the top of the stack
- **SWAP** -- Swap the top two elements on the stack
- **DUP** and **?DUP** -- Duplicate the top of the stack and do it
  only if it's not empty
- **OVER** -- Push a copy of the second element onto the stack
- **ROT** and **-ROT** -- Rotate the top three values of the stack
- **INCR** and **DECR** -- Increment or decrement the top of the stack
- **FETCH** and **STORE** -- Fetch and store from/to memory
- Math and comparison words

What I want from Forth isn't necessarily the exact language and
syntax, but the simple runtime: A linked list and a stupidly simple
interpreter.

We also need to look at
[Joy](https://en.wikipedia.org/wiki/Joy_(programming_language)).

## Rebol

Rebol has a naming problem. Up until just recently it was spelled 
**REBOL** like languages from the 1950s and even though it's supposed
to be pronounced like *rebel* it looks like it rhymes with **COBOL**.
Now you take that naming problem and combine it with the fact that all
we know about the language is that it's supposed to be simple to
program in (ummmm... like **COBOL**) makes it a language that I want
to maintain a large distance from.

If you somehow get past the name and find a screenshot of an
application written in Rebol then you shutter and say "Oh my god it
looks like an application written in 1995."

In fact, it was indeed stuck in 1995 until just very recently. It was
a closed-source, commercial programming language that wasn't backed
by a major corporation. If nothing else that would have killed it off.

We've now filtered out like 99.99999% of the programmers in the world
and if you've made it this far then you'll find a kernel of beauty.

And as of 2018 there are *zero* academic articles on this
language/environment. 

Rebol satisfies a bunch of the requirements for my computer. It's
tiny, the runtime for the GUI is only a megabyte and full applications
written in Rebol are on the order of 10s of kilobytes at the most.

Like many languages types can be inferred from the syntax of values,
but Rebol goes much further than most and includes type inference for
date/times, currency, tags, email addresses, urls, filenames, pairs,
and ids (what they call issues).

All code and data are defined within blocks (enclosed in square
brackets). Variables are defined with the colon and functions wih the
func or function words. A particularly interesting feature is that
one can *refine* blocks, strings, and functions with a slash. You can
use this to pull a value from a dictionary or select an option on a
function.

Because Rebol has a very simple syntax that's homoiconic it should be
relatively easy to create a nicer syntax that's isomorphic to it.

What really blows my mind is seeing something like a spreadsheet
written in only 80 lines of Rebol. I think that the test for my new
language is that one should be able to write a spreadsheet or
similarly complex program in less than a hundred lines of code.

What I want to steel from Rebol is the tiny runtime, tiny apps, and
minimal code for making a graphical app.

We also need to look at [Flutter](https://flutter.io).
