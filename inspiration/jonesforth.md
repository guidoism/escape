---
layout: code
title: Jones Forth
---

## Jones Forth
### A sometimes minimal FORTH compiler and tutorial for Linux / i386 systems

By Richard W.M. Jones <rich@annexia.org> http://annexia.org/forth

This is PUBLIC DOMAIN (see public domain release statement below).

## INTRODUCTION

FORTH is one of those alien languages which most working programmers regard in the same
way as Haskell, LISP, and so on.  Something so strange that they'd rather any thoughts
of it just go away so they can get on with writing this paying code.  But that's wrong
and if you care at all about programming then you should at least understand all these
languages, even if you will never use them.

LISP is the ultimate high-level language, and features from LISP are being added every
decade to the more common languages.  But FORTH is in some ways the ultimate in low level
programming.  Out of the box it lacks features like dynamic memory management and even
strings.  In fact, at its primitive level it lacks even basic concepts like IF-statements
and loops.

Why then would you want to learn FORTH?  There are several very good reasons.  First
and foremost, FORTH is minimal.  You really can write a complete FORTH in, say, 2000
lines of code.  I don't just mean a FORTH program, I mean a complete FORTH operating
system, environment and language.  You could boot such a FORTH on a bare PC and it would
come up with a prompt where you could start doing useful work.  The FORTH you have here
isn't minimal and uses a Linux process as its 'base PC' (both for the purposes of making
it a good tutorial). It's possible to completely understand the system.  Who can say they
completely understand how Linux works, or gcc?

Secondly FORTH has a peculiar bootstrapping property.  By that I mean that after writing
a little bit of assembly to talk to the hardware and implement a few primitives, all the
rest of the language and compiler is written in FORTH itself.  Remember I said before
that FORTH lacked IF-statements and loops?  Well of course it doesn't really because
such a lanuage would be useless, but my point was rather that IF-statements and loops are
written in FORTH itself.

Now of course this is common in other languages as well, and in those languages we call
them 'libraries'.  For example in C, 'printf' is a library function written in C.  But
in FORTH this goes way beyond mere libraries.  Can you imagine writing C's 'if' in C?
And that brings me to my third reason: If you can write 'if' in FORTH, then why restrict
yourself to the usual if/while/for/switch constructs?  You want a construct that iterates
over every other element in a list of numbers?  You can add it to the language.  What
about an operator which pulls in variables directly from a configuration file and makes
them available as FORTH variables?  Or how about adding Makefile-like dependencies to
the language?  No problem in FORTH.  How about modifying the FORTH compiler to allow
complex inlining strategies -- simple.  This concept isn't common in programming languages,
but it has a name (in fact two names): "macros" (by which I mean LISP-style macros, not
the lame C preprocessor) and "domain specific languages" (DSLs).

This tutorial isn't about learning FORTH as the language.  I'll point you to some references
you should read if you're not familiar with using FORTH.  This tutorial is about how to
write FORTH.  In fact, until you understand how FORTH is written, you'll have only a very
superficial understanding of how to use it.

So if you're not familiar with FORTH or want to refresh your memory here are some online
references to read:

http://en.wikipedia.org/wiki/Forth_%28programming_language%29

http://galileo.phys.virginia.edu/classes/551.jvn.fall01/primer.htm

http://wiki.laptop.org/go/Forth_Lessons

http://www.albany.net/~hello/simple.htm

Here is another "Why FORTH?" essay: http://www.jwdt.com/~paysan/why-forth.html

Discussion and criticism of this FORTH here: http://lambda-the-ultimate.org/node/2452

## ACKNOWLEDGEMENTS

This code draws heavily on the design of LINA FORTH (http://home.hccnet.nl/a.w.m.van.der.horst/lina.html)
by Albert van der Horst.  Any similarities in the code are probably not accidental.

Some parts of this FORTH are also based on this IOCCC entry from 1992:
http://ftp.funet.fi/pub/doc/IOCCC/1992/buzzard.2.design.
I was very proud when Sean Barrett, the original author of the IOCCC entry, commented in the LtU thread
http://lambda-the-ultimate.org/node/2452#comment-36818 about this FORTH.

And finally I'd like to acknowledge the (possibly forgotten?) authors of ARTIC FORTH because their
original program which I still have on original cassette tape kept nagging away at me all these years.
http://en.wikipedia.org/wiki/Artic_Software

## PUBLIC DOMAIN

I, the copyright holder of this work, hereby release it into the public domain. This applies worldwide.

In case this is not legally possible, I grant any entity the right to use this work for any purpose,
without any conditions, unless such conditions are required by law.

## SETTING UP

Let's get a few housekeeping things out of the way.  Firstly because I need to draw lots of
ASCII-art diagrams to explain concepts, the best way to look at this is using a window which
uses a fixed width font and is at least this wide:

 <------------------------------------------------------------------------------------------------------------------------>

Secondly make sure TABS are set to 8 characters.  The following should be a vertical
line.  If not, sort out your tabs.

                |
                |
                |

Thirdly I assume that your screen is at least 50 characters high.

## ASSEMBLING

If you want to actually run this FORTH, rather than just read it, you will need Linux on an
i386.  Linux because instead of programming directly to the hardware on a bare PC which I
could have done, I went for a simpler tutorial by assuming that the 'hardware' is a Linux
process with a few basic system calls (read, write and exit and that's about all).  i386
is needed because I had to write the assembly for a processor, and i386 is by far the most
common.  (Of course when I say 'i386', any 32- or 64-bit x86 processor will do.  I'm compiling
this on a 64 bit AMD Opteron).

Again, to assemble this you will need gcc and gas (the GNU assembler).  The commands to
assemble and run the code (save this file as 'jonesforth.S') are:

    gcc -m32 -nostdlib -static -Wl,-Ttext,0 -Wl,--build-id=none -o jonesforth jonesforth.S
    cat jonesforth.f - | ./jonesforth

If you want to run your own FORTH programs you can do:

    cat jonesforth.f myprog.f | ./jonesforth

If you want to load your own FORTH code and then continue reading user commands, you can do:

    cat jonesforth.f myfunctions.f - | ./jonesforth

## ASSEMBLER

(You can just skip to the next section -- you don't need to be able to read assembler to
follow this tutorial).

However if you do want to read the assembly code here are a few notes about gas (the GNU assembler):

(1) Register names are prefixed with '%', so %eax is the 32 bit i386 accumulator.  The registers
    available on i386 are: %eax, %ebx, %ecx, %edx, %esi, %edi, %ebp and %esp, and most of them
    have special purposes.

(2) Add, mov, etc. take arguments in the form SRC,DEST.  So mov %eax,%ecx moves %eax -> %ecx

(3) Constants are prefixed with '$', and you mustn't forget it!  If you forget it then it
    causes a read from memory instead, so:
    mov $2,%eax         moves number 2 into %eax
    mov 2,%eax          reads the 32 bit word from address 2 into %eax (ie. most likely a mistake)

(4) gas has a funky syntax for local labels, where '1f' (etc.) means label '1:' "forwards"
    and '1b' (etc.) means label '1:' "backwards".  Notice that these labels might be mistaken
    for hex numbers (eg. you might confuse 1b with $0x1b).

(5) 'ja' is "jump if above", 'jb' for "jump if below", 'je' "jump if equal" etc.

(6) gas has a reasonably nice .macro syntax, and I use them a lot to make the code shorter and
    less repetitive.

For more help reading the assembler, do "info gas" at the Linux prompt.

Now the tutorial starts in earnest.

## THE DICTIONARY

In FORTH as you will know, functions are called "words", and just as in other languages they
have a name and a definition.  Here are two FORTH words:

    : DOUBLE DUP + ;            \ name is "DOUBLE", definition is "DUP +"
    : QUADRUPLE DOUBLE DOUBLE ; \ name is "QUADRUPLE", definition is "DOUBLE DOUBLE"

Words, both built-in ones and ones which the programmer defines later, are stored in a dictionary
which is just a linked list of dictionary entries.

<svg height="96" width="680" xmlns="http://www.w3.org/2000/svg"><style>circle,line,path,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled,.nofill{fill:#fff}text{font-family:monospace;font-size:14px}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h680v96H0z"/><path class="filled" d="M80 4l-8 4 8 4z"/><path class="solid" d="M80 8h16"/><text x="106" y="12">DICTIONARY</text><text x="194" y="12">ENTRY</text><path class="nofill" d="M248 0a16 16 0 000 16"/><text x="258" y="12">HEADER</text><path class="nofill" d="M312 0a16 16 0 010 16"/><path class="solid" marker-end="url(#arrow)" d="M328 8h184"/><path class="solid" d="M448 24h8M464 24h8M480 24h8M496 24h8"/><text x="82" y="44">LINK</text><text x="122" y="44">POINTER</text><text x="282" y="44">LENGTH</text><path class="solid" d="M344 32l-8 16"/><text x="370" y="44">NAME</text><text x="530" y="44">DEFINITION</text><text x="282" y="60">FLAGS</text><text x="290" y="76">byte</text><path class="solid" d="M616 24h8M632 24h8M648 24h8M664 24h8"/><text x="114" y="76">4</text><text x="130" y="76">bytes</text><text x="378" y="76">n</text><text x="394" y="76">bytes</text><path class="solid" d="M448 72h8M464 72h8M480 72h8M496 72h8M616 72h8M632 72h8M648 72h8M664 72h8M68 24h372M68 24v48M268 24v48M356 24v48M68 72h36M176 72h104M328 72h40"/><g><path class="solid" d="M516 24h92M516 24v48M516 72h92"/></g></svg>

I'll come to the definition of the word later.  For now just look at the header.  The first
4 bytes are the link pointer.  This points back to the previous word in the dictionary, or, for
the first word in the dictionary it is just a NULL pointer.  Then comes a length/flags byte.
The length of the word can be up to 31 characters (5 bits used) and the top three bits are used
for various flags which I'll come to later.  This is followed by the name itself, and in this
implementation the name is rounded up to a multiple of 4 bytes by padding it with zero bytes.
That's just to ensure that the definition starts on a 32 bit boundary.

A FORTH variable called LATEST contains a pointer to the most recently defined word, in
other words, the head of this linked list.

DOUBLE and QUADRUPLE might look like this:

<svg height="256" width="648" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled{fill:#fff}text{font-family:monospace;font-size:14px}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h648v256H0z"/><text x="18" y="12">pointer</text><path class="filled" d="M24 28l4-12 4 12z"/><path class="solid" d="M28 32v32M84 48v48M116 48v48M148 48v48M180 48v48M212 48v48M244 48v48M276 48v48M308 48v48M340 48v48M456 56h8"/><text x="18" y="76">LINK</text><text x="98" y="76">6</text><text x="130" y="76">D</text><text x="162" y="76">O</text><text x="194" y="76">U</text><text x="226" y="76">B</text><text x="258" y="76">L</text><text x="290" y="76">E</text><text x="322" y="76">0</text><text x="354" y="76">definition</text><text x="442" y="76">...</text><path class="solid" d="M456 88h8"/><path class="filled" d="M24 108l4-12 4 12z"/><text x="90" y="108">len</text><text x="314" y="108">padding</text><path class="solid" d="M28 112v32M84 128v48M116 128v48M148 128v48M180 128v48M212 128v48M244 128v48M276 128v48M308 128v48M340 128v48M372 128v48M404 128v48M436 128v48M468 128v48M584 136h8"/><text x="18" y="156">LINK</text><text x="98" y="156">9</text><text x="130" y="156">Q</text><text x="162" y="156">U</text><text x="194" y="156">A</text><text x="226" y="156">D</text><text x="258" y="156">R</text><text x="290" y="156">U</text><text x="322" y="156">P</text><text x="354" y="156">L</text><text x="386" y="156">E</text><text x="418" y="156">0</text><text x="450" y="156">0</text><text x="482" y="156">definition</text><text x="570" y="156">...</text><path class="solid" d="M584 168h8"/><path class="filled" d="M24 188l4-12 4 12z"/><text x="90" y="188">len</text><text x="410" y="188">padding</text><path class="solid" d="M28 192v32"/><text x="18" y="236">LATEST</text><text x="82" y="12">to</text><text x="106" y="12">previous</text><text x="178" y="12">word</text><path class="solid" d="M472 56h8M488 56h8M504 56h8M472 88h8M488 88h8M504 88h8M600 136h8M616 136h8M632 136h8M600 168h8M616 168h8M632 168h8M4 56h444M4 56v32M4 88h444"/><g><path class="solid" d="M4 136h572M4 136v32M4 168h572"/></g></svg>

You should be able to see from this how you might implement functions to find a word in
the dictionary (just walk along the dictionary entries starting at LATEST and matching
the names until you either find a match or hit the NULL pointer at the end of the dictionary);
and add a word to the dictionary (create a new definition, set its LINK to LATEST, and set
LATEST to point to the new word).  We'll see precisely these functions implemented in
assembly code later on.

One interesting consequence of using a linked list is that you can redefine words, and
a newer definition of a word overrides an older one.  This is an important concept in
FORTH because it means that any word (even "built-in" or "standard" words) can be
overridden with a new definition, either to enhance it, to make it faster or even to
disable it.  However because of the way that FORTH words get compiled, which you'll
understand below, words defined using the old definition of a word continue to use
the old definition.  Only words defined after the new definition use the new definition.

## DIRECT THREADED CODE

Now we'll get to the really crucial bit in understanding FORTH, so go and get a cup of tea
or coffee and settle down.  It's fair to say that if you don't understand this section, then you
won't "get" how FORTH works, and that would be a failure on my part for not explaining it well.
So if after reading this section a few times you don't understand it, please email me
(rich@annexia.org).

Let's talk first about what "threaded code" means.  Imagine a peculiar version of C where
you are only allowed to call functions without arguments.  (Don't worry for now that such a
language would be completely useless!)  So in our peculiar C, code would look like this:

        f ()
        {
          a ();
          b ();
          c ();
        }

and so on.  How would a function, say 'f' above, be compiled by a standard C compiler?
Probably into assembly code like this.  On the right hand side I've written the actual
i386 machine code.

        f:
          CALL a                        E8 08 00 00 00
          CALL b                        E8 1C 00 00 00
          CALL c                        E8 2C 00 00 00
          ; ignore the return from the function for now

"E8" is the x86 machine code to "CALL" a function.  In the first 20 years of computing
memory was hideously expensive and we might have worried about the wasted space being used
by the repeated "E8" bytes.  We can save 20% in code size (and therefore, in expensive memory)
by compressing this into just:

        08 00 00 00             Just the function addresses, without
        1C 00 00 00             the CALL prefix.
        2C 00 00 00

On a 16-bit machine like the ones which originally ran FORTH the savings are even greater - 33%.

[Historical note: If the execution model that FORTH uses looks strange from the following
paragraphs, then it was motivated entirely by the need to save memory on early computers.
This code compression isn't so important now when our machines have more memory in their L1
caches than those early computers had in total, but the execution model still has some
useful properties].

Of course this code won't run directly on the CPU any more.  Instead we need to write an
interpreter which takes each set of bytes and calls it.

On an i386 machine it turns out that we can write this interpreter rather easily, in just
two assembly instructions which turn into just 3 bytes of machine code.  Let's store the
pointer to the next word to execute in the %esi register:

                08 00 00 00     <- We're executing this one now.  %esi is the _next_ one to execute.
        %esi -> 1C 00 00 00
                2C 00 00 00

The all-important i386 instruction is called LODSL (or in Intel manuals, LODSW).
It does two things. Firstly it reads the memory at %esi into the accumulator
(%eax). Secondly it increments %esi by 4 bytes. So after LODSL, the situation
now looks like this:

                08 00 00 00     <- We're still executing this one
                1C 00 00 00     <- %eax now contains this address (0x0000001C)
        %esi -> 2C 00 00 00

Now we just need to jump to the address in %eax.  This is again just a single x86 instruction
written JMP *(%eax).  And after doing the jump, the situation looks like:

                08 00 00 00
                1C 00 00 00     <- Now we're executing this subroutine.
        %esi -> 2C 00 00 00

To make this work, each subroutine is followed by the two instructions 'LODSL;
JMP *(%eax)' which literally make the jump to the next subroutine.

And that brings us to our first piece of actual code!  Well, it's a macro.

    /* NEXT macro. */
    .macro NEXT
    lodsl
    jmp *(%eax)
    .endm

The macro is called NEXT.  That's a FORTH-ism.  It expands to those two instructions.

Every FORTH primitive that we write has to be ended by NEXT.  Think of it kind of like
a return.

The above describes what is known as direct threaded code.

To sum up: We compress our function calls down to a list of addresses and use a somewhat
magical macro to act as a "jump to next function in the list".  We also use one register (%esi)
to act as a kind of instruction pointer, pointing to the next function in the list.

I'll just give you a hint of what is to come by saying that a FORTH definition such as:

    : QUADRUPLE DOUBLE DOUBLE ;

actually compiles (almost, not precisely but we'll see why in a moment) to a list of
function addresses for DOUBLE, DOUBLE and a special function called EXIT to finish off.

At this point, REALLY EAGLE-EYED ASSEMBLY EXPERTS are saying "JONES, YOU'VE MADE A MISTAKE!".

I lied about JMP *(%eax).

## THE INTERPRETER AND RETURN STACK

Going at these in no particular order, let's talk about issues (3) and (2), the interpreter
and the return stack.

Words which are defined in FORTH need a codeword which points to a little bit of code to
give them a "helping hand" in life.  They don't need much, but they do need what is known
as an "interpreter", although it doesn't really "interpret" in the same way that, say,
Java bytecode used to be interpreted (ie. slowly).  This interpreter just sets up a few
machine registers so that the word can then execute at full speed using the indirect
threaded model above.

One of the things that needs to happen when QUADRUPLE calls DOUBLE is that we save the old
%esi ("instruction pointer") and create a new one pointing to the first word in DOUBLE.
Because we will need to restore the old %esi at the end of DOUBLE (this is, after all, like
a function call), we will need a stack to store these "return addresses" (old values of %esi).

As you will have seen in the background documentation, FORTH has two stacks, an ordinary
stack for parameters, and a return stack which is a bit more mysterious.  But our return
stack is just the stack I talked about in the previous paragraph, used to save %esi when
calling from a FORTH word into another FORTH word.

In this FORTH, we are using the normal stack pointer (%esp) for the parameter stack.
We will use the i386's "other" stack pointer (%ebp, usually called the "frame pointer")
for our return stack.

I've got two macros which just wrap up the details of using %ebp for the return stack.
You use them as for example "PUSHRSP %eax" (push %eax on the return stack) or "POPRSP %ebx"
(pop top of return stack into %ebx).

    /* Macros to deal with the return stack. */
    .macro PUSHRSP reg
    lea -4(%ebp),%ebp       // push reg on to return stack
    movl \reg,(%ebp)
    .endm
    
    .macro POPRSP reg
    mov (%ebp),\reg         // pop top of return stack to reg
    lea 4(%ebp),%ebp
    .endm

And with that we can now talk about the interpreter.

In FORTH the interpreter function is often called DOCOL (I think it means "DO COLON" because
all FORTH definitions start with a colon, as in : DOUBLE DUP + ;

The "interpreter" (it's not really "interpreting") just needs to push the old %esi on the
stack and set %esi to the first word in the definition.  Remember that we jumped to the
function using JMP *(%eax)?  Well a consequence of that is that conveniently %eax contains
the address of this codeword, so just by adding 4 to it we get the address of the first
data word.  Finally after setting up %esi, it just does NEXT which causes that first word
to run.

    /* DOCOL - the interpreter! */
    .text
    .align 4
    DOCOL:
        PUSHRSP %esi            // push %esi on to the return stack
        addl $4,%eax            // %eax points to codeword, so make
        movl %eax,%esi          // %esi point to first data word
        NEXT

Just to make this absolutely clear, let's see how DOCOL works when jumping from QUADRUPLE
into DOUBLE:

<svg height="176" width="512" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled{fill:#fff}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h512v176H0z"/><text x="66" y="12">QUADRUPLE:</text><text x="82" y="44">codeword</text><text x="82" y="76">addr</text><text x="122" y="76">of</text><text x="146" y="76">DOUBLE</text><path class="solid end_marked_arrow" d="M208 72h128"/><text x="282" y="92">%eax</text><path class="solid end_marked_arrow" d="M320 88h16"/><text x="82" y="108">addr</text><text x="122" y="108">of</text><text x="146" y="108">DOUBLE</text><text x="82" y="140">addr</text><text x="122" y="140">of</text><text x="146" y="140">EXIT</text><text x="346" y="60">DOUBLE:</text><text x="362" y="92">addr</text><text x="402" y="92">of</text><text x="426" y="92">DOCOL</text><text x="362" y="124">addr</text><text x="402" y="124">of</text><text x="426" y="124">DUP</text><text x="362" y="156">etc.</text><text x="2" y="108">%esi</text><path class="solid end_marked_arrow" d="M40 104h16"/><path class="solid" d="M68 24h152M68 24v128M220 24v128M68 56h152M68 88h152M68 120h152M68 152h152"/><g><path class="solid" d="M348 72h152M348 72v88M500 72v88M348 104h152M348 136h152"/></g></svg>

First, the call to DOUBLE calls DOCOL (the codeword of DOUBLE).  DOCOL does this:  It
pushes the old %esi on the return stack.  %eax points to the codeword of DOUBLE, so we
just add 4 on to it to get our new %esi:

<svg height="176" width="576" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled{fill:#fff}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h576v176H0z"/><text x="130" y="12">QUADRUPLE:</text><text x="146" y="44">codeword</text><text x="146" y="76">addr</text><text x="186" y="76">of</text><text x="210" y="76">DOUBLE</text><path class="solid end_marked_arrow" d="M272 72h128"/><text x="346" y="92">%eax</text><path class="solid end_marked_arrow" d="M384 88h16"/><text x="146" y="108">addr</text><text x="186" y="108">of</text><text x="210" y="108">DOUBLE</text><text x="346" y="108">+</text><text x="362" y="108">4</text><path class="solid" d="M376 102h8M376 106h8"/><text x="346" y="124">%esi</text><path class="solid end_marked_arrow" d="M384 120h16"/><text x="146" y="140">addr</text><text x="186" y="140">of</text><text x="210" y="140">EXIT</text><text x="410" y="60">DOUBLE:</text><text x="426" y="92">addr</text><text x="466" y="92">of</text><text x="490" y="92">DOCOL</text><text x="426" y="124">addr</text><text x="466" y="124">of</text><text x="490" y="124">DUP</text><text x="426" y="156">etc.</text><text x="2" y="92">top</text><text x="34" y="92">of</text><text x="58" y="92">return</text><text x="2" y="108">stack</text><text x="50" y="108">points</text><path class="solid end_marked_arrow" d="M104 104h16"/><path class="solid" d="M132 24h152M132 24v128M284 24v128M132 56h152M132 88h152M132 120h152M132 152h152"/><g><path class="solid" d="M412 72h152M412 72v88M564 72v88M412 104h152M412 136h152"/></g></svg>

Then we do NEXT, and because of the magic of threaded code that increments %esi again
and calls DUP.

Well, it seems to work.

One minor point here.  Because DOCOL is the first bit of assembly actually to be defined
in this file (the others were just macros), and because I usually compile this code with the
text segment starting at address 0, DOCOL has address 0.  So if you are disassembling the
code and see a word with a codeword of 0, you will immediately know that the word is
written in FORTH (it's not an assembler primitive) and so uses DOCOL as the interpreter.

## STARTING UP

Now let's get down to nuts and bolts.  When we start the program we need to set up
a few things like the return stack.  But as soon as we can, we want to jump into FORTH
code (albeit much of the "early" FORTH code will still need to be written as
assembly language primitives).

This is what the set up code does.  Does a tiny bit of house-keeping, sets up the
separate return stack (NB: Linux gives us the ordinary parameter stack already), then
immediately jumps to a FORTH word called QUIT.  Despite its name, QUIT doesn't quit
anything.  It resets some internal state and starts reading and interpreting commands.
(The reason it is called QUIT is because you can call QUIT from your own FORTH code
to "quit" your program and go back to interpreting).

    /* Assembler entry point. */
        .text
        .globl _start
    _start:
        cld
        mov %esp,var_S0         // Save the initial data stack pointer in FORTH variable S0.
        mov $return_stack_top,%ebp // Initialise the return stack.
        call set_up_data_segment

        mov $cold_start,%esi    // Initialise interpreter.
        NEXT                    // Run interpreter!
    
        .section .rodata
    cold_start:                     // High-level code without a codeword.
        .int QUIT

## BUILT-IN WORDS

Remember our dictionary entries (headers)?  Let's bring those together with the codeword
and data words to see how : DOUBLE DUP + ; really looks in memory.

<svg height="160" width="832" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled{fill:#fff}text{font-family:monospace;font-size:14px}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h832v160H0z"/><text x="82" y="12">pointer</text><path class="filled" d="M88 28l4-12 4 12z"/><path class="solid" d="M92 32v32"/><text x="82" y="76">LINK</text><text x="162" y="76">6</text><text x="194" y="76">D</text><text x="226" y="76">O</text><text x="258" y="76">U</text><text x="290" y="76">B</text><text x="322" y="76">L</text><text x="354" y="76">E</text><text x="386" y="76">0</text><text x="418" y="76">DOCOL</text><text x="522" y="76">DUP</text><text x="626" y="76">+</text><text x="730" y="76">EXIT</text><path class="solid" marker-end="url(#arrow)" d="M532 80v48"/><path class="filled" d="M88 108l4-12 4 12z"/><text x="154" y="108">len</text><text x="378" y="108">pad</text><text x="418" y="108">codeword</text><path class="solid" d="M92 112v16"/><text x="82" y="140">LINK</text><text x="530" y="140">codeword</text><text x="146" y="12">to</text><text x="170" y="12">previous</text><text x="242" y="12">word</text><text x="122" y="140">in</text><text x="146" y="140">next</text><text x="186" y="140">word</text><text x="450" y="140">points</text><text x="506" y="140">to</text><text x="602" y="140">of</text><text x="626" y="140">DUP</text><path class="solid" d="M68 56h752M68 56v32M148 56v32M180 56v32M212 56v32M244 56v32M276 56v32M308 56v32M340 56v32M372 56v32M404 56v32M508 56v32M612 56v32M716 56v32M820 56v32M68 88h752"/></svg>
        
Initially we can't just write ": DOUBLE DUP + ;" (ie. that literal string) here because we
don't yet have anything to read the string, break it up at spaces, parse each word, etc. etc.
So instead we will have to define built-in words using the GNU assembler data constructors
(like .int, .byte, .string, .ascii and so on -- look them up in the gas info page if you are
unsure of them).

The long way would be:

            .int <link to previous word>
            .byte 6                 // len
            .ascii "DOUBLE"         // string
            .byte 0                 // padding
    DOUBLE: .int DOCOL              // codeword
            .int DUP                // pointer to codeword of DUP
            .int PLUS               // pointer to codeword of +
            .int EXIT               // pointer to codeword of EXIT

That's going to get quite tedious rather quickly, so here I define an assembler macro
so that I can just write:

        defword "DOUBLE",6,,DOUBLE
        .int DUP,PLUS,EXIT

and I'll get exactly the same effect.

Don't worry too much about the exact implementation details of this macro - it's complicated!

        /* Flags - these are discussed later. */
        .set F_IMMED,0x80
        .set F_HIDDEN,0x20
        .set F_LENMASK,0x1f     // length mask

        // Store the chain of links.
        .set link,0

        .macro defword name, namelen, flags=0, label
        .section .rodata
        .align 4
        .globl name_\label
    name_\label :
        .int link               // link
        .set link,name_\label
        .byte \flags+\namelen   // flags + length byte
        .ascii "\name"          // the name
        .align 4                // padding to next 4 byte boundary
        .globl \label
    \label :
        .int DOCOL              // codeword - the interpreter
        // list of word pointers follow
        .endm

Similarly I want a way to write words written in assembly language.  There will quite a few
of these to start with because, well, everything has to start in assembly before there's
enough "infrastructure" to be able to start writing FORTH words, but also I want to define
some common FORTH words in assembly language for speed, even though I could write them in FORTH.

This is what DUP looks like in memory:

<svg height="160" width="672" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon,rect{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled{fill:#fff}text{font-family:monospace;font-size:14px}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" d="M0 0h672v160H0z"/><rect class="solid" height="32" rx="0" width="312" x="4" y="56" fill="#fff"/><text x="18" y="76">LINK</text><text x="98" y="76">3</text><text x="130" y="76">D</text><text x="162" y="76">U</text><text x="194" y="76">P</text><text x="226" y="76">code</text><path class="solid" d="M256 80h8"/><text x="266" y="76">DUP</text><text x="18" y="12">pointer</text><path class="filled" d="M24 28l4-12 4 12z"/><path class="solid" d="M28 32v32M84 48v48M116 48v48M148 48v48M180 48v48M212 48v48"/><path class="solid" marker-end="url(#arrow)" d="M296 72h176"/><path class="filled" d="M24 108l4-12 4 12z"/><text x="90" y="108">len</text><text x="226" y="108">codeword</text><path class="solid" d="M28 112v16"/><text x="18" y="140">LINK</text><text x="82" y="12">to</text><text x="106" y="12">previous</text><text x="178" y="12">word</text><text x="482" y="76">points</text><text x="538" y="76">to</text><text x="562" y="76">the</text><text x="594" y="76">assembly</text><text x="482" y="92">code</text><text x="522" y="92">used</text><text x="562" y="92">to</text><text x="586" y="92">write</text><text x="634" y="92">DUP,</text><text x="482" y="108">which</text><text x="530" y="108">ends</text><text x="570" y="108">with</text><text x="610" y="108">NEXT.</text><text x="58" y="140">in</text><text x="82" y="140">next</text><text x="122" y="140">word</text></svg>

Again, for brevity in writing the header I'm going to write an assembler macro called defcode.
As with defword above, don't worry about the complicated details of the macro.

        .macro defcode name, namelen, flags=0, label
        .section .rodata
        .align 4
        .globl name_\label
    name_\label :
        .int link               // link
        .set link,name_\label
        .byte \flags+\namelen   // flags + length byte
        .ascii "\name"          // the name
        .align 4                // padding to next 4 byte boundary
        .globl \label
    \label :
        .int code_\label        // codeword
        .text
        //.align 4
        .globl code_\label
    code_\label :                   // assembler code follows
        .endm

Now some easy FORTH primitives.  These are written in assembly for speed.  If you understand
i386 assembly language then it is worth reading these.  However if you don't understand assembly
you can skip the details.

        defcode "DROP",4,,DROP
        pop %eax                // drop top of stack
        NEXT

        defcode "SWAP",4,,SWAP
        pop %eax                // swap top two elements on stack
        pop %ebx
        push %eax
        push %ebx
        NEXT

        defcode "DUP",3,,DUP
        mov (%esp),%eax         // duplicate top of stack
        push %eax
        NEXT

        defcode "OVER",4,,OVER
        mov 4(%esp),%eax        // get the second element of stack
        push %eax               // and push it on top
        NEXT

        defcode "ROT",3,,ROT
        pop %eax
        pop %ebx
        pop %ecx
        push %ebx
        push %eax
        push %ecx
        NEXT

        defcode "-ROT",4,,NROT
        pop %eax
        pop %ebx
        pop %ecx
        push %eax
        push %ecx
        push %ebx
        NEXT

        defcode "2DROP",5,,TWODROP // drop top two elements of stack
        pop %eax
        pop %eax
        NEXT

        defcode "2DUP",4,,TWODUP // duplicate top two elements of stack
        mov (%esp),%eax
        mov 4(%esp),%ebx
        push %ebx
        push %eax
        NEXT

        defcode "2SWAP",5,,TWOSWAP // swap top two pairs of elements of stack
        pop %eax
        pop %ebx
        pop %ecx
        pop %edx
        push %ebx
        push %eax
        push %edx
        push %ecx
        NEXT

        defcode "?DUP",4,,QDUP  // duplicate top of stack if non-zero
        movl (%esp),%eax
        test %eax,%eax
        jz 1f
        push %eax
    1:  NEXT

        defcode "1+",2,,INCR
        incl (%esp)             // increment top of stack
        NEXT

        defcode "1-",2,,DECR
        decl (%esp)             // decrement top of stack
        NEXT

        defcode "4+",2,,INCR4
        addl $4,(%esp)          // add 4 to top of stack
        NEXT

        defcode "4-",2,,DECR4
        subl $4,(%esp)          // subtract 4 from top of stack
        NEXT

        defcode "+",1,,ADD
        pop %eax                // get top of stack
        addl %eax,(%esp)        // and add it to next word on stack
        NEXT

        defcode "-",1,,SUB
        pop %eax                // get top of stack
        subl %eax,(%esp)        // and subtract it from next word on stack
        NEXT

        defcode "*",1,,MUL
        pop %eax
        pop %ebx
        imull %ebx,%eax
        push %eax               // ignore overflow
        NEXT

In this FORTH, only /MOD is primitive.  Later we will define the / and MOD words in
terms of the primitive /MOD.  The design of the i386 assembly instruction idiv which
leaves both quotient and remainder makes this the obvious choice.

        defcode "/MOD",4,,DIVMOD
        xor %edx,%edx
        pop %ebx
        pop %eax
        idivl %ebx
        push %edx               // push remainder
        push %eax               // push quotient
        NEXT

Lots of comparison operations like =, <, >, etc..

ANS FORTH says that the comparison words should return all (binary) 1's for
TRUE and all 0's for FALSE.  However this is a bit of a strange convention
so this FORTH breaks it and returns the more normal (for C programmers ...)
1 meaning TRUE and 0 meaning FALSE.

        defcode "=",1,,EQU      // top two words are equal?
        pop %eax
        pop %ebx
        cmp %ebx,%eax
        sete %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "<>",2,,NEQU    // top two words are not equal?
        pop %eax
        pop %ebx
        cmp %ebx,%eax
        setne %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "<",1,,LT
        pop %eax
        pop %ebx
        cmp %eax,%ebx
        setl %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode ">",1,,GT
        pop %eax
        pop %ebx
        cmp %eax,%ebx
        setg %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "<=",2,,LE
        pop %eax
        pop %ebx
        cmp %eax,%ebx
        setle %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode ">=",2,,GE
        pop %eax
        pop %ebx
        cmp %eax,%ebx
        setge %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0=",2,,ZEQU    // top of stack equals 0?
        pop %eax
        test %eax,%eax
        setz %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0<>",3,,ZNEQU  // top of stack not 0?
        pop %eax
        test %eax,%eax
        setnz %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0<",2,,ZLT     // comparisons with 0
        pop %eax
        test %eax,%eax
        setl %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0>",2,,ZGT
        pop %eax
        test %eax,%eax
        setg %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0<=",3,,ZLE
        pop %eax
        test %eax,%eax
        setle %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "0>=",3,,ZGE
        pop %eax
        test %eax,%eax
        setge %al
        movzbl %al,%eax
        pushl %eax
        NEXT

        defcode "AND",3,,AND    // bitwise AND
        pop %eax
        andl %eax,(%esp)
        NEXT

        defcode "OR",2,,OR      // bitwise OR
        pop %eax
        orl %eax,(%esp)
        NEXT

        defcode "XOR",3,,XOR    // bitwise XOR
        pop %eax
        xorl %eax,(%esp)
        NEXT

        defcode "INVERT",6,,INVERT // this is the FORTH bitwise "NOT" function (cf. NEGATE and NOT)
        notl (%esp)
        NEXT

## RETURNING FROM FORTH WORDS

Time to talk about what happens when we EXIT a function.  In this diagram QUADRUPLE has called
DOUBLE, and DOUBLE is about to exit (look at where %esi is pointing):

<svg height="224" width="448" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled{fill:#fff}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h448v224H0z"/><text x="2" y="12">QUADRUPLE</text><text x="18" y="44">codeword</text><text x="18" y="76">addr</text><text x="58" y="76">of</text><text x="82" y="76">DOUBLE</text><path class="solid end_marked_arrow" d="M144 72h128"/><text x="18" y="108">addr</text><text x="58" y="108">of</text><text x="82" y="108">DOUBLE</text><text x="18" y="140">addr</text><text x="58" y="140">of</text><text x="82" y="140">EXIT</text><text x="282" y="60">DOUBLE</text><text x="298" y="92">codeword</text><text x="298" y="124">addr</text><text x="338" y="124">of</text><text x="362" y="124">DUP</text><text x="298" y="156">addr</text><text x="338" y="156">of</text><text x="362" y="156">+</text><text x="298" y="188">addr</text><text x="338" y="188">of</text><text x="362" y="188">EXIT</text><text x="218" y="188">%esi</text><path class="solid end_marked_arrow" d="M256 184h16"/><path class="solid" d="M4 24h152M4 24v128M156 24v128M4 56h152M4 88h152M4 120h152M4 152h152"/><g><path class="solid" d="M284 72h152M284 72v128M436 72v128M284 104h152M284 136h152M284 168h152M284 200h152"/></g></svg>

What happens when the + function does NEXT?  Well, the following code is executed.

        defcode "EXIT",4,,EXIT
        POPRSP %esi             // pop return stack into %esi
        NEXT

EXIT gets the old %esi which we saved from before on the return stack, and puts it in %esi.
So after this (but just before NEXT) we get:

<svg height="224" width="512" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled{fill:#fff}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h512v224H0z"/><text x="66" y="12">QUADRUPLE</text><text x="82" y="44">codeword</text><text x="82" y="76">addr</text><text x="122" y="76">of</text><text x="146" y="76">DOUBLE</text><path class="solid end_marked_arrow" d="M208 72h128"/><text x="82" y="108">addr</text><text x="122" y="108">of</text><text x="146" y="108">DOUBLE</text><text x="82" y="140">addr</text><text x="122" y="140">of</text><text x="146" y="140">EXIT</text><text x="346" y="60">DOUBLE</text><text x="362" y="92">codeword</text><text x="362" y="124">addr</text><text x="402" y="124">of</text><text x="426" y="124">DUP</text><text x="362" y="156">addr</text><text x="402" y="156">of</text><text x="426" y="156">+</text><text x="362" y="188">addr</text><text x="402" y="188">of</text><text x="426" y="188">EXIT</text><text x="2" y="108">%esi</text><path class="solid end_marked_arrow" d="M40 104h16"/><path class="solid" d="M68 24h152M68 24v128M220 24v128M68 56h152M68 88h152M68 120h152M68 152h152"/><g><path class="solid" d="M348 72h152M348 72v128M500 72v128M348 104h152M348 136h152M348 168h152M348 200h152"/></g></svg>

And NEXT just completes the job by, well, in this case just by calling DOUBLE again :-)

## LITERALS

The final point I "glossed over" before was how to deal with functions that do anything
apart from calling other functions.  For example, suppose that DOUBLE was defined like this:

        : DOUBLE 2 * ;

It does the same thing, but how do we compile it since it contains the literal 2?  One way
would be to have a function called "2" (which you'd have to write in assembler), but you'd need
a function for every single literal that you wanted to use.

FORTH solves this by compiling the function using a special word called LIT:

<svg height="64" width="632" xmlns="http://www.w3.org/2000/svg"><style>circle,line,path,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled,.nofill{fill:#fff}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h632v64H0z"/><path class="nofill" d="M88 16a16 16 0 000 16"/><text x="90" y="28">usual</text><text x="138" y="28">header</text><text x="194" y="28">of</text><text x="218" y="28">DOUBLE</text><path class="nofill" d="M272 16a16 16 0 010 16"/><text x="314" y="28">DOCOL</text><text x="378" y="28">LIT</text><text x="442" y="28">2</text><text x="506" y="28">✱</text><text x="570" y="28">EXIT</text><path class="solid" d="M68 8h552M68 8v32M300 8v32M364 8v32M428 8v32M492 8v32M556 8v32M620 8v32M68 40h552"/></svg>

LIT is executed in the normal way, but what it does next is definitely not normal.  It
looks at %esi (which now points to the number 2), grabs it, pushes it on the stack, then
manipulates %esi in order to skip the number as if it had never been there.

What's neat is that the whole grab/manipulate can be done using a single byte single
i386 instruction, our old friend LODSL.  Rather than me drawing more ASCII-art diagrams,
see if you can find out how LIT works:

        defcode "LIT",3,,LIT
        // %esi points to the next command, but in this case it points to the next
        // literal 32 bit integer.  Get that literal into %eax and increment %esi.
        // On x86, it's a convenient single byte instruction!  (cf. NEXT macro)
        lodsl
        push %eax               // push the literal number on to stack
        NEXT

## MEMORY

As important point about FORTH is that it gives you direct access to the lowest levels
of the machine.  Manipulating memory directly is done frequently in FORTH, and these are
the primitive words for doing it.

        defcode "!",1,,STORE
        pop %ebx                // address to store at
        pop %eax                // data to store there
        mov %eax,(%ebx)         // store it
        NEXT

        defcode "@",1,,FETCH
        pop %ebx                // address to fetch
        mov (%ebx),%eax         // fetch it
        push %eax               // push value onto stack
        NEXT

        defcode "+!",2,,ADDSTORE
        pop %ebx                // address
        pop %eax                // the amount to add
        addl %eax,(%ebx)        // add it
        NEXT

        defcode "-!",2,,SUBSTORE
        pop %ebx                // address
        pop %eax                // the amount to subtract
        subl %eax,(%ebx)        // add it
        NEXT

! and @ (STORE and FETCH) store 32-bit words.  It's also useful to be able to read and write bytes
so we also define standard words C@ and C!.

Byte-oriented operations only work on architectures which permit them (i386 is one of those).

        defcode "C!",2,,STOREBYTE
        pop %ebx                // address to store at
        pop %eax                // data to store there
        movb %al,(%ebx)         // store it
        NEXT

        defcode "C@",2,,FETCHBYTE
        pop %ebx                // address to fetch
        xor %eax,%eax
        movb (%ebx),%al         // fetch it
        push %eax               // push value onto stack
        NEXT

        /* C@C! is a useful byte copy primitive. */
        defcode "C@C!",4,,CCOPY
        movl 4(%esp),%ebx       // source address
        movb (%ebx),%al         // get source character
        pop %edi                // destination address
        stosb                   // copy to destination
        push %edi               // increment destination address
        incl 4(%esp)            // increment source address
        NEXT

        /* and CMOVE is a block copy operation. */
        defcode "CMOVE",5,,CMOVE
        mov %esi,%edx           // preserve %esi
        pop %ecx                // length
        pop %edi                // destination address
        pop %esi                // source address
        rep movsb               // copy source to destination
        mov %edx,%esi           // restore %esi
        NEXT

## BUILT-IN VARIABLES

These are some built-in variables and related standard FORTH words.  Of these, the only one that we
have discussed so far was LATEST, which points to the last (most recently defined) word in the
FORTH dictionary.  LATEST is also a FORTH word which pushes the address of LATEST (the variable)
on to the stack, so you can read or write it using @ and ! operators.  For example, to print
the current value of LATEST (and this can apply to any FORTH variable) you would do:

        LATEST @ . CR

To make defining variables shorter, I'm using a macro called defvar, similar to defword and
defcode above.  (In fact the defvar macro uses defcode to do the dictionary header).

        .macro defvar name, namelen, flags=0, label, initial=0
        defcode \name,\namelen,\flags,\label
        push $var_\name
        NEXT
        .data
        .align 4
    var_\name :
        .int \initial
        .endm

The built-in variables are:

* STATE           Is the interpreter executing code (0) or compiling a word (non-zero)?
* LATEST          Points to the latest (most recently defined) word in the dictionary.
* HERE            Points to the next free byte of memory.  When compiling, compiled words go here.
* S0              Stores the address of the top of the parameter stack.
* BASE            The current base for printing and reading numbers.

        defvar "STATE",5,,STATE
        defvar "HERE",4,,HERE
        defvar "LATEST",6,,LATEST,name_SYSCALL0 // SYSCALL0 must be last in built-in dictionary
        defvar "S0",2,,SZ
        defvar "BASE",4,,BASE,10

## BUILT-IN CONSTANTS

It's also useful to expose a few constants to FORTH.  When the word is executed it pushes a
constant value on the stack.

The built-in constants are:

* VERSION         Is the current version of this FORTH.
* R0              The address of the top of the return stack.
* DOCOL           Pointer to DOCOL.
* F_IMMED         The IMMEDIATE flag's actual value.
* F_HIDDEN        The HIDDEN flag's actual value.
* F_LENMASK       The length mask in the flags/len byte.
* SYS_*           and the numeric codes of various Linux syscalls (from <asm/unistd.h>)

    //#include <asm-i386/unistd.h>  // you might need this instead
    #include <asm/unistd.h>

        .macro defconst name, namelen, flags=0, label, value
        defcode \name,\namelen,\flags,\label
        push $\value
        NEXT
        .endm

        defconst "VERSION",7,,VERSION,JONES_VERSION
        defconst "R0",2,,RZ,return_stack_top
        defconst "DOCOL",5,,__DOCOL,DOCOL
        defconst "F_IMMED",7,,__F_IMMED,F_IMMED
        defconst "F_HIDDEN",8,,__F_HIDDEN,F_HIDDEN
        defconst "F_LENMASK",9,,__F_LENMASK,F_LENMASK

        defconst "SYS_EXIT",8,,SYS_EXIT,__NR_exit
        defconst "SYS_OPEN",8,,SYS_OPEN,__NR_open
        defconst "SYS_CLOSE",9,,SYS_CLOSE,__NR_close
        defconst "SYS_READ",8,,SYS_READ,__NR_read
        defconst "SYS_WRITE",9,,SYS_WRITE,__NR_write
        defconst "SYS_CREAT",9,,SYS_CREAT,__NR_creat
        defconst "SYS_BRK",7,,SYS_BRK,__NR_brk

        defconst "O_RDONLY",8,,__O_RDONLY,0
        defconst "O_WRONLY",8,,__O_WRONLY,1
        defconst "O_RDWR",6,,__O_RDWR,2
        defconst "O_CREAT",7,,__O_CREAT,0100
        defconst "O_EXCL",6,,__O_EXCL,0200
        defconst "O_TRUNC",7,,__O_TRUNC,01000
        defconst "O_APPEND",8,,__O_APPEND,02000
        defconst "O_NONBLOCK",10,,__O_NONBLOCK,04000

## RETURN STACK

These words allow you to access the return stack.  Recall that the register %ebp always points to
the top of the return stack.

        defcode ">R",2,,TOR
        pop %eax                // pop parameter stack into %eax
        PUSHRSP %eax            // push it on to the return stack
        NEXT

        defcode "R>",2,,FROMR
        POPRSP %eax             // pop return stack on to %eax
        push %eax               // and push on to parameter stack
        NEXT

        defcode "RSP@",4,,RSPFETCH
        push %ebp
        NEXT

        defcode "RSP!",4,,RSPSTORE
        pop %ebp
        NEXT

        defcode "RDROP",5,,RDROP
        addl $4,%ebp            // pop return stack and throw away
        NEXT

## PARAMETER (DATA) STACK

These functions allow you to manipulate the parameter stack.  Recall that Linux sets up the parameter
stack for us, and it is accessed through %esp.

        defcode "DSP@",4,,DSPFETCH
        mov %esp,%eax
        push %eax
        NEXT

        defcode "DSP!",4,,DSPSTORE
        pop %esp
        NEXT

# INPUT AND OUTPUT

These are our first really meaty/complicated FORTH primitives.  I have chosen to write them in
assembler, but surprisingly in "real" FORTH implementations these are often written in terms
of more fundamental FORTH primitives.  I chose to avoid that because I think that just obscures
the implementation.  After all, you may not understand assembler but you can just think of it
as an opaque block of code that does what it says.

Let's discuss input first.

The FORTH word KEY reads the next byte from stdin (and pushes it on the parameter stack).
So if KEY is called and someone hits the space key, then the number 32 (ASCII code of space)
is pushed on the stack.

In FORTH there is no distinction between reading code and reading input.  We might be reading
and compiling code, we might be reading words to execute, we might be asking for the user
to type their name -- ultimately it all comes in through KEY.

The implementation of KEY uses an input buffer of a certain size (defined at the end of this
file).  It calls the Linux read(2) system call to fill this buffer and tracks its position
in the buffer using a couple of variables, and if it runs out of input buffer then it refills
it automatically.  The other thing that KEY does is if it detects that stdin has closed, it
exits the program, which is why when you hit ^D the FORTH system cleanly exits.

     buffer                           bufftop
        |                                |
        V                                V
        +-------------------------------|--------------------------------------+
        | INPUT READ FROM STDIN ....... | unused part of the buffer            |
        +-------------------------------|--------------------------------------+
                          ^
                          |
                       currkey (next character to read)

        <---------------------- BUFFER_SIZE (4096 bytes) ---------------------->
*/

        defcode "KEY",3,,KEY
        call _KEY
        push %eax               // push return value on stack
        NEXT
_KEY:
        mov (currkey),%ebx
        cmp (bufftop),%ebx
        jge 1f                  // exhausted the input buffer?
        xor %eax,%eax
        mov (%ebx),%al          // get next key from input buffer
        inc %ebx
        mov %ebx,(currkey)      // increment currkey
        ret

1:      // Out of input; use read(2) to fetch more input from stdin.
        xor %ebx,%ebx           // 1st param: stdin
        mov $buffer,%ecx        // 2nd param: buffer
        mov %ecx,currkey
        mov $BUFFER_SIZE,%edx   // 3rd param: max length
        mov $__NR_read,%eax     // syscall: read
        int $0x80
        test %eax,%eax          // If %eax <= 0, then exit.
        jbe 2f
        addl %eax,%ecx          // buffer+%eax = bufftop
        mov %ecx,bufftop
        jmp _KEY

2:      // Error or end of input: exit the program.
        xor %ebx,%ebx
        mov $__NR_exit,%eax     // syscall: exit
        int $0x80

        .data
        .align 4
currkey:
        .int buffer             // Current place in input buffer (next character to read).
bufftop:
        .int buffer             // Last valid data in input buffer + 1.

/*
        By contrast, output is much simpler.  The FORTH word EMIT writes out a single byte to stdout.
        This implementation just uses the write system call.  No attempt is made to buffer output, but
        it would be a good exercise to add it.
*/

        defcode "EMIT",4,,EMIT
        pop %eax
        call _EMIT
        NEXT
_EMIT:
        mov $1,%ebx             // 1st param: stdout

        // write needs the address of the byte to write
        mov %al,emit_scratch
        mov $emit_scratch,%ecx  // 2nd param: address

        mov $1,%edx             // 3rd param: nbytes = 1

        mov $__NR_write,%eax    // write syscall
        int $0x80
        ret

        .data                   // NB: easier to fit in the .data section
emit_scratch:
        .space 1                // scratch used by EMIT

/*
        Back to input, WORD is a FORTH word which reads the next full word of input.

        What it does in detail is that it first skips any blanks (spaces, tabs, newlines and so on).
        Then it calls KEY to read characters into an internal buffer until it hits a blank.  Then it
        calculates the length of the word it read and returns the address and the length as
        two words on the stack (with the length at the top of stack).

        Notice that WORD has a single internal buffer which it overwrites each time (rather like
        a static C string).  Also notice that WORD's internal buffer is just 32 bytes long and
        there is NO checking for overflow.  31 bytes happens to be the maximum length of a
        FORTH word that we support, and that is what WORD is used for: to read FORTH words when
        we are compiling and executing code.  The returned strings are not NUL-terminated.

        Start address+length is the normal way to represent strings in FORTH (not ending in an
        ASCII NUL character as in C), and so FORTH strings can contain any character including NULs
        and can be any length.

        WORD is not suitable for just reading strings (eg. user input) because of all the above
        peculiarities and limitations.

        Note that when executing, you'll see:
        WORD FOO
        which puts "FOO" and length 3 on the stack, but when compiling:
        : BAR WORD FOO ;
        is an error (or at least it doesn't do what you might expect).  Later we'll talk about compiling
        and immediate mode, and you'll understand why.
*/

        defcode "WORD",4,,WORD
        call _WORD
        push %edi               // push base address
        push %ecx               // push length
        NEXT

_WORD:
        /* Search for first non-blank character.  Also skip \ comments. */
1:
        call _KEY               // get next key, returned in %eax
        cmpb $'\\',%al          // start of a comment?
        je 3f                   // if so, skip the comment
        cmpb $' ',%al
        jbe 1b                  // if so, keep looking

        /* Search for the end of the word, storing chars as we go. */
        mov $word_buffer,%edi   // pointer to return buffer
2:
        stosb                   // add character to return buffer
        call _KEY               // get next key, returned in %al
        cmpb $' ',%al           // is blank?
        ja 2b                   // if not, keep looping

        /* Return the word (well, the static buffer) and length. */
        sub $word_buffer,%edi
        mov %edi,%ecx           // return length of the word
        mov $word_buffer,%edi   // return address of the word
        ret

        /* Code to skip \ comments to end of the current line. */
3:
        call _KEY
        cmpb $'\n',%al          // end of line yet?
        jne 3b
        jmp 1b

        .data                   // NB: easier to fit in the .data section
        // A static buffer where WORD returns.  Subsequent calls
        // overwrite this buffer.  Maximum word length is 32 chars.
word_buffer:
        .space 32

/*
        As well as reading in words we'll need to read in numbers and for that we are using a function
        called NUMBER.  This parses a numeric string such as one returned by WORD and pushes the
        number on the parameter stack.

        The function uses the variable BASE as the base (radix) for conversion, so for example if
        BASE is 2 then we expect a binary number.  Normally BASE is 10.

        If the word starts with a '-' character then the returned value is negative.

        If the string can't be parsed as a number (or contains characters outside the current BASE)
        then we need to return an error indication.  So NUMBER actually returns two items on the stack.
        At the top of stack we return the number of unconverted characters (ie. if 0 then all characters
        were converted, so there is no error).  Second from top of stack is the parsed number or a
        partial value if there was an error.
*/
        defcode "NUMBER",6,,NUMBER
        pop %ecx                // length of string
        pop %edi                // start address of string
        call _NUMBER
        push %eax               // parsed number
        push %ecx               // number of unparsed characters (0 = no error)
        NEXT

_NUMBER:
        xor %eax,%eax
        xor %ebx,%ebx

        test %ecx,%ecx          // trying to parse a zero-length string is an error, but will return 0.
        jz 5f

        movl var_BASE,%edx      // get BASE (in %dl)

        // Check if first character is '-'.
        movb (%edi),%bl         // %bl = first character in string
        inc %edi
        push %eax               // push 0 on stack
        cmpb $'-',%bl           // negative number?
        jnz 2f
        pop %eax
        push %ebx               // push <> 0 on stack, indicating negative
        dec %ecx
        jnz 1f
        pop %ebx                // error: string is only '-'.
        movl $1,%ecx
        ret

        // Loop reading digits.
1:      imull %edx,%eax         // %eax *= BASE
        movb (%edi),%bl         // %bl = next character in string
        inc %edi

        // Convert 0-9, A-Z to a number 0-35.
2:      subb $'0',%bl           // < '0'?
        jb 4f
        cmp $10,%bl             // <= '9'?
        jb 3f
        subb $17,%bl            // < 'A'? (17 is 'A'-'0')
        jb 4f
        addb $10,%bl

3:      cmp %dl,%bl             // >= BASE?
        jge 4f

        // OK, so add it to %eax and loop.
        add %ebx,%eax
        dec %ecx
        jnz 1b

        // Negate the result if first character was '-' (saved on the stack).
4:      pop %ebx
        test %ebx,%ebx
        jz 5f
        neg %eax

5:      ret

/*
        DICTIONARY LOOK UPS ----------------------------------------------------------------------

        We're building up to our prelude on how FORTH code is compiled, but first we need yet more infrastructure.

        The FORTH word FIND takes a string (a word as parsed by WORD -- see above) and looks it up in the
        dictionary.  What it actually returns is the address of the dictionary header, if it finds it,
        or 0 if it didn't.

        So if DOUBLE is defined in the dictionary, then WORD DOUBLE FIND returns the following pointer:

    pointer to this
        |
        |
        V
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+

        See also >CFA and >DFA.

        FIND doesn't find dictionary entries which are flagged as HIDDEN.  See below for why.
*/

        defcode "FIND",4,,FIND
        pop %ecx                // %ecx = length
        pop %edi                // %edi = address
        call _FIND
        push %eax               // %eax = address of dictionary entry (or NULL)
        NEXT

_FIND:
        push %esi               // Save %esi so we can use it in string comparison.

        // Now we start searching backwards through the dictionary for this word.
        mov var_LATEST,%edx     // LATEST points to name header of the latest word in the dictionary
1:      test %edx,%edx          // NULL pointer?  (end of the linked list)
        je 4f

        // Compare the length expected and the length of the word.
        // Note that if the F_HIDDEN flag is set on the word, then by a bit of trickery
        // this won't pick the word (the length will appear to be wrong).
        xor %eax,%eax
        movb 4(%edx),%al        // %al = flags+length field
        andb $(F_HIDDEN|F_LENMASK),%al // %al = name length
        cmpb %cl,%al            // Length is the same?
        jne 2f

        // Compare the strings in detail.
        push %ecx               // Save the length
        push %edi               // Save the address (repe cmpsb will move this pointer)
        lea 5(%edx),%esi        // Dictionary string we are checking against.
        repe cmpsb              // Compare the strings.
        pop %edi
        pop %ecx
        jne 2f                  // Not the same.

        // The strings are the same - return the header pointer in %eax
        pop %esi
        mov %edx,%eax
        ret

2:      mov (%edx),%edx         // Move back through the link field to the previous word
        jmp 1b                  // .. and loop.

4:      // Not found.
        pop %esi
        xor %eax,%eax           // Return zero to indicate not found.
        ret

/*
        FIND returns the dictionary pointer, but when compiling we need the codeword pointer (recall
        that FORTH definitions are compiled into lists of codeword pointers).  The standard FORTH
        word >CFA turns a dictionary pointer into a codeword pointer.

        The example below shows the result of:

                WORD DOUBLE FIND >CFA

        FIND returns a pointer to this
        |                               >CFA converts it to a pointer to this
        |                                          |
        V                                          V
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
                                                   codeword

        Notes:

        Because names vary in length, this isn't just a simple increment.

        In this FORTH you cannot easily turn a codeword pointer back into a dictionary entry pointer, but
        that is not true in most FORTH implementations where they store a back pointer in the definition
        (with an obvious memory/complexity cost).  The reason they do this is that it is useful to be
        able to go backwards (codeword -> dictionary entry) in order to decompile FORTH definitions
        quickly.

        What does CFA stand for?  My best guess is "Code Field Address".
*/

        defcode ">CFA",4,,TCFA
        pop %edi
        call _TCFA
        push %edi
        NEXT
_TCFA:
        xor %eax,%eax
        add $4,%edi             // Skip link pointer.
        movb (%edi),%al         // Load flags+len into %al.
        inc %edi                // Skip flags+len byte.
        andb $F_LENMASK,%al     // Just the length, not the flags.
        add %eax,%edi           // Skip the name.
        addl $3,%edi            // The codeword is 4-byte aligned.
        andl $~3,%edi
        ret

/*
        Related to >CFA is >DFA which takes a dictionary entry address as returned by FIND and
        returns a pointer to the first data field.

        FIND returns a pointer to this
        |                               >CFA converts it to a pointer to this
        |                                          |
        |                                          |    >DFA converts it to a pointer to this
        |                                          |             |
        V                                          V             V
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
                                                   codeword

        (Note to those following the source of FIG-FORTH / ciforth: My >DFA definition is
        different from theirs, because they have an extra indirection).

        You can see that >DFA is easily defined in FORTH just by adding 4 to the result of >CFA.
*/

        defword ">DFA",4,,TDFA
        .int TCFA               // >CFA         (get code field address)
        .int INCR4              // 4+           (add 4 to it to get to next word)
        .int EXIT               // EXIT         (return from FORTH word)

/*
        COMPILING ----------------------------------------------------------------------

        Now we'll talk about how FORTH compiles words.  Recall that a word definition looks like this:

                : DOUBLE DUP + ;

        and we have to turn this into:

          pointer to previous word
           ^
           |
        +--|------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|--|---------|------------|------------+
           ^       len                         pad  codeword      |
           |                                                      V
          LATEST points here                            points to codeword of DUP

        There are several problems to solve.  Where to put the new word?  How do we read words?  How
        do we define the words : (COLON) and ; (SEMICOLON)?

        FORTH solves this rather elegantly and as you might expect in a very low-level way which
        allows you to change how the compiler works on your own code.

        FORTH has an INTERPRET function (a true interpreter this time, not DOCOL) which runs in a
        loop, reading words (using WORD), looking them up (using FIND), turning them into codeword
        pointers (using >CFA) and deciding what to do with them.

        What it does depends on the mode of the interpreter (in variable STATE).

        When STATE is zero, the interpreter just runs each word as it looks them up.  This is known as
        immediate mode.

        The interesting stuff happens when STATE is non-zero -- compiling mode.  In this mode the
        interpreter appends the codeword pointer to user memory (the HERE variable points to the next
        free byte of user memory -- see DATA SEGMENT section below).

        So you may be able to see how we could define : (COLON).  The general plan is:

        (1) Use WORD to read the name of the function being defined.

        (2) Construct the dictionary entry -- just the header part -- in user memory:

    pointer to previous word (from LATEST)                      +-- Afterwards, HERE points here, where
           ^                                                    |   the interpreter will start appending
           |                                                    V   codewords.
        +--|------|---|---|---|---|---|---|---|---|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      |
        +---------|---|---|---|---|---|---|---|---|------------+
                   len                         pad  codeword

        (3) Set LATEST to point to the newly defined word, ...

        (4) .. and most importantly leave HERE pointing just after the new codeword.  This is where
            the interpreter will append codewords.

        (5) Set STATE to 1.  This goes into compile mode so the interpreter starts appending codewords to
            our partially-formed header.

        After : has run, our input is here:

        : DOUBLE DUP + ;
                 ^
                 |
                Next byte returned by KEY will be the 'D' character of DUP

        so the interpreter (now it's in compile mode, so I guess it's really the compiler) reads "DUP",
        looks it up in the dictionary, gets its codeword pointer, and appends it:

                                                                             +-- HERE updated to point here.
                                                                             |
                                                                             V
        +---------|---|---|---|---|---|---|---|---|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        |
        +---------|---|---|---|---|---|---|---|---|------------|------------+
                   len                         pad  codeword

        Next we read +, get the codeword pointer, and append it:

                                                                                          +-- HERE updated to point here.
                                                                                          |
                                                                                          V
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------+
                   len                         pad  codeword

        The issue is what happens next.  Obviously what we _don't_ want to happen is that we
        read ";" and compile it and go on compiling everything afterwards.

        At this point, FORTH uses a trick.  Remember the length byte in the dictionary definition
        isn't just a plain length byte, but can also contain flags.  One flag is called the
        IMMEDIATE flag (F_IMMED in this code).  If a word in the dictionary is flagged as
        IMMEDIATE then the interpreter runs it immediately _even if it's in compile mode_.

        This is how the word ; (SEMICOLON) works -- as a word flagged in the dictionary as IMMEDIATE.

        And all it does is append the codeword for EXIT on to the current definition and switch
        back to immediate mode (set STATE back to 0).  Shortly we'll see the actual definition
        of ; and we'll see that it's really a very simple definition, declared IMMEDIATE.

        After the interpreter reads ; and executes it 'immediately', we get this:

        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
                   len                         pad  codeword                                           ^
                                                                                                       |
                                                                                                      HERE
        STATE is set to 0.

        And that's it, job done, our new definition is compiled, and we're back in immediate mode
        just reading and executing words, perhaps including a call to test our new word DOUBLE.

        The only last wrinkle in this is that while our word was being compiled, it was in a
        half-finished state.  We certainly wouldn't want DOUBLE to be called somehow during
        this time.  There are several ways to stop this from happening, but in FORTH what we
        do is flag the word with the HIDDEN flag (F_HIDDEN in this code) just while it is
        being compiled.  This prevents FIND from finding it, and thus in theory stops any
        chance of it being called.

        The above explains how compiling, : (COLON) and ; (SEMICOLON) works and in a moment I'm
        going to define them.  The : (COLON) function can be made a little bit more general by writing
        it in two parts.  The first part, called CREATE, makes just the header:

                                                   +-- Afterwards, HERE points here.
                                                   |
                                                   V
        +---------|---|---|---|---|---|---|---|---+
        | LINK    | 6 | D | O | U | B | L | E | 0 |
        +---------|---|---|---|---|---|---|---|---+
                   len                         pad

        and the second part, the actual definition of : (COLON), calls CREATE and appends the
        DOCOL codeword, so leaving:

                                                                +-- Afterwards, HERE points here.
                                                                |
                                                                V
        +---------|---|---|---|---|---|---|---|---|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      |
        +---------|---|---|---|---|---|---|---|---|------------+
                   len                         pad  codeword

        CREATE is a standard FORTH word and the advantage of this split is that we can reuse it to
        create other types of words (not just ones which contain code, but words which contain variables,
        constants and other data).
*/

        defcode "CREATE",6,,CREATE

        // Get the name length and address.
        pop %ecx                // %ecx = length
        pop %ebx                // %ebx = address of name

        // Link pointer.
        movl var_HERE,%edi      // %edi is the address of the header
        movl var_LATEST,%eax    // Get link pointer
        stosl                   // and store it in the header.

        // Length byte and the word itself.
        mov %cl,%al             // Get the length.
        stosb                   // Store the length/flags byte.
        push %esi
        mov %ebx,%esi           // %esi = word
        rep movsb               // Copy the word
        pop %esi
        addl $3,%edi            // Align to next 4 byte boundary.
        andl $~3,%edi

        // Update LATEST and HERE.
        movl var_HERE,%eax
        movl %eax,var_LATEST
        movl %edi,var_HERE
        NEXT

/*
        Because I want to define : (COLON) in FORTH, not assembler, we need a few more FORTH words
        to use.

        The first is , (COMMA) which is a standard FORTH word which appends a 32 bit integer to the user
        memory pointed to by HERE, and adds 4 to HERE.  So the action of , (COMMA) is:

                                                        previous value of HERE
                                                                 |
                                                                 V
        +---------|---|---|---|---|---|---|---|---|-- - - - - --|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 |             |  <data>    |
        +---------|---|---|---|---|---|---|---|---|-- - - - - --|------------+
                   len                         pad                            ^
                                                                              |
                                                                        new value of HERE

        and <data> is whatever 32 bit integer was at the top of the stack.

        , (COMMA) is quite a fundamental operation when compiling.  It is used to append codewords
        to the current word that is being compiled.
*/

        defcode ",",1,,COMMA
        pop %eax                // Code pointer to store.
        call _COMMA
        NEXT
_COMMA:
        movl var_HERE,%edi      // HERE
        stosl                   // Store it.
        movl %edi,var_HERE      // Update HERE (incremented)
        ret

/*
        Our definitions of : (COLON) and ; (SEMICOLON) will need to switch to and from compile mode.

        Immediate mode vs. compile mode is stored in the global variable STATE, and by updating this
        variable we can switch between the two modes.

        For various reasons which may become apparent later, FORTH defines two standard words called
        [ and ] (LBRAC and RBRAC) which switch between modes:

        Word    Assembler       Action          Effect
        [       LBRAC           STATE := 0      Switch to immediate mode.
        ]       RBRAC           STATE := 1      Switch to compile mode.

        [ (LBRAC) is an IMMEDIATE word.  The reason is as follows: If we are in compile mode and the
        interpreter saw [ then it would compile it rather than running it.  We would never be able to
        switch back to immediate mode!  So we flag the word as IMMEDIATE so that even in compile mode
        the word runs immediately, switching us back to immediate mode.
*/

        defcode "[",1,F_IMMED,LBRAC
        xor %eax,%eax
        movl %eax,var_STATE     // Set STATE to 0.
        NEXT

        defcode "]",1,,RBRAC
        movl $1,var_STATE       // Set STATE to 1.
        NEXT

/*
        Now we can define : (COLON) using CREATE.  It just calls CREATE, appends DOCOL (the codeword), sets
        the word HIDDEN and goes into compile mode.
*/

        defword ":",1,,COLON
        .int WORD               // Get the name of the new word
        .int CREATE             // CREATE the dictionary entry / header
        .int LIT, DOCOL, COMMA  // Append DOCOL  (the codeword).
        .int LATEST, FETCH, HIDDEN // Make the word hidden (see below for definition).
        .int RBRAC              // Go into compile mode.
        .int EXIT               // Return from the function.

/*
        ; (SEMICOLON) is also elegantly simple.  Notice the F_IMMED flag.
*/

        defword ";",1,F_IMMED,SEMICOLON
        .int LIT, EXIT, COMMA   // Append EXIT (so the word will return).
        .int LATEST, FETCH, HIDDEN // Toggle hidden flag -- unhide the word (see below for definition).
        .int LBRAC              // Go back to IMMEDIATE mode.
        .int EXIT               // Return from the function.

/*
        EXTENDING THE COMPILER ----------------------------------------------------------------------

        Words flagged with IMMEDIATE (F_IMMED) aren't just for the FORTH compiler to use.  You can define
        your own IMMEDIATE words too, and this is a crucial aspect when extending basic FORTH, because
        it allows you in effect to extend the compiler itself.  Does gcc let you do that?

        Standard FORTH words like IF, WHILE, ." and so on are all written as extensions to the basic
        compiler, and are all IMMEDIATE words.

        The IMMEDIATE word toggles the F_IMMED (IMMEDIATE flag) on the most recently defined word,
        or on the current word if you call it in the middle of a definition.

        Typical usage is:

        : MYIMMEDWORD IMMEDIATE
                ...definition...
        ;

        but some FORTH programmers write this instead:

        : MYIMMEDWORD
                ...definition...
        ; IMMEDIATE

        The two usages are equivalent, to a first approximation.
*/

        defcode "IMMEDIATE",9,F_IMMED,IMMEDIATE
        movl var_LATEST,%edi    // LATEST word.
        addl $4,%edi            // Point to name/flags byte.
        xorb $F_IMMED,(%edi)    // Toggle the IMMED bit.
        NEXT

/*
        'addr HIDDEN' toggles the hidden flag (F_HIDDEN) of the word defined at addr.  To hide the
        most recently defined word (used above in : and ; definitions) you would do:

                LATEST @ HIDDEN

        'HIDE word' toggles the flag on a named 'word'.

        Setting this flag stops the word from being found by FIND, and so can be used to make 'private'
        words.  For example, to break up a large word into smaller parts you might do:

                : SUB1 ... subword ... ;
                : SUB2 ... subword ... ;
                : SUB3 ... subword ... ;
                : MAIN ... defined in terms of SUB1, SUB2, SUB3 ... ;
                HIDE SUB1
                HIDE SUB2
                HIDE SUB3

        After this, only MAIN is 'exported' or seen by the rest of the program.
*/

        defcode "HIDDEN",6,,HIDDEN
        pop %edi                // Dictionary entry.
        addl $4,%edi            // Point to name/flags byte.
        xorb $F_HIDDEN,(%edi)   // Toggle the HIDDEN bit.
        NEXT

        defword "HIDE",4,,HIDE
        .int WORD               // Get the word (after HIDE).
        .int FIND               // Look up in the dictionary.
        .int HIDDEN             // Set F_HIDDEN flag.
        .int EXIT               // Return.

/*
        ' (TICK) is a standard FORTH word which returns the codeword pointer of the next word.

        The common usage is:

        ' FOO ,

        which appends the codeword of FOO to the current word we are defining (this only works in compiled code).

        You tend to use ' in IMMEDIATE words.  For example an alternate (and rather useless) way to define
        a literal 2 might be:

        : LIT2 IMMEDIATE
                ' LIT ,         \ Appends LIT to the currently-being-defined word
                2 ,             \ Appends the number 2 to the currently-being-defined word
        ;

        So you could do:

        : DOUBLE LIT2 * ;

        (If you don't understand how LIT2 works, then you should review the material about compiling words
        and immediate mode).

        This definition of ' uses a cheat which I copied from buzzard92.  As a result it only works in
        compiled code.  It is possible to write a version of ' based on WORD, FIND, >CFA which works in
        immediate mode too.
*/
        defcode "'",1,,TICK
        lodsl                   // Get the address of the next word and skip it.
        pushl %eax              // Push it on the stack.
        NEXT

/*
        BRANCHING ----------------------------------------------------------------------

        It turns out that all you need in order to define looping constructs, IF-statements, etc.
        are two primitives.

        BRANCH is an unconditional branch. 0BRANCH is a conditional branch (it only branches if the
        top of stack is zero).

        The diagram below shows how BRANCH works in some imaginary compiled word.  When BRANCH executes,
        %esi starts by pointing to the offset field (compare to LIT above):

        +---------------------|-------|---- - - ---|------------|------------|---- - - - ----|------------+
        | (Dictionary header) | DOCOL |            | BRANCH     | offset     | (skipped)     | word       |
        +---------------------|-------|---- - - ---|------------|-----|------|---- - - - ----|------------+
                                                                   ^  |                       ^
                                                                   |  |                       |
                                                                   |  +-----------------------+
                                                                  %esi added to offset

        The offset is added to %esi to make the new %esi, and the result is that when NEXT runs, execution
        continues at the branch target.  Negative offsets work as expected.

        0BRANCH is the same except the branch happens conditionally.

        Now standard FORTH words such as IF, THEN, ELSE, WHILE, REPEAT, etc. can be implemented entirely
        in FORTH.  They are IMMEDIATE words which append various combinations of BRANCH or 0BRANCH
        into the word currently being compiled.

        As an example, code written like this:

                condition-code IF true-part THEN rest-code

        compiles to:

                condition-code 0BRANCH OFFSET true-part rest-code
                                          |             ^
                                          |             |
                                          +-------------+
*/

        defcode "BRANCH",6,,BRANCH
        add (%esi),%esi         // add the offset to the instruction pointer
        NEXT

        defcode "0BRANCH",7,,ZBRANCH
        pop %eax
        test %eax,%eax          // top of stack is zero?
        jz code_BRANCH          // if so, jump back to the branch function above
        lodsl                   // otherwise we need to skip the offset
        NEXT

/*
        LITERAL STRINGS ----------------------------------------------------------------------

        LITSTRING is a primitive used to implement the ." and S" operators (which are written in
        FORTH).  See the definition of those operators later.

        TELL just prints a string.  It's more efficient to define this in assembly because we
        can make it a single Linux syscall.
*/

        defcode "LITSTRING",9,,LITSTRING
        lodsl                   // get the length of the string
        push %esi               // push the address of the start of the string
        push %eax               // push it on the stack
        addl %eax,%esi          // skip past the string
        addl $3,%esi            // but round up to next 4 byte boundary
        andl $~3,%esi
        NEXT

        defcode "TELL",4,,TELL
        mov $1,%ebx             // 1st param: stdout
        pop %edx                // 3rd param: length of string
        pop %ecx                // 2nd param: address of string
        mov $__NR_write,%eax    // write syscall
        int $0x80
        NEXT

/*
        QUIT AND INTERPRET ----------------------------------------------------------------------

        QUIT is the first FORTH function called, almost immediately after the FORTH system "boots".
        As explained before, QUIT doesn't "quit" anything.  It does some initialisation (in particular
        it clears the return stack) and it calls INTERPRET in a loop to interpret commands.  The
        reason it is called QUIT is because you can call it from your own FORTH words in order to
        "quit" your program and start again at the user prompt.

        INTERPRET is the FORTH interpreter ("toploop", "toplevel" or "REPL" might be a more accurate
        description -- see: http://en.wikipedia.org/wiki/REPL).
*/

        // QUIT must not return (ie. must not call EXIT).
        defword "QUIT",4,,QUIT
        .int RZ,RSPSTORE        // R0 RSP!, clear the return stack
        .int INTERPRET          // interpret the next word
        .int BRANCH,-8          // and loop (indefinitely)

/*
        This interpreter is pretty simple, but remember that in FORTH you can always override
        it later with a more powerful one!
 */
        defcode "INTERPRET",9,,INTERPRET
        call _WORD              // Returns %ecx = length, %edi = pointer to word.

        // Is it in the dictionary?
        xor %eax,%eax
        movl %eax,interpret_is_lit // Not a literal number (not yet anyway ...)
        call _FIND              // Returns %eax = pointer to header or 0 if not found.
        test %eax,%eax          // Found?
        jz 1f

        // In the dictionary.  Is it an IMMEDIATE codeword?
        mov %eax,%edi           // %edi = dictionary entry
        movb 4(%edi),%al        // Get name+flags.
        push %ax                // Just save it for now.
        call _TCFA              // Convert dictionary entry (in %edi) to codeword pointer.
        pop %ax
        andb $F_IMMED,%al       // Is IMMED flag set?
        mov %edi,%eax
        jnz 4f                  // If IMMED, jump straight to executing.

        jmp 2f

1:      // Not in the dictionary (not a word) so assume it's a literal number.
        incl interpret_is_lit
        call _NUMBER            // Returns the parsed number in %eax, %ecx > 0 if error
        test %ecx,%ecx
        jnz 6f
        mov %eax,%ebx
        mov $LIT,%eax           // The word is LIT

2:      // Are we compiling or executing?
        movl var_STATE,%edx
        test %edx,%edx
        jz 4f                   // Jump if executing.

        // Compiling - just append the word to the current dictionary definition.
        call _COMMA
        mov interpret_is_lit,%ecx // Was it a literal?
        test %ecx,%ecx
        jz 3f
        mov %ebx,%eax           // Yes, so LIT is followed by a number.
        call _COMMA
3:      NEXT

4:      // Executing - run it!
        mov interpret_is_lit,%ecx // Literal?
        test %ecx,%ecx          // Literal?
        jnz 5f

        // Not a literal, execute it now.  This never returns, but the codeword will
        // eventually call NEXT which will reenter the loop in QUIT.
        jmp *(%eax)

5:      // Executing a literal, which means push it on the stack.
        push %ebx
        NEXT

6:      // Parse error (not a known word or a number in the current BASE).
        // Print an error message followed by up to 40 characters of context.
        mov $2,%ebx             // 1st param: stderr
        mov $errmsg,%ecx        // 2nd param: error message
        mov $errmsgend-errmsg,%edx // 3rd param: length of string
        mov $__NR_write,%eax    // write syscall
        int $0x80

        mov (currkey),%ecx      // the error occurred just before currkey position
        mov %ecx,%edx
        sub $buffer,%edx        // %edx = currkey - buffer (length in buffer before currkey)
        cmp $40,%edx            // if > 40, then print only 40 characters
        jle 7f
        mov $40,%edx
7:      sub %edx,%ecx           // %ecx = start of area to print, %edx = length
        mov $__NR_write,%eax    // write syscall
        int $0x80

        mov $errmsgnl,%ecx      // newline
        mov $1,%edx
        mov $__NR_write,%eax    // write syscall
        int $0x80

        NEXT

        .section .rodata
errmsg: .ascii "PARSE ERROR: "
errmsgend:
errmsgnl: .ascii "\n"

        .data                   // NB: easier to fit in the .data section
        .align 4
interpret_is_lit:
        .int 0                  // Flag used to record if reading a literal

/*
        ODDS AND ENDS ----------------------------------------------------------------------

        CHAR puts the ASCII code of the first character of the following word on the stack.  For example
        CHAR A puts 65 on the stack.

        EXECUTE is used to run execution tokens.  See the discussion of execution tokens in the
        FORTH code for more details.

        SYSCALL0, SYSCALL1, SYSCALL2, SYSCALL3 make a standard Linux system call.  (See <asm/unistd.h>
        for a list of system call numbers).  As their name suggests these forms take between 0 and 3
        syscall parameters, plus the system call number.

        In this FORTH, SYSCALL0 must be the last word in the built-in (assembler) dictionary because we
        initialise the LATEST variable to point to it.  This means that if you want to extend the assembler
        part, you must put new words before SYSCALL0, or else change how LATEST is initialised.
*/

        defcode "CHAR",4,,CHAR
        call _WORD              // Returns %ecx = length, %edi = pointer to word.
        xor %eax,%eax
        movb (%edi),%al         // Get the first character of the word.
        push %eax               // Push it onto the stack.
        NEXT

        defcode "EXECUTE",7,,EXECUTE
        pop %eax                // Get xt into %eax
        jmp *(%eax)             // and jump to it.
                                // After xt runs its NEXT will continue executing the current word.

        defcode "SYSCALL3",8,,SYSCALL3
        pop %eax                // System call number (see <asm/unistd.h>)
        pop %ebx                // First parameter.
        pop %ecx                // Second parameter
        pop %edx                // Third parameter
        int $0x80
        push %eax               // Result (negative for -errno)
        NEXT

        defcode "SYSCALL2",8,,SYSCALL2
        pop %eax                // System call number (see <asm/unistd.h>)
        pop %ebx                // First parameter.
        pop %ecx                // Second parameter
        int $0x80
        push %eax               // Result (negative for -errno)
        NEXT

        defcode "SYSCALL1",8,,SYSCALL1
        pop %eax                // System call number (see <asm/unistd.h>)
        pop %ebx                // First parameter.
        int $0x80
        push %eax               // Result (negative for -errno)
        NEXT

        defcode "SYSCALL0",8,,SYSCALL0
        pop %eax                // System call number (see <asm/unistd.h>)
        int $0x80
        push %eax               // Result (negative for -errno)
        NEXT

/*
        DATA SEGMENT ----------------------------------------------------------------------

        Here we set up the Linux data segment, used for user definitions and variously known as just
        the 'data segment', 'user memory' or 'user definitions area'.  It is an area of memory which
        grows upwards and stores both newly-defined FORTH words and global variables of various
        sorts.

        It is completely analogous to the C heap, except there is no generalised 'malloc' and 'free'
        (but as with everything in FORTH, writing such functions would just be a Simple Matter
        Of Programming).  Instead in normal use the data segment just grows upwards as new FORTH
        words are defined/appended to it.

        There are various "features" of the GNU toolchain which make setting up the data segment
        more complicated than it really needs to be.  One is the GNU linker which inserts a random
        "build ID" segment.  Another is Address Space Randomization which means we can't tell
        where the kernel will choose to place the data segment (or the stack for that matter).

        Therefore writing this set_up_data_segment assembler routine is a little more complicated
        than it really needs to be.  We ask the Linux kernel where it thinks the data segment starts
        using the brk(2) system call, then ask it to reserve some initial space (also using brk(2)).

        You don't need to worry about this code.
*/
        .text
        .set INITIAL_DATA_SEGMENT_SIZE,65536
set_up_data_segment:
        xor %ebx,%ebx           // Call brk(0)
        movl $__NR_brk,%eax
        int $0x80
        movl %eax,var_HERE      // Initialise HERE to point at beginning of data segment.
        addl $INITIAL_DATA_SEGMENT_SIZE,%eax    // Reserve nn bytes of memory for initial data segment.
        movl %eax,%ebx          // Call brk(HERE+INITIAL_DATA_SEGMENT_SIZE)
        movl $__NR_brk,%eax
        int $0x80
        ret

/*
        We allocate static buffers for the return static and input buffer (used when
        reading in files and text that the user types in).
*/
        .set RETURN_STACK_SIZE,8192
        .set BUFFER_SIZE,4096

        .bss
/* FORTH return stack. */
        .align 4096
return_stack:
        .space RETURN_STACK_SIZE
return_stack_top:               // Initial top of return stack.

/* This is used as a temporary input buffer when reading from files or the terminal. */
        .align 4096
buffer:
        .space BUFFER_SIZE

/*
        START OF FORTH CODE ----------------------------------------------------------------------

        We've now reached the stage where the FORTH system is running and self-hosting.  All further
        words can be written as FORTH itself, including words like IF, THEN, .", etc which in most
        languages would be considered rather fundamental.

        I used to append this here in the assembly file, but I got sick of fighting against gas's
        crack-smoking (lack of) multiline string syntax.  So now that is in a separate file called
        jonesforth.f

        If you don't already have that file, download it from http://annexia.org/forth in order
        to continue the tutorial.
*/

/* END OF jonesforth.S */

\ -*- text -*-
\       A sometimes minimal FORTH compiler and tutorial for Linux / i386 systems. -*- asm -*-
\       By Richard W.M. Jones <rich@annexia.org> http://annexia.org/forth
\       This is PUBLIC DOMAIN (see public domain release statement below).
\       $Id: jonesforth.f,v 1.18 2009-09-11 08:32:33 rich Exp $
\
\       The first part of this tutorial is in jonesforth.S.  Get if from http://annexia.org/forth
\
\       PUBLIC DOMAIN ----------------------------------------------------------------------
\
\       I, the copyright holder of this work, hereby release it into the public domain. This applies worldwide.
\
\       In case this is not legally possible, I grant any entity the right to use this work for any purpose,
\       without any conditions, unless such conditions are required by law.
\
\       SETTING UP ----------------------------------------------------------------------
\
\       Let's get a few housekeeping things out of the way.  Firstly because I need to draw lots of
\       ASCII-art diagrams to explain concepts, the best way to look at this is using a window which
\       uses a fixed width font and is at least this wide:
\
\<------------------------------------------------------------------------------------------------------------------------>
\
\       Secondly make sure TABS are set to 8 characters.  The following should be a vertical
\       line.  If not, sort out your tabs.
\
\               |
\               |
\               |
\
\       Thirdly I assume that your screen is at least 50 characters high.
\
\       START OF FORTH CODE ----------------------------------------------------------------------
\
\       We've now reached the stage where the FORTH system is running and self-hosting.  All further
\       words can be written as FORTH itself, including words like IF, THEN, .", etc which in most
\       languages would be considered rather fundamental.
\
\       Some notes about the code:
\
\       I use indenting to show structure.  The amount of whitespace has no meaning to FORTH however
\       except that you must use at least one whitespace character between words, and words themselves
\       cannot contain whitespace.
\
\       FORTH is case-sensitive.  Use capslock!

\ The primitive word /MOD (DIVMOD) leaves both the quotient and the remainder on the stack.  (On
\ i386, the idivl instruction gives both anyway).  Now we can define the / and MOD in terms of /MOD
\ and a few other primitives.
: / /MOD SWAP DROP ;
: MOD /MOD DROP ;

\ Define some character constants
: '\n' 10 ;
: BL   32 ; \ BL (BLank) is a standard FORTH word for space.

\ CR prints a carriage return
: CR '\n' EMIT ;

\ SPACE prints a space
: SPACE BL EMIT ;

\ NEGATE leaves the negative of a number on the stack.
: NEGATE 0 SWAP - ;

\ Standard words for booleans.
: TRUE  1 ;
: FALSE 0 ;
: NOT   0= ;

\ LITERAL takes whatever is on the stack and compiles LIT <foo>
: LITERAL IMMEDIATE
        ' LIT ,         \ compile LIT
        ,               \ compile the literal itself (from the stack)
        ;

\ Now we can use [ and ] to insert literals which are calculated at compile time.  (Recall that
\ [ and ] are the FORTH words which switch into and out of immediate mode.)
\ Within definitions, use [ ... ] LITERAL anywhere that '...' is a constant expression which you
\ would rather only compute once (at compile time, rather than calculating it each time your word runs).
: ':'
        [               \ go into immediate mode (temporarily)
        CHAR :          \ push the number 58 (ASCII code of colon) on the parameter stack
        ]               \ go back to compile mode
        LITERAL         \ compile LIT 58 as the definition of ':' word
;

\ A few more character constants defined the same way as above.
: ';' [ CHAR ; ] LITERAL ;
: '(' [ CHAR ( ] LITERAL ;
: ')' [ CHAR ) ] LITERAL ;
: '"' [ CHAR " ] LITERAL ;
: 'A' [ CHAR A ] LITERAL ;
: '0' [ CHAR 0 ] LITERAL ;
: '-' [ CHAR - ] LITERAL ;
: '.' [ CHAR . ] LITERAL ;

\ While compiling, '[COMPILE] word' compiles 'word' if it would otherwise be IMMEDIATE.
: [COMPILE] IMMEDIATE
        WORD            \ get the next word
        FIND            \ find it in the dictionary
        >CFA            \ get its codeword
        ,               \ and compile that
;

\ RECURSE makes a recursive call to the current word that is being compiled.
\
\ Normally while a word is being compiled, it is marked HIDDEN so that references to the
\ same word within are calls to the previous definition of the word.  However we still have
\ access to the word which we are currently compiling through the LATEST pointer so we
\ can use that to compile a recursive call.
: RECURSE IMMEDIATE
        LATEST @        \ LATEST points to the word being compiled at the moment
        >CFA            \ get the codeword
        ,               \ compile it
;

\       CONTROL STRUCTURES ----------------------------------------------------------------------
\
\ So far we have defined only very simple definitions.  Before we can go further, we really need to
\ make some control structures, like IF ... THEN and loops.  Luckily we can define arbitrary control
\ structures directly in FORTH.
\
\ Please note that the control structures as I have defined them here will only work inside compiled
\ words.  If you try to type in expressions using IF, etc. in immediate mode, then they won't work.
\ Making these work in immediate mode is left as an exercise for the reader.

\ condition IF true-part THEN rest
\       -- compiles to: --> condition 0BRANCH OFFSET true-part rest
\       where OFFSET is the offset of 'rest'
\ condition IF true-part ELSE false-part THEN
\       -- compiles to: --> condition 0BRANCH OFFSET true-part BRANCH OFFSET2 false-part rest
\       where OFFSET if the offset of false-part and OFFSET2 is the offset of rest

\ IF is an IMMEDIATE word which compiles 0BRANCH followed by a dummy offset, and places
\ the address of the 0BRANCH on the stack.  Later when we see THEN, we pop that address
\ off the stack, calculate the offset, and back-fill the offset.
: IF IMMEDIATE
        ' 0BRANCH ,     \ compile 0BRANCH
        HERE @          \ save location of the offset on the stack
        0 ,             \ compile a dummy offset
;

: THEN IMMEDIATE
        DUP
        HERE @ SWAP -   \ calculate the offset from the address saved on the stack
        SWAP !          \ store the offset in the back-filled location
;

: ELSE IMMEDIATE
        ' BRANCH ,      \ definite branch to just over the false-part
        HERE @          \ save location of the offset on the stack
        0 ,             \ compile a dummy offset
        SWAP            \ now back-fill the original (IF) offset
        DUP             \ same as for THEN word above
        HERE @ SWAP -
        SWAP !
;

\ BEGIN loop-part condition UNTIL
\       -- compiles to: --> loop-part condition 0BRANCH OFFSET
\       where OFFSET points back to the loop-part
\ This is like do { loop-part } while (condition) in the C language
: BEGIN IMMEDIATE
        HERE @          \ save location on the stack
;

: UNTIL IMMEDIATE
        ' 0BRANCH ,     \ compile 0BRANCH
        HERE @ -        \ calculate the offset from the address saved on the stack
        ,               \ compile the offset here
;

\ BEGIN loop-part AGAIN
\       -- compiles to: --> loop-part BRANCH OFFSET
\       where OFFSET points back to the loop-part
\ In other words, an infinite loop which can only be returned from with EXIT
: AGAIN IMMEDIATE
        ' BRANCH ,      \ compile BRANCH
        HERE @ -        \ calculate the offset back
        ,               \ compile the offset here
;

\ BEGIN condition WHILE loop-part REPEAT
\       -- compiles to: --> condition 0BRANCH OFFSET2 loop-part BRANCH OFFSET
\       where OFFSET points back to condition (the beginning) and OFFSET2 points to after the whole piece of code
\ So this is like a while (condition) { loop-part } loop in the C language
: WHILE IMMEDIATE
        ' 0BRANCH ,     \ compile 0BRANCH
        HERE @          \ save location of the offset2 on the stack
        0 ,             \ compile a dummy offset2
;

: REPEAT IMMEDIATE
        ' BRANCH ,      \ compile BRANCH
        SWAP            \ get the original offset (from BEGIN)
        HERE @ - ,      \ and compile it after BRANCH
        DUP
        HERE @ SWAP -   \ calculate the offset2
        SWAP !          \ and back-fill it in the original location
;

\ UNLESS is the same as IF but the test is reversed.
\
\ Note the use of [COMPILE]: Since IF is IMMEDIATE we don't want it to be executed while UNLESS
\ is compiling, but while UNLESS is running (which happens to be when whatever word using UNLESS is
\ being compiled -- whew!).  So we use [COMPILE] to reverse the effect of marking IF as immediate.
\ This trick is generally used when we want to write our own control words without having to
\ implement them all in terms of the primitives 0BRANCH and BRANCH, but instead reusing simpler
\ control words like (in this instance) IF.
: UNLESS IMMEDIATE
        ' NOT ,         \ compile NOT (to reverse the test)
        [COMPILE] IF    \ continue by calling the normal IF
;

\       COMMENTS ----------------------------------------------------------------------
\
\ FORTH allows ( ... ) as comments within function definitions.  This works by having an IMMEDIATE
\ word called ( which just drops input characters until it hits the corresponding ).
: ( IMMEDIATE
        1               \ allowed nested parens by keeping track of depth
        BEGIN
                KEY             \ read next character
                DUP '(' = IF    \ open paren?
                        DROP            \ drop the open paren
                        1+              \ depth increases
                ELSE
                        ')' = IF        \ close paren?
                                1-              \ depth decreases
                        THEN
                THEN
        DUP 0= UNTIL            \ continue until we reach matching close paren, depth 0
        DROP            \ drop the depth counter
;

(
        From now on we can use ( ... ) for comments.

        STACK NOTATION ----------------------------------------------------------------------

        In FORTH style we can also use ( ... -- ... ) to show the effects that a word has on the
        parameter stack.  For example:

        ( n -- )        means that the word consumes an integer (n) from the parameter stack.
        ( b a -- c )    means that the word uses two integers (a and b, where a is at the top of stack)
                                and returns a single integer (c).
        ( -- )          means the word has no effect on the stack
)

( Some more complicated stack examples, showing the stack notation. )
: NIP ( x y -- y ) SWAP DROP ;
: TUCK ( x y -- y x y ) SWAP OVER ;
: PICK ( x_u ... x_1 x_0 u -- x_u ... x_1 x_0 x_u )
        1+              ( add one because of 'u' on the stack )
        4 *             ( multiply by the word size )
        DSP@ +          ( add to the stack pointer )
        @               ( and fetch )
;

( With the looping constructs, we can now write SPACES, which writes n spaces to stdout. )
: SPACES        ( n -- )
        BEGIN
                DUP 0>          ( while n > 0 )
        WHILE
                SPACE           ( print a space )
                1-              ( until we count down to 0 )
        REPEAT
        DROP
;

( Standard words for manipulating BASE. )
: DECIMAL ( -- ) 10 BASE ! ;
: HEX ( -- ) 16 BASE ! ;

(
        PRINTING NUMBERS ----------------------------------------------------------------------

        The standard FORTH word . (DOT) is very important.  It takes the number at the top
        of the stack and prints it out.  However first I'm going to implement some lower-level
        FORTH words:

        U.R     ( u width -- )  which prints an unsigned number, padded to a certain width
        U.      ( u -- )        which prints an unsigned number
        .R      ( n width -- )  which prints a signed number, padded to a certain width.

        For example:
                -123 6 .R
        will print out these characters:
                <space> <space> - 1 2 3

        In other words, the number padded left to a certain number of characters.

        The full number is printed even if it is wider than width, and this is what allows us to
        define the ordinary functions U. and . (we just set width to zero knowing that the full
        number will be printed anyway).

        Another wrinkle of . and friends is that they obey the current base in the variable BASE.
        BASE can be anything in the range 2 to 36.

        While we're defining . &c we can also define .S which is a useful debugging tool.  This
        word prints the current stack (non-destructively) from top to bottom.
)

( This is the underlying recursive definition of U. )
: U.            ( u -- )
        BASE @ /MOD     ( width rem quot )
        ?DUP IF                 ( if quotient <> 0 then )
                RECURSE         ( print the quotient )
        THEN

        ( print the remainder )
        DUP 10 < IF
                '0'             ( decimal digits 0..9 )
        ELSE
                10 -            ( hex and beyond digits A..Z )
                'A'
        THEN
        +
        EMIT
;

(
        FORTH word .S prints the contents of the stack.  It doesn't alter the stack.
        Very useful for debugging.
)
: .S            ( -- )
        DSP@            ( get current stack pointer )
        BEGIN
                DUP S0 @ <
        WHILE
                DUP @ U.        ( print the stack element )
                SPACE
                4+              ( move up )
        REPEAT
        DROP
;

( This word returns the width (in characters) of an unsigned number in the current base )
: UWIDTH        ( u -- width )
        BASE @ /        ( rem quot )
        ?DUP IF         ( if quotient <> 0 then )
                RECURSE 1+      ( return 1+recursive call )
        ELSE
                1               ( return 1 )
        THEN
;

: U.R           ( u width -- )
        SWAP            ( width u )
        DUP             ( width u u )
        UWIDTH          ( width u uwidth )
        ROT             ( u uwidth width )
        SWAP -          ( u width-uwidth )
        ( At this point if the requested width is narrower, we'll have a negative number on the stack.
          Otherwise the number on the stack is the number of spaces to print.  But SPACES won't print
          a negative number of spaces anyway, so it's now safe to call SPACES ... )
        SPACES
        ( ... and then call the underlying implementation of U. )
        U.
;

(
        .R prints a signed number, padded to a certain width.  We can't just print the sign
        and call U.R because we want the sign to be next to the number ('-123' instead of '-  123').
)
: .R            ( n width -- )
        SWAP            ( width n )
        DUP 0< IF
                NEGATE          ( width u )
                1               ( save a flag to remember that it was negative | width n 1 )
                SWAP            ( width 1 u )
                ROT             ( 1 u width )
                1-              ( 1 u width-1 )
        ELSE
                0               ( width u 0 )
                SWAP            ( width 0 u )
                ROT             ( 0 u width )
        THEN
        SWAP            ( flag width u )
        DUP             ( flag width u u )
        UWIDTH          ( flag width u uwidth )
        ROT             ( flag u uwidth width )
        SWAP -          ( flag u width-uwidth )

        SPACES          ( flag u )
        SWAP            ( u flag )

        IF                      ( was it negative? print the - character )
                '-' EMIT
        THEN

        U.
;

( Finally we can define word . in terms of .R, with a trailing space. )
: . 0 .R SPACE ;

( The real U., note the trailing space. )
: U. U. SPACE ;

( ? fetches the integer at an address and prints it. )
: ? ( addr -- ) @ . ;

( c a b WITHIN returns true if a <= c and c < b )
(  or define without ifs: OVER - >R - R>  U<  )
: WITHIN
        -ROT            ( b c a )
        OVER            ( b c a c )
        <= IF
                > IF            ( b c -- )
                        TRUE
                ELSE
                        FALSE
                THEN
        ELSE
                2DROP           ( b c -- )
                FALSE
        THEN
;

( DEPTH returns the depth of the stack. )
: DEPTH         ( -- n )
        S0 @ DSP@ -
        4-                      ( adjust because S0 was on the stack when we pushed DSP )
;

(
        ALIGNED takes an address and rounds it up (aligns it) to the next 4 byte boundary.
)
: ALIGNED       ( addr -- addr )
        3 + 3 INVERT AND        ( (addr+3) & ~3 )
;

(
        ALIGN aligns the HERE pointer, so the next word appended will be aligned properly.
)
: ALIGN HERE @ ALIGNED HERE ! ;

(
        STRINGS ----------------------------------------------------------------------

        S" string" is used in FORTH to define strings.  It leaves the address of the string and
        its length on the stack, (length at the top of stack).  The space following S" is the normal
        space between FORTH words and is not a part of the string.

        This is tricky to define because it has to do different things depending on whether
        we are compiling or in immediate mode.  (Thus the word is marked IMMEDIATE so it can
        detect this and do different things).

        In compile mode we append
                LITSTRING <string length> <string rounded up 4 bytes>
        to the current word.  The primitive LITSTRING does the right thing when the current
        word is executed.

        In immediate mode there isn't a particularly good place to put the string, but in this
        case we put the string at HERE (but we _don't_ change HERE).  This is meant as a temporary
        location, likely to be overwritten soon after.
)
( C, appends a byte to the current compiled word. )
: C,
        HERE @ C!       ( store the character in the compiled image )
        1 HERE +!       ( increment HERE pointer by 1 byte )
;

: S" IMMEDIATE          ( -- addr len )
        STATE @ IF      ( compiling? )
                ' LITSTRING ,   ( compile LITSTRING )
                HERE @          ( save the address of the length word on the stack )
                0 ,             ( dummy length - we don't know what it is yet )
                BEGIN
                        KEY             ( get next character of the string )
                        DUP '"' <>
                WHILE
                        C,              ( copy character )
                REPEAT
                DROP            ( drop the double quote character at the end )
                DUP             ( get the saved address of the length word )
                HERE @ SWAP -   ( calculate the length )
                4-              ( subtract 4 (because we measured from the start of the length word) )
                SWAP !          ( and back-fill the length location )
                ALIGN           ( round up to next multiple of 4 bytes for the remaining code )
        ELSE            ( immediate mode )
                HERE @          ( get the start address of the temporary space )
                BEGIN
                        KEY
                        DUP '"' <>
                WHILE
                        OVER C!         ( save next character )
                        1+              ( increment address )
                REPEAT
                DROP            ( drop the final " character )
                HERE @ -        ( calculate the length )
                HERE @          ( push the start address )
                SWAP            ( addr len )
        THEN
;

(
        ." is the print string operator in FORTH.  Example: ." Something to print"
        The space after the operator is the ordinary space required between words and is not
        a part of what is printed.

        In immediate mode we just keep reading characters and printing them until we get to
        the next double quote.

        In compile mode we use S" to store the string, then add TELL afterwards:
                LITSTRING <string length> <string rounded up to 4 bytes> TELL

        It may be interesting to note the use of [COMPILE] to turn the call to the immediate
        word S" into compilation of that word.  It compiles it into the definition of .",
        not into the definition of the word being compiled when this is running (complicated
        enough for you?)
)
: ." IMMEDIATE          ( -- )
        STATE @ IF      ( compiling? )
                [COMPILE] S"    ( read the string, and compile LITSTRING, etc. )
                ' TELL ,        ( compile the final TELL )
        ELSE
                ( In immediate mode, just read characters and print them until we get
                  to the ending double quote. )
                BEGIN
                        KEY
                        DUP '"' = IF
                                DROP    ( drop the double quote character )
                                EXIT    ( return from this function )
                        THEN
                        EMIT
                AGAIN
        THEN
;

(
        CONSTANTS AND VARIABLES ----------------------------------------------------------------------

        In FORTH, global constants and variables are defined like this:

        10 CONSTANT TEN         when TEN is executed, it leaves the integer 10 on the stack
        VARIABLE VAR            when VAR is executed, it leaves the address of VAR on the stack

        Constants can be read but not written, eg:

        TEN . CR                prints 10

        You can read a variable (in this example called VAR) by doing:

        VAR @                   leaves the value of VAR on the stack
        VAR @ . CR              prints the value of VAR
        VAR ? CR                same as above, since ? is the same as @ .

        and update the variable by doing:

        20 VAR !                sets VAR to 20

        Note that variables are uninitialised (but see VALUE later on which provides initialised
        variables with a slightly simpler syntax).

        How can we define the words CONSTANT and VARIABLE?

        The trick is to define a new word for the variable itself (eg. if the variable was called
        'VAR' then we would define a new word called VAR).  This is easy to do because we exposed
        dictionary entry creation through the CREATE word (part of the definition of : above).
        A call to WORD [TEN] CREATE (where [TEN] means that "TEN" is the next word in the input)
        leaves the dictionary entry:

                                   +--- HERE
                                   |
                                   V
        +---------|---|---|---|---+
        | LINK    | 3 | T | E | N |
        +---------|---|---|---|---+
                   len

        For CONSTANT we can continue by appending DOCOL (the codeword), then LIT followed by
        the constant itself and then EXIT, forming a little word definition that returns the
        constant:

        +---------|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 3 | T | E | N | DOCOL      | LIT        | 10         | EXIT       |
        +---------|---|---|---|---|------------|------------|------------|------------+
                   len              codeword

        Notice that this word definition is exactly the same as you would have got if you had
        written : TEN 10 ;

        Note for people reading the code below: DOCOL is a constant word which we defined in the
        assembler part which returns the value of the assembler symbol of the same name.
)
: CONSTANT
        WORD            ( get the name (the name follows CONSTANT) )
        CREATE          ( make the dictionary entry )
        DOCOL ,         ( append DOCOL (the codeword field of this word) )
        ' LIT ,         ( append the codeword LIT )
        ,               ( append the value on the top of the stack )
        ' EXIT ,        ( append the codeword EXIT )
;

(
        VARIABLE is a little bit harder because we need somewhere to put the variable.  There is
        nothing particularly special about the user memory (the area of memory pointed to by HERE
        where we have previously just stored new word definitions).  We can slice off bits of this
        memory area to store anything we want, so one possible definition of VARIABLE might create
        this:

           +--------------------------------------------------------------+
           |                                                              |
           V                                                              |
        +---------|---------|---|---|---|---|------------|------------|---|--------|------------+
        | <var>   | LINK    | 3 | V | A | R | DOCOL      | LIT        | <addr var> | EXIT       |
        +---------|---------|---|---|---|---|------------|------------|------------|------------+
                             len              codeword

        where <var> is the place to store the variable, and <addr var> points back to it.

        To make this more general let's define a couple of words which we can use to allocate
        arbitrary memory from the user memory.

        First ALLOT, where n ALLOT allocates n bytes of memory.  (Note when calling this that
        it's a very good idea to make sure that n is a multiple of 4, or at least that next time
        a word is compiled that HERE has been left as a multiple of 4).
)
: ALLOT         ( n -- addr )
        HERE @ SWAP     ( here n )
        HERE +!         ( adds n to HERE, after this the old value of HERE is still on the stack )
;

(
        Second, CELLS.  In FORTH the phrase 'n CELLS ALLOT' means allocate n integers of whatever size
        is the natural size for integers on this machine architecture.  On this 32 bit machine therefore
        CELLS just multiplies the top of stack by 4.
)
: CELLS ( n -- n ) 4 * ;

(
        So now we can define VARIABLE easily in much the same way as CONSTANT above.  Refer to the
        diagram above to see what the word that this creates will look like.
)
: VARIABLE
        1 CELLS ALLOT   ( allocate 1 cell of memory, push the pointer to this memory )
        WORD CREATE     ( make the dictionary entry (the name follows VARIABLE) )
        DOCOL ,         ( append DOCOL (the codeword field of this word) )
        ' LIT ,         ( append the codeword LIT )
        ,               ( append the pointer to the new memory )
        ' EXIT ,        ( append the codeword EXIT )
;

(
        VALUES ----------------------------------------------------------------------

        VALUEs are like VARIABLEs but with a simpler syntax.  You would generally use them when you
        want a variable which is read often, and written infrequently.

        20 VALUE VAL    creates VAL with initial value 20
        VAL             pushes the value (20) directly on the stack
        30 TO VAL       updates VAL, setting it to 30
        VAL             pushes the value (30) directly on the stack

        Notice that 'VAL' on its own doesn't return the address of the value, but the value itself,
        making values simpler and more obvious to use than variables (no indirection through '@').
        The price is a more complicated implementation, although despite the complexity there is no
        performance penalty at runtime.

        A naive implementation of 'TO' would be quite slow, involving a dictionary search each time.
        But because this is FORTH we have complete control of the compiler so we can compile TO more
        efficiently, turning:
                TO VAL
        into:
                LIT <addr> !
        and calculating <addr> (the address of the value) at compile time.

        Now this is the clever bit.  We'll compile our value like this:

        +---------|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 3 | V | A | L | DOCOL      | LIT        | <value>    | EXIT       |
        +---------|---|---|---|---|------------|------------|------------|------------+
                   len              codeword

        where <value> is the actual value itself.  Note that when VAL executes, it will push the
        value on the stack, which is what we want.

        But what will TO use for the address <addr>?  Why of course a pointer to that <value>:

                code compiled   - - - - --|------------|------------|------------|-- - - - -
                by TO VAL                 | LIT        | <addr>     | !          |
                                - - - - --|------------|-----|------|------------|-- - - - -
                                                             |
                                                             V
        +---------|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 3 | V | A | L | DOCOL      | LIT        | <value>    | EXIT       |
        +---------|---|---|---|---|------------|------------|------------|------------+
                   len              codeword

        In other words, this is a kind of self-modifying code.

        (Note to the people who want to modify this FORTH to add inlining: values defined this
        way cannot be inlined).
)
: VALUE         ( n -- )
        WORD CREATE     ( make the dictionary entry (the name follows VALUE) )
        DOCOL ,         ( append DOCOL )
        ' LIT ,         ( append the codeword LIT )
        ,               ( append the initial value )
        ' EXIT ,        ( append the codeword EXIT )
;

: TO IMMEDIATE  ( n -- )
        WORD            ( get the name of the value )
        FIND            ( look it up in the dictionary )
        >DFA            ( get a pointer to the first data field (the 'LIT') )
        4+              ( increment to point at the value )
        STATE @ IF      ( compiling? )
                ' LIT ,         ( compile LIT )
                ,               ( compile the address of the value )
                ' ! ,           ( compile ! )
        ELSE            ( immediate mode )
                !               ( update it straightaway )
        THEN
;

( x +TO VAL adds x to VAL )
: +TO IMMEDIATE
        WORD            ( get the name of the value )
        FIND            ( look it up in the dictionary )
        >DFA            ( get a pointer to the first data field (the 'LIT') )
        4+              ( increment to point at the value )
        STATE @ IF      ( compiling? )
                ' LIT ,         ( compile LIT )
                ,               ( compile the address of the value )
                ' +! ,          ( compile +! )
        ELSE            ( immediate mode )
                +!              ( update it straightaway )
        THEN
;

(
        PRINTING THE DICTIONARY ----------------------------------------------------------------------

        ID. takes an address of a dictionary entry and prints the word's name.

        For example: LATEST @ ID. would print the name of the last word that was defined.
)
: ID.
        4+              ( skip over the link pointer )
        DUP C@          ( get the flags/length byte )
        F_LENMASK AND   ( mask out the flags - just want the length )

        BEGIN
                DUP 0>          ( length > 0? )
        WHILE
                SWAP 1+         ( addr len -- len addr+1 )
                DUP C@          ( len addr -- len addr char | get the next character)
                EMIT            ( len addr char -- len addr | and print it)
                SWAP 1-         ( len addr -- addr len-1    | subtract one from length )
        REPEAT
        2DROP           ( len addr -- )
;

(
        'WORD word FIND ?HIDDEN' returns true if 'word' is flagged as hidden.

        'WORD word FIND ?IMMEDIATE' returns true if 'word' is flagged as immediate.
)
: ?HIDDEN
        4+              ( skip over the link pointer )
        C@              ( get the flags/length byte )
        F_HIDDEN AND    ( mask the F_HIDDEN flag and return it (as a truth value) )
;
: ?IMMEDIATE
        4+              ( skip over the link pointer )
        C@              ( get the flags/length byte )
        F_IMMED AND     ( mask the F_IMMED flag and return it (as a truth value) )
;

(
        WORDS prints all the words defined in the dictionary, starting with the word defined most recently.
        However it doesn't print hidden words.

        The implementation simply iterates backwards from LATEST using the link pointers.
)
: WORDS
        LATEST @        ( start at LATEST dictionary entry )
        BEGIN
                ?DUP            ( while link pointer is not null )
        WHILE
                DUP ?HIDDEN NOT IF      ( ignore hidden words )
                        DUP ID.         ( but if not hidden, print the word )
                        SPACE
                THEN
                @               ( dereference the link pointer - go to previous word )
        REPEAT
        CR
;

(
        FORGET ----------------------------------------------------------------------

        So far we have only allocated words and memory.  FORTH provides a rather primitive method
        to deallocate.

        'FORGET word' deletes the definition of 'word' from the dictionary and everything defined
        after it, including any variables and other memory allocated after.

        The implementation is very simple - we look up the word (which returns the dictionary entry
        address).  Then we set HERE to point to that address, so in effect all future allocations
        and definitions will overwrite memory starting at the word.  We also need to set LATEST to
        point to the previous word.

        Note that you cannot FORGET built-in words (well, you can try but it will probably cause
        a segfault).

        XXX: Because we wrote VARIABLE to store the variable in memory allocated before the word,
        in the current implementation VARIABLE FOO FORGET FOO will leak 1 cell of memory.
)
: FORGET
        WORD FIND       ( find the word, gets the dictionary entry address )
        DUP @ LATEST !  ( set LATEST to point to the previous word )
        HERE !          ( and store HERE with the dictionary address )
;

(
        DUMP ----------------------------------------------------------------------

        DUMP is used to dump out the contents of memory, in the 'traditional' hexdump format.

        Notice that the parameters to DUMP (address, length) are compatible with string words
        such as WORD and S".

        You can dump out the raw code for the last word you defined by doing something like:

                LATEST @ 128 DUMP
)
: DUMP          ( addr len -- )
        BASE @ -ROT             ( save the current BASE at the bottom of the stack )
        HEX                     ( and switch to hexadecimal mode )

        BEGIN
                ?DUP            ( while len > 0 )
        WHILE
                OVER 8 U.R      ( print the address )
                SPACE

                ( print up to 16 words on this line )
                2DUP            ( addr len addr len )
                1- 15 AND 1+    ( addr len addr linelen )
                BEGIN
                        ?DUP            ( while linelen > 0 )
                WHILE
                        SWAP            ( addr len linelen addr )
                        DUP C@          ( addr len linelen addr byte )
                        2 .R SPACE      ( print the byte )
                        1+ SWAP 1-      ( addr len linelen addr -- addr len addr+1 linelen-1 )
                REPEAT
                DROP            ( addr len )

                ( print the ASCII equivalents )
                2DUP 1- 15 AND 1+ ( addr len addr linelen )
                BEGIN
                        ?DUP            ( while linelen > 0)
                WHILE
                        SWAP            ( addr len linelen addr )
                        DUP C@          ( addr len linelen addr byte )
                        DUP 32 128 WITHIN IF    ( 32 <= c < 128? )
                                EMIT
                        ELSE
                                DROP '.' EMIT
                        THEN
                        1+ SWAP 1-      ( addr len linelen addr -- addr len addr+1 linelen-1 )
                REPEAT
                DROP            ( addr len )
                CR

                DUP 1- 15 AND 1+ ( addr len linelen )
                TUCK            ( addr linelen len linelen )
                -               ( addr linelen len-linelen )
                >R + R>         ( addr+linelen len-linelen )
        REPEAT

        DROP                    ( restore stack )
        BASE !                  ( restore saved BASE )
;

(
        CASE ----------------------------------------------------------------------

        CASE...ENDCASE is how we do switch statements in FORTH.  There is no generally
        agreed syntax for this, so I've gone for the syntax mandated by the ISO standard
        FORTH (ANS-FORTH).

                ( some value on the stack )
                CASE
                test1 OF ... ENDOF
                test2 OF ... ENDOF
                testn OF ... ENDOF
                ... ( default case )
                ENDCASE

        The CASE statement tests the value on the stack by comparing it for equality with
        test1, test2, ..., testn and executes the matching piece of code within OF ... ENDOF.
        If none of the test values match then the default case is executed.  Inside the ... of
        the default case, the value is still at the top of stack (it is implicitly DROP-ed
        by ENDCASE).  When ENDOF is executed it jumps after ENDCASE (ie. there is no "fall-through"
        and no need for a break statement like in C).

        The default case may be omitted.  In fact the tests may also be omitted so that you
        just have a default case, although this is probably not very useful.

        An example (assuming that 'q', etc. are words which push the ASCII value of the letter
        on the stack):

                0 VALUE QUIT
                0 VALUE SLEEP
                KEY CASE
                        'q' OF 1 TO QUIT ENDOF
                        's' OF 1 TO SLEEP ENDOF
                        ( default case: )
                        ." Sorry, I didn't understand key <" DUP EMIT ." >, try again." CR
                ENDCASE

        (In some versions of FORTH, more advanced tests are supported, such as ranges, etc.
        Other versions of FORTH need you to write OTHERWISE to indicate the default case.
        As I said above, this FORTH tries to follow the ANS FORTH standard).

        The implementation of CASE...ENDCASE is somewhat non-trivial.  I'm following the
        implementations from here:
        http://www.uni-giessen.de/faq/archiv/forthfaq.case_endcase/msg00000.html

        The general plan is to compile the code as a series of IF statements:

        CASE                            (push 0 on the immediate-mode parameter stack)
        test1 OF ... ENDOF              test1 OVER = IF DROP ... ELSE
        test2 OF ... ENDOF              test2 OVER = IF DROP ... ELSE
        testn OF ... ENDOF              testn OVER = IF DROP ... ELSE
        ... ( default case )            ...
        ENDCASE                         DROP THEN [THEN [THEN ...]]

        The CASE statement pushes 0 on the immediate-mode parameter stack, and that number
        is used to count how many THEN statements we need when we get to ENDCASE so that each
        IF has a matching THEN.  The counting is done implicitly.  If you recall from the
        implementation above of IF, each IF pushes a code address on the immediate-mode stack,
        and these addresses are non-zero, so by the time we get to ENDCASE the stack contains
        some number of non-zeroes, followed by a zero.  The number of non-zeroes is how many
        times IF has been called, so how many times we need to match it with THEN.

        This code uses [COMPILE] so that we compile calls to IF, ELSE, THEN instead of
        actually calling them while we're compiling the words below.

        As is the case with all of our control structures, they only work within word
        definitions, not in immediate mode.
)
: CASE IMMEDIATE
        0               ( push 0 to mark the bottom of the stack )
;

: OF IMMEDIATE
        ' OVER ,        ( compile OVER )
        ' = ,           ( compile = )
        [COMPILE] IF    ( compile IF )
        ' DROP ,        ( compile DROP )
;

: ENDOF IMMEDIATE
        [COMPILE] ELSE  ( ENDOF is the same as ELSE )
;

: ENDCASE IMMEDIATE
        ' DROP ,        ( compile DROP )

        ( keep compiling THEN until we get to our zero marker )
        BEGIN
                ?DUP
        WHILE
                [COMPILE] THEN
        REPEAT
;

(
        DECOMPILER ----------------------------------------------------------------------

        CFA> is the opposite of >CFA.  It takes a codeword and tries to find the matching
        dictionary definition.  (In truth, it works with any pointer into a word, not just
        the codeword pointer, and this is needed to do stack traces).

        In this FORTH this is not so easy.  In fact we have to search through the dictionary
        because we don't have a convenient back-pointer (as is often the case in other versions
        of FORTH).  Because of this search, CFA> should not be used when performance is critical,
        so it is only used for debugging tools such as the decompiler and printing stack
        traces.

        This word returns 0 if it doesn't find a match.
)
: CFA>
        LATEST @        ( start at LATEST dictionary entry )
        BEGIN
                ?DUP            ( while link pointer is not null )
        WHILE
                2DUP SWAP       ( cfa curr curr cfa )
                < IF            ( current dictionary entry < cfa? )
                        NIP             ( leave curr dictionary entry on the stack )
                        EXIT
                THEN
                @               ( follow link pointer back )
        REPEAT
        DROP            ( restore stack )
        0               ( sorry, nothing found )
;

(
        SEE decompiles a FORTH word.

        We search for the dictionary entry of the word, then search again for the next
        word (effectively, the end of the compiled word).  This results in two pointers:

        +---------|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 3 | T | E | N | DOCOL      | LIT        | 10         | EXIT       |
        +---------|---|---|---|---|------------|------------|------------|------------+
         ^                                                                             ^
         |                                                                             |
        Start of word                                                         End of word

        With this information we can have a go at decompiling the word.  We need to
        recognise "meta-words" like LIT, LITSTRING, BRANCH, etc. and treat those separately.
)
: SEE
        WORD FIND       ( find the dictionary entry to decompile )

        ( Now we search again, looking for the next word in the dictionary.  This gives us
          the length of the word that we will be decompiling.  (Well, mostly it does). )
        HERE @          ( address of the end of the last compiled word )
        LATEST @        ( word last curr )
        BEGIN
                2 PICK          ( word last curr word )
                OVER            ( word last curr word curr )
                <>              ( word last curr word<>curr? )
        WHILE                   ( word last curr )
                NIP             ( word curr )
                DUP @           ( word curr prev (which becomes: word last curr) )
        REPEAT

        DROP            ( at this point, the stack is: start-of-word end-of-word )
        SWAP            ( end-of-word start-of-word )

        ( begin the definition with : NAME [IMMEDIATE] )
        ':' EMIT SPACE DUP ID. SPACE
        DUP ?IMMEDIATE IF ." IMMEDIATE " THEN

        >DFA            ( get the data address, ie. points after DOCOL | end-of-word start-of-data )

        ( now we start decompiling until we hit the end of the word )
        BEGIN           ( end start )
                2DUP >
        WHILE
                DUP @           ( end start codeword )

                CASE
                ' LIT OF                ( is it LIT ? )
                        4 + DUP @               ( get next word which is the integer constant )
                        .                       ( and print it )
                ENDOF
                ' LITSTRING OF          ( is it LITSTRING ? )
                        [ CHAR S ] LITERAL EMIT '"' EMIT SPACE ( print S"<space> )
                        4 + DUP @               ( get the length word )
                        SWAP 4 + SWAP           ( end start+4 length )
                        2DUP TELL               ( print the string )
                        '"' EMIT SPACE          ( finish the string with a final quote )
                        + ALIGNED               ( end start+4+len, aligned )
                        4 -                     ( because we're about to add 4 below )
                ENDOF
                ' 0BRANCH OF            ( is it 0BRANCH ? )
                        ." 0BRANCH ( "
                        4 + DUP @               ( print the offset )
                        .
                        ." ) "
                ENDOF
                ' BRANCH OF             ( is it BRANCH ? )
                        ." BRANCH ( "
                        4 + DUP @               ( print the offset )
                        .
                        ." ) "
                ENDOF
                ' ' OF                  ( is it ' (TICK) ? )
                        [ CHAR ' ] LITERAL EMIT SPACE
                        4 + DUP @               ( get the next codeword )
                        CFA>                    ( and force it to be printed as a dictionary entry )
                        ID. SPACE
                ENDOF
                ' EXIT OF               ( is it EXIT? )
                        ( We expect the last word to be EXIT, and if it is then we don't print it
                          because EXIT is normally implied by ;.  EXIT can also appear in the middle
                          of words, and then it needs to be printed. )
                        2DUP                    ( end start end start )
                        4 +                     ( end start end start+4 )
                        <> IF                   ( end start | we're not at the end )
                                ." EXIT "
                        THEN
                ENDOF
                                        ( default case: )
                        DUP                     ( in the default case we always need to DUP before using )
                        CFA>                    ( look up the codeword to get the dictionary entry )
                        ID. SPACE               ( and print it )
                ENDCASE

                4 +             ( end start+4 )
        REPEAT

        ';' EMIT CR

        2DROP           ( restore stack )
;

(
        EXECUTION TOKENS ----------------------------------------------------------------------

        Standard FORTH defines a concept called an 'execution token' (or 'xt') which is very
        similar to a function pointer in C.  We map the execution token to a codeword address.

                        execution token of DOUBLE is the address of this codeword
                                                    |
                                                    V
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
        | LINK    | 6 | D | O | U | B | L | E | 0 | DOCOL      | DUP        | +          | EXIT       |
        +---------|---|---|---|---|---|---|---|---|------------|------------|------------|------------+
                   len                         pad  codeword                                           ^

        There is one assembler primitive for execution tokens, EXECUTE ( xt -- ), which runs them.

        You can make an execution token for an existing word the long way using >CFA,
        ie: WORD [foo] FIND >CFA will push the xt for foo onto the stack where foo is the
        next word in input.  So a very slow way to run DOUBLE might be:

                : DOUBLE DUP + ;
                : SLOW WORD FIND >CFA EXECUTE ;
                5 SLOW DOUBLE . CR      \ prints 10

        We also offer a simpler and faster way to get the execution token of any word FOO:

                ['] FOO

        (Exercises for readers: (1) What is the difference between ['] FOO and ' FOO?
        (2) What is the relationship between ', ['] and LIT?)

        More useful is to define anonymous words and/or to assign xt's to variables.

        To define an anonymous word (and push its xt on the stack) use :NONAME ... ; as in this
        example:

                :NONAME ." anon word was called" CR ;   \ pushes xt on the stack
                DUP EXECUTE EXECUTE                     \ executes the anon word twice

        Stack parameters work as expected:

                :NONAME ." called with parameter " . CR ;
                DUP
                10 SWAP EXECUTE         \ prints 'called with parameter 10'
                20 SWAP EXECUTE         \ prints 'called with parameter 20'

        Notice that the above code has a memory leak: the anonymous word is still compiled
        into the data segment, so even if you lose track of the xt, the word continues to
        occupy memory.  A good way to keep track of the xt and thus avoid the memory leak is
        to assign it to a CONSTANT, VARIABLE or VALUE:

                0 VALUE ANON
                :NONAME ." anon word was called" CR ; TO ANON
                ANON EXECUTE
                ANON EXECUTE

        Another use of :NONAME is to create an array of functions which can be called quickly
        (think: fast switch statement).  This example is adapted from the ANS FORTH standard:

                10 CELLS ALLOT CONSTANT CMD-TABLE
                : SET-CMD CELLS CMD-TABLE + ! ;
                : CALL-CMD CELLS CMD-TABLE + @ EXECUTE ;

                :NONAME ." alternate 0 was called" CR ;  0 SET-CMD
                :NONAME ." alternate 1 was called" CR ;  1 SET-CMD
                        \ etc...
                :NONAME ." alternate 9 was called" CR ;  9 SET-CMD

                0 CALL-CMD
                1 CALL-CMD
)

: :NONAME
        0 0 CREATE      ( create a word with no name - we need a dictionary header because ; expects it )
        HERE @          ( current HERE value is the address of the codeword, ie. the xt )
        DOCOL ,         ( compile DOCOL (the codeword) )
        ]               ( go into compile mode )
;

: ['] IMMEDIATE
        ' LIT ,         ( compile LIT )
;

(
        EXCEPTIONS ----------------------------------------------------------------------

        Amazingly enough, exceptions can be implemented directly in FORTH, in fact rather easily.

        The general usage is as follows:

                : FOO ( n -- ) THROW ;

                : TEST-EXCEPTIONS
                        25 ['] FOO CATCH        \ execute 25 FOO, catching any exception
                        ?DUP IF
                                ." called FOO and it threw exception number: "
                                . CR
                                DROP            \ we have to drop the argument of FOO (25)
                        THEN
                ;
                \ prints: called FOO and it threw exception number: 25

        CATCH runs an execution token and detects whether it throws any exception or not.  The
        stack signature of CATCH is rather complicated:

                ( a_n-1 ... a_1 a_0 xt -- r_m-1 ... r_1 r_0 0 )         if xt did NOT throw an exception
                ( a_n-1 ... a_1 a_0 xt -- ?_n-1 ... ?_1 ?_0 e )         if xt DID throw exception 'e'

        where a_i and r_i are the (arbitrary number of) argument and return stack contents
        before and after xt is EXECUTEd.  Notice in particular the case where an exception
        is thrown, the stack pointer is restored so that there are n of _something_ on the
        stack in the positions where the arguments a_i used to be.  We don't really guarantee
        what is on the stack -- perhaps the original arguments, and perhaps other nonsense --
        it largely depends on the implementation of the word that was executed.

        THROW, ABORT and a few others throw exceptions.

        Exception numbers are non-zero integers.  By convention the positive numbers can be used
        for app-specific exceptions and the negative numbers have certain meanings defined in
        the ANS FORTH standard.  (For example, -1 is the exception thrown by ABORT).

        0 THROW does nothing.  This is the stack signature of THROW:

                ( 0 -- )
                ( * e -- ?_n-1 ... ?_1 ?_0 e )  the stack is restored to the state from the corresponding CATCH

        The implementation hangs on the definitions of CATCH and THROW and the state shared
        between them.

        Up to this point, the return stack has consisted merely of a list of return addresses,
        with the top of the return stack being the return address where we will resume executing
        when the current word EXITs.  However CATCH will push a more complicated 'exception stack
        frame' on the return stack.  The exception stack frame records some things about the
        state of execution at the time that CATCH was called.

        When called, THROW walks up the return stack (the process is called 'unwinding') until
        it finds the exception stack frame.  It then uses the data in the exception stack frame
        to restore the state allowing execution to continue after the matching CATCH.  (If it
        unwinds the stack and doesn't find the exception stack frame then it prints a message
        and drops back to the prompt, which is also normal behaviour for so-called 'uncaught
        exceptions').

        This is what the exception stack frame looks like.  (As is conventional, the return stack
        is shown growing downwards from higher to lower memory addresses).

                +------------------------------+
                | return address from CATCH    |   Notice this is already on the
                |                              |   return stack when CATCH is called.
                +------------------------------+
                | original parameter stack     |
                | pointer                      |
                +------------------------------+  ^
                | exception stack marker       |  |
                | (EXCEPTION-MARKER)           |  |   Direction of stack
                +------------------------------+  |   unwinding by THROW.
                                                  |
                                                  |

        The EXCEPTION-MARKER marks the entry as being an exception stack frame rather than an
        ordinary return address, and it is this which THROW "notices" as it is unwinding the
        stack.  (If you want to implement more advanced exceptions such as TRY...WITH then
        you'll need to use a different value of marker if you want the old and new exception stack
        frame layouts to coexist).

        What happens if the executed word doesn't throw an exception?  It will eventually
        return and call EXCEPTION-MARKER, so EXCEPTION-MARKER had better do something sensible
        without us needing to modify EXIT.  This nicely gives us a suitable definition of
        EXCEPTION-MARKER, namely a function that just drops the stack frame and itself
        returns (thus "returning" from the original CATCH).

        One thing to take from this is that exceptions are a relatively lightweight mechanism
        in FORTH.
)

: EXCEPTION-MARKER
        RDROP                   ( drop the original parameter stack pointer )
        0                       ( there was no exception, this is the normal return path )
;

: CATCH         ( xt -- exn? )
        DSP@ 4+ >R              ( save parameter stack pointer (+4 because of xt) on the return stack )
        ' EXCEPTION-MARKER 4+   ( push the address of the RDROP inside EXCEPTION-MARKER ... )
        >R                      ( ... on to the return stack so it acts like a return address )
        EXECUTE                 ( execute the nested function )
;

: THROW         ( n -- )
        ?DUP IF                 ( only act if the exception code <> 0 )
                RSP@                    ( get return stack pointer )
                BEGIN
                        DUP R0 4- <             ( RSP < R0 )
                WHILE
                        DUP @                   ( get the return stack entry )
                        ' EXCEPTION-MARKER 4+ = IF      ( found the EXCEPTION-MARKER on the return stack )
                                4+                      ( skip the EXCEPTION-MARKER on the return stack )
                                RSP!                    ( restore the return stack pointer )

                                ( Restore the parameter stack. )
                                DUP DUP DUP             ( reserve some working space so the stack for this word
                                                          doesn't coincide with the part of the stack being restored )
                                R>                      ( get the saved parameter stack pointer | n dsp )
                                4-                      ( reserve space on the stack to store n )
                                SWAP OVER               ( dsp n dsp )
                                !                       ( write n on the stack )
                                DSP! EXIT               ( restore the parameter stack pointer, immediately exit )
                        THEN
                        4+
                REPEAT

                ( No matching catch - print a message and restart the INTERPRETer. )
                DROP

                CASE
                0 1- OF ( ABORT )
                        ." ABORTED" CR
                ENDOF
                        ( default case )
                        ." UNCAUGHT THROW "
                        DUP . CR
                ENDCASE
                QUIT
        THEN
;

: ABORT         ( -- )
        0 1- THROW
;

( Print a stack trace by walking up the return stack. )
: PRINT-STACK-TRACE
        RSP@                            ( start at caller of this function )
        BEGIN
                DUP R0 4- <             ( RSP < R0 )
        WHILE
                DUP @                   ( get the return stack entry )
                CASE
                ' EXCEPTION-MARKER 4+ OF        ( is it the exception stack frame? )
                        ." CATCH ( DSP="
                        4+ DUP @ U.             ( print saved stack pointer )
                        ." ) "
                ENDOF
                                                ( default case )
                        DUP
                        CFA>                    ( look up the codeword to get the dictionary entry )
                        ?DUP IF                 ( and print it )
                                2DUP                    ( dea addr dea )
                                ID.                     ( print word from dictionary entry )
                                [ CHAR + ] LITERAL EMIT
                                SWAP >DFA 4+ - .        ( print offset )
                        THEN
                ENDCASE
                4+                      ( move up the stack )
        REPEAT
        DROP
        CR
;

(
        C STRINGS ----------------------------------------------------------------------

        FORTH strings are represented by a start address and length kept on the stack or in memory.

        Most FORTHs don't handle C strings, but we need them in order to access the process arguments
        and environment left on the stack by the Linux kernel, and to make some system calls.

        Operation       Input           Output          FORTH word      Notes
        ----------------------------------------------------------------------

        Create FORTH string             addr len        S" ..."

        Create C string                 c-addr          Z" ..."

        C -> FORTH      c-addr          addr len        DUP STRLEN

        FORTH -> C      addr len        c-addr          CSTRING         Allocated in a temporary buffer, so
                                                                        should be consumed / copied immediately.
                                                                        FORTH string should not contain NULs.

        For example, DUP STRLEN TELL prints a C string.
)

(
        Z" .." is like S" ..." except that the string is terminated by an ASCII NUL character.

        To make it more like a C string, at runtime Z" just leaves the address of the string
        on the stack (not address & length as with S").  To implement this we need to add the
        extra NUL to the string and also a DROP instruction afterwards.  Apart from that the
        implementation just a modified S".
)
: Z" IMMEDIATE
        STATE @ IF      ( compiling? )
                ' LITSTRING ,   ( compile LITSTRING )
                HERE @          ( save the address of the length word on the stack )
                0 ,             ( dummy length - we don't know what it is yet )
                BEGIN
                        KEY             ( get next character of the string )
                        DUP '"' <>
                WHILE
                        HERE @ C!       ( store the character in the compiled image )
                        1 HERE +!       ( increment HERE pointer by 1 byte )
                REPEAT
                0 HERE @ C!     ( add the ASCII NUL byte )
                1 HERE +!
                DROP            ( drop the double quote character at the end )
                DUP             ( get the saved address of the length word )
                HERE @ SWAP -   ( calculate the length )
                4-              ( subtract 4 (because we measured from the start of the length word) )
                SWAP !          ( and back-fill the length location )
                ALIGN           ( round up to next multiple of 4 bytes for the remaining code )
                ' DROP ,        ( compile DROP (to drop the length) )
        ELSE            ( immediate mode )
                HERE @          ( get the start address of the temporary space )
                BEGIN
                        KEY
                        DUP '"' <>
                WHILE
                        OVER C!         ( save next character )
                        1+              ( increment address )
                REPEAT
                DROP            ( drop the final " character )
                0 SWAP C!       ( store final ASCII NUL )
                HERE @          ( push the start address )
        THEN
;

: STRLEN        ( str -- len )
        DUP             ( save start address )
        BEGIN
                DUP C@ 0<>      ( zero byte found? )
        WHILE
                1+
        REPEAT

        SWAP -          ( calculate the length )
;

: CSTRING       ( addr len -- c-addr )
        SWAP OVER       ( len saddr len )
        HERE @ SWAP     ( len saddr daddr len )
        CMOVE           ( len )

        HERE @ +        ( daddr+len )
        0 SWAP C!       ( store terminating NUL char )

        HERE @          ( push start address )
;

(
        THE ENVIRONMENT ----------------------------------------------------------------------

        Linux makes the process arguments and environment available to us on the stack.

        The top of stack pointer is saved by the early assembler code when we start up in the FORTH
        variable S0, and starting at this pointer we can read out the command line arguments and the
        environment.

        Starting at S0, S0 itself points to argc (the number of command line arguments).

        S0+4 points to argv[0], S0+8 points to argv[1] etc up to argv[argc-1].

        argv[argc] is a NULL pointer.

        After that the stack contains environment variables, a set of pointers to strings of the
        form NAME=VALUE and on until we get to another NULL pointer.

        The first word that we define, ARGC, pushes the number of command line arguments (note that
        as with C argc, this includes the name of the command).
)
: ARGC
        S0 @ @
;

(
        n ARGV gets the nth command line argument.

        For example to print the command name you would do:
                0 ARGV TELL CR
)
: ARGV ( n -- str u )
        1+ CELLS S0 @ + ( get the address of argv[n] entry )
        @               ( get the address of the string )
        DUP STRLEN      ( and get its length / turn it into a FORTH string )
;

(
        ENVIRON returns the address of the first environment string.  The list of strings ends
        with a NULL pointer.

        For example to print the first string in the environment you could do:
                ENVIRON @ DUP STRLEN TELL
)
: ENVIRON       ( -- addr )
        ARGC            ( number of command line parameters on the stack to skip )
        2 +             ( skip command line count and NULL pointer after the command line args )
        CELLS           ( convert to an offset )
        S0 @ +          ( add to base stack address )
;

(
        SYSTEM CALLS AND FILES  ----------------------------------------------------------------------

        Miscellaneous words related to system calls, and standard access to files.
)

( BYE exits by calling the Linux exit(2) syscall. )
: BYE           ( -- )
        0               ( return code (0) )
        SYS_EXIT        ( system call number )
        SYSCALL1
;

(
        UNUSED returns the number of cells remaining in the user memory (data segment).

        For our implementation we will use Linux brk(2) system call to find out the end
        of the data segment and subtract HERE from it.
)
: GET-BRK       ( -- brkpoint )
        0 SYS_BRK SYSCALL1      ( call brk(0) )
;

: UNUSED        ( -- n )
        GET-BRK         ( get end of data segment according to the kernel )
        HERE @          ( get current position in data segment )
        -
        4 /             ( returns number of cells )
;

(
        MORECORE increases the data segment by the specified number of (4 byte) cells.

        NB. The number of cells requested should normally be a multiple of 1024.  The
        reason is that Linux can't extend the data segment by less than a single page
        (4096 bytes or 1024 cells).

        This FORTH doesn't automatically increase the size of the data segment "on demand"
        (ie. when , (COMMA), ALLOT, CREATE, and so on are used).  Instead the programmer
        needs to be aware of how much space a large allocation will take, check UNUSED, and
        call MORECORE if necessary.  A simple programming exercise is to change the
        implementation of the data segment so that MORECORE is called automatically if
        the program needs more memory.
)
: BRK           ( brkpoint -- )
        SYS_BRK SYSCALL1
;

: MORECORE      ( cells -- )
        CELLS GET-BRK + BRK
;

(
        Standard FORTH provides some simple file access primitives which we model on
        top of Linux syscalls.

        The main complication is converting FORTH strings (address & length) into C
        strings for the Linux kernel.

        Notice there is no buffering in this implementation.
)

: R/O ( -- fam ) O_RDONLY ;
: R/W ( -- fam ) O_RDWR ;

: OPEN-FILE     ( addr u fam -- fd 0 (if successful) | c-addr u fam -- fd errno (if there was an error) )
        -ROT            ( fam addr u )
        CSTRING         ( fam cstring )
        SYS_OPEN SYSCALL2 ( open (filename, flags) )
        DUP             ( fd fd )
        DUP 0< IF       ( errno? )
                NEGATE          ( fd errno )
        ELSE
                DROP 0          ( fd 0 )
        THEN
;

: CREATE-FILE   ( addr u fam -- fd 0 (if successful) | c-addr u fam -- fd errno (if there was an error) )
        O_CREAT OR
        O_TRUNC OR
        -ROT            ( fam addr u )
        CSTRING         ( fam cstring )
        420 -ROT        ( 0644 fam cstring )
        SYS_OPEN SYSCALL3 ( open (filename, flags|O_TRUNC|O_CREAT, 0644) )
        DUP             ( fd fd )
        DUP 0< IF       ( errno? )
                NEGATE          ( fd errno )
        ELSE
                DROP 0          ( fd 0 )
        THEN
;

: CLOSE-FILE    ( fd -- 0 (if successful) | fd -- errno (if there was an error) )
        SYS_CLOSE SYSCALL1
        NEGATE
;

: READ-FILE     ( addr u fd -- u2 0 (if successful) | addr u fd -- 0 0 (if EOF) | addr u fd -- u2 errno (if error) )
        >R SWAP R>      ( u addr fd )
        SYS_READ SYSCALL3

        DUP             ( u2 u2 )
        DUP 0< IF       ( errno? )
                NEGATE          ( u2 errno )
        ELSE
                DROP 0          ( u2 0 )
        THEN
;

(
        PERROR prints a message for an errno, similar to C's perror(3) but we don't have the extensive
        list of strerror strings available, so all we can do is print the errno.
)
: PERROR        ( errno addr u -- )
        TELL
        ':' EMIT SPACE
        ." ERRNO="
        . CR
;

(
        ASSEMBLER CODE ----------------------------------------------------------------------

        This is just the outline of a simple assembler, allowing you to write FORTH primitives
        in assembly language.

        Assembly primitives begin ': NAME' in the normal way, but are ended with ;CODE.  ;CODE
        updates the header so that the codeword isn't DOCOL, but points instead to the assembled
        code (in the DFA part of the word).

        We provide a convenience macro NEXT (you guessed what it does).  However you don't need to
        use it because ;CODE will put a NEXT at the end of your word.

        The rest consists of some immediate words which expand into machine code appended to the
        definition of the word.  Only a very tiny part of the i386 assembly space is covered, just
        enough to write a few assembler primitives below.
)

HEX

( Equivalent to the NEXT macro )
: NEXT IMMEDIATE AD C, FF C, 20 C, ;

: ;CODE IMMEDIATE
        [COMPILE] NEXT          ( end the word with NEXT macro )
        ALIGN                   ( machine code is assembled in bytes so isn't necessarily aligned at the end )
        LATEST @ DUP
        HIDDEN                  ( unhide the word )
        DUP >DFA SWAP >CFA !    ( change the codeword to point to the data area )
        [COMPILE] [             ( go back to immediate mode )
;

( The i386 registers )
: EAX IMMEDIATE 0 ;
: ECX IMMEDIATE 1 ;
: EDX IMMEDIATE 2 ;
: EBX IMMEDIATE 3 ;
: ESP IMMEDIATE 4 ;
: EBP IMMEDIATE 5 ;
: ESI IMMEDIATE 6 ;
: EDI IMMEDIATE 7 ;

( i386 stack instructions )
: PUSH IMMEDIATE 50 + C, ;
: POP IMMEDIATE 58 + C, ;

( RDTSC instruction )
: RDTSC IMMEDIATE 0F C, 31 C, ;

DECIMAL

(
        RDTSC is an assembler primitive which reads the Pentium timestamp counter (a very fine-
        grained counter which counts processor clock cycles).  Because the TSC is 64 bits wide
        we have to push it onto the stack in two slots.
)
: RDTSC         ( -- lsb msb )
        RDTSC           ( writes the result in %edx:%eax )
        EAX PUSH        ( push lsb )
        EDX PUSH        ( push msb )
;CODE

(
        INLINE can be used to inline an assembler primitive into the current (assembler)
        word.

        For example:

                : 2DROP INLINE DROP INLINE DROP ;CODE

        will build an efficient assembler word 2DROP which contains the inline assembly code
        for DROP followed by DROP (eg. two 'pop %eax' instructions in this case).

        Another example.  Consider this ordinary FORTH definition:

                : C@++ ( addr -- addr+1 byte ) DUP 1+ SWAP C@ ;

        (it is equivalent to the C operation '*p++' where p is a pointer to char).  If we
        notice that all of the words used to define C@++ are in fact assembler primitives,
        then we can write a faster (but equivalent) definition like this:

                : C@++ INLINE DUP INLINE 1+ INLINE SWAP INLINE C@ ;CODE

        One interesting point to note is that this "concatenative" style of programming
        allows you to write assembler words portably.  The above definition would work
        for any CPU architecture.

        There are several conditions that must be met for INLINE to be used successfully:

        (1) You must be currently defining an assembler word (ie. : ... ;CODE).

        (2) The word that you are inlining must be known to be an assembler word.  If you try
        to inline a FORTH word, you'll get an error message.

        (3) The assembler primitive must be position-independent code and must end with a
        single NEXT macro.

        Exercises for the reader: (a) Generalise INLINE so that it can inline FORTH words when
        building FORTH words. (b) Further generalise INLINE so that it does something sensible
        when you try to inline FORTH into assembler and vice versa.

        The implementation of INLINE is pretty simple.  We find the word in the dictionary,
        check it's an assembler word, then copy it into the current definition, byte by byte,
        until we reach the NEXT macro (which is not copied).
)
HEX
: =NEXT         ( addr -- next? )
           DUP C@ AD <> IF DROP FALSE EXIT THEN
        1+ DUP C@ FF <> IF DROP FALSE EXIT THEN
        1+     C@ 20 <> IF      FALSE EXIT THEN
        TRUE
;
DECIMAL

( (INLINE) is the lowlevel inline function. )
: (INLINE)      ( cfa -- )
        @                       ( remember codeword points to the code )
        BEGIN                   ( copy bytes until we hit NEXT macro )
                DUP =NEXT NOT
        WHILE
                DUP C@ C,
                1+
        REPEAT
        DROP
;

: INLINE IMMEDIATE
        WORD FIND               ( find the word in the dictionary )
        >CFA                    ( codeword )

        DUP @ DOCOL = IF        ( check codeword <> DOCOL (ie. not a FORTH word) )
                ." Cannot INLINE FORTH words" CR ABORT
        THEN

        (INLINE)
;

HIDE =NEXT

(
        NOTES ----------------------------------------------------------------------

        DOES> isn't possible to implement with this FORTH because we don't have a separate
        data pointer.
)

(
        WELCOME MESSAGE ----------------------------------------------------------------------

        Print the version and OK prompt.
)

: WELCOME
        S" TEST-MODE" FIND NOT IF
                ." JONESFORTH VERSION " VERSION . CR
                UNUSED . ." CELLS REMAINING" CR
                ." OK "
        THEN
;

WELCOME
HIDE WELCOME
## INDIRECT THREADED CODE

It turns out that direct threaded code is interesting but only if you want to just execute
a list of functions written in assembly language.  So QUADRUPLE would work only if DOUBLE
was an assembly language function.  In the direct threaded code, QUADRUPLE would look like:

<svg height="96" width="544" xmlns="http://www.w3.org/2000/svg"><style>circle,line,path,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}text{fill:#000;font-family:monospace;font-size:14px}.bg_filled,.nofill{fill:#fff}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h544v96H0z"/><text x="82" y="28">addr</text><text x="122" y="28">of</text><text x="146" y="28">DOUBLE</text><path class="solid end_marked_arrow" d="M208 24h48"/><text x="82" y="60">addr</text><text x="122" y="60">of</text><text x="146" y="60">DOUBLE</text><path class="nofill" d="M272 16a16 16 0 000 16"/><text x="282" y="28">assembly</text><text x="314" y="44">NEXT</text><text x="354" y="28">code</text><text x="394" y="28">to</text><text x="418" y="28">do</text><text x="442" y="28">the</text><text x="474" y="28">double</text><path class="nofill" d="M528 16a16 16 0 010 16"/><text x="2" y="60">%esi</text><path class="solid end_marked_arrow" d="M40 56h16"/><path class="solid" d="M68 8h152M68 8v64M220 8v64M68 40h152M68 72h152"/></svg>

We can add an extra indirection to allow us to run both words written in assembly language
(primitives written for speed) and words written in FORTH themselves as lists of addresses.

The extra indirection is the reason for the brackets in JMP *(%eax).

Let's have a look at how QUADRUPLE and DOUBLE really look in FORTH:

<svg height="448" width="736" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled{fill:#fff}text{font-family:monospace;font-size:14px}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h736v448H0z"/><text x="2" y="12">:</text><text x="18" y="12">QUADRUPLE</text><text x="98" y="12">DOUBLE</text><text x="154" y="12">DOUBLE</text><text x="210" y="12">;</text><text x="18" y="60">codeword</text><text x="18" y="92">addr</text><text x="58" y="92">of</text><text x="82" y="92">DOUBLE</text><path class="solid end_marked_arrow" d="M144 88h128"/><text x="18" y="124">addr</text><text x="58" y="124">of</text><text x="82" y="124">DOUBLE</text><text x="18" y="156">addr</text><text x="58" y="156">of</text><text x="82" y="156">EXIT</text><text x="282" y="60">:</text><text x="298" y="60">DOUBLE</text><text x="354" y="60">DUP</text><text x="386" y="60">+</text><text x="402" y="60">;</text><text x="298" y="108">codeword</text><text x="298" y="140">addr</text><text x="338" y="140">of</text><text x="362" y="140">DUP</text><path class="solid end_marked_arrow" d="M408 136h120"/><text x="298" y="172">addr</text><text x="338" y="172">of</text><text x="362" y="172">+</text><text x="298" y="204">addr</text><text x="338" y="204">of</text><text x="362" y="204">EXIT</text><path class="solid end_marked_arrow" d="M476 296h52"/><text x="554" y="156">codeword</text><text x="554" y="188">assembly</text><text x="626" y="188">to</text><path class="filled" d="M680 180l-8 4 8 4z"/><text x="554" y="204">implement</text><text x="634" y="204">DUP</text><text x="586" y="220">..</text><text x="586" y="236">..</text><text x="554" y="252">NEXT</text><text x="218" y="172">%esi</text><path class="solid end_marked_arrow" d="M256 168h16"/><text x="554" y="316">codeword</text><text x="554" y="348">assembly</text><text x="626" y="348">to</text><path class="filled" d="M672 340l-8 4 8 4z"/><text x="554" y="364">implement</text><text x="634" y="364">+</text><text x="586" y="380">..</text><text x="586" y="396">..</text><text x="554" y="412">NEXT</text><path class="solid" d="M4 40h152M4 40v128M156 40v128M4 72h152M4 104h152M4 136h152M4 168h152"/><g><path class="solid" d="M284 88h152M284 88v128M436 88v128M284 120h152M284 152h152M284 184h152M284 216h152"/></g><g><path class="solid" d="M408 168h68M476 168v128"/></g><g><path class="solid" d="M540 136h152M540 136v128M692 136v128M540 168h152M540 264h152"/></g><g><path class="solid" d="M664 152h60M724 152v32M680 184h44"/></g><g><path class="solid" d="M540 296h152M540 296v128M692 296v128M540 328h152M540 424h152"/></g><g><path class="solid" d="M664 312h60M724 312v32M672 344h52"/></g></svg>

This is the part where you may need an extra cup of tea/coffee/favourite caffeinated
beverage.  What has changed is that I've added an extra pointer to the beginning of
the definitions.  In FORTH this is sometimes called the "codeword".  The codeword is
a pointer to the interpreter to run the function.  For primitives written in
assembly language, the "interpreter" just points to the actual assembly code itself.
They don't need interpreting, they just run.

In words written in FORTH (like QUADRUPLE and DOUBLE), the codeword points to an interpreter
function.

I'll show you the interpreter function shortly, but let's recall our indirect
JMP *(%eax) with the "extra" brackets.  Take the case where we're executing DOUBLE
as shown, and DUP has been called.  Note that %esi is pointing to the address of +

The assembly code for DUP eventually does a NEXT.  That:

(1) reads the address of + into %eax            %eax points to the codeword of +
(2) increments %esi by 4
(3) jumps to the indirect %eax                  jumps to the address in the codeword of +,
                                                ie. the assembly code to implement +

<svg height="416" width="736" xmlns="http://www.w3.org/2000/svg"><style>circle,line,polygon{stroke:#000;stroke-width:2;stroke-opacity:1;fill-opacity:1;stroke-linecap:round;stroke-linejoin:miter}.filled,text{fill:#000}.bg_filled{fill:#fff}text{font-family:monospace;font-size:14px}.end_marked_arrow{marker-end:url(#arrow)}</style><defs><marker id="arrow" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 0v4l4-2-4-2z"/></marker><marker id="diamond" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="2" viewBox="-2 -2 8 8"><path d="M0 2l2-2 2 2-2 2-2-2z"/></marker><marker id="circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="filled" cx="4" cy="4" r="2"/></marker><marker id="open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="2"/></marker><marker id="big_open_circle" markerHeight="7" markerWidth="7" orient="auto-start-reverse" refX="4" refY="4" viewBox="0 0 8 8"><circle class="bg_filled" cx="4" cy="4" r="3"/></marker></defs><path class="backdrop" fill="#fff" stroke-width="2" stroke-linecap="round" d="M0 0h736v416H0z"/><text x="18" y="28">codeword</text><text x="18" y="60">addr</text><text x="58" y="60">of</text><text x="82" y="60">DOUBLE</text><path class="solid end_marked_arrow" d="M144 56h128"/><text x="18" y="92">addr</text><text x="58" y="92">of</text><text x="82" y="92">DOUBLE</text><text x="18" y="124">addr</text><text x="58" y="124">of</text><text x="82" y="124">EXIT</text><text x="298" y="76">codeword</text><text x="298" y="108">addr</text><text x="338" y="108">of</text><text x="362" y="108">DUP</text><path class="solid end_marked_arrow" d="M408 104h120"/><text x="298" y="140">addr</text><text x="338" y="140">of</text><text x="362" y="140">+</text><text x="298" y="172">addr</text><text x="338" y="172">of</text><text x="362" y="172">EXIT</text><path class="solid end_marked_arrow" d="M476 264h52"/><text x="554" y="124">codeword</text><text x="554" y="156">assembly</text><text x="626" y="156">to</text><path class="filled" d="M680 148l-8 4 8 4z"/><text x="554" y="172">implement</text><text x="634" y="172">DUP</text><text x="586" y="188">..</text><text x="586" y="204">..</text><text x="554" y="220">NEXT</text><text x="218" y="172">%esi</text><path class="solid end_marked_arrow" d="M256 168h16"/><text x="554" y="284">codeword</text><text x="554" y="316">assembly</text><text x="626" y="316">to</text><path class="filled" d="M680 308l-8 4 8 4z"/><text x="554" y="332">implement</text><text x="634" y="332">+</text><text x="586" y="348">..</text><text x="586" y="364">..</text><text x="554" y="380">NEXT</text><text x="450" y="316">now</text><text x="482" y="316">we&apos;re</text><text x="450" y="332">executing</text><text x="450" y="348">this</text><text x="450" y="364">function</text><path class="solid" d="M4 8h152M4 8v128M156 8v128M4 40h152M4 72h152M4 104h152M4 136h152"/><g><path class="solid" d="M284 56h152M284 56v128M436 56v128M284 88h152M284 120h152M284 152h152M284 184h152"/></g><g><path class="solid" d="M408 136h68M476 136v128"/></g><g><path class="solid" d="M540 104h152M540 104v128M692 104v32M540 136h152M692 160v72M540 232h152"/></g><g><path class="solid" d="M664 120h60M724 120v32M680 152h44"/></g><g><path class="solid" d="M540 264h152M540 264v128M692 264v32M540 296h152M692 320v72M540 392h152"/></g><g><path class="solid" d="M664 280h60M724 280v32M680 312h44"/></g></svg>

So I hope that I've convinced you that NEXT does roughly what you'd expect.  This is
indirect threaded code.

I've glossed over four things.  I wonder if you can guess without reading on what they are?

.
.
.

My list of four things are: (1) What does "EXIT" do?  (2) which is related to (1) is how do
you call into a function, ie. how does %esi start off pointing at part of QUADRUPLE, but
then point at part of DOUBLE.  (3) What goes in the codeword for the words which are written
in FORTH?  (4) How do you compile a function which does anything except call other functions
ie. a function which contains a number like : DOUBLE 2 * ; ?

