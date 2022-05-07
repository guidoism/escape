---
layout: default
title: Escape the Local Maxima
---

The current *state of the art* in computing with our superscalar-pipelined, speculatively-executed, multi-level cached, multi-core cpus using closed-source **BIOS** running operating systems built upon layers and layers of ancient buggy code written in ancient programmer-hostle languages with its model based on a physical desk and its fetish-like desire to be general purpose while focusing on the the performance of arithmetic rather than human interaction is a local maximum. Indeed, many local maxima. Let us work together to break free of these and invent the future of computing.

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

### A (work-in-progress) breakdown of overlapping projects

#### Attempts to change the way we read and understand programs

* [Literate Programming](https://en.wikipedia.org/wiki/Literate_programming) - Should be able to read a program like a novel in bed.
* [Mu](https://github.com/akkartik/mu) - Source files are numbered in the order that they are used to build upon what came before -- Therefore there is a clear direction for comprehensibility with no circular dependencies.
* [ChibiCC](https://github.com/rui314/chibicc) - Git commits are made to be read from start to finish to understand how the compiler was incrementally built. Each commit means something and he changed github history to not have meaningless bug fix commits.
    
#### Attempts to reinvent the whole computing stack   

* [GNU](https://en.wikipedia.org/wiki/GNU_Project) (Stallman) - The OG. Goals were to rewrite Unix from scratch and make sure that any improvements could never be hidden from the community. A very very very successful project.
* [Oberon](https://en.wikipedia.org/wiki/Oberon_(operating_system)) (Wirth) - Inspired by the (too expensive) Xerox Alto. Goal was efficiency and understandability. All code in a single book.
* [Canon Cat](https://en.wikipedia.org/wiki/Canon_Cat) (Raskin) - Attempt at a real "people's computer"
* [STEPS](http://www.vpri.org/pdf/tr2012001_steps.pdf) (Kay) - Goal was a whole computing stack in fewer than 20k lines of code using domain specific languages.
* [Mu](https://github.com/akkartik/mu) (Agaram) - (TODO: pull from Section 1.1 of his paper)
    
#### Attempts to bootstrap a compiler from nothing

* [bcompiler](https://github.com/certik/bcompiler) - Start with hex, end up with a tiny compiler for a toy programming language somewhat reminiscent of C and Forth.
* [Stage0](https://github.com/oriansj/stage0) for GNU - Reproducible builds and verifiable base for defeating the trusting trust attack.
* [StoneKnifeForth](https://github.com/kragen/stoneknifeforth) (Kragen) - Start with hex just like bcompiler. Awesome name!
* [SubX for Mu](https://github.com/akkartik/mu) (Agaram) - Hex (with annotations) is the language!
* [META-II](https://en.wikipedia.org/wiki/META_II) (Schorre) - Start with a dead-simple VM, output is interspersed with parse info.

### Programming Language Inspiration

* **APL**
* Forth
* **REBOL/RED**
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

### Guido's Current Project Status <a name="status"/>

I've decided to slice off and focus on a more tractable, more
constrained part of the problem for now. Instead of redesigning a cpu
and programming language and computer, I'm going to concentrate on
improving the pedagogy of some of the best existing ideas.

Motivation/Problems-to-solve: I *love* Project Oberon. I think that
Niklaus Wirth is a genius and it's a tragedy that his work has been
slept on by the current generation of programmers (myself included).
But there's something about his presentation that doesn't work for me.
For one, there's *way* too much seperation between prose and code. It
seems like the perfect candidate for a Literate Programming treatment.
Second, the top-down approach doesn't work for me. I can't concentrate
on the UI code if I don't know how the kernel works. Third, I feel
like something is missing. The pieces don't connect in my head and it
makes me wonder why. It's a little hand-wavy for me. Wirth is
*complete* but not *precise*. Donald Knuth on the other hand is
*perfectionist in his precision* but not *complete*. **MMIX** would be
an amazing architecture on which to run Oberon. There is so much
defined for analysing performance and understand what is really
happening inside the computer. He has a massive archive of heavily
studied algorithms written in **MMIXAL** that could be taken advantage
of. TeX would be amazing to presentation of the literate program form
of Project Oberon and it would be amazing to use as the foundation of
the text layout within the OS, along with MetaPost. Also, both Knuth
and Wirth are still [slaying the dragons of the
1960s](http://www.bayfronttechnologies.com/mc_tutorial.html) when it
comes to parsing. Oberon should be re-written with a simple
self-hosting Parsing Expression Grammar.

I'm calling my project **Knuth × Wirth**.

The stack will look as follows:




My plan is as follows:

1. Bang my head against the wall until I truly understand how **PEG**s
work. Kragen's [**PEG** Bootstrap](https://github.com/kragen/peg-bootstrap/blob/master/peg.md)
so far has been the best teacher. I think that [I finally grok
it](https://github.com/guidoism/peg-bootstrap/blob/master/guido/understanding/peg.org)
enough to contiune forth with it.

2. Write a self-hosting **PEG** in **MMIXAL**. The **MMIX**
instruction set is simple enough that I should be able to also
generate runnable object code directly without the need for a seperate
assembler. I *might* add a small StoneKnifeForth layer in the
bootstrap layer, but only if it's really needed.

3. Produce a tiny bootstrapable core in hex that could conceivably
hand entered with switches into a computer.

4. Moving back up the stack, rewrite the Oberon compiler as a PEG. I
have a lot of this finished already. It was difficult because the
ambiguity of the published grammar didn't align well with the
hand-written recusive descent parser written in Oberon itself.

5. Get the Oberon system as a whole running on the **MMIX** simulator.

6. Rewrite Project Oberon using techniques from *literate
programming*, either by using **WEB** directly, or by creating
something new, in Oberon, that fits in with a modern sensibility like
Org Mode Babel.

7. Write enough of a C compiler with the PEG and Oberon to be able to
compile CWEB and MMIXWare.

8. Publish it as a book, with the copyright set to Public Domain or
one of the Creative Commons licenses.

