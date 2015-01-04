# -*- coding: utf-8 -*-
"""
Created on Sun Jan 04 12:34:35 2015

@author: Quan
"""
#------------------------------------------------------------------------------
import cv2
import numpy

from cv2 import *
from numpy import *
#------------------------------------------------------------------------------
def im2cols(image, w):
    print "Extracting image patches..."    
    
    r = floor(w/2)
    n = w*w
    padded  = pad(image, ((r,r),(r,r)), 'reflect');
    
    index   = 0;  
    dimy, dimx = image.shape
    print dimy, dimx
    C = zeros((n, dimy*dimx), 'float64') # z, y, x order
    for y in range(0, dimy):
        for x in range(0, dimx):
            roi   = padded[y:y+w, x:x+w];
            patch = reshape(roi, (n))           # Reshape to 1D column vector
            C[:,index] = patch            
            index = index+1
    print C.shape
    return C
    
#------------------------------------------------------------------------------
def cols2im(C, shape):
    print "Aggregating image patches..."
    
    step = 1
    n, s = C.shape
    w    = sqrt(n)
    I    = zeros(shape, 'float64')
    W    = zeros(shape, 'float64')
    
    y = 0
    x = 0
    dimy, dimx = shape
    for index in range(s):
        patch = reshape(C[:, index], (w, w))
        ### Caution: transpose
        I[x:x+w,y:y+w] = I[x:x+w,y:y+w] + patch
        W[x:x+w,y:y+w] = W[x:x+w,y:y+w] + 1
        if(y < (dimy - w)):
            y = y + step; 
        else:
            y = 0;
            x = x + step; 
    I = divide(I, W)      
    I = I.astype('uint8')
    return I
    
#------------------------------------------------------------------------------
#class DictionaryLearningPlan:
#    w = 9       # Width of image patches
#    p = 256     # Number of atoms
#    s = 10000   # Number of training samples
    
    
#------------------------------------------------------------------------------
#class DictionaryLearning:
    # Class members
    
    # Class methods

#------------------------------------------------------------------------------
if  __name__ == "__main__":
    image = imread("lena.png", IMREAD_GRAYSCALE)
    imshow("Original", image)
    dimy, dimx = image.shape
    #
    w = 9
    r = floor(w/2)
    
    ## Extract the patches from image to column vectors
    C = im2cols(image, w)
    
    ## Aggregate the patches, need to truncate
    I = cols2im(C, add(image.shape, (2*r, 2*r)))
    I = I[r:-r, r:-r]
    imshow("Aggregate", I)    
    #print I
