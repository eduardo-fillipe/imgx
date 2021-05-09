from typing import NamedTuple
from imgx.types.image import Printable
from imgx.types.image import Image
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import math


class PrintableAxe(NamedTuple):
    printable: Printable
    ax_title: str


def plot_images(axes: list[PrintableAxe], title: str = None, markers: bool = False):
    lines = math.ceil(len(axes) / 3)
    for num, p in enumerate(axes):
        ax = plt.subplot(lines, min(len(axes), 3), num + 1)
        p.printable.plot_on_axe(ax)
        ax.set_title(p.ax_title)
        ax.axis('off' if not markers else 'on')
    if title is not None:
        plt.suptitle(title)
    plt.show()


def plot_histogram(img: Image, show_image=False):
    if show_image:
        ax: Axes = plt.subplot(1, 2, 2)
        ax.set_title(img.name)
        ax.axis('off')
        img.plot_on_axe(ax)

        ax = plt.subplot(1, 2, 1)
        ax.set_xlabel('Pixel Color')
        ax.set_title(f'Pixel histogram of "{img.name}"')
        img.plot_histogram_on_axe(ax)
    else:
        ax = plt.subplot(1, 1, 1)
        ax.set_xlabel('Pixel Color')
        ax.set_title(f'Pixel histogram of "{img.name}"')
        img.plot_histogram_on_axe(ax)

    plt.show()
