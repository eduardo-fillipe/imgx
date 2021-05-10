import numpy as np
import matplotlib.axes as axes
import seaborn as sns
import copy
from imgx.mask.masks import SpatialMask


class Printable:
    def plot_on_axe(self, ax: axes.Axes):
        pass

    def plot_histogram_on_axe(self, ax: axes.Axes):
        pass


class Image(Printable):
    def __init__(self, name: str, origin_file_path: str, dimensions: tuple[int, int], max_pixel_color: int,
                 channels_number: int = 3, description: str = 'This is a types', comments: list[str] = '',
                 raw_data: np.ndarray = None):
        self.name = name
        self.origin_file_path = origin_file_path
        self.description = description
        self.dimensions = dimensions
        self.max_pixel_color = max_pixel_color
        self.comments = comments
        self.channels_number = channels_number
        if raw_data is None:
            self.raw_data = np.zeros(dimensions[0] * dimensions[1] * channels_number, dtype=int)
        elif raw_data.shape[0] == dimensions[0] * dimensions[1] * channels_number:
            self.raw_data = raw_data
        else:
            raise ValueError(f'Inconsistent Raw Data dimensions: {raw_data.shape[0]} instead of '
                             f'{dimensions[0] * dimensions[1] * channels_number}')

    def negative(self) -> 'Image':
        pass

    def threshold(self, threshold: float = 127) -> 'Image':
        pass

    def get_pixel_histogram(self) -> np.ndarray:
        pass

    def histogram_equalized(self) -> 'Image':
        pass

    def apply_mask(self, mask: SpatialMask) -> 'Image':
        pass

    def get_image_matrix(self) -> np.ndarray:
        pass

    def copy(self) -> 'Image':
        return copy.deepcopy(self)


class PPMImage(Image):

    def __init__(self, name: str, origin_file_path: str, ppm_type: str, dimensions: tuple[int, int],
                 max_pixel_color: int, channels_number: int = 3, description: str = 'This is a image.',
                 comments: list[str] = '', raw_data: np.ndarray = None):
        super().__init__(name, origin_file_path, dimensions, max_pixel_color, channels_number, description, comments,
                         raw_data)
        self.ppm_type = ppm_type

    def negative(self) -> 'PPMImage':
        new_image = self.copy()
        new_image.raw_data = self.max_pixel_color - self.raw_data
        return new_image

    def threshold(self, threshold: float = 127) -> 'PPMImage':
        new_image = self.copy()

        new_image.raw_data[new_image.raw_data < threshold] = 0
        new_image.raw_data[new_image.raw_data >= threshold] = 255

        return new_image

    def get_image_matrix(self) -> np.ndarray:
        return self.raw_data.copy().reshape(self.dimensions)

    def apply_mask(self, mask: SpatialMask) -> 'PPMImage':
        new_image_matrix = mask.apply_mask(self.get_image_matrix(), self.max_pixel_color)
        result = self.copy()
        result.dimensions = new_image_matrix.shape
        result.raw_data = new_image_matrix.reshape(-1)
        return result

    def get_pixel_histogram(self) -> np.ndarray:
        histogram = np.zeros(self.max_pixel_color + 1, dtype=int)
        for color in self.raw_data:
            histogram[color] += 1

        return histogram

    def histogram_equalized(self) -> 'PPMImage':
        histogram = self.get_pixel_histogram()
        p = histogram / sum(histogram)  # Nesse ponto, p é o vetor de probabilidades
        print(p)
        g = np.zeros(self.max_pixel_color + 1)
        g[0] = p[0]
        for i in range(1, len(p)):
            g[i] = p[i] + g[i - 1]

        # Nesse ponto, g é o vetor de probabilidades acumuladas
        # Equalização das cores
        equalized_colors = np.array([round(c * self.max_pixel_color) for c in g], dtype=int)
        # Criação da imagem resultado, cada cor na imagem original é substituída pela equalização correspondente
        equalized_image = np.array([equalized_colors[original_color] for original_color in self.raw_data], dtype=int)

        result = self.copy()
        result.raw_data = equalized_image
        return result

    def plot_on_axe(self, ax: axes.Axes):
        ax.imshow(self.raw_data.reshape(self.dimensions if self.channels_number == 1
                                        else (self.dimensions[0], self.dimensions[1], self.channels_number)),
                  cmap='gray', interpolation='none', vmax=self.max_pixel_color)

    def plot_histogram_on_axe(self, ax: axes.Axes):
        sns.histplot(self.raw_data, discrete=True, ax=ax)
