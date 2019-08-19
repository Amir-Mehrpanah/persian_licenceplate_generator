import cv2
import numpy


def perspective_transform(image: numpy.ndarray, config) -> numpy.ndarray:
    alpha = (alpha) * numpy.pi / 180.

    beta = (beta) * numpy.pi / 180.

    gamma = (gamma) * numpy.pi / 180.
    src = numpy.array([
        [0, 0],
        [image.shape[0], 0],
        [image.shape[0], image.shape[1]],
        [0, image.shape[1]]], dtype="float32")
    dst = numpy.array([
        [0 + x, 0 + y],
        [image.shape[0] * numpy.cos(theta) + x, image.shape[0] * numpy.sin(theta) + y],
        [image.shape[0] + x, image.shape[1] + y],
        [-image.shape[1] * numpy.sin(alpha) + x, image.shape[1] * numpy.cos(alpha) + y]], dtype="float32")
    transformation_matrix = cv2.getPerspectiveTransform(src, dst)
    result = cv2.warpPerspective(image, transformation_matrix, (1200, 400))
    return result
