import glob
import json
import random
import warnings

import cv2
import numpy
import psutil
from tqdm import tqdm


class AssetManager:
    __bg_counter: int

    def __init__(self, config_path, log_warning=False):
        self.log_warning = log_warning
        # no need to change the code, just tweak the config file :)
        project_config_file = json.loads(config_path)
        self.__backgrounds = None
        self.__bg_counter = 0
        self.__bg_pack = 0
        self.__bg_addresses = glob.glob(project_config_file['components']['backgrounds'])
        self.__init_components(project_config_file)
        self.annotations_config = project_config_file['annotations_config']
        self.plate_config = project_config_file['plate_config']
        self.noise_config = project_config_file['noise_config']
        self.generator_config = project_config_file['generator_config']
        self.__bg_limit = project_config_file['generator_config']['background_load_limit']
        self.__init_backgrounds()
        self.transformations_config = project_config_file['transformations_config']

    def __init_components(self, project_config_file) -> None:
        print('\ninit components...')
        component_addresses = {}
        for item in project_config_file['components']:
            component_addresses[item] = glob.glob(project_config_file['components'][item])
        self.__components = {}
        self.__annotations = {}
        for item in component_addresses:
            self.__components[item] = []
            self.__annotations[item] = []
            if item != 'backgrounds':
                for file_name in component_addresses[item]:
                    image = cv2.imread(file_name, -1)
                    self.__components[item].append(image)

                    key = file_name.split('/')[-1].replace('.png', '').split('_')[0]
                    if key in project_config_file['annotations_config']:
                        annotation_value = project_config_file['annotations_config'][key][0]
                        annotation = (numpy.array(image[:, :, 3]) > 192).astype(numpy.uint8)
                        annotation = numpy.multiply(annotation, annotation_value)
                        self.__annotations[item].append(annotation)
                    else:
                        if self.log_warning:
                            warnings.warn(
                                f'key: {key} for {file_name} not found in project_config ->'
                                f' annotations_config.\n Annotation skipped.')

    def __init_backgrounds(self):
        print(f'\nloading backgrounds (pack {self.__bg_pack})...')
        if self.__backgrounds is not None:
            del self.__backgrounds
        self.__backgrounds = []
        if self.__bg_limit * self.__bg_pack >= len(self.__bg_addresses):
            self.__bg_pack = 0
        progress = tqdm(self.__bg_addresses[self.__bg_limit * self.__bg_pack:self.__bg_limit * (self.__bg_pack + 1)])
        for item in progress:
            self.__backgrounds.append(cv2.imread(item))
        self.__bg_counter = 0
        self.__bg_pack += 1

    def get_bg_image_addresses(self):
        return self.__bg_addresses

    def get_rnd_raw_plate(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['plates']) - 1)
        return self.__components['plates'][index].copy(), self.__annotations['plates'][index].copy()

    def get_rnd_number(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['numbers']) - 1)
        return self.__components['numbers'][index].copy(), self.__annotations['numbers'][index].copy()

    def get_rnd_mini_number(self, include_zero=False) -> (numpy.ndarray, numpy.ndarray):
        start = (1, 0)[include_zero]  # awkwardly hardcoded but works fine till '0' is the first element!
        index = random.randint(start, len(self.__components['mini_numbers']) - 1)
        return self.__components['mini_numbers'][index].copy(), self.__annotations["mini_numbers"][index].copy()

    def get_rnd_letter(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['letters']) - 1)
        return self.__components['letters'][index].copy(), self.__annotations['letters'][index].copy()

    def get_rnd_numbers(self) -> [(numpy.ndarray, numpy.ndarray)]:
        numbers = []
        for _ in range(5):
            numbers.append(self.get_rnd_number())
        return numbers

    def get_rnd_mini_numbers(self) -> [(numpy.ndarray, numpy.ndarray)]:
        mini_numbers = [self.get_rnd_mini_number(), self.get_rnd_mini_number(include_zero=True)]
        return mini_numbers

    def get_rnd_dirt(self) -> numpy.ndarray:
        return random.choice(self.__components['dirt']).copy()

    def get_rnd_misc_noise(self) -> numpy.ndarray:
        misc = random.choice(self.__components['misc']).copy()
        return misc

    def get_nxt_background(self) -> numpy.ndarray:
        if self.__bg_counter == len(self.__backgrounds):
            self.__init_backgrounds()
        image = self.__backgrounds[self.__bg_counter]
        self.__bg_counter += 1
        return image.copy()
