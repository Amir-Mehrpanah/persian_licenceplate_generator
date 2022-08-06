import argparse
import os

import psutil
import _jsonnet
import cv2
from tqdm import tqdm
from plate_generator import PlateGenerator
from transformations import perspective_transform
from asset_manager import AssetManager
from pascal_voc import bounding_rects_to_xml

project_config_path = 'project_configurations.jsonnet'
project_config = _jsonnet.evaluate_file(project_config_path)
assets = AssetManager(project_config)
parser = argparse.ArgumentParser(description='Reading input arguments.')
parser.add_argument('--num_out_img', default=assets.generator_config['num_out_img'], type=int)
parser.add_argument('--output_directory', default=assets.generator_config['output_directory'], type=str)
parser.add_argument('--img_per_package', default=assets.generator_config['img_per_package'], type=int)
parser.add_argument('--apply_misc_noise', default=assets.generator_config['apply_misc_noise'], type=bool)
parser.add_argument('--apply_dirt', default=assets.generator_config['apply_dirt'], type=bool)
args = parser.parse_args()
if False==os.path.exists(args.output_directory):
    os.makedirs(args.output_directory)
annotation_path = ''
images_path = ''
xmls_path = ''
package_counter = 0
print(f'\ngenerating {args.num_out_img} images.')
progress = tqdm(range(args.num_out_img))


for index in progress:
    plate_generator = PlateGenerator(assets)
    plate, annotation = plate_generator.get_rnd_plate(apply_misc_noise=args.apply_misc_noise,
                                                      apply_dirt=args.apply_dirt)
    plate, annotation = perspective_transform(plate, annotation, assets.transformations_config)
    plate = plate_generator.fill_background(plate)
    if index % args.img_per_package == 0:
        current_directory = os.path.join(args.output_directory, f'{package_counter:02}')
        os.mkdir(current_directory)

        annotation_path = os.path.join(current_directory, 'anns')
        os.mkdir(annotation_path)
        xmls_path = os.path.join(annotation_path, 'xmls')
        os.mkdir(xmls_path)
        images_path = os.path.join(current_directory, 'imgs')
        os.mkdir(images_path)
        package_counter += 1

    cv2.imwrite(os.path.join(images_path, f'{index:05}.jpg'), plate)
    cv2.imwrite(os.path.join(annotation_path, f'{index:05}.png'), annotation)

for index in range(package_counter):
    # pascal voc format
    input_address = os.path.join(args.output_directory, f'{index:02}/anns')
    bounding_rects_to_xml(input_address + '/*.png', os.path.join(input_address, 'xmls'), assets.annotations_config)
