---
layout: default
title: Proposal 1
---

In this document I will describe what I imagine what one of these
computers might look like.

The **CPU** is a 32 bit stack machine. We choose a stack machine
because we want to prioritize code density, to use Forth as the
assembly language, and want the **CPU** to use as few transistors as
possible. We choose a 32 bit word length because we want our computer
to use less than 4 billion words of **RAM**.

We also choose to index **RAM** by words rather than bytes since we
will generally operate on entire words.

The computer also makes heavy use of **ROM** to store library
functions. This **ROM** will be accessed just like **RAM** but
it will be denser than the equivilent amount of **RAM** and consume
less power. We will prepopulate it with a plethora of algorithms
from computer science.

The assembly langauge, while similar to Forth, uses special Unicode
characters to represent its words instead of multi-character strings.
We take inspiration from **APL** for doing calculations and **SQL**
for manipulating table data. What is particularly nice is that all
assembly language can be read and understood by any normal programmer.

The entire operating system is stored as a **GIT** respository so it's
always possible to see what has changed and to be able to revert to
a previous version using a special debug mode.
