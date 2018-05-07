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
[WPS (Postscript for the Web)](http://logand.com/sw/wps/index.html) and [PostscriptJS](https://github.com/zaphod42/PostscriptJS). There are also 
[examples](http://www.williammalone.com/articles/create-html5-canvas-javascript-sprite-animation/) of making
sprites for use on the Canvas. I'd use the sprite technique for pulling glyphs out of the font map image.
While Postscript isn't really were I want to end up
it will be useful because MetaPost generates Postscript as the output, which means
that I should be able to compile MetaPost to WASM and run it directly in the browser.

What I'd like is to be able to experiment with the display by typing in MetaPost and TeX
and compiling it in the browser to a little screen. Asymtopte is also something to look
at since it's similar to MetaPost but also does animations... I think.

## Move Web Complexity to Server

I want to move the computationaly intensive task of rendering a web page to a server. There's
no need to do all of this work over and over again on a battery-constrained device. Chrome now
allows you to run headless. I would like to be able to glue this all together into an AWS Lambda
service that fetches the page with Headless Chrome and then converts it to Markdown with html2text
and then converts that to a DVI which is sent back to the client. All of this should be cached for
each device screen width. It might also make sense to run this automatically on website that I
goto regularly so it's already cached for me in the morning. 

I will be able to start using this as a proxy for the web immediately. I also want a trail for web
pages that I want to remember. The proxy should insert a quick tap save. It should save it on the
device immediately in the local storage, in a queue, and in the background should send it up to the
server. 
