# We will successively add layers of meaning to the stream of bytes. If we do our job well then
# it will end up with one pass and the generators will be able to be collapsed into a simple
# sequence of instructions.

# 1. Convert stream of bytes into list of commands with operands
operand_size = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,4,5,9,2,3,4,5,9,1,45,
                1,1,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                1,2,3,4,5,2,3,4,5,16,17,18,19,15,29,10]
commands = consume(open('foo.dvi'), operand_size)
# Now we have an iterable of DVI commands, which are each an iterable of bytes.

# 2. Add the state of the h, v, w, x, y, z variables at the end of each command
