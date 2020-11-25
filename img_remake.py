import os
import cv2
import numpy as np
from scipy import ndimage

current_path = os.path.abspath(os.curdir)
ORIGIN_FORMAT_PATH = current_path + '/images/org_image'
RESULT_FORMAT_PATH = current_path + '/images/res_image'
XML_FORMAT_PATH = current_path + '/images/annotation'

class img_ramake:
    
    def __init__(self):
        self.angle = 0

    def rotate_chg(self, img, angle):
        dst = ndimage.rotate(img, angle)
        return dst

    def rotate_matrix(self, x, y, w, h, nw, nh, angle):
        cos, sin = np.cos(np.pi * (angle/180)), np.sin(np.pi * (angle/180))

        ww = (nw - w) / 2
        hh = (nh - h) / 2
        # print(hh, ww)

        nx = ((x * w) + ww) / nw
        ny = ((y * h) + hh) / nh
        # print(ny, nx)
        
        xx = ((nx - 0.5) * cos) - ((0.5 - ny) * sin)
        yy = ((nx - 0.5) * sin) + ((0.5 - ny) * cos)

        # xx = ((x - 0.5) * cos) - ((0.5 - y) * sin)
        # yy = ((x - 0.5) * sin) + ((0.5 - y) * cos)
        return xx + 0.5, 0.5 - yy

    def img_ramake(self, degree):
        filename = os.listdir(ORIGIN_FORMAT_PATH)
        for file in filename:
            if not file.endswith('.txt'):
                filename.remove(file)

        for file in filename:
            org_img_path = ORIGIN_FORMAT_PATH + "/" + file.split('.')[0] + '.jpg'
            org_img = cv2.imread(org_img_path)
            # cv2.imshow('image', org_img)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

            while True:
                if self.angle >= 360:
                    self.angle = 0
                    break   
                
                res_img = self.rotate_chg(org_img, self.angle)
                
                res_img_path = RESULT_FORMAT_PATH + "/" + file.split('.')[0] + str(self.angle) + '.jpg'  
                self.angle = self.angle + degree

                
        print(filename)

if __name__ == "__main__":
    remake = img_ramake()
    remake.img_ramake(30)
