import numpy as np
import matplotlib.axes as axes
import seaborn as sns
from copy import copy, deepcopy
from imgx.mask.masks import SpatialMask
from imgx.types.image_color_type import ImageColorType
import imgx.morphology.operations as morph_operations


class Printable:
    def plot_on_axe(self, ax: axes.Axes):
        pass

    def plot_histogram_on_axe(self, ax: axes.Axes):
        pass


class Image(Printable):
    def __init__(self, data: np.ndarray, max_channel_color: int,
                 color_type: ImageColorType = None,
                 name: str = None,
                 origin_file_path: str = None,
                 description: str = 'This is a image.',
                 comments: list[str] = None
                 ):
        self.name = name
        self.origin_file_path = origin_file_path
        self.description = description
        self.comments = comments

        if max_channel_color is None or max_channel_color < 0:
            raise ValueError('Invalid max_channel_color.')

        self.__max_channel_color = max_channel_color

        if data is None:
            raise ValueError('Image data cannot be None.')

        if 2 > len(data.shape) > 3:
            raise ValueError(f'Invalid image data dimensions: {data.shape}')

        self.__data = data
        self.__dimensions = (data.shape[0], data.shape[1])
        self.__channels_number = 1 if len(data.shape) == 2 else data.shape[2]

        if color_type is None:
            self.__color_type = ImageColorType.SHADES_OF_GRAY if self.__channels_number == 1 \
                else ImageColorType.RGB if self.__channels_number == 3 \
                else ImageColorType.RGBA
        else:
            self.__color_type = color_type

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.__dimensions

    @property
    def channels_number(self) -> int:
        return self.__channels_number

    @property
    def max_channel_color(self) -> int:
        return self.__max_channel_color

    @property
    def data(self) -> np.ndarray:
        return self.__data

    @property
    def is_rgb(self) -> bool:
        return self.__color_type == ImageColorType.RGB

    @property
    def color_type(self) -> ImageColorType:
        return self.__color_type

    @data.setter
    def data(self, new_data: np.ndarray):
        if new_data is None:
            raise ValueError('Image data cannot be None.')
        if 2 > len(new_data.shape) > 4:
            raise ValueError(f'Invalid image data dimensions: {new_data.shape}')

        self.__data = new_data
        self.__dimensions = (new_data.shape[0], new_data.shape[1])

    def negative(self) -> 'Image':
        new_image = deepcopy(self)
        if self.is_rgb:
            new_image.data = self.max_channel_color - self.data[:, :, :3]
        else:
            new_image.data = self.max_channel_color - self.data
        return new_image

    def threshold(self, threshold: float = None) -> 'Image':
        if threshold is None:
            threshold = int(self.max_channel_color // 2)

        new_image = deepcopy(self)
        if self.is_rgb:
            new_image.data[:, :, :3][new_image.data < threshold] = 0
            new_image.data[:, :, :3][new_image.data >= threshold] = self.max_channel_color
        else:
            new_image.data[new_image.data < threshold] = 0
            new_image.data[new_image.data >= threshold] = self.max_channel_color

        return new_image

    def apply_mask(self, mask: SpatialMask) -> 'Image':
        new_image_matrix = mask.apply_mask(self.data.copy(), self.max_channel_color, self.color_type)
        result = copy(self)
        result.data = new_image_matrix
        return result

    def get_pixel_histogram(self) -> np.ndarray:
        if self.is_rgb:
            histogram = np.zeros(shape=(3, self.max_channel_color + 1), dtype=int)
            for i in range(self.dimensions[0]):
                for j in range(self.dimensions[1]):
                    for k in range(3):
                        histogram[k][self.data[i, j, k]] += 1
        else:
            histogram = np.zeros(self.max_channel_color + 1, dtype=int)
            for i in range(self.dimensions[0]):
                for j in range(self.dimensions[1]):
                    histogram[self.data[i, j]] += 1
        return histogram

    def histogram_equalized(self) -> 'Image':
        histogram = self.get_pixel_histogram()

        if self.is_rgb:
            p = histogram / np.sum(histogram, axis=1)
            g = np.zeros(shape=(3, self.max_channel_color + 1))
            for i in range(3):
                g[i][0] = p[i][0]
                for k in range(1, len(p[i])):
                    g[i][k] = p[i][k] + g[i][k - 1]

            equalized_colors = np.zeros((3, len(g)), dtype=int)
            for i in range(3):
                equalized_colors[i] = round(g[i] * self.max_channel_color)

            equalized_image = self.data.copy()
            for i in range(self.dimensions[0]):
                for j in range(self.dimensions[1]):
                    for k in range(3):
                        equalized_colors[i][j][k] = equalized_colors[k][self.data[i, j, k]]
        else:
            p = histogram / np.sum(histogram)
            g = np.zeros(self.max_channel_color + 1)
            g[0] = p[0]
            for i in range(1, len(p)):
                g[i] = p[i] + g[i - 1]
            equalized_colors = np.array([round(c * self.max_channel_color) for c in g], dtype=int)
            equalized_image = np.array([equalized_colors[original_color] for original_color in self.data], dtype=int)

        result = copy(self)
        result.data = equalized_image
        return result

    def erode(self, structuring_element: np.ndarray) -> 'Image':
        if self.color_type != ImageColorType.BINARY:
            raise ValueError('Can not erode a not Binary image')

        result = copy(self)
        result.data = morph_operations.erode(self.data, structuring_element)

        return result

    def dilate(self, structuring_element: np.ndarray) -> 'Image':
        if self.color_type != ImageColorType.BINARY:
            raise ValueError('Can not dilate a not Binary image')

        result = copy(self)
        result.data = morph_operations.dilate(self.data, structuring_element)

        return result

    def plot_on_axe(self, ax: axes.Axes):
        if self.is_rgb:
            reshaped = self.data
        else:
            reshaped = self.data
        ax.imshow(reshaped, cmap=self.color_type.value, interpolation='none', vmax=self.max_channel_color, vmin=0)

    def plot_histogram_on_axe(self, ax: axes.Axes):
        if self.is_rgb:
            channels = np.zeros(shape=(3, self.dimensions[0] * self.dimensions[1]), dtype=int)
            c = 0
            for i in range(self.dimensions[0]):
                for j in range(self.dimensions[1]):
                    for k in range(3):
                        channels[k][c] = self.data[i, j, k]
                        c += 1
            sns.histplot(channels[0], discrete=True, ax=ax)
            sns.histplot(channels[1], discrete=True, ax=ax)
            sns.histplot(channels[2], discrete=True, ax=ax)

        else:
            sns.histplot(self.data.reshape(-1), discrete=True, ax=ax)
