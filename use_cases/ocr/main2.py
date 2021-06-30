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

    se = np.ones(shape=(79, 19), dtype=int)

    img = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(se).dilate(se).dilate(se)

    # vs.plot_images([
    #      vs.PrintableAxe(img, "Normal"),
    #                 vs.PrintableAxe(img, "Dilate")], markers=True)

    column_count = 0
    p = 0
    while True:
        if np.any(img.data[:, p] == 1):
            column_count += 1
            break
        p += 1

    print('p ', p)

    last = 1
    for j in range(p, img.data.shape[1]):
        if last == 0 and np.any(img.data[:, j]):
            column_count += 1
            last = 1
        elif np.alltrue(img.data[:, j] == 0):
            last = 0
        else:
            last = 1

    print(column_count)




