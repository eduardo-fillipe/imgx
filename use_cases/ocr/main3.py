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

    se = np.ones(shape=(3, 51), dtype=int)

    img2 = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(se)

    last = 0
    column_count = 0
    for i in range(img2.data.shape[0]):
        if last == 0 and np.any(img2.data[i, :]):
            print(i)
            print(list(img2.data[i, :]))
            column_count += 1
            last = 1
        elif np.alltrue(img2.data[i, :] == 0):
            last = 0
        else:
            last = 1

    print(column_count)

    vs.plot_images([
         # vs.PrintableAxe(img, "Normal"),
                    vs.PrintableAxe(img2, "Dilate")], markers=True)