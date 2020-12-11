import urllib3
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pn
from PIL import Image, ImageDraw, ImageFont


import settings

IMG_SIZE = 512

Point = (int, int)


def get_structure(path) -> np.array:

    img = cv2.imread(path, 0)

    # image to binary format
    _, thres = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV)

    # get only vertical lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,25))
    vertical = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel)
    
    # recovery vertical lines
    kernel = np.ones((50,1),np.uint8)
    vertical = cv2.dilate(vertical,kernel,iterations = 1)

    # get only horisontal lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(110,1))
    horisontal = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel)

    # recovery horisontal lines
    kernel = np.ones((2,50),np.uint8)
    horisontal = cv2.dilate(horisontal,kernel,iterations = 1)

    # merge horicontal and vertical lines 
    structure = cv2.add(horisontal,vertical)

    return structure


# find orientir line
def find_column(orinentir, structure) -> Point:
    row = structure[orinentir[0], :orinentir[1]]
    left = 0
    lenght = len(row)
    while lenght:
        lenght -= 1
        point = row[lenght]
        if point > 0:
            left = lenght
            break
            
    return (orinentir[0], left)


def find_n_row(column_point, structure, n) -> Point:
    offset = 20
    column = structure[column_point[0]:-1,column_point[1]+2:-1][:,offset]
    
    row_position = 0
    line_finded_count = 0
    index = 0
    while True:
        point = column[index]
        if point == 255 and index-1 > 0 and column[index-1] == 0:
            line_finded_count += 1

        if line_finded_count == n:
            row_position = index
            break
        
        index +=1

        if index == len(column):
            break

    return (column_point[1],row_position + column_point[0])

def draw_line_to_row(path):
    with Image.open(path) as doc_image:
        draw = ImageDraw.Draw(doc_image)

        draw.line((0,0) + row_point, fill=128, width=10)
        doc_image.save("test.png", "PNG")

    with Image.open('structure.png') as doc_image:
        draw = ImageDraw.Draw(doc_image)

        draw.line((0,0) + row_point, fill=255, width=10)
        draw.line((0,0, 956,507), fill=255, width=10)

        doc_image.save("structure.png", "PNG")


def load_image_from_setting(save_path):
    http = urllib3.PoolManager()
    r = http.request('GET', settings.image_href)
    f = open(save_path, 'wb')
    print(f'Load image from { settings.image_href} type {settings.type}')
    f.write(r.data)
    f.close()


def load_ocr():
    http = urllib3.PoolManager()
    r = http.request('GET', settings.ocr_href)
    ocrData = r.data.decode('utf-8')
    f = open('ocrData.csv', 'w')
    f.write(ocrData)
    f.close()

load_image_from_setting(settings.image_name)
structure = get_structure(settings.image_name)

cv2.imwrite('structure.png', structure)




load_ocr()
ocr = pn.read_csv('ocrData.csv')

type = settings.type
if type == 'ТТН':
    row_count = 4
    orinentir_name = 'прибытия'
else:
    row_count = 3
    orinentir_name = 'Сдача'

orinentir_ocr = ocr.query(f"text == '{orinentir_name}'")
left = orinentir_ocr.iloc[0]['left']
top = orinentir_ocr.iloc[0]['top']
orinentir = (top, left)

column_point = find_column(orinentir, structure)
row_point = find_n_row(column_point, structure, row_count)
print('Success search point %s', row_point)
draw_line_to_row(settings.image_name)