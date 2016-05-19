# maastereotypiat

nations_ready.txt --> country code and a list of search words

zcat /usr/share/ParseBank/parsebank_v4_UD.conllu.gz | python filter_pb.py | gzip -c > nationality_data_pb.conllu.gz
zcat /usr/share/ParseBank/Suomi24/UD_parsed/* | python filter_pb.py | gzip -c > nationality_data_s24.conllu.gz

zcat nationality_data_pb.conllu.gz | python grep_country_code.py SE | less 

zcat nationality_data_s24.conllu.gz | python significant_features.py SE

