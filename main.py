import _jsonnet
import cv2

import transformations
from asset_manager import AssetManager
from plate_generator import PlateGenerator

project_config_path = 'project_configurations.jsonnet'
project_config = _jsonnet.evaluate_file(project_config_path)

assets = AssetManager(project_config)
plate_generator = PlateGenerator(assets)
plate, annotation = plate_generator.get_rnd_plate(apply_misc_noise=True, apply_dirt=True)
plate, annotation = transformations.perspective_transform(plate, annotation, assets.transformations_config)
cv2.imwrite("transformed_out.png", plate)
cv2.imwrite("ann_transformed_out.png", annotation)
