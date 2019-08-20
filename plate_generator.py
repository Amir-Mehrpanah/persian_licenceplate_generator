import random

import numpy

from asset_manager import AssetManager


def elementwise_add(t1, t2):
    return tuple([sum(i) for i in zip(t1, t2)])


def alpha_blend(src: numpy.ndarray, temp: numpy.ndarray, point) -> numpy.ndarray:
    alpha_temp = temp[:, :, 3] / 255.0
    alpha_n_temp = 1.0 - alpha_temp

    for ch in range(0, 3):
        src[point[0]:point[0] + temp.shape[0], point[1]:point[1] + temp.shape[1], ch] = (
                alpha_temp * temp[:, :, ch] + alpha_n_temp * src[point[0]:point[0] + temp.shape[0],
                                                             point[1]:point[1] + temp.shape[1], ch])
    return src


def annotation_blend(src: numpy.ndarray, temp: numpy.ndarray, point) -> numpy.ndarray:
    src[point[0]:point[0] + temp.shape[0], point[1]:point[1] + temp.shape[1]] = numpy.maximum(
        temp[:, :], src[point[0]:point[0] + temp.shape[0], point[1]:point[1] + temp.shape[1]])
    return src


class PlateGenerator:
    def __init__(self, asset_manager: AssetManager):
        self.asset_manager = asset_manager

    def fill_bakground(self, plate: numpy.ndarray) -> numpy.ndarray:
        bg = self.asset_manager.get_rnd_background()
        plate = alpha_blend(bg, plate, [0, 0])
        return plate

    def get_rnd_plate(self, apply_dirt=False, apply_misc_noise=False) -> (numpy.ndarray, numpy.ndarray):
        plate, annotation = self.asset_manager.get_rnd_raw_plate()

        for index, (number, number_annotation) in enumerate(self.asset_manager.get_rnd_numbers()):
            offset1 = tuple(self.asset_manager.plate_config['numbers_offset'][index])
            offset2 = (-number.shape[0] // 2, -number.shape[1] // 2)
            offset = elementwise_add(offset1, offset2)
            alpha_blend(plate, number, offset)
            annotation_blend(annotation, number_annotation, offset)

        for index, (number, mini_number_annotation) in enumerate(self.asset_manager.get_rnd_mini_numbers()):
            offset1 = tuple(self.asset_manager.plate_config['mini_numbers_offset'][index])
            offset2 = (-number.shape[0] // 2, -number.shape[1] // 2)
            offset = elementwise_add(offset1, offset2)
            alpha_blend(plate, number, offset)
            annotation_blend(annotation, mini_number_annotation, offset)

        letter, letter_annotation = self.asset_manager.get_rnd_letter()
        offset1 = tuple(self.asset_manager.plate_config['letter_offset'])
        offset2 = (-letter.shape[0] // 2, -letter.shape[1] // 2)
        offset = elementwise_add(offset1, offset2)
        alpha_blend(plate, letter, offset)
        annotation_blend(annotation, letter_annotation, offset)

        if apply_misc_noise:
            for noise_box in self.asset_manager.noise_config['misc_bounds']:
                if random.uniform(0, 1) < self.asset_manager.noise_config['misc_probability']:
                    misc = self.asset_manager.get_rnd_misc_noise()
                    x_location = random.randint(noise_box['x_min'], noise_box['x_max'])
                    y_location = random.randint(noise_box['y_min'], noise_box['y_max'])
                    alpha_blend(plate, misc, [x_location - misc.shape[0] // 2, y_location - misc.shape[1] // 2])

        if apply_dirt:
            if random.uniform(0, 1) < self.asset_manager.noise_config['dirt_probability']:
                dirt = self.asset_manager.get_rnd_dirt()
                alpha_blend(plate, dirt, (0, 0))

        return plate, annotation
