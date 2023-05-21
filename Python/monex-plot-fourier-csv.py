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
fname = sys.argv[1]
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
ax1.set_ylabel("Amplitude")
ax2.set_ylabel("Phase (tangent value)")


ax1.plot( data0, data1, color=color_1, label="Amplitude" )
ax2.plot( data0, data2, color=color_2, label="Phase (tangent value)" )

handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()
ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)

plt.title("Fourier expansion result")
#plt.xlabel("period (day with 0.5 day interval)")
#plt.ylabel("Amplitude")

fname_split = fname.split('.')

plt.savefig( fname_split[0] + ".png")   # プロットしたグラフをファイルsin.pngに保存する
plt.show()

