import numpy as np
from enum import Enum


class OverlapStrategy(Enum):
    """
    The Strategy used when the mask overlaps the image borders.
    """
    PADDING_MIN = 1
    PADDING_MEAN = 2
    PADDING_MAX = 3
    PARTIAL_APPLY = 4
    CROP = 5


class SpatialMask:
    """
        This class represents a generic mask.

        Other Masks can extend this class in order to perform spatial filters in a image.
        All masks take the matrix of an image, the target pixel and run the mask on the target pixel and, then returns
        the result pixel for the target_pixel.

        Attributes:
            size: The size of the mask

            overlap_strategy: The Strategy the the mask overlaps the image in the borders.

            params: Dict of the extra params that an mask can have. Each mask can have different params.
        """
    def __init__(self, size: int = 3,
                 overlap_strategy: OverlapStrategy = OverlapStrategy.CROP, params: dict = None):
        if params is None:
            params = {}
        if size < 3 or size % 2 == 0:
            raise ValueError("The size of the mask needs to be higher than 1 and an odd value.")

        self.overlap_strategy = overlap_strategy
        self.size = size
        self.params = params

    def apply_mask(self, image_matrix: np.ndarray, max_pixel_color: int) -> np.ndarray:
        """
            Apply the mask on a image.

        :param max_pixel_color: The max value that a color can reach in the image. Its used in the
            OverlapStrategy.PADDING_MEAN.
        :param image_matrix:  A matrix representing each pixel of the image. If the image has one 1 channel,
            each pixel is an integer. Otherwise, each pixel is a tuple formed by the channels of the image
            where the first 3 positions of this tuple are de color channels, RGB, respectively.
        :return: The image after the mask application.
        """
        m, n = image_matrix.shape[0], image_matrix.shape[1]
        padding: int = (self.size - 1) // 2

        if str(self.overlap_strategy.name).startswith("PADDING"):  # if the strategy is to Pad
            padded_matrix = pad_matrix(image_matrix, self.size, max_pixel_color, self.overlap_strategy)
            for i in range(m):
                for j in range(n):
                    image_matrix[i, j] = self._apply_on_pixel(padded_matrix, (i + padding, j + padding))
            return image_matrix

        elif self.overlap_strategy == OverlapStrategy.PARTIAL_APPLY:  # if the strategy is to apply partially
            w_image = image_matrix.copy()
            for i in range(m):
                for j in range(n):
                    image_matrix[i, j] = self._apply_on_pixel_partially(w_image, (i, j))

            return image_matrix

        elif self.overlap_strategy == OverlapStrategy.CROP:  # if the strategy is to crop
            i_start, i_stop = padding, m - padding
            j_start, j_stop = padding, n - padding

            w_image = image_matrix.copy()
            for i in range(i_start, i_stop + 1):
                for j in range(j_start, j_stop + 1):
                    image_matrix[i, j] = self._apply_on_pixel(w_image, (i, j))

            return image_matrix[i_start:i_stop, j_start:j_stop]

        return image_matrix

    def _apply_on_pixel(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        """
        This method apply the mask to a specific pixel. It is only called for pixels such that the mask does not
            extend beyond(Overlaps) the edges of the image.
        :param image_matrix:  A matrix representing each pixel of the image. If the image has one 1 channel,
            each pixel is an integer. Otherwise, each pixel is a tuple formed by the channels of the image
            where the first 3 positions of this tuple are de color channels, RGB, respectively.
        :param target_pixel: The pixel that is center of the mask.
        :return: A tuple (R,G,B) or a int, that represents the new pixel color
        """
        pass

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        """
        This method apply the mask around a pixel and returns the new value for that pixel, however is no guarantee that
            the target_pixel is a pixel such that the mask applied on it do not overlaps the image, so the application
            of the mask needs to be partially, respecting the limits of the image.
        :param image_matrix:  A matrix representing each pixel of the image. If the image has one 1 channel,
            each pixel is an integer. Otherwise, each pixel is a tuple formed by the channels of the image
            where the first 3 positions of this tuple are de color channels, RGB, respectively.
        :param target_pixel: The pixel that is center of the mask.
        :return: A tuple (R,G,B) or a int, that represents the new pixel color
        """
        pass


def pad_matrix(image_matrix: np.ndarray, mask_size: int, max_value: int, overlap: OverlapStrategy):
    m, n = image_matrix.shape[0], image_matrix.shape[1]
    padding: int = (mask_size - 1) // 2
    result_matrix = np.zeros(shape=(m + (padding * 2), n + (padding * 2)), dtype=int)

    if overlap == OverlapStrategy.PADDING_MAX:
        result_matrix[:padding, :], result_matrix[-padding:, :], result_matrix[:, -padding:],\
            result_matrix[:, :padding] = max_value, max_value, max_value, max_value
    elif overlap == OverlapStrategy.PADDING_MEAN:
        result_matrix[:padding, :], result_matrix[-padding:, :], result_matrix[:, -padding:],\
            result_matrix[:, :padding] = max_value // 2, max_value // 2, max_value // 2, max_value // 2

    result_matrix[padding:-padding, padding:-padding] = image_matrix

    return result_matrix


class IdentitySpatialMask(SpatialMask):
    def apply_mask(self, image_matrix: np.ndarray, max_pixel_color: int) -> np.ndarray:
        return image_matrix


class AverageSpatialMask(SpatialMask):
    def _apply_on_pixel(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        d = (self.size - 1) // 2
        area = (self.size * self.size)
        i_start, i_stop = target_pixel[0] - d, target_pixel[0] + d
        j_start, j_stop = target_pixel[1] - d, target_pixel[1] + d

        sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop+1]

        result = int(np.sum((sub_matrix * (1/area))))

        return result

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        d = (self.size - 1) // 2
        area = 0
        total = 0
        i_start, i_stop = target_pixel[0] - d, target_pixel[0] + d
        j_start, j_stop = target_pixel[1] - d, target_pixel[1] + d

        for i in range(i_start, i_stop + 1):
            if 0 <= i < image_matrix.shape[0]:
                for j in range(j_start, j_stop + 1):
                    if 0 <= j < image_matrix.shape[1]:
                        area += 1
                        total += image_matrix[i, j]

        if area > 0:
            return total//area

        return image_matrix[target_pixel[0], target_pixel[1]]


class MedianSpatialMask(SpatialMask):
    """
        Median Smoothing Mask.
        (Digital Image Processing, GONZALES & Woods - 3edition - Cap. 3.5.2 - Order-statistic filters).
        Extra parameters:
            'order': value between of 0 and 100. Represents the percentile order used to calculate the resulting pixel.
                Default: 50
    """
    def _apply_on_pixel(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        try:
            percentile = self.params['order']
        except KeyError:
            percentile = 50

        d = (self.size - 1) // 2
        i_start, i_stop = target_pixel[0] - d, target_pixel[0] + d
        j_start, j_stop = target_pixel[1] - d, target_pixel[1] + d

        sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop + 1].reshape(-1)

        result = int(np.percentile(sub_matrix, percentile))

        return result

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, target_pixel: tuple[int, int]) -> object:
        try:
            percentile = self.params['order']
        except KeyError:
            percentile = 50

        d = (self.size - 1) // 2
        i_start, i_stop = target_pixel[0] - d, target_pixel[0] + d
        j_start, j_stop = target_pixel[1] - d, target_pixel[1] + d

        valid_pixels = []
        for i in range(i_start, i_stop + 1):
            if 0 <= i < image_matrix.shape[0]:
                for j in range(j_start, j_stop + 1):
                    if 0 <= j < image_matrix.shape[1]:
                        valid_pixels.append(image_matrix[i, j])

        result = int(np.percentile(np.array(valid_pixels, dtype=int), percentile))
        return result
