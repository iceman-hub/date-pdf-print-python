import numpy as np
import pandas as pn
import cv2
import urllib3
import json
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
import sys
import config

np.set_printoptions(threshold=sys.maxsize)
IMG_SIZE = 128
LINE_COUNT = 3

def get_structure(img, size=IMG_SIZE) -> np.array:
    _, thresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    k_size = int(max(img.shape) // 196)
    h_kernel = np.ones((1, k_size), np.uint8)
    v_kernel = np.ones((k_size, 1), np.uint8)
    h_erosion = cv2.erode(thresh, h_kernel, iterations=5)
    v_erosion = cv2.erode(thresh, v_kernel, iterations=5)
    erosion = cv2.add(h_erosion, v_erosion)
    dil_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    dilation = cv2.dilate(erosion, dil_kernel, iterations=3)
    resize = cv2.resize(dilation, (size, size),
                        interpolation=cv2.INTER_NEAREST)
    k_size = int(k_size // 2)
    h_kernel = np.ones((1, k_size), np.uint8)
    v_kernel = np.ones((k_size, 1), np.uint8)
    h_erosion = cv2.erode(resize, h_kernel, iterations=1)
    v_erosion = cv2.erode(resize, v_kernel, iterations=1)
    erosion = cv2.add(h_erosion, v_erosion)
    result = erosion
    plt.imshow(result, cmap = 'gray')
    plt.xticks([]), plt.yticks([])
    return result

def get_line_position(structure, crop_y):
    line_y_position = 0
    line_finded_count = 0
    img_array = structure[crop_y:-1, 0:-1]

    np.savetxt("imageArray.csv", img_array, delimiter=",",fmt="%s")
    cv2.imwrite('string_structure.png', structure)
    for (indx, line) in enumerate(img_array):
        print(indx, line.sum())
        print(line)
        if line.sum() > 50:
            line_finded_count += 1

        if(line_finded_count == 3):
            print(indx)
            line_y_position = indx
            break    

    line_y_position += crop_y        
    return line_y_position

def get_data_insert_point(img, basis_point):
    structure = get_structure(img)
    crop_y = int(IMG_SIZE / img.shape[0] * basis_point[0])
    point_y = get_line_position(structure, crop_y)
    structure_to_img = int(img.shape[0] / IMG_SIZE  * point_y)
    return [basis_point[0], structure_to_img]

def load_image():
    http = urllib3.PoolManager()
    r = http.request('GET', config.image_href)
    f = open(config.image_name, 'wb')
    print(config.image_href)
    f.write(r.data)
    f.close()
    return True