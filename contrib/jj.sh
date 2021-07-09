#!/bin/bash
pybin=~/.cache/pypoetry/virtualenvs/joplin-jrnl-nWsdVp2M-py3.9/bin/python
jrnl=~/projects/arachnitech/joplin-jrnl/jj/main.py

if test $# -gt 0;then
    ${pybin} ${jrnl} "$@"
elif test ! -t 0; then
    while IFS= read -r line
    do
        entry="$entry $line"
    done
    echo $entry
    ${pybin} ${jrnl} "$entry"
else
    echo "Error: no entry given"
fi

