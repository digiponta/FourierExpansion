# マネックス証券の口座全体の資産推移の損益率の
# フーリエ展開プログラム (monex-fourier.py)
# made by digi-p@nifty.com,(C)2023, MIT License
#
import os
import glob
import csv
from datetime import datetime
import math
import sys
import datetime

# マネックス証券の口座全体の資産推移からダウンロードしたcsvファイル名
# スクリプト引数で、ファイル名を渡す場合
# ハードコーディグで、ファイル名を渡す場合

top = 0

# ここで、データのフィルタリング完了
#period_max = 16

total_sample = 0
data1 = []
data2 = []
fname =[]


print(sys.argv, len(sys.argv) )

if (len(sys.argv) > 1):
	print( 'use the sys.argv' )
	for ii in range(0, len(sys.argv)): 
	 	fname += [sys.argv[ii]]
	 	print( ii, sys.argv[ii] )
else:
	print( 'use all the csv-files in the current folder' )
	for name in glob.glob('./*-fourier.csv'):
		#print(name)
		fname += [name]

print( '------- fname -------')
for ii in range(0, len(fname)): 
 	print( ii, fname[ii] )

print( '------- Average value calculation -------')
for ii in range(0, len(fname)): 
	if ii != 0:
		if total_sample == 0:
			print( total_sample, ii, fname[ii] )
			with open( fname[ii], 'r', encoding="utf-8") as fr:
				reader = csv.reader(fr)
				idx = 0
				for line in reader:
					data1 += [line[2]]
					idx += 1
			fr.close()
		else:
			print( total_sample, ii, fname[ii] )
			with open( fname[ii], 'r', encoding="utf-8") as fr:
				reader = csv.reader(fr)
				idx = 0
				for line in reader:
					data1[idx] = str( float(data1[idx]) + float(line[2]) )
					idx += 1
			fr.close()
		total_sample += 1
	else:
		print( total_sample, ii, fname[ii] )

avg = []
for ii in range(0, len(data1)):
	 avg += [float(data1[ii]) / total_sample]

print( '------- Standard deviation calculation -------')


total_sample = 0
for ii in range(0, len(fname)): 
	if ii != 0:
		if total_sample == 0:
			print( total_sample, ii, fname[ii] )
			with open( fname[ii], 'r', encoding="utf-8") as fr:
				reader = csv.reader(fr)
				idx = 0
				for line in reader:
					#print( idx, data2 );
					data2 += [str((float(line[2]) - avg[idx]) * (float(line[2]) - avg[idx]) )]
					idx += 1
			fr.close()
		else:
			print( total_sample, ii, fname[ii] )
			with open( fname[ii], 'r', encoding="utf-8") as fr:
				reader = csv.reader(fr)
				idx = 0
				for line in reader:
					#print( data2 );
					data2[idx] = str((float(line[2])  - avg[idx]) * (float(line[2])  - avg[idx]) )
					idx += 1
			fr.close()
		total_sample += 1
	else:
		print( total_sample, ii, fname[ii] )


dt_now = datetime.datetime.now()
dt_string = dt_now.strftime('%Y%m%d_%H%M%S')
print ( "DataTime: ", dt_string )

print( '------- Output Result -------')
print( 'Total Samples: ' + str(total_sample) )
fw = open ( 'total-phase-analysis_' + dt_string + '.csv', 'w')	#
idx = 0
fsum = total_sample
for data in  data1:
	d1sum = float(data1[idx])
	d2sum = float(data2[idx])
	print ( idx/2+0.5, fsum, avg[idx], math.sqrt( d2sum / fsum )/math.fabs(avg[idx]) )
	fw.write( str(idx/2+0.5) + ', ' + str(avg[idx]) + ", " + str(math.sqrt( d2sum / fsum )/math.fabs(avg[idx])) + '\n')
	idx += 1
fw.close()
print( '------- Finish -------')
