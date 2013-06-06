from pylab import *

RED_COEFF = .2989
GREEN_COEFF = .5870
BLUE_COEFF = .1140

def rgb2gray (rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1] , rgb[:,:,2]
    gray = RED_COEFF * r + GREEN_COEFF * g + BLUE_COEFF * b
    return gray
