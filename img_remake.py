import os
import cv2
import numpy as np
from scipy import ndimage

class img_remake:
    
    def __init__(self, resize):
        self.angle = 0
        self.resize = resize
        self.width = 0
        self.height = 0
        self.resized_width = 0
        self.resized_height = 0
        self.current_path = os.path.abspath(os.curdir)
        self.ORIGIN_FORMAT_PATH = self.current_path + '/images/org_image'
        self.RESULT_FORMAT_PATH = self.current_path + '/images/res_image'

    def resize_img(self, img):
        ratio = self.resize / img.shape[1]

        resized_img = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)

        return resized_img


    def rotate_img(self, img):
        dst = ndimage.rotate(img, self.angle)
        return dst

    def rotate_point(self, point, cos, sin):
        x, y = point
        xx = (x * cos) - ((-y) * sin)
        yy = (x * sin) + ((-y) * cos)

        if 0 <= self.angle <= 90:
            move_point = np.rint(sin * self.width)

            return xx, (-yy) + move_point

        elif 90 < self.angle <=180:
            move_point = np.sin(np.pi * ((self.angle - 90)/180))
            move_point = np.rint(move_point * self.width)

            return xx + move_point, (-yy) + self.resized_height

        elif 180 < self.angle <=270:
            move_point = np.cos(np.pi * ((self.angle - 180)/180))
            move_point = np.rint(move_point * self.height)

            return xx + self.resized_width, (-yy) + move_point

        elif 270 < self.angle <=360:
            move_point = np.cos(np.pi * ((self.angle - 270)/180))
            move_point = np.rint(move_point * self.height)

            return xx + move_point, (-yy)


    def rotate_matrix(self, points):
        cos, sin = np.cos(np.pi * (self.angle/180)), np.sin(np.pi * (self.angle/180))

        result = list()

        for point in points:
            point_x = list()
            point_y = list()

            classes, p0, p1, p2, p3 = point
            
            for p in (p0, p1, p2, p3):
                x, y = self.rotate_point(p, cos, sin)
                point_x.append(x)
                point_y.append(y)

            xmin = min(point_x)
            xmax = max(point_x)
            ymin = min(point_y)
            ymax = max(point_y)

            cx = (np.rint((xmin + xmax)/2)) / self.resized_width
            cy = (np.rint((ymin + ymax)/2)) / self.resized_height
            w = (np.rint(xmax - xmin)) / self.resized_width
            h = (np.rint(ymax - ymin)) / self.resized_height  

            result.append((classes, cx, cy, w, h))
        
        return result

    
    def search_point(self, coords):
        result_point = list()
        for coord in coords:
            classes, cx, cy, w, h = coord.split(' ')

            ccx, ccy, ww, hh = float(cx) * self.width, float(cy) * self.height, float(w) * self.width, float(h) * self.height

            xmin = np.rint(ccx - (ww/2))
            xmax = np.rint(ccx + (ww/2))
            ymin = np.rint(ccy - (hh/2))
            ymax = np.rint(ccy + (hh/2))

            p0 = (xmin, ymin)
            p1 = (xmin, ymax)
            p2 = (xmax, ymax)
            p3 = (xmax, ymin)

            result_point.append((classes, p0, p1, p2, p3))

        return result_point


    # Draw boundingbox
    def test_img(self, img, result):

        for res in result:
            classes, cx, cy, w, h = res

            ccx, ccy, ww, hh = float(cx) * self.resized_width, float(cy) * self.resized_height, float(w) * self.resized_width, float(h) * self.resized_height

            xmin = np.rint(ccx - (ww/2))
            xmax = np.rint(ccx + (ww/2))
            ymin = np.rint(ccy - (hh/2))
            ymax = np.rint(ccy + (hh/2))

            res_img = cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0,0,255), 2)
        
        return res_img

    def contrast_img(self, img):
        alpha = 10 / 10.0
        dst = np.clip((1 + alpha) * img - 128 - alpha, 0, 255).astype(np.uint8)

        return dst

    def blur_img(self, img):
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img,-1,kernel)

        return dst

    def img_remake(self, degree, contrast, blur):
        filename = os.listdir(self.ORIGIN_FORMAT_PATH)
        filename.sort()
        
        for file in filename:
            if not file.endswith('.txt'):
                filename.remove(file)

        for n, file in enumerate(filename):
            print(n, file)
            org_img_path = self.ORIGIN_FORMAT_PATH + "/" + file.split('.')[0] + '.jpg'

            with open(self.ORIGIN_FORMAT_PATH + '/' + file.split('.')[0] + '.txt', 'r') as txt:
                yolo_txt = txt.read()
            
            yolo_list = yolo_txt.split('\n')[:-1]

            org_img = cv2.imread(org_img_path)
            if self.resize != 0:
                org_img = self.resize_img(org_img)
            self.height, self.width = org_img.shape[:2]

            points = self.search_point(yolo_list)

            while True:
                if self.angle >= 360:
                    self.angle = 0
                    break   
                
                res_img = self.rotate_img(org_img)
                res_img_path = self.RESULT_FORMAT_PATH + "/" + file.split('.')[0] + '_' + str(self.angle) + '.jpg' 
                self.resized_height, self.resized_width = res_img.shape[:2]
                
                result = self.rotate_matrix(points)

                # Draw boundingbox
                # res_img = self.test_img(res_img, result)

                cv2.imwrite(res_img_path, res_img)
                
                with open(res_img_path.split('.')[0] + '.txt', 'w') as f:
                    for i in result:
                        f.write(i[0] + " " + " ".join([("%.6f" % a) for a in i[1:5]]) + '\n')

                if contrast:
                    con_img = self.contrast_img(res_img)
                    con_img_path = self.RESULT_FORMAT_PATH + "/" + file.split('.')[0] + '_' + str(self.angle) + '_contrast.jpg' 

                    cv2.imwrite(con_img_path, con_img)

                    with open(con_img_path.split('.')[0] + '.txt', 'w') as f:
                        for i in result:
                            f.write(i[0] + " " + " ".join([("%.6f" % a) for a in i[1:5]]) + '\n')

                if blur:
                    blur_img = self.blur_img(res_img)
                    blur_img_path = self.RESULT_FORMAT_PATH + "/" + file.split('.')[0] + '_' + str(self.angle) + '_blur.jpg' 

                    cv2.imwrite(blur_img_path, blur_img)

                    with open(blur_img_path.split('.')[0] + '.txt', 'w') as f:
                        for i in result:
                            f.write(i[0] + " " + " ".join([("%.6f" % a) for a in i[1:5]]) + '\n')

                if blur and contrast:
                    cont_blur_img = self.blur_img(con_img)
                    cont_blur_img_path = self.RESULT_FORMAT_PATH + "/" + file.split('.')[0] + '_' + str(self.angle) + '_cont_blur.jpg' 
                    
                    cv2.imwrite(cont_blur_img_path, cont_blur_img)

                    with open(cont_blur_img_path.split('.')[0] + '.txt', 'w') as f:
                        for i in result:
                            f.write(i[0] + " " + " ".join([("%.6f" % a) for a in i[1:5]]) + '\n')

                    blur_cont_img = self.contrast_img(blur_img)
                    blur_cont_img_path = self.RESULT_FORMAT_PATH + "/" + file.split('.')[0] + '_' + str(self.angle) + '_blur_cont.jpg' 
                    
                    cv2.imwrite(blur_cont_img_path, blur_cont_img)

                    with open(blur_cont_img_path.split('.')[0] + '.txt', 'w') as f:
                        for i in result:
                            f.write(i[0] + " " + " ".join([("%.6f" % a) for a in i[1:5]]) + '\n')


                self.angle = self.angle + degree


# if __name__ == "__main__":
#     remake = img_remake()
#     remake.img_remake(30)
