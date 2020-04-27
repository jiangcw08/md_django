# 图像处理
import cv2
#读图
img = cv2.imread('./login.png',cv2.IMREAD_GRAYSCALE)
#写图
cv2.imwrite('./code1.png',img)

