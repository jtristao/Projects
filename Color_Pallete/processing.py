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
def prepare_image(file_name):
	print("Loading image ....")
	image = cv2.imread(file_name, cv2.IMREAD_COLOR)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	image = rgb_to_dec(image)

	data = np.asarray(image)
	
	return data.ravel()

def euclidean_distance(a, b):
	return abs(a - b)

def k_means(array, n_centers, treshold):
	if array.size == 0 or array is None:
		print("Invalid iput")
		exit()

	if n_centers < 1:
		print("Invalid number of clusters")
		exit()

	# Choses n_centers random points
	centers = rd.choices(array, k=n_centers)
	centers = np.asarray(centers)

	change_ratio = 3.14
	while change_ratio > threshold:
		# Centers copy
		old_centers = centers.copy()

		# Calculates the distances from the point to the centers
		print("Calculating distances ....")
		distances = np.zeros((len(array), n_centers))
		for i in range(len(array)):
			distances[i] = abs(array[i] - centers)
				# print(i, j, array[i], centers[j], distances[i][j])

		# Find to which centers the points are closer
		close = np.zeros(len(array))
		print("Finding closest points ....")
		for i in range(array.size):
			close[i] = np.argmin(distances[i])

		# Update the centers
		print("Updating centers ....")
		for i in range(n_centers):
			closest = np.where(close == i)
			if len(closest[0]) > 0:
				# Average
				# centers[i] = sum(array[closest])/len(closest[0])
				
				# Median
				centers[i] = stat.median(array[closest])
				# print(array[closest], stat.median(array[closest]))

		# Updates the change_ratio
		print("Calculating change ratio ...")
		change_ratio = np.linalg.norm(old_centers - centers)
		
		# print(centers)
		print("Change = ", change_ratio)
		print("----------------------------------------------------------------")

	return centers

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

	# Adds the color pallete rectangles
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

def redraw(centers, image_name):
	# Open the original image
	original_array = prepare_image(image_name)
	original_image = Image.open(image_name)
	original_size = original_image.size

	# Creates the new image
	new_image = Image.new("RGB", original_size, (255, 255, 255))

	# Find the equivalent colors
	aux = np.zeros((original_size))
	for i in range(original_size[0]):
		for j in range(original_size[1]):
			aux[i,j] = centers[np.argmin(abs(original_array[i] - centers))]

	colors = hex_to_rgb(aux)

	img = Image.fromarray(aux, 'RGB')
	new_image.paste(img, (pos, old_size[1]+2*board_size))
	new_image.paste()


			

image_name = "cut.png"
image = prepare_image(image_name)

# Transformar centers em array de inteiros
n_centers = 10
threshold = 0.000001
centers = k_means(image, n_centers, threshold)
colors = hex_to_rgb(centers)
redraw(centers, image_name)
# new_image = draw_image(colors, image_name)

# new_image.save("result.png")
# new_image.show()	
