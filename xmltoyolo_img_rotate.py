from xml.dom import minidom
import os
import cv2
import numpy as np
from scipy import ndimage

current_path = os.path.abspath(os.curdir)
print("Current path is {}".format(current_path))
ORIGIN_FORMAT_PATH = current_path + '/images/org_image'
RESULT_FORMAT_PATH = current_path + '/images/res_image'
XML_FORMAT_PATH = current_path + '/images/annotation'


file_count = 0
classes={}
classes["horse"] = 0
classes["person"] = 1
classes["dog"] = 2
classes["bird"] = 3

def getYoloCordinates(size, box):
    width_ratio = 1.0/size[0]
    height_ratio = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x * width_ratio
    w = w * width_ratio
    y = y * height_ratio
    h = h * height_ratio
    return (x,y,w,h)

def rotate_chg(img, angle):
        dst = ndimage.rotate(img, angle)
        return dst

def rotate_test(x, y, w, h, nw, nh):
    cos, sin = np.cos(np.pi * (ANGLE/180)), np.sin(np.pi * (ANGLE/180))

    print(x, y, w, h, nw, nh)

    ww, hh = int((w - nw)/2), int((h - nh)/2)
    print(ww, hh)

    cx, cy = int(x * w), int(y * h)
    print(cx, cy)

    # cx, cy = cx - (w/2), (h/2) - cy
    # print(cx, cy)

    xx = (cx * cos) - (cy * sin)
    yy = (cx * sin) + (cy * cos)
    print(int(xx), int(yy))
    
    cx, cy = int(xx + (ww/2)), int((hh/2) + yy)

    print(cx, cy) 


ANGLE = 180

def rotate_matrix(x, y, w, h, nw, nh):
    cos, sin = np.cos(np.pi * (ANGLE/180)), np.sin(np.pi * (ANGLE/180))

    # print(x, y, w, h, nw, nh)

    ww = (nw - w) / 2
    hh = (nh - h) / 2
    # print('2.', hh, ww)
    # print('a.', y*h, x*w)

    nx = ((x * w) + ww)
    ny = ((y * h) + hh)
    # print('3.', 0.5 - ny, nx - 0.5)
    
    xx = ((nx - 0.5) * cos) - ((0.5 - ny) * sin)
    yy = (((nx - 0.5) * sin) + ((0.5 - ny) * cos))
    # print('5.', yy, xx)

    # xx = ((x - 0.5) * cos) - ((0.5 - y) * sin)
    # yy = ((x - 0.5) * sin) + ((0.5 - y) * cos)
    # print('5.', yy, xx)

    # xx = ((xx * w) + ww) / nw
    # yy = ((yy * h) + hh) / nh
    # print('5.', yy, xx)

    return xx + 0.5, 0.5 - yy

    # nx = ((x * w) + ww)
    # ny = ((y * h) + hh)
    # # print('3.', ny-0.5, 0.5-nx)
    
    # xx = ((nx - (w/2)) * cos) - (((h/2) - ny) * sin)
    # yy = (((nx - (w/2)) * sin) + (((h/2) - ny) * cos))
    # print('5.', yy, xx)

    # # xx = ((x - 0.5) * cos) - ((0.5 - y) * sin)
    # # yy = ((x - 0.5) * sin) + ((0.5 - y) * cos)
    # return xx + (nw/2), (nh/2) - yy

def find_minmax(x1, x2, y1, y2, w, h):
    chk_x = list()
    chk_y = list()
    for x in (x1, x2):
        for y in (y1, y2):
            # xx, yy = rotate_matrix(x, y, w, h)
            # chk_x.append(xx)
            # chk_y.append(yy)
            pass

    # print(chk_x, chk_y)


os.chdir(XML_FORMAT_PATH)

with open(current_path + '/' + 'classes.txt', 'w') as txt:
    for item in classes:
        txt.write(item + '\n')
        print ("[%s] is added in classes.txt" % item)
    
for current_dir, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml'):
            xmldoc = minidom.parse(file)
            yolo_format = (RESULT_FORMAT_PATH+'/'+file.split('.')[0]+'.txt')
            org_img_path = ORIGIN_FORMAT_PATH + '/' + file.split('.')[0] + '.jpg'
            
            org_img = cv2.imread(org_img_path)
            
            with open(yolo_format, "w") as f:
    
                objects = xmldoc.getElementsByTagName('object')
                size = xmldoc.getElementsByTagName('size')[0]
                width = int((size.getElementsByTagName('width')[0]).firstChild.data)
                height = int((size.getElementsByTagName('height')[0]).firstChild.data)
    
                for item in objects:
                    name =  (item.getElementsByTagName('name')[0]).firstChild.data
                    if name in classes:
                        class_name = str(classes[name])
                    else:
                        class_name = "-1"
                        print ("[Warning]Class name ['%s'] is not in classes" % name)
    
                    # get bbox coordinates
                    xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                    ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                    xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                    ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                    xml_cordinates = (float(xmin), float(xmax), float(ymin), float(ymax))
                    yolo_cordinates = getYoloCordinates((width,height), xml_cordinates)

                    ocx = (float(xmin) + float(xmax))/2
                    ocy = (float(ymin) + float(ymax))/2
                    cv2.line(org_img, (int(ocx), int(ocy)), (int(ocx), int(ocy)), (255,100,255), 25)

                    rot_img = rotate_chg(org_img, ANGLE)

                    print(org_img.shape)
                    print(rot_img.shape)

                    n_height, n_width = rot_img.shape[:2]

                    # print(yolo_cordinates)
                    cx, cy = yolo_cordinates[0], yolo_cordinates[1]
                    rotate_test(cx, cy, width, height, n_width, n_height)
                    # print('1.', cy, cx)
                    cx, cy = rotate_matrix(cx, cy, width, height, n_width, n_height)
                    # print('4.', cy, cx)
                    cx1, cy1 = cx*n_width, cy*n_height
                    # cx1, cy1 = cx, cy
                    # print(cx1, cy1)
                    
                    # minmax = list()

                    # minmax.append(find_minmax(float(xmin), float(xmax), float(ymin), float(ymax), width, height))

                    # cv2.rectangle(rot_img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255,0,255), 2)
                    cv2.line(rot_img, (int(cx1), int(cy1)), (int(cx1), int(cy1)), (0,0,255), 25)
                    # cv2.rectangle(org_img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255,255,255), 2)
                    # cv2.rectangle(rot_img, (int(x0), int(y0)), (int(x1), int(y1)), (255,255,255), 2)
                    # cv2.imshow('image2', org_img)
                    cv2.imshow('image', rot_img)
                    cv2.waitKey()
                    cv2.destroyAllWindows()
    
                    f.write(class_name + " " + " ".join([("%.6f" % a) for a in yolo_cordinates]) + '\n')
                    file_count += 1
    
            print ("{}. [{}] is created".format(file_count, yolo_format))
