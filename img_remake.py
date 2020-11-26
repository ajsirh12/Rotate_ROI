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

    def rotate_matrix(self, list, angle):
        x, y, w, h = list
        cos, sin = np.cos(np.pi * (angle/180)), np.sin(np.pi * (angle/180))

        # print(x, y, w, h)

    def img_ramake(self, degree):
        filename = os.listdir(ORIGIN_FORMAT_PATH)
        for file in filename:
            if not file.endswith('.txt'):
                filename.remove(file)

        for file in filename:
            org_img_path = ORIGIN_FORMAT_PATH + "/" + file.split('.')[0] + '.jpg'

            with open(ORIGIN_FORMAT_PATH + '/' + file.split('.')[0] + '.txt', 'r') as txt:
                yolo_txt = txt.read()
            
            yolo_list = yolo_txt.split('\n')[:-1]
            print(yolo_list)

            org_img = cv2.imread(org_img_path)

            while True:
                if self.angle >= 360:
                    self.angle = 0
                    break   
                
                res_img = self.rotate_chg(org_img, self.angle)
                res_img_path = RESULT_FORMAT_PATH + "/" + file.split('.')[0] + str(self.angle) + '.jpg' 

                self.rotate_matrix((1, 2, 3, 4), self.angle)


                self.angle = self.angle + degree

                
        print(filename)

if __name__ == "__main__":
    remake = img_ramake()
    remake.img_ramake(30)
