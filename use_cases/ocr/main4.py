import numpy as np

from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy
from copy import copy
import time

if __name__ == '__main__':
    img = load_as_ppm('pequeno_smooth.pbm')
    se = np.ones(shape=(1, 13), dtype=int)

    dilated = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(np.ones(shape=(3, 3))).dilate(se).dilate(se.transpose())

    borders = dilated.subtract(dilated.erode(np.ones(shape=(3, 3), dtype=int)))
    result_data = img.data.copy()
    result = copy(img)

    for i in range(borders.data.shape[0]):
        for j in range(borders.data.shape[1]):
            if borders.data[i, j] == 1:
                result_data[i, j] = 1

    result.data = result_data

    vs.plot_images([
        # vs.PrintableAxe(img, "Normal"),
        vs.PrintableAxe(result, "Dilate")
    ], markers=True)