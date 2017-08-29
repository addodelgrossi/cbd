import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import glob
import ntpath

FILE_PATTERN = '/home/addo/dev/personal/cbd/images/transformed/*.png'
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 75

files = glob.glob(FILE_PATTERN)
titles = []
images = []

for f in files:
    filename = ntpath.basename(f)
    img = cv2.imread(f)
    titles.append(filename)
    images.append(img)    

for i in xrange(len(files)):
    # plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.subplot(2,3,i+1),plt.imshow(images[i])    
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

# plt.show()

# img = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
# plt.imshow(img)

# https://codewords.recurse.com/issues/six/image-processing-101
image = cv2.imread('/home/addo/dev/personal/cbd/images/transformed/4geq0.png')
# image[np.where((image==[0,0,0]).all(axis=2))] = [255,255,255]
image[np.where((image==[169,169,169]).all(axis=2))] = [0,0,0]
image[np.where((image==[211,211,211]).all(axis=2))] = [255,255,255]
image[np.where((image==[190,190,190]).all(axis=2))] = [255,255,255]
image[np.where((image==[198,198,198]).all(axis=2))] = [255,255,255]

cv2.imwrite('/home/addo/dev/personal/cbd/images/transformed/4geq0-2.png', image)