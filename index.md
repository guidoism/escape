---
layout: default
title: Escape the Local Maxima
---

The current *state of the art* in computing with our superscalar-pipelined, speculatively-executed, multi-level cached, multi-core cpus using closed-source BIOS running operating systems built upon layers and layers of ancient buggy code written in ancient programmer-hostle languages with its model based on physical desk and its fetish-like desire to be general purpose while focusing on the the performance of arithmetic rather than human interaction is a local maximum. Indeed, many local maxima. Let us work together to break free of these and invent the future of computing.

* [One-pager](one-pager)
* [A Manifesto](day_two_manifesto)
* [Study Guide](study)
* [Tools](tools)

### Wishes and dreams

* A computer should be personal but not scary to share
* A computer should be usable from multiple screens and form factors
* A computer should enable multiple contexts without causing confusion
* A computer should be pleasant to use and should be aesthetically pleasing to the eye and touch
* A computer should not need to be babied, one should never need to think about charging batteries or updating
* A computer should never prioritize novelty over usabilty or stability
* A computer should be trusted
* A computer should be provide the world's best form of reading
* A computer should be understandable -- Any normal curious person should be able to start with the highest level abstractions and figure out how it works on their own
* A computer should be programmable -- Everything should be available
  for hacking (with appropriate warnings and guards and training
  wheels). A simple app shouldn't require a computer science degree, a
  year of full-time work and hundreds of thousands of dollars.
* A computer shouldn't lose data
* A computer should treat numbers as precisely as required and include units where applicable

I have a dream of one day possessing a set of devices that together I will call "my computer". This computer will consist of 1. An earpiece that's always with me, 2. A pocketable all-screen multi-touch device that's with me most of the time, 3. A novel-sized all-screen multi-touch device, 4. A larger screen with a proxy for the screen that I can use to manipulate it without moving my arm all across the screen, and 5. A series of input devices like a keyboard.

I will be able to continue working on the same task as I switch devices and if I want use multiple devices at the same time. When consuming content, the text, figures, and images will all be presented in a way to optimize comprehension -- There will be no place for navigation chrome, share buttons, or advertisements. Updating software will *never* make the computer feel slower. Caching will happen aggresively to minimize the latency of the network, entire websites will be slurped down opportunistically -- Often used references like wikipedia will be kept locally.

It will be trivially easy to write simple applications. I will be able to assign many shades of trust to others' applications -- Trying something out shouldn't be scary or permanent in any way. I shouldn't have to rely on the manufacturer's reputation, all code should be open for inspection, modification, and research. Payment for the development of applications and profit should be obtained by providing services or non-executable digital assets rather than obscured code.

Important systems, such as cryptography and data integrity, should be formally verified.

### Existing research and ideas

* [*Project Oberon*](http://www.projectoberon.com) -- Wirth's book about a **cpu**, compiler, and OS written from scratch. Demonstrates that it's entirely possible to design an entire system from the ground up without relying on legacy code.
* [*Seven Laws of Sane Personal Computing*](http://www.loper-os.org/?p=284) -- From Loper OS
* [*Stack Computers: the new wave*](https://users.ece.cmu.edu/~koopman/stack_computers/index.html) -- Koopman's book about an alternative way to design cpus -- Lots about stacks and Forth.
* [*The Architecture of Symbolic Computers*](https://www.amazon.com/Architecture-Computers-Mcgraw-Hill-Supercomputing-Processing/dp/0070355967/) -- Kogge's book about computers that don't focus so much on raw arithmatic throughput -- Lots of information on designing a **lisp** or Prolog **cpu**.
* [*Genera Concepts*](http://bitsavers.trailing-edge.com/pdf/symbolics/software/genera_8/Genera_Concepts.pdf) -- Good intro to Lisp computers
* [*Notation as a Tool of Thought*](http://www.eecg.toronto.edu/~jzhu/csc326/readings/iverson.pdf) -- Iverson's 1979 Turing Award lecture -- An example of succinctness and operating on entire data structures rather than manually looping. Also an example of how we might break free of the chains of **ascii**.
* [*A Programming Language*](http://www.softwarepreservation.org/projects/apl/Books/APROGRAMMING%20LANGUAGE) -- Iverson's 1962 book about **apl**.
* [*Reconfigurable Computing*](https://www.amazon.com/Reconfigurable-Computing-Practice-FPGA-Based-Computation/dp/0123705223) -- Book about changing the layout of your **cpu** on-the-fly rather than just the software. 
* [*Category Theory for Programmers*](https://github.com/hmemcpy/milewski-ctfp-pdf) -- Book about programming in a more formal way -- Haskell used for examples.
* [*Microprocessor Architectures: From VLIW to TTA*](https://www.wiley.com/en-us/Microprocessor+Architectures%3A+From+VLIW+to+TTA-p-9780471971573) -- Henk Corporaal's book about transport triggered architectures, where the only **cpu** instruction is move and you specify which function unit data moves to next instead of the higher-level instruction. Somewhat in between **fpga** and standard **cpu**s.

### Programming Language Inspiration

* APL
* Forth
* REBOL/RED
* Smalltalk
* Hypercard

### Observations

* It seems to be easier to communicate with symbols than a sequence of actions. For example, it's difficult to learn that you are supposed to press option and the left mouse button on one part of the program and drag the cursor over to another part of the program to connect them. Code on a page is easier for the learning process.
* Laptops have stunted the experimentation with keyboard layouts and therefore reduced the comfort of using non-ASCII characters in programming languages.
* There is a tension between making programming easy and finding yourself wading through a prolifieration of horrible apps (see Roblox as the canonical example)

### Areas of new research

* Quit doing stuff over and over again on battery-constrained devices. How many cpu cycles are wasted, how many pounds of CO₂ are emitted, in order to display static text on a phone? The website is probably generating html over and over again. The phone is parsing that html over and over again and converting it to glyphs positioned in the same place on the same device type over and over again. And all of this shitty typography!
* Quit doing work on battery-constrained devices that could be safely done on an non-mobile device. Under normal circumstances battery-constrained devices should do as little computation as possible. If latency requirements can be satisfied we should move the work onto a server, whether owned by the user or not.
* Offload the work of scrolling a page of text onto a dedicated processor -- Nothing the main processors is doing should ever make scrolling janky.
* Data should be specified using relational algebra for the whole system.

### Proposals

* [Proposal 1](proposal_001)
* [Proposal 2](proposal_002)
* [Proposal 3](proposal_003)
* [Proposal 4](proposal_004)
* [Proposal 5](proposal_005)
* [Proposal 6](proposal_006)
