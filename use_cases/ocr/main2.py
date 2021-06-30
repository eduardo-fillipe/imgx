import numpy as np

from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy
import time

if __name__ == '__main__':
    img = load_as_ppm('pequeno_smooth.pbm')

    # se = np.array(
    #     [[0, 1, 0],
    #      [1, 1, 1],
    #      [0, 1, 0]], dtype=int)

    # se = [[0, 0, 1, 0, 0],
    #       [0, 0, 1, 0, 0],
    #       [1, 1, 1, 1, 1],
    #       [0, 0, 1, 0, 0],
    #       [0, 0, 1, 0, 0]]

    # se = np.array(se, dtype=int)

    se = np.ones(shape=(35, 19), dtype=int)

    vs.plot_images([
         vs.PrintableAxe(img, "Normal"),
                    vs.PrintableAxe(img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(se).dilate(se).dilate(se), "Dilate")], markers=True)
