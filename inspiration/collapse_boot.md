## Block 089
Initialization sequence

On boot, we jump to the "main" routine in B289 which does
very few things.

1. Set `SP` to `PS_ADDR` and `IX` to `RS_ADDR`
2. Sets `HERE` to `RAMEND` (`RAMSTART+0x80`).
3. Sets `CURRENT` to value of `LATEST` field in stable ABI.
4. Look for the word "`BOOT`" and calls it.

In a normal system, `BOOT` is in xcomp core (B411) and does a
few things:

1. Initialize all overrides to 0.
2. Write `LATEST` in `BOOT C< PTR` ( see below )
3. Set "`C<*`", the word that `C<` calls to (boot<).
4. Call `INTERPRET` which interprets boot source code until
   ASCII EOT (4) is met. This usually init drivers.
5. Initialize rdln buffer, _sys entry (for EMPTY), prints
   "CollapseOS" and then calls (main).
6. (main) interprets from rdln input (usually from KEY) until
   EOT is met, then calls BYE.

In RAM-only environment, we will typically have a
"`CURRENT @ HERE !`" line during init to have HERE begin at the
end of the binary instead of RAMEND.

## Block 280
Z80 boot code

This assembles the boot binary. It requires the Z80 assembler
(B200) and cross compilation setup (B260). It also requires
these constants to be set:

RAMSTART: beginning address of RAM. This is where system
variables are placed. HERE is then placed at RAM+80 (ref B80).

RS_ADDR: to be set to the bottom address of the Return Stack.

PS_ADDR: top address of the Parameter stack (PS grows down-
wards). Allow space for stack underflow protection (B76).

RESERVED REGISTERS: At all times, IX points to RSP TOS and IY
is IP. SP points to PSP TOS, but you can still use the stack\
in native code. you just have to make sure you've restored it
before "next".

STABLE ABI: The boot binary starts with a list of references.
The address of these references have to stay to those addr-
esses. The rest of the Collapse OS code depend on it. In fact,
up until 0x67, the (?br) wordref, pretty much everything has
to stay put.

To assemble, run "282 LOAD".

## Block 282
1 53 LOADR+
