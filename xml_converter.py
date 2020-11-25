from xml.dom import minidom
import os

current_path = os.path.abspath(os.curdir)
print("Current path is {}".format(current_path))
ORIGIN_FORMAT_PATH = current_path + '/images/org_image'
RESULT_FORMAT_PATH = current_path + '/images/res_image'
XML_FORMAT_PATH = current_path + '/images/annotation'

class xml_converter:

    def __init__(self):
        self.classes={}
        self.classes["horse"] = 0
        self.classes["person"] = 1
        self.classes["dog"] = 2
        self.classes["bird"] = 3    
        self.file_count = 0

    def getYoloCordinates(self, size, box):
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

    os.chdir(XML_FORMAT_PATH)

    def xml_to_yolo(self):
        with open(current_path + '/' + 'classes.txt', 'w') as txt:
            for item in self.classes:
                txt.write(item + '\n')
                print ("[%s] is added in classes.txt" % item)
            
        for current_dir, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.xml'):
                    xmldoc = minidom.parse(file)
                    yolo_format = (RESULT_FORMAT_PATH+'/'+file[:-4]+'.txt')

                    with open(yolo_format, "w") as f:
            
                        objects = xmldoc.getElementsByTagName('object')
                        size = xmldoc.getElementsByTagName('size')[0]
                        width = int((size.getElementsByTagName('width')[0]).firstChild.data)
                        height = int((size.getElementsByTagName('height')[0]).firstChild.data)
            
                        for item in objects:
                            name =  (item.getElementsByTagName('name')[0]).firstChild.data
                            if name in self.classes:
                                class_name = str(self.classes[name])
                            else:
                                class_name = "-1"
                                print ("[Warning]Class name ['%s'] is not in classes" % name)
            
                            # get bbox coordinates
                            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                            xml_cordinates = (float(xmin), float(xmax), float(ymin), float(ymax))
                            yolo_cordinates = self.getYoloCordinates((width,height), xml_cordinates)
            
                            f.write(class_name + " " + " ".join([("%.6f" % a) for a in yolo_cordinates]) + '\n')
                            self.file_count += 1
            
                    print ("{}. [{}] is created".format(self.file_count, yolo_format))