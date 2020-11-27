from xml_converter import *
from img_remake import *
import argparse
import os

current_path = os.path.abspath(os.curdir)
print("Current path is {}".format(current_path))

def main(xml, degree):
    if xml:
        converter = xml_converter()
        converter.xml_to_yolo()

    img_rotate = img_remake()
    img_rotate.img_remake(degree)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--xml', type=str, default=True, help="convert xml file to yolo coordinate")
    parser.add_argument('--degree', type=int, default=30, help="set degree")

    args = parser.parse_args()
    _xml = False if str(args.xml).lower() == 'false' else True
    _degree = int(args.degree) 

    main(_xml, _degree)
