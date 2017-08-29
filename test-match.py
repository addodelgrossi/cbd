import cv2
import numpy as np
from matplotlib import pyplot as plt

# http://www.meccanismocomplesso.org/en/english-opencv-python-drawing-shapes-text-on-images/
# Create a black image
# img = np.zeros((512,512,3), np.uint8)
# # img.fill(0)
# img[:] = 0
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,'Hello World!',(10,500), font, 1,(0,0,0),2)
# cv2.imshow("img",img)
# cv2.waitKey(0)


# https://pythonprogramming.net/drawing-writing-python-opencv-tutorial/
# https://books.google.com/books?id=LPm3DQAAQBAJ&pg=PA166&lpg=PA166&dq=opencv3+font+SansSerif&source=bl&ots=2vHlZgagza&sig=WozHvIQooJ3YY1Ov_o1VwBAdxbc&hl=pt-BR&sa=X&ved=0ahUKEwi_6c3OjfvVAhULySYKHR9TAQIQ6AEIMzAB#v=onepage&q=opencv3%20font%20SansSerif&f=false
# https://github.com/cinder/Cinder-OpenCV3/blob/master/include/opencv2/core.hpp


# img = cv2.imread('images/Hkc3n.png')
img = cv2.imread('images/4geq0.png')
img = img[10: 80, 55:250]
img[np.where((img==[169,169,169]).all(axis=2))] = [0,0,0]
img[np.where((img==[211,211,211]).all(axis=2))] = [255,255,255]
img[np.where((img==[190,190,190]).all(axis=2))] = [255,255,255]
img[np.where((img==[198,198,198]).all(axis=2))] = [255,255,255]
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_gray = cv2.resize(img_gray, None, fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
# cv2.imwrite('aaa.png', img_gray)
# cv2.imshow('Image', res)
# cv2.waitKey(0)

kernel = np.ones((4,4),np.uint8)
closing = cv2.morphologyEx(img_gray, cv2.MORPH_CLOSE, kernel)

# closing[np.where((closing==[198,198,198]).all(axis=2))] = [255,255,255]
closing[np.where(closing != [255])] = [0]


# closing = cv2.resize(closing, None, fx=1.5, fy=1.5, interpolation = cv2.INTER_CUBIC)


cv2.imwrite('extract-g.png', closing)

# /home/addo/Downloads/chars/_H.jpg
# template = cv2.imread('/home/addo/Desktop/_H.jpg', 0)
# w, h = template.shape[::-1]

template = np.zeros((30,30,3), np.uint8)
template[:] = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(template,'g',(0,14), font, 1.2,(0,0,0), 2)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image', template)
# cv2.waitKey(0)

# w, h, _ = template.shape
w, h = template.shape[::-1]

res = cv2.matchTemplate(closing, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.40
loc = np.where(res >= threshold)
# print res
print loc
for pt in zip(*loc[::-1]):
    cv2.rectangle(closing, pt, (pt[0]+w, pt[1]+h), (0, 255, 255), 2)

# cv2.imshow('Image', closing)
# cv2.waitKey(0)
# http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
# http://www.learnopencv.com/homography-examples-using-opencv-python-c/ <http://www.learnopencv.com/homography-examples-using-opencv-python-c/>  

# http://docs.opencv.org/2.4/doc/tutorials/features2d/feature_homography/feature_homography.html <http://docs.opencv.org/2.4/doc/tutorials/features2d/feature_homography/feature_homography.html>  


plt.subplot(121),plt.imshow(closing)
plt.subplot(122),plt.imshow(template)
plt.show()