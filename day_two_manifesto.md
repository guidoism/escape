## The Day Two Computer Manifesto

(Or: Let’s stop pretending it’s still day one)

### Proposal

In the spirit of Project Oberon, design and build a “phone”-like computer that handles the most common uses, excluding games. The computer should support multi-touch and UI animations should feel instantaneous with absolutely no jankiness. It should be optimized for excellent typography since reading text is the center of almost every use case. The battery should last for weeks and the device shouldn’t ever get hot. The software should be as bug-free as avionics software and updates should be handled without user intervention or interruption. The device should be miserly with network usage. The hardware components should be as inexpensive as the cheapest smartphones.

### What we Believe

* Home computers in the 1980s feel faster than computers in the 2010s. https://danluu.com/input-lag/ so something must be wrong. And doing more and pushing more pixels can’t possibly be the only reasons.
* The executable size for simple programs (like text messaging) should be measured in kilobytes, not megabytes, and certainly never hundreds of megabytes.
* Background computations should never affect scrolling or user interaction. If they do then it’s a problem with the design of the computer.
* The size of a nicely typeset document shouldn’t be much more than a small multiple of the number of characters in bytes, excluding images.
* ROM is cheap and should be used more often, especially with the increase of dark silicon.
* If you dispense with the need to run legacy software the system becomes simpler, easier to write, less buggy, and more performant. A phone shouldn’t need to run software designed for a mini-computer.
* A whole (usable) system can be written from scratch by a few people with a good programming language. There is no need for legacy libraries and decades of cruft.
* Normal people should be able to write applications for the computer and they should be able to do it without hours, days, (or years!) of preparation. Normal people shouldn’t worry about accidentally breaking their computer. (See HyperCard, REBOL, and RED)
* A “phone”-like computer doesn’t need to be optimized for raw computational throughput. Linpack is a very bad estimate for making the computer feel snappy. If you are doing lots of integer and floating point calculations directly on the device then you are doing something wrong. Expensive calculations should be able to be handled by a proxy in the cloud.
* There are no “general purpose” computers. We should optimize for the common uses first.
