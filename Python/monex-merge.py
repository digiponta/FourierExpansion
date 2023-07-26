#
import os
import glob
import csv
from datetime import datetime
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as ticker
import numpy as np
from mpl_toolkits.mplot3d import axes3d
#from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import codecs
import shutil

org = datetime (2023, 3, 1 ); # 資金運用開始年月日


# merge fname1 to fname2
fname1 =''
fname2 =''

#print (len(sys.argv))

if len(sys.argv) != 3:
	print ("merge fname1 to fname2")
	exit()

lines1 = []
lines2 = []

fname1 = sys.argv[1]
fname2 = sys.argv[2]

with open ( fname1, 'r', encoding="utf-8-sig") as fr:
#with open ( fname1, 'r') as fr:
	reader = csv.reader(fr)
	for line in reader:
		lines1 += [line]
fr.close()

#print( "lines1",lines1 )

with open ( fname2, 'r', encoding="utf-8-sig") as fr:
	reader = csv.reader(fr)
	for line in reader:
		lines2 += [line]
fr.close()
#print( "lines2",lines2 )


diff =  len (lines1) - len (lines2)

print ("diff", diff)

if (diff <= 0):
	print ("no action")
	exit()

fname2_sprit = fname2.split('.')

if (not os.path.isfile("org-" + fname2_sprit[0] + ".csv") ):
	print ("make the backup to ","org-" + fname2_sprit[0] + ".csv" )
	shutil.copyfile( fname2, "org-" + fname2_sprit[0] + ".csv") 
else:
	print ("exist: ","org-" + fname2_sprit[0] + ".csv" )

for ii in range (len(lines2)-2,len(lines1) ):
	lines2 += [lines1[ii]]

diff = len (lines1) - len (lines2) 

#print ("diff", diff)

#print ("lines2", lines2 )

fw = open ( fname2, 'w', encoding="utf-8" )
#fw = open ( "test.csv", 'w' )
for ii in range(0, len(lines2)):
	line = lines2[ii]
	fw.write( line[0] )
	for jj in range (1, len(line)):
		fw.write( "," )
		fw.write( str(line[jj]).replace( ",", "").replace( "'", "") )
	fw.write( '\n' )
fw.close()

#print ("lines1", lines1)
#print ("lines2", lines2)

