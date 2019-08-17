import glob
import json
import random
import warnings

import cv2
import numpy


class AssetManager:
    def __init__(self, config_path):
        # no need to change the code, just tweak the config file :)
        project_config_file = json.loads(config_path)
        self.__init_components(project_config_file)
        self.plate_config = project_config_file['plate_config']
        self.noise_config = project_config_file['noise_config']
        self.transformations_config = project_config_file['transformations_config']

    def __init_components(self, project_config_file) -> None:
        component_addresses = {}
        for item in project_config_file['components']:
            component_addresses[item] = glob.glob(project_config_file['components'][item])
        self.__components = {}
        self.__annotations = {}
        for item in component_addresses:
            self.__components[item] = []
            self.__annotations[item] = []
            for file_name in component_addresses[item]:
                image = cv2.imread(file_name, -1)
                self.__components[item].append(image)

                key = file_name.replace('.png', '').split('/')[-1]
                try:
                    annotation_value = project_config_file['annotations_config'][key]
                    annotation = (numpy.array(image[:, :, 3]) > 0).astype(int)
                    annotation = numpy.multiply(annotation, annotation_value)
                    self.__annotations[item].append(annotation)
                except KeyError:
                    warnings.warn(
                        f'key: {key} for {file_name} not found in project_config ->'
                        f' annotations_config.\n Annotation skipped.')

    def get_rnd_raw_plate(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['plates']) - 1)
        return self.__components['plates'][index].copy(), self.__annotations['plates'][index]

    def get_rnd_number(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['numbers']) - 1)
        return self.__components['numbers'][index].copy(), self.__annotations['numbers'][index]

    def get_rnd_mini_number(self, include_zero=False) -> (numpy.ndarray, numpy.ndarray):
        start = (1, 0)[include_zero]  # awkwardly hardcoded but works fine till '0' is the first element!
        index = random.randint(start, len(self.__components['mini_numbers']) - 1)
        return self.__components['mini_numbers'][index], self.__annotations["mini_numbers"][index]

    def get_rnd_letter(self) -> (numpy.ndarray, numpy.ndarray):
        index = random.randint(0, len(self.__components['letters']) - 1)
        return self.__components['letters'][index], self.__annotations['letters'][index]

    def get_rnd_numbers(self) -> [(numpy.ndarray, numpy.ndarray)]:
        numbers = []
        for _ in range(5):
            numbers.append(self.get_rnd_number())
        return numbers

    def get_rnd_mini_numbers(self) -> [(numpy.ndarray, numpy.ndarray)]:
        mini_numbers = [self.get_rnd_mini_number(), self.get_rnd_mini_number(include_zero=True)]
        return mini_numbers

    def get_rnd_dirt(self) -> numpy.ndarray:
        return random.choice(self.__components['dirt'])

    def get_rnd_misc_noise(self) -> numpy.ndarray:
        noise = random.choice(self.__components['misc'])
        return noise
