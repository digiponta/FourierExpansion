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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as ticker
import numpy as np
import numpy as np
from mpl_toolkits.mplot3d import axes3d
#from sklearn.datasets import load_iris

org = datetime (2023, 3, 1 ); # 資金運用開始年月日

fname = ''
flist = []

# マネックス証券の口座全体の資産推移からダウンロードしたcsvファイル名
if len(sys.argv) > 1:
	# スクリプト引数で、ファイル名を渡す場合
	print( 'use the csv-files in argv' )
	fname = sys.argv[1]

else:
	# カレントディレクトリになる未経産のファイル名を対象にする場合、但し、１度に１ファイルの処理
	#fname = 'view_20230513_064542.csv'
	print( 'use all the csv-files in the current folder' )
	for name in glob.glob('view_*[0-9].csv'):
		#print(name)
		name_split = name.split('.')
		#print(name_split)
		if os.path.isfile( name_split[0] + "-fourier.csv"):
			# print( 'skip ' + name )
			continue
		else:
			#print( name_split[0] ) 
			fname = name_split[0] + ".csv"
			break
if fname == '':
	print('no csv file to be converted!');
	print( 'Done' )
	exit();

print( fname )

fname_split = fname.split('.')

delta1 = []
delta2 = []

with open( fname, 'r', encoding="utf-8") as fr:
	reader = csv.reader(fr)
	top = True
	data = []
	zz = []
	delta1 = []
	delta2 = []
	for line in reader:
		if top:
			top = False
		else:
			ds = line[0].split('/')
			yy = int( ds[0] )
			mm = int( ds[1] )
			dd = int( ds[2] )
			days = (datetime(yy, mm, dd) - org).days
			ratio = line[53].split('%')
			if ( days <= 0 ):
				ratio = '0.0'
			if ( days >= 0 ):
				data += [ [str(days), ratio[0]] ]
	# ここで、データのフィルタリング完了
	period_max = 15.5
	fw = open ( fname_split[0] + '-fourier.csv', 'w')
	for  ii in  range(1, int( period_max * 2 + 1) ):
		sum_sin = 0
		sum_cos = 0
		for elem in data:
			sum_cos += math.cos (2 * 3.14 * int(elem[0]) / (ii/2)) * float(elem[1])  
			sum_sin += math.sin (2 * 3.14 * int(elem[0]) / (ii/2)) * float(elem[1])  
		# 振幅amp（スペクトラム）
		amp = math.sqrt(  sum_cos * sum_cos + sum_sin * sum_sin  )
		# 位相tilt（但し、tan値）
		if sum_cos == 0:
			tilt = 0
		else:
			tilt = sum_sin / sum_cos
		# print ( ii/2, amp, tilt )
		fw.write( str(ii/2) + ', ' + str(amp)  + ', '+ str(tilt) + '\n' )
	fw.close()

	# delta1

	for ii in range( 0, len(data)-1 ):
		#print ( ii, data[ii] )
		zz += [float(data[ii][1])]
		delta1 += [float(data[ii][1]) - float(data[ii+1][1])]
	delta1 += [ 0.0 ]
	zz +=  [ float(data[len(data)-1][1]) ]
	#print ( 'delta1: ' )
	#print (delta1)

	#delta2

	for ii in range( 0, len(delta1)-1 ):
		print ( ii, delta1[ii] )
		delta2 += [float(delta1[ii]) - float(delta1[ii+1])]
	delta2 += [ 0.0 ]
	#print ( 'delta2: ' )
	#print (delta2)

	fw = open ( fname_split[0] + '-topological.csv', 'w')
	for ii in range (0, len(delta1)):
		fw.write( str(ii/2) + ', ' + str(delta1[ii])  + ', '+ str(delta2[ii]) + '\n' )

	fw.close()

	print ("zz ", zz)
	print ("delta1 ", delta1)

	#plt.plot(x, y)
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	#y = np.cos(x)
	#x = np.random.rand(50)
	#y = np.random.rand(50)
	#z = np.random.rand(50)
	#ax.scatter( x, y, z, color='blue')
	ax.plot( delta1, delta2, zz, color='blue')

	ax.set_title('Topological Space of Gains and losses on shares held (3d view)')
	ax.set_xlabel('dx/dt (Daily delta)')
	ax.set_ylabel('d2x/dt2 (Daily delta delta)')
	ax.set_zlabel('x')
	ax.legend()

	sxx = 0
	syy = 0
	szz = 0
	sxy = 0
	syz = 0
	szx = 0
	for ii in range(0, len(delta1)):
		sxx += delta1[ii] * delta1[ii]/ 10000.0
		syy += delta2[ii] * delta2[ii]/ 10000.0
		szz += zz[ii] * zz[ii] / 10000.0
		sxy += delta1[ii] * delta2[ii] / 10000.0
		syz += delta2[ii] * zz[ii] / 10000.0
		szx += zz[ii] * delta1[ii] / 10000.0

	mmtx = [
		[syy * syy + szz * szz, -1.0 * sxy, -1.0 * szx ],
		[ -1.0 * sxy, sxx * sxx + szz * szz, -1.0 * syz], 
		[ -1.0 * szx, -1.0 * syz, sxx * sxx + syy *syy ]]

	print ( "mmtx: ", mmtx)

	mmtx_eig = np.linalg.eig(mmtx)

	print("位相空間内のモーメントの固有値 {}\n".format(mmtx_eig[0]))

	# 固有ベクトルを表示
	print("位相空間内のモーメントの固有ベクトル\n{}\n".format(mmtx_eig[1]))

	xa = -1.0 * mmtx_eig[1][0]
	ya = -1.0 * mmtx_eig[1][1]
	za = -1.0 * mmtx_eig[1][2]

	print("xa, ya, za: ", xa, ya, za )

	print ("xa.ya: ", xa[0] * ya[0] + xa[1] * ya[1] + xa[2] * ya[2])
	print ("ya.za: ", ya[0] * za[0] + ya[1] * za[1] + ya[2] * za[2])
	print ("za.xa: ", za[0] * xa[0] + za[1] * xa[1] + za[2] * xa[2])


	# 表示がなんか、へん？　軸のスケールが違うのか？
	ax.quiver( 0,0,0, xa[0], xa[1], xa[2], color = "red")
	ax.quiver( 0,0,0, ya[0], ya[1], ya[2], color = "red")
	ax.quiver( 0,0,0, za[0], za[1], za[2], color = "red")

	for angle in range(0, 360):
	    ax.view_init(30, angle)
	    plt.draw()
	    plt.pause(.001)

	plt.savefig( fname_split[0] + "-3d-topological.png")   # プロットしたグラフをファイルsin.pngに保存する
	plt.show()
	

	plt.plot( zz, delta1 )
	plt.grid(True)

	plt.title("Topological Space of Gains and losses on shares held (side view 1)")
	plt.xlabel("x")
	plt.ylabel("dx/dt (Daily delta)")
	 
	plt.savefig( fname_split[0] + "-side1-topological.png")   # プロットしたグラフをファイルsin.pngに保存する
	plt.show()

	plt.plot( delta1, delta2 )
	plt.grid(True)

	plt.title("Topological Space of Gains and losses on shares held (top view)")
	plt.xlabel("dx/dt (Daily delta)")
	plt.ylabel("d2x/dt2 (Daily delta delta)")
 
	plt.savefig( fname_split[0] + "-top-topological.png")   # プロットしたグラフをファイルsin.pngに保存する
	plt.show()

	plt.plot( zz, delta2 )
	plt.grid(True)

	plt.title("Topological Space of Gains and losses on shares held (side view 2)")
	plt.xlabel("x")
	plt.ylabel("d2x/dt2 (Daily delta delta)")
	 
	plt.savefig( fname_split[0] + "-side2-topological.png")   # プロットしたグラフをファイルsin.pngに保存する
	plt.show()



# make graph


# マネックス証券の口座全体の資産推移の損益率の
# フーリエ展開プログラム (monex-fourier.py)
# made by digi-p@nifty.com,(C)2023, MIT License
#


 
x = np.arange(0, 17, 0.5)
#y = np.sin(x)
 
#plt.plot(x, y)

#y = np.cos(x)
#plt.plot(x, y)


 
#plt.savefig("sin.png")   # プロットしたグラフをファイルsin.pngに保存する
#plt.show()


#print(sys.argv, len(sys.argv) )

numcol = 2
fname = fname_split[0] + '-fourier.csv'
#fname = sys.argv[1]
data0 = []
data1 = []
data2 = []


print( 'Make graph:' , fname )

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




print( 'Done' )

