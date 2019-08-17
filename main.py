import _jsonnet
import cv2

import transformations
from asset_manager import AssetManager
from plate_generator import PlateGenerator

project_config_path = 'project_configurations.jsonnet'
project_config = _jsonnet.evaluate_file(project_config_path)

assets = AssetManager(project_config)
plate_generator = PlateGenerator(assets)

plate, annotations = plate_generator.get_rnd_plate(apply_misc_noise=True, apply_dirt=True)
result = transformations.perspective_transform(plate, assets.transformations_config)
cv2.imshow("simple_out.png", result)
cv2.waitKey(0)
