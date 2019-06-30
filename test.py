import numpy as np
import cv2
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
import random

def thin_plate_spline(img, init_points):
	tps = cv2.createThinPlateSplineShapeTransformer()

	sshape = init_points.astype(np.float32)
	l = sshape.shape[0]
	print(l)

	delta = np.empty((0,2))
	for n in range(l):
		randx = random.randint(-50,50)*1
		randy = random.randint(-100, 100)*1
		delta = np.concatenate([delta, np.array([[randx, randy]])])

	# delta = np.array([[-10,100],[10,100],[-10,-100],[10,-100]],np.float32)
	tshape = sshape + delta
	sshape = sshape.reshape(1,-1,2)
	tshape = tshape.reshape(1,-1,2)

	matches = list()
	for n in range(l):
		matches.append(cv2.DMatch(n,n,0))

	tps.estimateTransformation(tshape,sshape,matches)

	out_img = tps.warpImage(img)

	return out_img


if __name__ == "__main__":
	root = Tk()
	root.withdraw()
	init_dir = os.path.abspath(os.path.dirname(__file__))
	file = filedialog.askopenfilenames(filetypes=[('jpgファイル','*.jpg *.jpeg')], initialdir = init_dir)
	
	img_name = file[0]
	img = cv2.imread(img_name)
	img = img[:,:,::-1]
	plt.imshow(img)
	init_points = plt.ginput(n=-1, mouse_add=1, mouse_pop=3, mouse_stop=2)
	plt.show()
	# n=-1でインプットが終わるまで座標を取得
	# mouse_addで座標を取得（左クリック）
	# mouse_popでUndo（右クリック）
	# mouse_stopでインプットを終了する（ミドルクリック）
	init_points = np.array(init_points)

	out_img = thin_plate_spline(img, init_points)
	
	plt.imshow(out_img)
	plt.show()

	out_img = out_img[:,:,::-1]
	cv2.imwrite('output.jpg', out_img)

	print('end')

