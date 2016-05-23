# maastereotypiat

nations_ready.txt --> country code and a list of search words

zcat /usr/share/ParseBank/parsebank_v4_UD.conllu.gz | python3 filter_pb.py | gzip -c > nationality_data_pb.conllu.gz
zcat /usr/share/ParseBank/Suomi24/UD_parsed/* | python3 filter_pb.py | gzip -c > nationality_data_s24.conllu.gz

zcat nationality_data_pb.conllu.gz | python3 grep_country_code.py SE | less 

zcat nationality_data_s24.conllu.gz | python3 significant_features.py SE

zcat nationality_data_s24.conllu.gz | python3 grep_country_code.py GR | python3 grep_type.py citizen | less

zcat nationality_data_s24.conllu.gz | python3 grep_type.py citizen | python3 significant_features.py GR


