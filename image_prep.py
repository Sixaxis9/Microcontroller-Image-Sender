import numpy as np
from matplotlib import pyplot as plt
from imageio import imread # Need 'Imageio' 'Pillow' packages
import cv2
from math import floor, ceil

def prep_img(img_name, x_size=32, y_size=32, img_position = [-1]):
    # Adapting test data to network input dimension from data dataset
    x_size = 32
    y_size = 32

    image_read = imread(img_name)[:,:,0]*0.2989 + imread(img_name)[:,:,1]*0.5870 + imread(img_name)[:,:,2]*0.1140
    
    image_test = np.asarray(image_read)
    if img_position[0] is not -1:
        # Cutting the image to match the content
        x2 = int(img_position[2]) 
        x1 = int(img_position[0])
        y2 = int(img_position[3]) 
        y1 = int(img_position[1])
        size = max(x2-x1, y2-y1)
        
        # Padding to have square images
        padded = np.pad(image_test[x1:x2+1, y1:y2+1], ((floor((size-x2+x1)/2), ceil((size-x2+x1)/2)), (floor((size-y2+y1)/2), ceil((size-y2+y1)/2))))
        reshaped = cv2.resize(padded, (x_size, y_size), interpolation = cv2.INTER_AREA)
    else:
        reshaped = cv2.resize(image_test, (x_size, y_size), interpolation = cv2.INTER_AREA)
    
    # Reshaping the image to match the selected dimension
    
    #plt.imshow(reshaped)
    #plt.title(np.argmax(Y_test[first_to_test]))
    #plt.show()

    return reshaped
    
