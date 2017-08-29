import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('images/Hkc3n.png')
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img[np.where((img==[169,169,169]).all(axis=2))] = [0,0,0]
img[np.where((img==[211,211,211]).all(axis=2))] = [255,255,255]
img[np.where((img==[190,190,190]).all(axis=2))] = [255,255,255]
img[np.where((img==[198,198,198]).all(axis=2))] = [255,255,255]

dst = cv2.fastNlMeansDenoising(img,None,1,21,7)
# dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)


# template = np.zeros((25,25,3), np.uint8)
# template[:] = (255, 255, 255)
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(template,'K',(0,25), font, 1,(0,0,0),2)
# template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Image', template)
# cv2.waitKey(0)

# # w, h, _ = template.shape
# w, h = template.shape[::-1]

# res = cv2.matchTemplate(dst, template, cv2.TM_CCOEFF_NORMED)
# threshold = 0.55
# loc = np.where(res >= threshold)
# # print res
# print loc
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(dst, pt, (pt[0]+w, pt[1]+h), (0, 255, 255), 2)


plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(dst)
plt.show()