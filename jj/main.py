#!/bin/env python
import yaml
import requests
import json
import sys
from datetime import datetime

# import select
import click


with open("/home/kellya/.config/jj/conf.yaml") as file:
    config = yaml.safe_load(file)


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

    def dump_journal(self):
        return json.loads(self.get_journal())["body"]


@click.command()
@click.option("--dump", is_flag=True, help="Dump the contents of the journal")
@click.argument("entry", nargs=-1)
def main(dump, entry):
    # instantiate a journal
    journal = Journal(config["base_url"], config["token"], config["note_id"])
    # Test the URL and write what was given in argv if we get an OK
    if dump and journal.ping():
        print(journal.dump_journal())
    if journal.ping():
        #        if select.select(
        #            [
        #                sys.stdin,
        #            ],
        #            [],
        #            [],
        #            0.0,
        #        )[0]:
        #            journal.write_entry(sys.stdin.readlines()[0])
        #        else:
        journal.write_entry(" ".join(sys.argv[1:]))

    else:
        print(f"Error: did not get successful response from {journal.joplin_url}")


if __name__ == "__main__":
    main()
