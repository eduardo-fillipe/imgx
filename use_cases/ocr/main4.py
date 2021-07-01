import numpy as np

from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy
import time

if __name__ == '__main__':
    img = load_as_ppm('pequeno_smooth.pbm')
    r = np.subtract(np.zeros(shape=(3, 3)), np.ones(shape=(3, 3)))
    se = np.ones(shape=(5, 7), dtype=int)

    dilated = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(se).dilate(se).dilate(se).dilate(se).erode(np.ones(shape=(5, 5), dtype=int))
    # result = dilated.subtract(dilated.erode(np.ones(shape=(5, 5), dtype=int)))

    vs.plot_images([
        # vs.PrintableAxe(img, "Normal"),
        vs.PrintableAxe(dilated, "Dilate")
    ], markers=True)
