Data should never silently corrupt itself and it should be very difficult if not impossible to accidentally use data, even when writing code that manipulates files. 

We should tease out the data from files and present it as something more similar to a database. Clearly the relational model works for a lot of data, but we should allow for graph database views or key-value views where it makes sense. File types are just another view of the data and it should be clear to the user whether the format is isomorphic to the data in that particular context. 

I believe that WinFS was going to be something like this. We should investigate their approaches and conclusions.

This really isn’t that crazy. A filesystem is just a blob of bits. Metadata gives meaning to it. Each file itself is just a blob of bits. Metadata gives meaning to it. It would be nice to be able to describe all of those layers with one language and be able to manipulate the data all together.

Nayuki’s [Designing better file organization around tags, not hierarchies](https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies) is a good place to begin.


