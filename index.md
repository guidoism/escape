The current *state of the art* in computing with our superscalar-pipelined, speculatively-executed, multi-level cached, multi-core cpus using closed-source BIOS running operating systems built upon layers and layers of ancient buggy code written in ancient programmer-hostle languages with its model based on physical desk and its fetish-like desire to be general purpose while focusing on the the performance of arithmetic rather than human interaction is a local maximum. Indeed, many local maxima. Let us work together to break free of these and invent the future of computing.

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
* A computer should be programmable -- Everything should be available for hacking (with appropriate warnings and guards and training wheels)
* A computer shouldn't lose data

I have a dream of one day possessing a set of devices that together I will call "my computer". This computer will consist of 1. An earpiece that's always with me, 2. A pocketable all-screen multi-touch device that's with me most of the tie, 3. A novel-sized all-screen multi-touch device, 4. A larger screen with a proxy for the screen that I can use to manipulate it without moving my arm all across the screen, and 5. A series of input devices like a keyboard.

I will be able to continue working on the same task as I switch devices and if I want use multiple devices at the same time. When consuming content, the text, figures, and images will all be presented in a way to optimize comprehension -- There will be no place for navigation chrome, share buttons, or advertisements. Updating software will *never* make the computer feel slower. Caching will happen aggresively to minimize the latency of the network, entire websites will be slurped down opportunistically -- Often used references like wikipedia will be kept locally.

It will be trivially easy to write simple applications. I will be able to assign many shades of trust to others' applications -- Trying something out shouldn't be scary or permanent in any way. I shouldn't have to rely on the manufacturer's reputation, all code should be open for inspection, modification, and research. Payment for the development of applications and profit should be obtained by providing services or non-executable digital assets rather than obscured code.

Important systems, such as cryptography and data integrity, should be formally verified.

### Existing research and ideas

* [*Project Oberon*](http://www.projectoberon.com) -- Book about a CPU, Compiler, and OS written from scratch. Wirth demonstrates that it's entirely possible to design an entire system from the ground up -- Without relying on legacy code.
* [*Seven Laws of Sane Personal Computing*](http://www.loper-os.org/?p=284) -- From Loper OS
* [*Stack Computers: the new wave*](https://users.ece.cmu.edu/~koopman/stack_computers/index.html) -- Book about an alternative way to design cpus.
* [*The Architecture of Symbolic Computers*](https://www.amazon.com/Architecture-Computers-Mcgraw-Hill-Supercomputing-Processing/dp/0070355967/) -- Book about computers that don't focus so much on raw arithmatic throughput -- Lots of information on designing a LISP or Prolog cpu.

### Areas of new research

* Quit doing stuff over and over again on battery-constrained devices. How many cpu cycles are wasted, how many pounds of CO2 are emitted, in order to display static text on a phone? The website is probably generating html over and over again. The phone is parsing that html over and over again and converting it to glyphs positioned in the same place on the same device type over and over again. And all of this shitty typography!
* Quit doing work on battery-constrained devices that could be safely done on an non-mobile device. Under normal circumstances battery-constrained devices should do as little computation as possible. If latency requirements can be satisfied we should move the work onto a server, whether owned by the user or not.
