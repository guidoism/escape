## Block 089
Initialization sequence

On boot, we jump to the "main" routine in B289 which does
very few things.

1. Set `SP` to `PS_ADDR` and `IX` to `RS_ADDR`
2. Sets HERE to RAMEND (RAMSTART+0x80).
3. Sets CURRENT to value of LATEST field in stable ABI.
4. Look for the word "BOOT" and calls it.

In a normal system, BOOT is in xcomp core (B411) and does a
few things:

1. Initialize all overrides to 0.
2. Write LATEST in BOOT C< PTR ( see below )
3. Set "C<*", the word that C< calls to (boot<).
4. Call INTERPRET which interprets boot source code until
   ASCII EOT (4) is met. This usually init drivers.
5. Initialize rdln buffer, _sys entry (for EMPTY), prints
   "CollapseOS" and then calls (main).
6. (main) interprets from rdln input (usually from KEY) until
   EOT is met, then calls BYE.

In RAM-only environment, we will typically have a
"CURRENT @ HERE !" line during init to have HERE begin at the
end of the binary instead of RAMEND.
