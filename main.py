import argparse

import _jsonnet
import cv2
import psutil
from tqdm import tqdm

import transformations
from asset_manager import AssetManager
from plate_generator import PlateGenerator

project_config_path = 'project_configurations.jsonnet'
project_config = _jsonnet.evaluate_file(project_config_path)
assets = AssetManager(project_config)
parser = argparse.ArgumentParser(description='Reading input arguments.')
parser.add_argument('--num_out_img', default=assets.generator_config['num_out_img'], type=int)
parser.add_argument('--apply_misc_noise', default=assets.generator_config['apply_misc_noise'], type=bool)
parser.add_argument('--apply_dirt', default=assets.generator_config['apply_dirt'], type=bool)
args = parser.parse_args()

print(f'generating {args.num_out_img} number of images.')
progress = tqdm(range(args.num_out_img))

for index in progress:
    plate_generator = PlateGenerator(assets)
    plate, annotation = plate_generator.get_rnd_plate(apply_misc_noise=args.apply_misc_noise,
                                                      apply_dirt=args.apply_dirt)
    plate, annotation = transformations.perspective_transform(plate, annotation, assets.transformations_config)
    plate = plate_generator.fill_background(plate)
    cv2.imwrite("output/{0:05}.jpg".format(index), plate)
    cv2.imwrite("ann_output/{0:05}.png".format(index), annotation)
    progress.set_postfix_str('memory: %' + str(psutil.virtual_memory()[2]))
