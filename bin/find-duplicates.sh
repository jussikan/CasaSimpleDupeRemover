#!/usr/bin/env bash

DIR="$1"

SUMPATH="${HOME}/.checksums"
SUMFILE="checksums"
SUMFILEPATH="${SUMPATH}/${SUMFILE}"

# TODO tähän pvm+aika sekunnin tarkkuudella, alkamisaika
#THIS_RUN_SUMFILE="${}"

find "$DIR" -type f -not -name '.DS_Store' > "${SUMPATH}/files_unsorted.txt"
sort "${SUMPATH}/files_unsorted.txt" > "${SUMPATH}/files_sorted.txt"

while read filepath; do
    result="$(shasum -a 512 "$filepath")"
    sum=$(echo $result | awk '{print $1}')
    echo -e "${sum}\t${filepath}" >> "$SUMFILEPATH"
done < "${SUMPATH}/files_sorted.txt"

# TODO sit toisella skriptillä etsii tiedostot joilla on sama summa
# niistä sitte selvittää mikä on viimeisin, ja merkkaa muut vaikka tagaamalla.
#    tietty kaikkihan ne voi tagata heti alkuun ja poistaa tagin sit viimeisimmiltä.
# sit jos vieläpä samalla aikaleimalla ..
#   on samassa hakemistossa eri nimisiä, ni jos niistä sit merkkaa sen jolla on leksikaalisesti isompi nimi
#   on eri hakemistossa sama/eri nimisiä ... ni sama sääntö tähän?
#
# ykshän vois olla et luo erillisen hakemiston, jonka alle luo tarkastussumman nimisiä hakemistoja, joihin linkkaa kaikki duplikaatit.. niihin vois laittaa sit postifixillä juoksevan luvun erottuakseen.
#   sit jotta sekä linkit että alkuperäiset saa poistettua ni taas poistettavat pitäs merkata. kun on valmis poistamaan ni sit ajaa kolmannen skriptin joka etsii merkatut ja poistaa ne.
#   onkohan tää turhan paljon efforttia. no ei tätä MVP:hen tarvita.
