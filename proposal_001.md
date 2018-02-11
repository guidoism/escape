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

We also choose to index **RAM** by words rather than bytes.
