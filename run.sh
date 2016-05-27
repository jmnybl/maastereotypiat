#!/bin/bash

#countries=`cat nations_ready.txt | cut -f 1 | head -100`
countries=`cat nations_ready.txt | cut -f 1 | tail -64`

for c in $countries
do
    echo $c
    if [ "$c" = "FI" ]
    then
        zcat nationality_data_s24.conllu.gz | python3 significant_features.py $c 20 > results/s24_allwords_$c &
        zcat nationality_data_pb.conllu.gz | python3 significant_features.py $c 20 > results/pb_allwords_$c &
        wait
    else
        zcat nationality_data_s24.conllu.gz | python3 remove_country_code.py FI | python3 significant_features.py $c 20 > results/s24_allwords_$c &
        zcat nationality_data_pb.conllu.gz | python3 remove_country_code.py FI | python3 significant_features.py $c 20 > results/pb_allwords_$c &
        wait
    fi
    
done
