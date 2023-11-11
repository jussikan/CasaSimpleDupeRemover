#!/usr/bin/env bash

# can be e.g. ${HOME}/.checksums/checksums-231111T1850
WORKDIR="$1"

SUMPATH="$WORKDIR"
SUMFILE="checksums"
SUMFILEPATH="${SUMPATH}/${SUMFILE}"

tag=dupecand

while read line; do
    filepath="$( echo -e "$line" | sed -E 's/^(.+)\t//g' )"
    tags="$( tag -l "$filepath" | sed "s#${filepath}##" | sed -E 's/^[[:space:]]+//; s/,/\ /g' )"

    if [[ "${tags[*]}" =~ "$tag" ]]; then
        # echo "would delete file '$filepath'" >> deletedupes.log
        # rm -f "$filepath"
        trash "$filepath"
    fi
done < "$SUMFILEPATH"
