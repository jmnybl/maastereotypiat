import re
import json
import random

count_re=re.compile("^\s*([0-9]+) # nationality: ([A-Z]+)$")

def c2j(fname_in,fname_out,varname):
    counts={} # nationality -> count
    with open(fname_in) as f:
        for line in f:
            match=count_re.match(line.strip())
            if match:
                counts[match.group(2)]=int(match.group(1))
    with open(fname_out,"w") as f:
        print("{} = '{}';".format(varname,json.dumps(counts,sort_keys=True)),file=f)

c2j("/home/jmnybl/git_checkout/maastereotypiat/counts_pb","counts_pb.json","counts_pb")
c2j("/home/jmnybl/git_checkout/maastereotypiat/counts_s24","counts_s24.json","counts_s24")



