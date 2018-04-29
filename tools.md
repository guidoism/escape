---
layout: default
title: Tools
---

## Emulate Display

It will be helpful to get a terminal-like interface up and running early.
Since I clearly won't be able to make the kind of hardware I want I will
instead emulate the display on an existing system. The seperation of
the computationally intensive modern web rendering and a simplified on-device
protocol will be helpful to use on existing devices for the time being too!

Ideally I'd run something very minimal on a single board computer connected to a
monitor. It would be the smallest possible operating system that can take input
from a keyboard and send display commands to the GPU. It's possible that I'll
need a library like SDL or Vulcan for this.

The other, and more intensive solution, is to do everything with web technology.
Ideally here too we'd use the GPU with webgl. This too seems a bit complex to start
with do we might just start with the HTML Canvas.

There are existing examples of Postscript being translated to Canvas commands:
[WPS (Postscript for the Web)](http://logand.com/sw/wps/index.html) and [PostscriptJS](https://github.com/zaphod42/PostscriptJS).

