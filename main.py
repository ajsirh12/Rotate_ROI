from xml_converter import *
import argparse

def main(xml):
    if xml:
        converter = xml_converter()
        converter.xml_to_yolo()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--xml', type=str, default=False, help="convert xml file to yolo coordinate")

    args = parser.parse_args()
    _xml = False if str(args.xml).lower() == 'false' else True
    # print(_xml)

    main(_xml)
