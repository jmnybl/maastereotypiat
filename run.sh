#!/bin/bash

#countries=`cat nations_ready.txt | cut -f 1 | head -100`

DATADIR="/home/jmnybl/git_checkout/maastereotypiat"

RESDIR="/home/jmnybl/git_checkout/maastereotypiat/results4"

#countries=$(cat $DATADIR/nations_ready.txt | cut -f 1 )
countries=$(cat $DATADIR/counts_s24 | cut -d":" -f 2 | perl -pe 's/ //')

for c in $countries
do
#    echo "#$c" > /dev/stderr
#    if [ ! -s "$RESDIR/s24_allwords_$c" ]
#    then
#	echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 significant_features.py $c > $RESDIR/s24_allwords_$c"
#    fi

    # s24 all data, just adjectives
    echo "#$c" > /dev/stderr
    if [ ! -s "$RESDIR/s24_alladj_$c" ]
    then
	echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 significant_features.py $c ADJ > $RESDIR/s24_alladj_$c"
    fi
 
#    if [ ! -s "$RESDIR/s24_citizenadj_$c" ]
#    then
#	echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 grep_type.py citizen | python3 significant_features.py $c ADJ > $RESDIR/s24_citizenadj_$c"
#    fi

    # if [ ! -s "$RESDIR/pb_citizenadj_$c" ]
    # then
    # 	echo "zcat $DATADIR/nationality_data_pb_limited.conllu.gz | python3 grep_type.py citizen | python3 significant_features2.py $c > $RESDIR/pb_citizenadj_$c"
    # fi

#    if [ ! -s "$RESDIR/s24_sentadjcitizen_$c" ]
#    then
#	echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 grep_type.py citizen | python3 sentiment_features.py $c > $RESDIR/s24_sentadjcitizen_$c"
#    fi

    # if [ ! -s $RESDIR/s24_sentadj_$c ]
    # then
    # 	echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 sentiment_features.py $c > $RESDIR/s24_sentadj_$c"
    # fi







   # if [ "$c" = "FI" ]
    # then
    #    # echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 significant_features.py $c > $RESDIR/s24_allwords_$c"

    # else
    #    # echo "zcat $DATADIR/nationality_data_s24_limited.conllu.gz | python3 significant_features.py $c > $RESDIR/s24_allwords_$c"
    #     echo "zcat $DATADIR/nationality_data_pb_limited.conllu.gz | python3 significant_features.py $c > $RESDIR/pb_allwords_$c"
    # fi
done
#echo "#Pipe me to | parallel -j 24" > /dev/stderr
