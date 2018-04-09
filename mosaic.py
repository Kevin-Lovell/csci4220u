#Kevin Lovell
#Image Mosaic
#April 09,2017
import argparse
import os
import numpy as np
import scipy as sp
from scipy import signal
import cv2

longest_dim = 4000
tile_dim = 40

#Find the average colour of an image given the entire image or a part of an image
#This function is used to find the average colour of every photo and the average colour of every tile
def findavg(img):
	avgcolour = np.average(img,axis=0)
	avgcolour = np.average(avgcolour, axis=0)
	avgcolour = int(avgcolour[0]),int(avgcolour[1]),int(avgcolour[2])
	return avgcolour


def mosaic(imgfile):
	#Reading in images
	img = cv2.imread(imgfile)
	img1 = img
	img1_height, img1_width, _= sp.ndimage.imread(imgfile).shape

	#Preserves the dimensions of the image while increasing image size
	if (img1_width > img1_height):
		img_width = longest_dim
		img_height = (img1_height * (img_width/img1_width))
		img_height = img_height - (img_height%tile_dim)
	elif(img1_height > img1_width):
		img_height = longest_dim
		img_width = (img1_width * (img_height/img1_height))
		img_width = img_width - (img_width%tile_dim)
	else:
		img_height, img_width = longest_dim

	img1 = cv2.resize(img1,(img_width,img_height))

	tile_colour = {}
	image_info = {}
	tile_dir = ".\img_library"
	#Reads through every file in the image directory and obtains the average colour in every image and the image properties
	for file in os.listdir(tile_dir):
		path = os.path.join(tile_dir,file)
		image_info[file]  = cv2.imread(path)
		avg_colour_tile = findavg(image_info[file])
		tile_colour[file] = avg_colour_tile


	for i in range (0, img_height, tile_dim):
		for j in range (0, img_width, tile_dim):
			avg = findavg(img1[i:i+tile_dim,j:j+tile_dim]) #avg colour in img block
			colour_dist_list = {} #hash of filename to colour difference
	 		for k in tile_colour:
	 			tavg = tile_colour[k] # tavg is the average colour of a lib image
	 			colour_dist = abs(avg[0]-tavg[0]) + abs(avg[1]-tavg[1]) + abs(avg[2]-tavg[2]) # finds difference between colours
	 			colour_dist_list[colour_dist] = k # records colour distance of every image

	 		# finds the best image match be finding the image with smallest average colour difference
			closest_match_dist = sorted(colour_dist_list)[0] 
	 		closest_match_file = colour_dist_list[closest_match_dist]

	 		
	 		tile_block = image_info[closest_match_file]
	 		tile_block = cv2.resize(tile_block,(tile_dim,tile_dim))
	 		#Replaces image block with new image from library
	 		img1[i:i+tile_dim,j:j+tile_dim] = tile_block

	cv2.imwrite('mosaic.jpg', img1)
	img1 = cv2.resize(img1,(img1_height, img1_height))
	while(True):
		cv2.namedWindow("Mosaic", cv2.WINDOW_NORMAL) 

		window_height = 600.0
		window_width = img1_width * (window_height/img1_height)

		cv2.resizeWindow('Mosaic', int(window_width),int(window_height))
	
		cv2.imshow('Mosaic',img)
		cv2.imshow('Mosaic',img1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	#img1.release()
	cv2.destroyAllWindows()
	
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Final Project')
    parser.add_argument('imgfile', help='Output file')
    args = parser.parse_args()

    mosaic(args.imgfile)
    