#!/usr/bin/env bash

# can be e.g. ${HOME}/.checksums/checksums-231111T1850
WORKDIR="$1"

SUMPATH="$WORKDIR"
SUMFILE="checksums"
SUMFILEPATH="${SUMPATH}/${SUMFILE}"

# TODO iteroi dupes.txt, tagaa jokainen filu "dupe" tai "dupecand"
# tässä vois kans järjestää duplikaattiryhmän luomisajan mukaan ja jättää merkkaamatta viimeisin

function setTagOnListedFiles() {
    tag="$1"
    # while read sum filepath; do
    while read -u 10 line1; do
        filepath="$( echo -e "$line1" | sed -E 's/^(.+)\t//g' )"
        if [ ! -f "$filepath" ]; then
            echo "File $filepath" >> log
            exit 68
        fi
        tag -s "$tag" "$filepath"
        echo "Tagged file '$filepath'" >> tagging.log
    done 10< "${SUMPATH}/tmp_tag_these.txt"
}

function untagAllReferencedFilesInFile() {
    filelist="$1"

    while read -u 13 filepath; do
        if [ -z "$filepath" ]; then
            continue
        fi

        echo "Would remove tag off file '$filepath'" >> tagging.log
        tag -r "$tag" "$filepath"
    done 13< "$filelist"
}

function removeTagOfLatestDuplicate() {
    tag="$1"

    # create / erase
    echo -n > "${SUMPATH}/tmp_remove_tag_of.txt"

    # makes sense to do something here only if there are more than 1 filepaths in the file.
    if [ $(wc -l "${SUMPATH}/tmp_with_timestamps_unsorted.txt" | awk '{print $1}') -gt 1 ]; then
        sort -n -k 1 "${SUMPATH}/tmp_with_timestamps_unsorted.txt" > "${SUMPATH}/tmp_with_timestamps_sorted.txt"

        uniqueTimestampCount="$( awk '{print $1}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | uniq | wc -l )"
        if [ $uniqueTimestampCount -eq 1 ]; then
            # järjestä filut koko polun mukaan. ois hienoo jos vois vaik tietyn ylähakemiston lasten luontiaikojen mukaan järjestää mutmut..
            # sit pitäs tietää että miks just se ylähakemisto. tarvis siis yleispätevän ratkaisun.
            awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | sort > "${SUMPATH}/tmp_paths_only_sorted.txt"
            # poista tagi sitten tiedostossa ensimmäisenä mainitulta tiedostolta.
            fileToRemoveTagOff="$(head -1 "${SUMPATH}/tmp_paths_only_sorted.txt")"
            # echo "$fileToRemoveTagOff" > "${SUMPATH}/tmp_remove_tag_of.txt"
            # echo "unique timestamp on file($fileToRemoveTagOff), will remove tag."
            # poista tagi sitten viimeiseltä.
            # tail -1 "${SUMPATH}/tmp_paths_only_sorted.txt" > "${SUMPATH}/tmp_remove_tag_of.txt"
            # HUOM tää on aika spesifi eli räätälöity ratkaisu. ei tule olemaan tällaisena tietokantavariantissa.
        else
            ## muussa tapauksessa poista tagi tiedostossa ylimmältä mainitulta tiedostolta.

            # sort -n -k 1 -r "${SUMPATH}/tmp_with_timestamps_sorted.txt" > "${SUMPATH}/tmp_with_timestamps_reversed.txt"

            # muussa tapauksessa poista tagi tiedostossa alimmalta mainitulta tiedostolta.
            latestTimestamp="$( awk '{print $1}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | tail -1 )"
            # echo "latestTimestamp($latestTimestamp)"

            rowCount="$( wc -l "${SUMPATH}/tmp_with_timestamps_sorted.txt" | awk '{print $1}' )"

            i=1
            while read -u 12 timestamp __path; do
                if [ -z "$timestamp" ]; then
                    continue
                fi
                if [ $i -eq $rowCount ]; then
                    # echo "skipping last (?) row: $timestamp $__path"
                    continue
                fi

                if [ ! -f "$path" ]; then
                    echo "File $path does not exist" >> log
                    exit 67
                fi
                # echo "Removing tag off file '$path'" >> tagging.log
                # echo "Would remove tag off file '$__path'" >> tagging.log
                tag -r "$tag" "$__path"
                # echo "$__path" >> "${SUMPATH}/tmp_remove_tag_of.txt"

                ((i++))

            done 12< "${SUMPATH}/tmp_with_timestamps_sorted.txt"
        fi

        untagAllReferencedFilesInFile "${SUMPATH}/tmp_remove_tag_of.txt"
    fi
}

function removeTagOfLatestFiles() {
    tag="$1"
    filepaths=()
    # filepaths="$(awk -F "\t" '{print $NF}' "${SUMPATH}/tmp_tag_these.txt")"
    while read -u 11 line2; do
        echo "line2($line2)line2" >> log
        filepath="$( echo -e "$line2" | sed -E 's/^(.+)\t//g' )"
        echo "filepath($filepath)filepath" >> log
        filepaths+=("$filepath")
    done 11< "${SUMPATH}/tmp_tag_these.txt"

    # create / erase
    echo -n > "${SUMPATH}/tmp_with_timestamps_unsorted.txt"

    # filepaths here contain all the duplicates of a single file (that have same checksum).
    for path in "${filepaths[@]}"; do
        # otetaan viimeisin muokkausaika joka tiedostosta
        # echo "derp path($path)" >> log
        stat -f "%m %N" -t "%s" "$path" >> "${SUMPATH}/tmp_with_timestamps_unsorted.txt"
        removeTagOfLatestDuplicate "$tag"
    done
    if [ ! -f "${SUMPATH}/tmp_with_timestamps_unsorted.txt" ]; then
        echo "File ${SUMPATH}/tmp_with_timestamps_unsorted.txt does not exist" >> log
        exit 66
    fi
}

function markDupesWithSameChecksum() {
    cp "${SUMPATH}/tmp_dupes.txt" "${SUMPATH}/tmp_tag_these.txt"

    # DEBUGGING
    # if grep -n 'VID-20160311-WA0000.mp4' "${SUMPATH}/tmp_tag_these.txt"; then
    #     echo -e "\n\n" >> log
    #     echo "KIINNOSTAA" >> log
    #     cat "${SUMPATH}/tmp_tag_these.txt" >> log
    #     echo -e "\n\n" >> log
    #     # exit 70
    # fi

    setTagOnListedFiles dupecand

    # removeTagOfLatestFiles dupecand
}

function markDupes() {
    while read -u 9 sum; do
        echo "checking sum($sum)"
        grep -E "^${sum}" "$SUMFILEPATH" > "${SUMPATH}/tmp_dupes.txt"
        markDupesWithSameChecksum
        removeTagOfLatestFiles dupecand
    done 9< "${SUMPATH}/tmp_dupe_checksums.txt"
}

rm -f ${SUMPATH}/tmp_*

# nappaa raakadatasta pelkät summat ja laita ne aakkosjärjestykseen
awk '{print $1}' "$SUMFILEPATH" | sort | uniq -c | sort -n -k 1 | grep -E -v '\ +1' | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' | sort > "${SUMPATH}/tmp_dupe_checksums.txt"

markDupes

# TODO ellei tuossa edellisessä vaiheessa ni tässä: iteroi dupes.txt taas, selvitä jokaisen filun kohdalla mikä on viimeisin ja poista siitä tagi.

# viimeisessä skriptissä sit etsitään filut joilla on dupe-tagi ja poistetaan kys. filut.
# eli ei tässä skriptissä.
