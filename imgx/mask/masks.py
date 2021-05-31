import numpy as np
from enum import Enum
from imgx.util.util_functions import is_matrix_rgb


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
        m, n, is_rgb = image_matrix.shape[0], image_matrix.shape[1], len(image_matrix.shape) > 2

        padding: int = (self.size - 1) // 2

        if str(self.overlap_strategy.name).startswith("PADDING"):  # if the strategy is to Pad
            padded_matrix = pad_matrix(image_matrix, self.size,
                                       _get_padding_strategy_value(max_pixel_color, self.overlap_strategy))
            for i in range(m):
                for j in range(n):
                    image_matrix[i, j] = self._apply_on_pixel(padded_matrix, padding, is_rgb,
                                                              (i + padding, j + padding))
            return image_matrix

        elif self.overlap_strategy == OverlapStrategy.PARTIAL_APPLY:  # if the strategy is to apply partially
            w_image = image_matrix.copy()
            for i in range(m):
                for j in range(n):
                    image_matrix[i, j] = self._apply_on_pixel_partially(w_image, padding, is_rgb, (i, j))

            return image_matrix

        elif self.overlap_strategy == OverlapStrategy.CROP:  # if the strategy is to crop
            i_start, i_stop = padding, m - padding
            j_start, j_stop = padding, n - padding

            w_image = image_matrix.copy()
            for i in range(i_start, i_stop):
                for j in range(j_start, j_stop):
                    image_matrix[i, j] = self._apply_on_pixel(w_image, padding, is_rgb, (i, j))

            return image_matrix[i_start:i_stop, j_start:j_stop]

        return image_matrix

    def _apply_on_pixel(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                        target_pixel: tuple[int, int]) -> object:
        """
        This method apply the mask to a specific pixel. It is only called for pixels such that the mask does not
            extend beyond(Overlaps) the edges of the image.
        :param image_matrix:  A matrix representing each pixel of the image. If the image has one 1 channel,
            each pixel is an integer. Otherwise, each pixel is a tuple formed by the channels of the image
            where the first 3 positions of this tuple are de color channels, RGB, respectively.
        :param target_pixel: The pixel that is center of the mask.
        :param padding: The number of pixels that overlaps the image's bounds when the mask is applied to a pixel on it.
        :return: A tuple (R,G,B) or a int, that represents the new pixel color
        """
        pass

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                                  target_pixel: tuple[int, int]) -> object:
        """
        This method apply the mask around a pixel and returns the new value for that pixel, however is no guarantee that
            the target_pixel is a pixel such that the mask applied on it do not overlaps the image, so the application
            of the mask needs to be partially, respecting the limits of the image.
        :param image_matrix:  A matrix representing each pixel of the image. If the image has one 1 channel,
            each pixel is an integer. Otherwise, each pixel is a tuple formed by the channels of the image
            where the first 3 positions of this tuple are de color channels, RGB, respectively.
        :param target_pixel: The pixel that is center of the mask.
        :param padding: The number of pixels that overlaps the image's bounds when the mask is applied to a pixel on it.
        :return: A tuple (R,G,B) or a int, that represents the new pixel color
        """
        pass


def _get_padding_strategy_value(max_channel_value: int, overlap: OverlapStrategy) -> int:
    if overlap == OverlapStrategy.PADDING_MAX:
        return max_channel_value

    if overlap == OverlapStrategy.PADDING_MEAN:
        return max_channel_value//2

    if overlap == OverlapStrategy.PADDING_MIN:
        return 0


def pad_matrix(image_matrix: np.ndarray, padding_value: int, mask_size: int):
    m, n, is_rgb = image_matrix.shape[0], image_matrix.shape[1], len(image_matrix.shape) > 2
    padding: int = (mask_size - 1) // 2

    if is_rgb:
        result_matrix = np.zeros(shape=(m + (padding * 2), n + (padding * 2), image_matrix.shape[2]), dtype=int)
    else:
        result_matrix = np.zeros(shape=(m + (padding * 2), n + (padding * 2)), dtype=int)

    result_matrix[:padding, :], result_matrix[-padding:, :], result_matrix[:, -padding:], result_matrix[:, :padding] \
        = padding_value, padding_value, padding_value, padding_value

    result_matrix[padding:-padding, padding:-padding] = image_matrix

    return result_matrix


class IdentitySpatialMask(SpatialMask):
    def apply_mask(self, image_matrix: np.ndarray, max_pixel_color: int) -> np.ndarray:
        return image_matrix


class AverageSpatialMask(SpatialMask):
    def _apply_on_pixel(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                        target_pixel: tuple[int, int]) -> object:
        area = (self.size * self.size)
        i_start, i_stop = target_pixel[0] - padding, target_pixel[0] + padding
        j_start, j_stop = target_pixel[1] - padding, target_pixel[1] + padding

        if is_rgb:
            sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop + 1, :3]
        else:
            sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop + 1]

        if is_rgb:
            r_pixel = image_matrix[target_pixel[0], target_pixel[1]].copy()
            r_pixel[:3] = np.sum(sub_matrix, axis=(0, 1))
            return r_pixel
        else:
            result = int(np.sum((sub_matrix * (1 / area))))
            return result

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                                  target_pixel: tuple[int, int]) -> object:
        area = 0
        if is_rgb:
            total = np.zeros(3, dtype=int)
        else:
            total = 0

        i_start, i_stop = target_pixel[0] - padding, target_pixel[0] + padding
        j_start, j_stop = target_pixel[1] - padding, target_pixel[1] + padding

        for i in range(i_start, i_stop + 1):
            if 0 <= i < image_matrix.shape[0]:
                for j in range(j_start, j_stop + 1):
                    if 0 <= j < image_matrix.shape[1]:
                        area += 1
                        if is_matrix_rgb(image_matrix):
                            total += image_matrix[i, j, :3]
                        else:
                            total += image_matrix[i, j]

        if area > 0:
            if is_rgb:
                r_pixel = image_matrix[target_pixel[0], target_pixel[1]].copy()
                r_pixel[:3] = total//area
                return r_pixel
            else:
                return total // area

        return image_matrix[target_pixel[0], target_pixel[1]]


class MedianSpatialMask(SpatialMask):
    """
        Median Smoothing Mask.
        (Digital Image Processing, GONZALES & Woods - 3edition - Cap. 3.5.2 - Order-statistic filters).
        Extra parameters:
            'order': value between of 0 and 100. Represents the percentile order used to calculate the resulting pixel.
                Default: 50
    """

    def _apply_on_pixel(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                        target_pixel: tuple[int, int]) -> object:
        try:
            percentile = self.params['order']
        except KeyError:
            percentile = 50

        i_start, i_stop = target_pixel[0] - padding, target_pixel[0] + padding
        j_start, j_stop = target_pixel[1] - padding, target_pixel[1] + padding

        if is_rgb:
            sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop + 1, :3].reshape(-1, 3)
            rgb_result = np.percentile(sub_matrix, percentile, axis=0).astype(int)
            pixel_result = image_matrix[target_pixel[0], target_pixel[1]].copy()
            pixel_result[:3] = rgb_result
            return pixel_result
        else:
            sub_matrix = image_matrix[i_start:i_stop + 1, j_start:j_stop + 1].reshape(-1)
            result = int(np.percentile(sub_matrix, percentile))
            return result

    def _apply_on_pixel_partially(self, image_matrix: np.ndarray, padding: int, is_rgb: bool,
                                  target_pixel: tuple[int, int]) -> object:
        try:
            percentile = self.params['order']
        except KeyError:
            percentile = 50

        i_start, i_stop = target_pixel[0] - padding, target_pixel[0] + padding
        j_start, j_stop = target_pixel[1] - padding, target_pixel[1] + padding

        valid_pixels = []
        for i in range(i_start, i_stop + 1):
            if 0 <= i < image_matrix.shape[0]:
                for j in range(j_start, j_stop + 1):
                    if 0 <= j < image_matrix.shape[1]:
                        valid_pixels.append(image_matrix[i, j])

        if is_rgb:
            rgb_result = np.percentile(np.array(valid_pixels, dtype=int), percentile, axis=0).astype(int)
            pixel_result = image_matrix[target_pixel[0], target_pixel[1]].copy()
            pixel_result[:3] = rgb_result
            return pixel_result
        else:
            result = int(np.percentile(np.array(valid_pixels, dtype=int), percentile))
            return result
