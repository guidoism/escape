---
layout: default
title: Escape the Local Maxima — One Pager
---

## Introduction
I will design a computer from the ground up.

## Motivations
- Shits-and-giggles
- Learn how all parts of the computer work
- Make a computer that I want to use
- Make at least some contribution to the field of Computer Science

## Assumptions
- Everything above the **CMOS** transistors is subject to diverge from common patterns
- A computer from the **CPU** through the apps can be designed and written by a single person
- We will write make heavy use of mini languages to reduce code size and complexity
- Networking and **USB** are out-of-scope — we will isolate these features into separate microcontrollers
- The targeted user will be me: Focus on writing, reading the web, and programming. No games or 3D graphics. Interface will mostly be (custom) keyboard with limited trackpad use.
- Avoid the von Neumann bottleneck
- Consider the use of non-volatile memory
- Avoid preemptive multitasking
- Favor snappiness over computational throughput

## Existing Solutions
- Wirth’s [Project Oberon](http://www.projectoberon.com) is the canonical example of a project like this, particularly the 2013 Edition which includes a custom CPU.
- Kay and Ingalls’ [**STEPS**](http://www.vpri.org/pdf/tr2012001_steps.pdf) project is the model of revolutionary change that I want to emulate. I particularly like OMeta and their **TCP** from **ASCII** art. 

## Exploration Projects
- Mechanical keyboard with FPGA for the matrix scan — Get some experience programming an FPGA and building hardware. Create the core input mechanism for the computer without using an existing microcontroller. 
- MetaPost canvas for output — I want to use something elegant for display. I took inspiration from Knuth/Hobby (TeX/**DVI**/MetaPost), Warnock (PostScript/**PDF**), and Gosling (NeWS). From the **DVI** format I like the opcode/operand model of decoding the format, it is concise and fast even on early-1980s computers, and favors the common case of building up lines out output from left to right. I have written several DVI and PostScript interpreters in various languages and have explored changing the output of the **WEB** in MetaPost to other intermediate languages.
- Exploring Ohm — A modern **PEG** parser based on OMeta from the **STEPS** project. I’ve been using it to implement PostScript and other mini languages. 
- Exploring **APL** — I like the conciseness and elegance and the use of non-**ASCII** characters
- Rewriting the ARM1 simulator — Trying to really understand how a processor works. Rewriting using several techniques: Modern Javascript for readability, bit arrays and matrices for performance and mathematical elegance. Along the way learning the **APL** way of programming and finally getting comfortable with graph theory. 
