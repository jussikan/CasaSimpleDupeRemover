#!/usr/bin/env bash

SUMPATH="${HOME}/.checksums"
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
