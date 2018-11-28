from PIL import Image
import sys
import math
import numpy

# --------- Define helper functions ---------

# On converting between hex and rgb
# http://www.psychocodes.in/rgb-to-hex-conversion-and-hex-to-rgb-conversion-in-python.html

# Find unique elements
# https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.unique.html

def rgbToHex(r, g, b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

# Precondition: len(arr) == 3
def rgbArrayToHex(arr):
	hex = "#{:02x}{:02x}{:02x}".format(arr[0], arr[1], arr[2])
	return hex

def mapColors(colormap, arr):
	return list( map(lambda x: colormap.index(x), arr) )


def sampleTheImage(img, smplsize):
	# If there is less than smplsize of image left that part is not sampled
	width, height = img.size

	pixelsX = math.floor(width / smplsize)
	pixelsY = math.floor(height / smplsize)
	
	# Get pixel values as a 2d array
	pix = img.load()

	# Initilize a 0-array for the resulting pixelized image
	pixelized = [[0]* pixelsX for x in range(pixelsY)]

	# Iterate over the pixel values and take sample from each 'cell'
	# (size of each cell is smplsize)
	for y in range(0, pixelsY):
		for x in range(0, pixelsX):
			yCoord = math.floor(smplsize/2) + y * smplsize
			xCoord = math.floor(smplsize/2) + x * smplsize
			pixelized[y][x] = rgbArrayToHex( pix[xCoord, yCoord] )

	return pixelized

def colorsToInts(colors, pixelized):
	for row in range( len(pixelized) ):
		pixelized[row] = mapColors(colors, pixelized[row])
	return pixelized

# -------------------------------------------

# Get path to the image file to be pixelized
print('Enter the filename / path (including extension):')
filename = input()
print('You entered the filename / path: ' + filename)

# Get sample cell size (as pixels)
print('Enter the sample cell size (integer):')
smplsizeInput = input()

try:
   smplsize = int(smplsizeInput)
   print('You entered the sample size: ', smplsize)
	# TODO Input validation!! (Check that the sample size is not two large for the image)

except ValueError:
   print("You entered a value that was not a number. The program will exit now.")
   sys.exit()



# Try to open the image 
try:
	img = Image.open(filename)
except IOError:
	print('Error occurred trying to open the image. The program will exit.')
	sys.exit()

# Sample the image
pixelized = sampleTheImage(img, smplsize)

# Get the unique color values
colors = numpy.unique(pixelized).tolist()
print(colors)

# Map the colors to simply numbers
pixelized = colorsToInts(colors, pixelized)

print(pixelized)

# Write the image and the colors to a file
file = open(filename + ".txt", "w")
file.write("\n".join(str(row) for row in pixelized))





