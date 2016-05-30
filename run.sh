#!/bin/bash

#countries=`cat nations_ready.txt | cut -f 1 | head -100`

DATADIR="/home/jmnybl/git_checkout/maastereotypiat"

RESDIR="/home/jmnybl/git_checkout/maastereotypiat/results2"

countries=$(cat $DATADIR/nations_ready.txt | cut -f 1 )

for c in $countries
do
    echo "#$c" > /dev/stderr
    if [ "$c" = "FI" ]
    then
        echo "zcat $DATADIR/nationality_data_s24.conllu.gz | python3 significant_features.py $c 20 > $RESDIR/s24_allwords_$c"
        echo "zcat $DATADIR/nationality_data_pb.conllu.gz | python3 significant_features.py $c 20 > $RESDIR/pb_allwords_$c"
    else
        echo "zcat $DATADIR/nationality_data_s24.conllu.gz | python3 remove_country_code.py FI | python3 significant_features.py $c 20 > $RESDIR/s24_allwords_$c"
        echo "zcat $DATADIR/nationality_data_pb.conllu.gz | python3 remove_country_code.py FI | python3 significant_features.py $c 20 > $RESDIR/pb_allwords_$c"
    fi
done
echo "#Pipe me to | parallel -j 24" > /dev/stderr
