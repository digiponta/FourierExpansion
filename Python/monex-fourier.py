# マネックス証券の口座全体の資産推移の損益率の
# フーリエ展開プログラム (monex-fourier.py)
# made by digi-p@nifty.com,(C)2023, MIT License
#
import csv
from datetime import datetime
import math
import sys

org = datetime (2023, 3, 1 ); # 資金運用開始年月日

# マネックス証券の口座全体の資産推移からダウンロードしたcsvファイル名
# スクリプト引数で、ファイル名を渡す場合
fname = sys.argv[1]
# ハードコーディグで、ファイル名を渡す場合
#fname = 'view_20230513_064542.csv'
print( fname )

fname_split = fname.split('.')

with open( fname, 'r', encoding="utf-8") as fr:
	reader = csv.reader(fr)
	top = True
	data = []
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

