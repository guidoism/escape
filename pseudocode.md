
[Unicode Symbol Charts](http://unicode.org/charts/)

## Messaging

We write this with the aid of context to subsume excrutiating detail.
We don't need variables because we have context and pronouns.

    messages is a sequenece
    show message summaries as vertical list, reverse chronological
    a message summary shows from name, date sent, one line summary
    a tap on the message summary brings up the conversation
    the conversation is between me and 1 or more other people
    it's shows a vertical list of messages between me and all of those other people
    messages from me are blue and those from others are gray
    
    messages:▤↧

* TODO: define show as vertical list
* TODO: define tap
* TODO: more specific layout for message summary (maybe using unicode control characters)

## Spreadsheets

    spreadsheet is a matrix of cells
    cells are numbers with or without types, strings, or formulas

Is a spreadsheet really something seperate? Maybe it's just another
interface to code, notes, and a database of numbers.

In Python I might write:

	adhoc = tablib.Dataset()
    adhoc.headers = ('Date', 'Amount', 'Category', 'Notes')
	daily = tablib.Dataset()
	daily.headers = ('Date', 'Fixed', 'Adhoc')
	# TODO: Load all the days for 2018 here
	daily.Adhoc = adhoc.
	daily.latex()


## Wiki, Documentation, and Notes

* Use a git repo for everything
* Everything is automatically saved as you type, explicit commit with
  optional comments are available too
* Compile to DVI immediately, these are ephemeral
* WYSIWYG, Markdown, and TeX layers

Can sprinkle code in docs and refer to it in other code. Should we
just combine both docs and code together (especially since we want
literate code)? p
