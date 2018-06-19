---
layout: default
title: Building a computer from the ground up
---

## Keyboard Matrix

http://blog.komar.be/how-to-make-a-keyboard-the-matrix/

https://deskthority.net/workshop-f7/brownfox-step-by-step-t6050.html

Instead of using a microcontroller like existing keyboards I want to cycle through the matrix
manually. I can do this by making a self-starting straight ring counter. A straight ring counter
is a series D Flip-Flops that are all clocked together where the output of the last is wrapped
around to the input of the first. It can be made self-starting by sending the output of all but
the first FFs into a NOR gate and sending that to the input of the counter.
