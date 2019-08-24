import glob
import os

import cv2
import numpy
from json2xml import json2xml

kernel = numpy.ones((2, 2), numpy.uint8)


def get_rects(img, threshold) -> [tuple]:
    bbox_list = []
    thresh = (img == 40).astype(numpy.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)  # noise removal steps
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        bbox_list.append((x, y, x + w, y + h))
    return bbox_list


def bounding_rects_to_xml(input_directory, output_directory, annotations_config):
    file_names = glob.glob(input_directory)
    for file in file_names:
        real_path = os.path.realpath(file)
        path = real_path.split('/')
        annotation = numpy.load(file)
        data_dic = {
            'folder': path[-2],
            'path': real_path,
            'filename': path[-1],
            'source': {
                'database': annotations_config['source']
            },
            'size': {
                'width': annotation.shape[0],
                'height': annotation.shape[1],
                'depth': 3  # awfully hardcoded!
            },
            'segmented': 0  # awfully hardcoded!
        }
        for key in annotations_config:
            rects_list = get_rects(annotation, annotations_config[key])
            data_dic['object'] = []
            for index, _object in enumerate(rects_list):
                data_dic['object'].append({})
                data_dic['object'][index]['name'] = key
                data_dic['object'][index]['pose'] = 'unspecified'  # awfully hardcoded!
                data_dic['object'][index]['truncated'] = 0  # awfully hardcoded!
                data_dic['object'][index]['difficult'] = 0  # awfully hardcoded!
                data_dic['object'][index]['bndbox'] = {
                    'xmin': _object[0],
                    'ymin': _object[1],
                    'xmax': _object[2],
                    'ymax': _object[3]
                }
        xml = json2xml.Json2xml(data_dic, wrapper='annotation').to_xml()
        with open(os.path.join(output_directory, path[-1].replace('.npy', '.xml')), "w") as f_out:
            f_out.write(xml)
