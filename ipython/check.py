# Загрузка окра, запускать при смене документа.  
import numpy as np
import pandas as pn
import cv2
import urllib3
import json
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt

import ipython.config as config
from ipython.loadImage import *

http = urllib3.PoolManager()
r = http.request('GET', config.ocr_href)
ocrData = r.data.decode('utf-8')
f = open('ocrData.csv', 'w')
f.write(ocrData)
f.close()

ocr = pn.read_csv('ocrData.csv')

# Точка начала базиса.  

one_point = ocr.query("text == 'Указания'")

# Вспомогательные вектора (в принципе достаточно одного, для масштабирования использую А, второй для быстрой замены при тестах).  

a_point = ocr.query("text == 'Прием'")
b_point = ocr.query("text == 'Сдача'")
load_image()


with Image.open("test.png").convert("RGBA") as doc_image:

    draw = ImageDraw.Draw(doc_image)
    basis = config.basis
    x = b_point.iloc[0]['left']
    y = b_point.iloc[0]['top']
    img = cv2.imread("test.png",0)
    point = get_data_insert_point(img, [x, y])
    print(point)

    draw.line([0,0] + ( x * 9 // 16,
        y * 19 // 32), fill=(255, 255, 0), width=10)


    doc_image.save("test.png", "PNG")