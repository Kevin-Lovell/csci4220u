# Image Mosaic

For this project I decided to creat an Image Mosaic builder that would allow you to choose an image and have a program convert it
into an Mosaic of other images. 

This program takes an image, blows it up to a very large size with a width of 8000px and separates the image into fixed tile sizes. 

From there it calculates the average colour of each square and compares that colour with the average colour of every image in a library of photos. 

The images with the closest colour match replace each individual block with an image of 80px by 80px to produce a mosaic across the entire image.

In order to obtain the best results, a library with at least several hundred images is encouraged.

# Author
Kevin lovell

To run this program insert your library of images into the .\img_library folder then enter into the command line

mosaic.py --path-to-image-file
