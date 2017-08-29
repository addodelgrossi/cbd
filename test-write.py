import cv2
import numpy as np


# http://www.meccanismocomplesso.org/en/english-opencv-python-drawing-shapes-text-on-images/
# template = np.zeros((40,40,3), np.uint8)
# template.fill(0)
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(template,'H',(10,30), font, 1,(255,255,255),2)


# cv2.imshow("img",img)
# cv2.waitKey(0)

image = cv2.imread('/home/addo/dev/personal/cbd/images/transformed/Hkc3n.png')
# image[np.where((image==[0,0,0]).all(axis=2))] = [255,255,255]
image[np.where((image==[169,169,169]).all(axis=2))] = [0,0,0]
image[np.where((image==[211,211,211]).all(axis=2))] = [255,255,255]
image[np.where((image==[190,190,190]).all(axis=2))] = [255,255,255]
image[np.where((image==[198,198,198]).all(axis=2))] = [255,255,255]
# img = cv2.imread('out.png')
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template = cv2.imread('H.png', 0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.2
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_gray, pt, (pt[0]+w, pt[1]+h), (0, 255, 255), 2)

cv2.imshow('Image', img_gray)
cv2.waitKey(0)



# img = np.zeros((200,200,3), np.uint8)
# img.fill(0)
# # img[:] = [255,0,97]
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,'H o j e h',(10,30), font, 1,(255,255,255),2)
# cv2.imshow("img",img)
# cv2.imwrite("out.png", img)
# cv2.waitKey(0)