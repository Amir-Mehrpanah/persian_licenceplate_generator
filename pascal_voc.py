import glob
import os
from tqdm import tqdm
import cv2
import numpy
from json2xml import json2xml

kernel = numpy.ones((2, 2), numpy.uint8)


def get_rects(img, threshold, single_instance) -> [tuple]:
    bbox_list = []
    thresh = (img == threshold).astype(numpy.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)  # noise removal steps
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        bbox_list.append((max(x - 2, 0), max(y - 2, 0), x + w - 2, y + h - 2))  # compensate dilation effect

    if single_instance and len(bbox_list) != 0:
        xmin = min([elem[0] for elem in bbox_list])
        ymin = min([elem[1] for elem in bbox_list])
        xmax = max([elem[2] for elem in bbox_list])
        ymax = max([elem[3] for elem in bbox_list])
        bbox_list.clear()
        bbox_list.append((xmin, ymin, xmax, ymax))
    return bbox_list

def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]
def getLanbelFromKey(key):
    if key == "A":
        return "10"
    elif key == "B":
        return "11"
    elif key == "P":
        return "12"    
    elif key == "T":
        return "13"
    elif key == "S":
        return "14"
    elif key == "J":
        return "15"    
    elif key == "CH":
        return "16"
    elif key == "HE":
        return "17"
    elif key == "KH":
        return "18"    
    elif key == "D":
        return "19"
    elif key == "Z":
        return "20"
    elif key == "R":
        return "21"    
    elif key == "ZE":
        return "22"
    elif key == "ZH":
        return "23"
    elif key == "SIN":
        return "24"
    elif key == "SHIN":
        return "25"
    elif key == "SAD":
        return "26"
    elif key == "ZAD":
        return "27"
    elif key == "TA":
        return "28"
    elif key == "ZA":
        return "28"
    elif key == "AIN":
        return "30"
    elif key == "GHAIN":
        return "31"
    elif key == "F":
        return "32"
    elif key == "Q":
        return "33"
    elif key == "K":
        return "34"
    elif key == "G":
        return "35"        
    elif key == "L":
        return "36" 
    elif key == "M":
        return "37"
    elif key == "N":
        return "38"
    elif key == "V":
        return "39"
    elif key == "H":
        return "30"
    elif key == "Y":
        return "41"
    elif key == "plate":
        return "43"
    return key     

                
def bounding_rects_to_xml(input_directory, output_directory, annotations_config):
    print('\ngenerating xmls...')
    file_names = glob.glob(input_directory)
    for file in tqdm(file_names):
        real_path = os.path.realpath(file)
        path = real_path.split('/')
        annotation = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        data_dic = {
            'folder': path[-2],
            'path': real_path,
            'filename': path[-1],
            'source': {
                'database': 'automated_lp'  # awfully hardcoded!
            },
            'size': {
                'width': annotation.shape[0],
                'height': annotation.shape[1],
                'depth': 3  # awfully hardcoded!
            },
            'segmented': 0  # awfully hardcoded!
        }
        index = 0
        data_dic['object'] = []
        yolostr="";
        for key in annotations_config:
         
            rects_list = get_rects(annotation, annotations_config[key][0], single_instance=annotations_config[key][1])
            for _object in rects_list:
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
                x_center, y_center, width, height=xml_to_yolo_bbox(_object, annotation.shape[0], annotation.shape[1])
                yolostr+=getLanbelFromKey(key)+" "+str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height)+"\n"
                index += 1
        # xml = json2xml.Json2xml(data_dic, wrapper='annotation').to_xml()
     
        with open(os.path.join(output_directory, path[-1].replace('.png', '.txt')), "w") as f_out:
            f_out.write(yolostr)
