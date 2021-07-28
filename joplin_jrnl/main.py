#!/bin/env python
import yaml
import requests
import json
import sys
from datetime import datetime
from pathlib import Path

import select
import click

__version__ = "0.3.2"


class Journal:
    """The basic object to track journaly things"""

    def __init__(self, joplin_url=None, joplin_token=None, note_id=None):
        self.joplin_url = joplin_url
        self.joplin_token = joplin_token
        self.note_id = note_id

    def ping(self):
        """Ensure the clipper/api service is answering"""
        try:
            r = requests.get(f"{self.joplin_url}/ping")
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception:
            # This is a broad exception clause, but ultimately whatever was
            # put in as the base_url is not valid, so just return false and
            # make them figure out what it is
            return False

    def get_journal(self):
        """Returns the journal json content"""
        r = requests.get(
            f"{self.joplin_url}/notes/{self.note_id}?token={self.joplin_token}&fields=body"
        )
        return r.content.decode()

    def write_entry(self, entry=None):
        ###post the journal entry to joplin api###
        startnote = json.loads(self.get_journal())
        # There is probably a better way to do this, I don't want empty lines
        # at the first entry, but every other entry should start with newlines
        # to separate it from the other entries.  This only matters for the
        # first entry, seems stupid to check it every single time
        if not startnote["body"] == "":
            prefix = "\n\n"
        else:
            prefix = ""
        postdata = {
            "body": startnote["body"]
            + prefix
            + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {entry}"
        }
        r = requests.put(
            f"{self.joplin_url}/notes/{self.note_id}?token={self.joplin_token}",
            data=json.dumps(postdata),
        )
        if r.status_code == 200:
            return True
        else:
            return False

    def dump_journal(self):
        return json.loads(self.get_journal())["body"]


@click.command()
@click.version_option(__version__, prog_name="joplin-jrnl")
@click.option("--dump", is_flag=True, help="Dump the contents of the journal")
@click.option("--quiet", is_flag=True, help="Do not emit the 'entry added' output")
@click.option(
    "--edit",
    is_flag=True,
    help="Create a new entry from your default editor rather than from the command line",
)
@click.option(
    "--config",
    type=click.Path(),
    help="Specify an alternate configuration file location",
)
@click.argument("entry", nargs=-1)
def main(dump, quiet, edit, config, entry):
    """A utility to append journal entries to a note defined in Joplin"""
    if not config:
        home = str(Path.home())
        config = f"{home}/.config/joplin-jrnl/conf.yaml"
    with open(config) as file:
        # I am about to use config as the data contents, wiping out the
        # commandline option values for config.
        config = yaml.safe_load(file)
    # instantiate a journal
    journal = Journal(config["base_url"], config["token"], config["note_id"])
    # Test the URL and write what was given in argv if we get an OK
    if dump and journal.ping():
        print(journal.dump_journal())
        sys.exit()
    if edit and journal.ping():
        MARKER = "###### Everything below is ignored ######\n"
        entry = click.edit("\n" + MARKER)
        if entry is not None:
            entry_posted = journal.write_entry(entry.split(MARKER, 1)[0].rstrip("\n"))
        else:
            entry_posted = False
    elif journal.ping():
        if select.select(
            [
                sys.stdin,
            ],
            [],
            [],
            0.0,
        )[0]:
            entry_posted = journal.write_entry(sys.stdin.readlines()[0].rstrip("\n"))
            if entry_posted and entry_posted != "":
                click.echo(click.style("[Entry added]", fg="green"))
                sys.exit(0)
            else:
                click.echo(click.style("STDIN data not posted to journal"), fg="red")
        # Since I want the whole line to be the args, handle the fact that
        # specifying --quiet gives us one more argument to skip
        clean_args = []
        # Clean up the args to make sure we don't get the program name, or any --options
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                clean_args.append(arg)
        if clean_args:
            entry_posted = journal.write_entry(" ".join(clean_args))
        else:
            click.echo(click.style("- No entry added -", fg="yellow"))
            sys.exit()
    else:
        click.echo(
            click.style(
                f"Error: did not get successful response from {journal.joplin_url}",
                fg="red",
            )
        )
        sys.exit(99)
    if entry_posted and not quiet:
        click.echo(click.style("[Entry added]", fg="green"))
    elif not entry_posted:
        click.echo(click.style("- No entry added -", fg="yellow"))


if __name__ == "__main__":
    main()
