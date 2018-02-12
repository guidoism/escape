---
layout: default
title: Proposal 2 — A Language
---

Here I propose a language by way of a garden path by describing Forth
(as I learn it for real), and **APL**, **LISP**, **REBOL**, Smalltalk,
and other cool languages that aren't quite as mainstream as I'm used
to.

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
as a starting place, let's describe the build-in words.

- **DROP** -- Drop the top of the stack
- **SWAP** -- Swap the top two elements on the stack
- **DUP**  -- Duplicate the top of the stack
- **OVER** -- Push a copy of the second element onto the stack
- **ROT** and **-ROT** -- Rotate the stack?






