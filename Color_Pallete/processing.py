import random as rd
import numpy as np
import statistics as stat
import cv2
import matplotlib.pyplot as plt
import math

# Converts rgb image to decimal values
def rgb_to_dec(image):
	aux = np.zeros((len(image), len(image[0])))
	for i in range(len(image)):
		for j in range(len(image[0])):
			aux[i][j] = (image[i][j][0] << 16) + (image[i][j][1] << 8) + (image[i][j][2])

	return aux 

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

def euclidean_distance(a, b):
	return abs(a - b)

def k_means(array, n_centers):
	if array.size == 0 or array is None:
		print("Invalid iput")
		exit()

	if n_centers < 1:
		print("Invalid number of clusters")
		exit()

	# Choses n_centers random points
	centers = np.zeros(n_centers)
	for i in range(n_centers):
		centers[i] = rd.choice(array)


	change_ratio = 100000
	while change_ratio > 10000:
		# Centers copy
		old_centers = centers.copy()

		# Calculates the distances from the point to the centers
		print("Calculating distances ....")
		distances = np.zeros((len(array), n_centers))
		for i in range(len(array)):
			for j in range(n_centers):
				distances[i][j] = euclidean_distance(array[i], centers[j])
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
		print("Calculating ratio ...")
		change_ratio = math.sqrt(sum((centers - old_centers)**2))
		
		print(centers)
		print(change_ratio)
		print("----------------------------------------------------------------")

	return centers


image = load_image("cut.png")

# Transformar centers em array de inteiros
# centers = k_means(image, 10)

colors = np.zeros((10, 3), np.int32)
# centers = np.array([7432289, 15987960, 9406857, 2636547, 12566455, 11569013, 10526102, 5907983, 8548190, 4541464])

print(centers)
for i in range(10):
	colors[i][0] = centers[i]>>16
	colors[i][1] = (centers[i] - (colors[i][0]<<16))>>8
	colors[i][2] = centers[i] - (colors[i][0]<<16) - (colors[i][1]<<8)

print(colors)
