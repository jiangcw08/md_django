# # 图像处理
import cv2
# #读图
# img = cv2.imread('./login.png',cv2.IMREAD_GRAYSCALE)
# #写图
# cv2.imwrite('./code1.png',img)



# ========================= 添加水印 ==========================

from PIL import Image,ImageDraw,ImageFont
#读图
img = Image.open('./jay1.png')
# PNG (1066, 713) RGB
print(img.format,img.size,img.mode)
#生成画笔
draw = ImageDraw.Draw(img)
#绘制

# 修改字体为simsun.ttc
font = ImageFont.truetype("simsun.ttc", 40, encoding="unic")
draw.text((950,650),'没多','yellow',font=font)

img.show()


# =============================== END ===========================


# ============================ 压缩图片 ==========================

#读图
img = cv2.imread('./jay1.png')

#压缩 压缩等级0-9 压缩等级越低越清y晰
cv2.imwrite('./jay2.png',img,[cv2.IMWRITE_PNG_COMPRESSION,9])

#jpg
cv2.imwrite('./jay1.jpg',img,[cv2.IMWRITE_JPEG_CHROMA_QUALITY,10])

# ============================== END ================================