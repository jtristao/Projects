from sklearn.cluster import KMeans
import random as rd
import numpy as np
import statistics as stat
import cv2
import matplotlib.pyplot as plt
import math
from PIL import Image

# Converts rgb image to decimal values
def rgb_to_dec(image):
	aux = np.zeros((len(image), len(image[0])))
	for i in range(len(image)):
		for j in range(len(image[0])):
			aux[i][j] = (image[i][j][0] << 16) + (image[i][j][1] << 8) + (image[i][j][2])

	return aux 

def hex_to_rgb(centers):
	centers = centers.astype(np.int32)
	colors = np.zeros((len(centers), 3), np.int32)
	for i in range(len(centers)):
		colors[i][0] = centers[i]>>16
		colors[i][1] = (centers[i] - (colors[i][0]<<16))>>8
		colors[i][2] = centers[i] - (colors[i][0]<<16) - (colors[i][1]<<8)

	return colors

# Reads a image and returns a numpy array with one line
def load_image(file_name):
	image = cv2.imread(file_name, cv2.IMREAD_COLOR)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# cv2.imshow("image", image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	image = rgb_to_dec(image)

	data = np.asarray(image)
	
	return data.ravel()

def draw_image(colors, image_name):
	board_size = 5
	rec_heigth = 20

	# Open the old file
	old = Image.open(image_name)
	old_size = old.size

	# Creates the new image and paste the old image
	new_size = (math.ceil(old.size[0]+2*board_size), math.ceil(old.size[1]+rec_heigth+3*board_size))
	new_image = Image.new("RGB", new_size, (255, 255, 255))
	new_image.paste(old, (board_size, board_size))

	n_colors = len(colors)
	pos = board_size
	rec_width = (old.size[0]-((n_colors-1)*5))//n_colors
	advance = (old.size[0]-((n_colors-1)*5))/n_colors
	for i in colors:
		rec = np.full((rec_heigth, rec_width, 3), i, dtype=np.uint8)
		img = Image.fromarray(rec, 'RGB')
		new_image.paste(img, (pos, old_size[1]+2*board_size))
		pos = round(pos+advance+board_size)

	return new_image

image_name = "cut.png"
image = load_image(image_name)

# Transformar centers em array de inteiros
image = image.reshape(-1, 1)
# Number of clusters
kmeans = KMeans(n_clusters=10)
# Fitting the input data
kmeans = kmeans.fit(image)
# Getting the cluster labels
labels = kmeans.predict(image)
# Centroid values
centroids = kmeans.cluster_centers_

colors = hex_to_rgb(centroids)
new_image = draw_image(colors, image_name)

new_image.save("result.png")
new_image.show()
