---
layout: default
title: Building a computer from the ground up
---

## Keyboard Matrix

[Hand-wiring a keyboard](https://deskthority.net/workshop-f7/brownfox-step-by-step-t6050.html) and
[Writing the matrix scanner](http://blog.komar.be/how-to-make-a-keyboard-the-matrix/)

Instead of using a microcontroller like existing keyboards I want to cycle through the matrix
manually. I can do this by making a self-starting straight ring counter. A straight ring counter
is a series D Flip-Flops that are all clocked together where the output of the last is wrapped
around to the input of the first. It can be made self-starting by sending the output of all but
the first FFs into a NOR gate and sending that to the input of the counter. This counter will
continue to cycle around forever for the columns.

I also need a similar ring counter for the rows that will only move when the 1 bit cycles back to
the first column. This should be easy to do.

There's also the question of cycling around and around at full speed forever. I assume this will
use electricity and generate heat, so how slow do we want this? According to
[the answers to my question on geekhack](https://geekhack.org/index.php?topic=96205.msg2625241#msg2625241)
once a millisecond for the whole matrix should be enough. Therefore we should be able to
use a clock of 50 kHz.

Assuming 20 transistors per flip-flop and 12 columns and 4 columns then we will need
about a thousand transistors for the matrix scanner.

The matrix scanner is the only thing for the keyboard that really could be fixed. The interpretation
of the keys should be dynamic, therefore we should allow the user to define a state machine
to translate key sequences into characters or commands. And then these can be put into a queue.

I can prototype this on an FPGA and have it show the character code on the two 7-segment displays.
It's apparently easy to add VGA IP to the FPGA so the next step would be to output pre-defined
fixed characters to the screen, and then change it to move the cursor for each letter and then scroll
and then allow to movement of the cursor with the arrow keys.

Another option is to use the schematic from inside the TI 4017 Decade Counter

https://i.imgur.com/DddhpeB.png

I believe the Flip Flops in the schematic are [Gated SR Latches](https://en.wikipedia.org/wiki/Flip-flop_(electronics)#Gated_SR_latch), but I'm not quite sure.

We can describe and test this hypothesis by creating a gate-level model of the circuit in Verilog
using nands, nors, etc.

## Output

I don't want a screen that scans across the screen and updates one pixel at a time. I instead want
something more like cellular automata where you poke one at the bottom and they all move up, pushing
each other, and agreeing on a clock cycle to make their update show.
