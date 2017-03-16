a = open('crop001700.xml', 'r')
b = open('annoxml/crop001700.xml', 'r')
an = a.readlines()
bn = b.readlines()
for i in range(len(an)):
    ana = an[i].replace(' ','')
    ana = ana.replace('\t','')
    bna = bn[i].replace(' ','')
    bna = bna.replace('\t','')
    if ana != bna:
        print '#',i,':'
        print ana
        print bna
