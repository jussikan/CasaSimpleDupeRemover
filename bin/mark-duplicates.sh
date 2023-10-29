#!/usr/bin/env bash

SUMPATH="${HOME}/.checksums"
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
    # filepath="$2"

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
            echo "$fileToRemoveTagOff" > "${SUMPATH}/tmp_remove_tag_of.txt"
            echo "unique timestamp on file($fileToRemoveTagOff), will remove tag."
            # poista tagi sitten viimeiseltä.
            # tail -1 "${SUMPATH}/tmp_paths_only_sorted.txt" > "${SUMPATH}/tmp_remove_tag_of.txt"
            # HUOM tää on aika spesifi eli räätälöity ratkaisu. ei tule olemaan tällaisena tietokantavariantissa.
        else
            # sort -n -k 1 -r "${SUMPATH}/tmp_with_timestamps_unsorted.txt" > "${SUMPATH}/tmp_with_timestamps_sorted.txt"

            # muussa tapauksessa poista tagi tiedostossa ylimmältä mainitulta tiedostolta.
            # latestTimestamp="$( awk '{print $1}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | head -1 )"

            # echo "KATO tmp_with_timestamps_sorted.txt NYT !! paina ctrl+z"
            # sleep 3

            # sort -n -k 1 -r "${SUMPATH}/tmp_with_timestamps_sorted.txt" > "${SUMPATH}/tmp_with_timestamps_reversed.txt"

            # muussa tapauksessa poista tagi tiedostossa alimmalta mainitulta tiedostolta.
            # head -1 "${SUMPATH}/tmp_with_timestamps_sorted.txt" > "${SUMPATH}/tmp_remove_tag_of.txt"
            latestTimestamp="$( awk '{print $1}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | tail -1 )"
            echo "latestTimestamp($latestTimestamp)"

            rowCount="$( wc -l "${SUMPATH}/tmp_with_timestamps_sorted.txt" | awk '{print $1}' )"

            # latest="$( ls -t $filepaths | head -1 )"
            # latestFiles="$( awk '$1 == "$latestTimestamp" {print $2}' tmp_with_timestamps_sorted.txt)"
            # latestFiles="$( awk -v var="$latestTimestamp" '$1 == var {print $2}' "${SUMPATH}/tmp_with_timestamps_sorted.txt")"
            # for path in "${latestFiles[@]}"; do
            i=1
            while read -u 12 timestamp __path; do
                if [ -z "$timestamp" ]; then
                    continue
                fi
                if [ $i -eq $rowCount ]; then
                    echo "skipping last (?) row: $timestamp $__path"
                    continue
                fi

                echo "timestamp($timestamp) __path($__path)" >> tagging.log
                # if [ "$timestamp" -eq "$latestTimestamp" ]; then
                #     echo "derp? timestamp($timestamp) __path($__path)"
                #     # älä ainakaan tältä tiedostolta poista tagia.
                #     continue
                # fi
                # eli jos useammalla filulla on sekä sama tarkastussumma ja sama aikaleima,
                # niiltä jokaiselta poistetaan tagi.
                # echo "tagging path($path)path" >> log

                # 28.10.2023: täs käy nyt niin et aikaisemmin muokattu poistetaan, eikä se viimeisin..
                # jos (kun) latestTimestamp on eri filulta kuin mitä käsitellään, voi vaikuttaa asiaan..
                # senhän pitäis olla duplikaattien kesken viimeisimmän filun aika.

                if [ ! -f "$path" ]; then
                    echo "File $path does not exist" >> log
                    exit 67
                fi
                # echo "Removing tag off file '$path'" >> tagging.log
                echo "Would remove tag off file '$__path'" >> tagging.log
                tag -r "$tag" "$__path"
                echo "$__path" >> "${SUMPATH}/tmp_remove_tag_of.txt"

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
        echo "derp path($path)" >> log
        stat -f "%m %N" -t "%s" "$path" >> "${SUMPATH}/tmp_with_timestamps_unsorted.txt"

        # TODO? siirrä toi pitkä if-blokki funktioon, joka ottais filunimen argumentiksi?

        removeTagOfLatestDuplicate "$tag"
    done
    if [ ! -f "${SUMPATH}/tmp_with_timestamps_unsorted.txt" ]; then
        echo "File ${SUMPATH}/tmp_with_timestamps_unsorted.txt does not exist" >> log
        exit 66
    fi

    # # create / erase
    # echo > "${SUMPATH}/tmp_remove_tag_of.txt"

    # # TODO jos filussa on vain 1 rivi, skippaa looppi
    # if [ $(wc -l "${SUMPATH}/tmp_with_timestamps_unsorted.txt" | awk '{print $1}') -gt 1 ]; then
    #     sort -n -k 1 -r "${SUMPATH}/tmp_with_timestamps_unsorted.txt" > "${SUMPATH}/tmp_with_timestamps_sorted.txt"

    #     # ongelma: tää ei nyt ota huomioon sitä et tmp_with_timestamps_sorted.txt:ssä on useampi filu, ja duplikaateilla on samat aikaleimat.

    #     # TODO jos filun kaikki aikaleimat on samoja, järjestä filut polkujen mukaan siten, että vanhin on alimpana.
    #     uniqueTimestampCount="$( uniq "${SUMPATH}/tmp_with_timestamps_sorted.txt" | wc -l )"
    #     if [ $uniqueTimestampCount -eq 1 ]; then
    #         # järjestä filut koko polun mukaan. ois hienoo jos vois vaik tietyn ylähakemiston lasten luontiaikojen mukaan järjestää mutmut..
    #         # sit pitäs tietää että miks just se ylähakemisto. tarvis siis yleispätevän ratkaisun.
    #         awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | sort > "${SUMPATH}/tmp_paths_only_sorted.txt"
    #         # poista tagi sitten ensimmäiseltä.
    #         head -1 "${SUMPATH}/tmp_paths_only_sorted.txt" > "${SUMPATH}/tmp_remove_tag_of.txt"
    #         # HUOM tää on aika spesifi eli räätälöity ratkaisu. ei tule olemaan tällaisena tietokantavariantissa.
    #     else
    #         # muussa tapauksessa poista tagi ensimmäiseltä.
    #         # head -1 "${SUMPATH}/tmp_with_timestamps_sorted.txt" > "${SUMPATH}/tmp_remove_tag_of.txt"
    #         latestTimestamp="$( awk '{print $1}' "${SUMPATH}/tmp_with_timestamps_sorted.txt" | head -1 )"
    #         echo "latestTimestamp($latestTimestamp)"

    #         # latest="$( ls -t $filepaths | head -1 )"
    #         # latestFiles="$( awk '$1 == "$latestTimestamp" {print $2}' tmp_with_timestamps_sorted.txt)"
    #         # latestFiles="$( awk -v var="$latestTimestamp" '$1 == var {print $2}' "${SUMPATH}/tmp_with_timestamps_sorted.txt")"
    #         # for path in "${latestFiles[@]}"; do
    #         while read -u 12 line3 __path; do
    #             timestamp="$( echo "$line3" | awk '{print $1}')"
    #             echo "timestamp($timestamp)" >> tagging.log
    #             if [ "$timestamp" -eq "$latestTimestamp" ]; then
    #                 echo "derp? timestamp($timestamp) __path($__path)"
    #                 continue
    #             fi
    #             # eli jos useammalla filulla on sekä sama tarkastussumma ja sama aikaleima,
    #             # niiltä jokaiselta poistetaan tagi.
    #             # echo "tagging path($path)path" >> log

    #             # 28.10.2023: täs käy nyt niin et aikaisemmin muokattu poistetaan, eikä se viimeisin..
    #             # jos (kun) latestTimestamp on eri filulta kuin mitä käsitellään, voi vaikuttaa asiaan..
    #             # senhän pitäis olla duplikaattien kesken viimeisimmän filun aika.

    #             if [ ! -f "$path" ]; then
    #                 echo "File $path does not exist" >> log
    #                 exit 67
    #             fi
    #             # echo "Removing tag off file '$path'" >> tagging.log
    #             # tag -r "$tag" "$path"
    #             echo "$path" > "${SUMPATH}/tmp_remove_tag_of.txt"
    #         done 12< "${SUMPATH}/tmp_with_timestamps_sorted.txt"
    #     fi

    #     # use a loop..
    #     fileToRemoveTagOf="$( <"${SUMPATH}/tmp_remove_tag_of.txt" )"
    #     echo "Removing tag off file '$fileToRemoveTagOf'" >> tagging.log
    #     tag -r "$tag" "$fileToRemoveTagOf"
    # fi
}

# function markDupesWithSameChecksum0() {
#     dupeCount=$(wc -l "${SUMPATH}/tmp_dupes.txt" | awk '{print $1}')
#     # echo "dupeCount($dupeCount)"

#     let i=0
#     while [ $i -lt $dupeCount ]; do
#         echo "i($i)" >> log
#         let i_plus_1="$i + 1"
#         # sum="$( sed -n "${i}p;${i_plus_1}p" < "${SUMPATH}/tmp_dupes.txt" | awk '{print $1}' )"
#         sum="$( awk 'NR==1{print $1}' )"
#         thisSumCount="$(grep -c "^${sum}" "${SUMPATH}/tmp_dupes.txt")"

#         echo "sum($sum)" >> log
#         echo "thisSumCount($thisSumCount)" >> log
#         # let end="$i + $thisSumCount"
#         # echo "end($end)" >> log
#         # sed -n "${i}p;${end}p" < "${SUMPATH}/tmp_dupes.txt" > "${SUMPATH}/tmp_tag_these.txt"
#         cp "${SUMPATH}/tmp_dupes.txt" "${SUMPATH}/tmp_tag_these.txt"

#         # DEBUGGING
#         if grep -n 'VID-20160311-WA0000.mp4' "${SUMPATH}/tmp_tag_these.txt"; then
#             echo -e "\n\n" >> log
#             echo "KIINNOSTAA" >> log
#             cat "${SUMPATH}/tmp_tag_these.txt" >> log
#             echo -e "\n\n" >> log
#             exit 70
#         fi

#         setTagOnListedFiles dupecand

#         removeTagOfLatestFiles dupecand

#         # let i="$end + 1"
#         let i="$i + 1"

#     done
#     # < "${SUMPATH}/tmp_dupes.txt"
# }

function markDupesWithSameChecksum() {
    # sum="$( awk 'NR==1{print $1}' "${SUMPATH}/tmp_dupes.txt" )"
    # thisSumCount="$(grep -c "^${sum}" "${SUMPATH}/tmp_dupes.txt")"

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
