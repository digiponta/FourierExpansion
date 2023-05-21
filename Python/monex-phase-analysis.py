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
import numpy as np
import matplotlib.pyplot as plt

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


 
#x = np.arange(-5, 5, 0.1)
#y = np.sin(x)
 
#plt.plot(x, y)

#y = np.cos(x)
#plt.plot(x, y)


 
#plt.savefig("sin.png")   # プロットしたグラフをファイルsin.pngに保存する
#plt.show()


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


# Make graph

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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as ticker

 
x = np.arange(0, 17, 0.5)
#y = np.sin(x)
 
#plt.plot(x, y)

#y = np.cos(x)
#plt.plot(x, y)


 
#plt.savefig("sin.png")   # プロットしたグラフをファイルsin.pngに保存する
#plt.show()


print(sys.argv, len(sys.argv) )

numcol = 2
fname = 'total-phase-analysis_' + dt_string + '.csv'
data0 = []
data1 = []
data2 = []


print( fname )

with open( fname, 'r', encoding="utf-8") as fr:
	reader = csv.reader(fr)
	idx = 0
	for line in reader:
		data0 += [float(line[0])]
		data1 += [float(line[1])]
		data2 += [float(line[2])]
		idx += 1
fr.close()


print( data0 )
print( data1 )
#print( data2 )
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.grid(True)
ax2.grid(False)

color_1 = cm.Set1.colors[1]
color_2 = cm.Set1.colors[0]

ax2.spines['left'].set_color(color_1)
ax2.spines['right'].set_color(color_2)
ax1.tick_params(axis='y', colors=color_1)
ax2.tick_params(axis='y', colors=color_2)

ax1.set_xlabel("period (day with 0.5 day interval)")
ax2.set_xlabel("period (day with 0.5 day interval)")
ax1.set_ylabel("Average value of Phase (tangent value)")
ax2.set_ylabel("Standard deviation")


ax1.plot( data0, data1, color=color_1, label="Average value of Phase (tangent value)" )
ax2.plot( data0, data2, color=color_2, label="Standard deviation" )

handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()
ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)

plt.title("Average Phase and each Standard deviation")
plt.xlabel("period (day with 0.5 day interval)")
#plt.ylabel("Amplitude")

fname_split = fname.split('.')

plt.savefig( fname_split[0] + ".png")   # プロットしたグラフをファイルsin.pngに保存する
plt.show()





print( '------- Finish -------')
