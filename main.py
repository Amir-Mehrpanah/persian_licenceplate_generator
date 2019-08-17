import _jsonnet
import cv2
import matplotlib

import transformations  # comes with a bunch of static methods
from asset_manager import AssetManager
from plate_generator import PlateGenerator

matplotlib.use('TkAgg')

project_config_path = 'project_configurations.jsonnet'
project_config = _jsonnet.evaluate_file(project_config_path)

assets = AssetManager(project_config)
plate_generator = PlateGenerator(assets)

plate, annotations = plate_generator.get_rnd_plate(apply_noise=True, apply_dirt=True)
result = transformations.perspective_transform(plate, assets.transformations_config)
cv2.imshow("a", result)
cv2.waitKey(0)
