import random

import cv2
import numpy


def perspective_transform(image: numpy.ndarray, config) -> numpy.ndarray:
    alpha = random.uniform(-config['max_dalpha'], config['max_dalpha'])
    beta = random.uniform(-config['max_dbeta'], config['max_dbeta'])
    gamma = random.uniform(-config['max_dgamma'], config['max_dgamma'])
    h = image.shape[0]
    w = image.shape[1]
    f = 1000
    dz = f * random.uniform(1, config['max_dz'])

    a_1 = numpy.array([[1, 0, -w / 2],
                       [0, 1, -h / 2],
                       [0, 0, 0],
                       [0, 0, 1]])
    r_x = numpy.array([[1, 0, 0, 0],
                       [0, numpy.cos(alpha), -numpy.sin(alpha), 0],
                       [0, numpy.sin(alpha), numpy.cos(alpha), 0],
                       [0, 0, 0, 1]])
    r_y = numpy.array([[numpy.cos(beta), 0, -numpy.sin(beta), 0],
                       [0, 1, 0, 0],
                       [numpy.sin(beta), 0, numpy.cos(beta), 0],
                       [0, 0, 0, 1]])
    r_z = numpy.array([[numpy.cos(gamma), -numpy.sin(gamma), 0, 0],
                       [numpy.sin(gamma), numpy.cos(gamma), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    r = numpy.matmul(numpy.matmul(r_x, r_y), r_z)
    t = numpy.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])
    a_2 = numpy.array([[f, 0, 512, 0],
                       [0, f, 512, 0],
                       [0, 0, 1, 0]])

    trans = numpy.matmul(a_2, numpy.matmul(t, numpy.matmul(r, a_1)))

    result = cv2.warpPerspective(image, trans, (1024, 1024), cv2.INTER_LANCZOS4)
    return result
