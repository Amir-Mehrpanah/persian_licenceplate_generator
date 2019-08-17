import cv2
import numpy


def perspective_transform(image: numpy.ndarray, config) -> numpy.ndarray:
    pts1 = numpy.float32([[0, 0], [800, 0], [0, 176], [800, 176]])
    pts2 = numpy.float32([[0, 0], [780, 20], [0, 176], [780, 156]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    result = cv2.warpPerspective(open_cv_image, matrix, (1024, 1024))
    return result
