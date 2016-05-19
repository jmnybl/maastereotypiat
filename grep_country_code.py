import codecs
import sys
import re
import conllutil

code=sys.argv[1]
comment=u"# nationality: "+unicode(code)
print >> sys.stderr,comment

counter=1
for comm,sent in conllutil.read_conllu(codecs.getreader(u"utf-8")(sys.stdin)):

    if comment in comm:

        conllutil.plain_print(sys.stdout,comm,sent)
        counter+=1

print >> sys.stderr,counter
