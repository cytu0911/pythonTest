#author: cytu

import os
ls = os.linesep
import pdb
pdb.set_trace()

while True :
    fname = raw_input('input file name:  ')
    if os.path.exists(fname):
        print "Error"
    else:
        break

all=[]
print "\nEnter lines ('.' by itself to quit).\n"

while True:
    entry = raw_input('>')
    if entry == '.':
        break
    else:
        all.append(entry)

fobj = open(fname,'w')
fobj.writelines( ['%s%s' %(x,ls) for x in all] )
fobj.close()
print 'Done'

