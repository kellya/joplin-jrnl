# Joplin-jrnl
This is a CLI to append notes to a notebook as a running, append-only journaling system.  The general inspiration was the [jrnl](https://jrnl.sh/en/stable/) command line tool.  I like the general simplicity of how it works, but wanted the data to be more accessible through Joplin, which I use for general notetaking.

# How the heck to I use this?
joplin-jrnl has been published to PyPi, so you should be able to get this
running by simply executing `pip install joplin-jrnl`.  You may then run the
`jj` command to see how to further interact with it.

This is an early development version, as such there aren't many sanity checks in
place.  So at the moment you have to create an area for the configuration to
live and there is currently no option to specify an alternate location (I'll get
there ;) )

## Create a note in joplin that will serve as your journal
In order for the script to work, you must have a note designated as the journal.
To do this:

    1. Open Joplin
    2. Create a note (you can name it anything you wish)
    3. Right click the note and select "copy markdown link"
    4. You will get a value like "[note-name](:/df36fc8138da4169b29f0a577cba601e)  You need to paste in just the 'df36fc8138da4169b29f0a577cba601e' part as the note id in ~/.config/jj/conf.yaml.

## create configuration file and path

    1. `mkdir ~/.config/joplin-jrnl/`
    2. `cp conf.yaml ~/.config/joplin-jrnl/`
    3. Edit conf.yaml to reflect your values

# Roadmap/Hopes and Dreams
- [x] Add entries to a joplin note
- [x] Optionally use editor to make bigger edits (or to deal with annoying
    characters in entry that shell wants to expand to something
- [ ] Search for entries based on content
- [ ] Search for entries based on tags
- [x] More intelligent handling of options
    - [ ] Create a note if you don't specify one
    - [ ] Utilize options to override settings
- [x] Print out entries to CLI
- [ ] Basically work like jrnl, but with joplin :)
- [ ] Figure out asyncio stuff and use that instead of requests
