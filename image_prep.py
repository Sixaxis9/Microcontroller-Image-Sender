import numpy as np
from matplotlib import pyplot as plt
from imageio import imread # Need 'Imageio' 'Pillow' packages
import cv2
from math import floor, ceil

def prep_img(img_name, x_size=32, y_size=32, *img_position):
    image_read = imread(img_name)[:,:,0]*0.2989 + imread(img_name)[:,:,1]*0.5870 + imread(img_name)[:,:,2]*0.1140
    image_test = np.asarray(image_read)

    if x_size != -1 and y_size != -1:
        if len(img_position) > 0:
            # Cutting the image to match the content
            x2 = int(img_position[0][2]) 
            x1 = int(img_position[0][0])
            y2 = int(img_position[0][3]) 
            y1 = int(img_position[0][1])
            size = max(x2-x1, y2-y1)
            
            # Padding to have square images
            padded = np.pad(image_test[x1:x2+1, y1:y2+1], ((floor((size-x2+x1)/2), ceil((size-x2+x1)/2)), (floor((size-y2+y1)/2), ceil((size-y2+y1)/2))))
            reshaped = cv2.resize(padded, (x_size, y_size), interpolation = cv2.INTER_AREA)
            return reshaped
        else:
            reshaped = cv2.resize(image_test, (x_size, y_size), interpolation = cv2.INTER_AREA)
            return reshaped

    return image_test
    
