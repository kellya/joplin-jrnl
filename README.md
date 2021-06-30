# Joplin-jrnl
This is a CLI to append notes to a notebook as a running, append-only journaling system.  The general inspiration was the [jrnl](https://jrnl.sh/en/stable/) command line tool.  I like the general simplicity of how it works, but wanted the data to be more accessible through Joplin, which I use for general notetaking.

Currently this is a barely functional mess.  But it does work, so I'm going to
be tweaking it as I run into things that break.

# Roadmap/Hopes and Dreams
- [x] Add entries to a joplin note
- [ ] Optionally use editor to make bigger edits (or to deal with annoying
    characters in entry that shell wants to expand to something
- [ ] Search for entries based on content
- [ ] Search for entries based on tags
- [ ] More intelligent handling of options
    - [ ] Create a note if you don't specify one
    - [ ] Utilize options to override settings
- [ ] Print out entries to CLI
- [ ] Basically work like jrnl, but with joplin :)
