from xml_converter import *
from img_remake import *
import argparse
import os

current_path = os.path.abspath(os.curdir)
print("Current path is {}".format(current_path))

ORIGIN_FORMAT_PATH = current_path + '/images/org_image'
RESULT_FORMAT_PATH = current_path + '/images/res_image'
XML_FORMAT_PATH = current_path + '/images/annotation'

def directory_chk():
    if not os.path.isdir(ORIGIN_FORMAT_PATH):
        os.mkdir(ORIGIN_FORMAT_PATH)
    if not os.path.isdir(RESULT_FORMAT_PATH):
        os.mkdir(RESULT_FORMAT_PATH)
    if not os.path.isdir(XML_FORMAT_PATH):
        os.mkdir(XML_FORMAT_PATH)

def main(xml, degree, resize, contrast, blur):
    directory_chk()

    if xml:
        converter = xml_converter()
        converter.xml_to_yolo()

    img_rotate = img_remake(resize)
    img_rotate.img_remake(degree, contrast, blur)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--xml', type=str, default=True, help="convert xml file to yolo coordinate")
    parser.add_argument('--degree', type=int, default=30, help="set degree")
    parser.add_argument('--resize', type=int, default=0, help="set resize width")
    parser.add_argument('--contrast', type=str, default=True, help="make contrast image")
    parser.add_argument('--blur', type=str, default=True, help="make gaussian blur image")

    args = parser.parse_args()
    _xml = False if str(args.xml).lower() == 'false' else True
    _degree = int(args.degree) 
    _resize = int(args.resize)
    _contrast = False if str(args.contrast).lower() == 'false' else True
    _blur = False if str(args.blur).lower() == 'false' else True

    main(_xml, _degree, _resize, _contrast, _blur)
