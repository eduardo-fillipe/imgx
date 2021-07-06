import time

import numpy as np
from copy import copy
from imgx.io import visualization as vs
from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy

from imgx.io.load import load_as_ppm

STRUCTURING_ELEMENT_REMOVE_NOISE = np.ones(shape=(3, 3))
STRUCTURING_ELEMENT_COUNT_COLUMNS = np.ones(shape=(79, 19), dtype=int)
STRUCTURING_ELEMENT_COUNT_ROWS = np.ones(shape=(3, 51), dtype=int)


def remove_noise(img):
    return img.erode(STRUCTURING_ELEMENT_REMOVE_NOISE)


def count_columns(img):
    img = remove_noise(img). \
        dilate(STRUCTURING_ELEMENT_COUNT_COLUMNS). \
        dilate(STRUCTURING_ELEMENT_COUNT_COLUMNS). \
        dilate(STRUCTURING_ELEMENT_COUNT_COLUMNS)
    column_count = 0
    p = 0
    while True:
        if np.any(img.data[:, p] == 1):
            column_count += 1
            break
        p += 1
    last = 1
    for j in range(p, img.data.shape[1]):
        if last == 0 and np.any(img.data[:, j]):
            column_count += 1
            last = 1
        elif np.alltrue(img.data[:, j] == 0):
            last = 0
        else:
            last = 1
    return column_count


def count_rows(img):
    se = np.ones(shape=(3, 51), dtype=int)
    img2 = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(se).erode(np.ones(shape=(9,1), dtype=int))
    last = 0
    row_count = 0
    for i in range(img2.data.shape[0]):
        if last == 0 and np.any(img2.data[i, :]):
            row_count += 1
            last = 1
        elif np.alltrue(img2.data[i, :] == 0):
            last = 0
        else:
            last = 1
    return row_count

def detect_words(img):
    se = np.ones(shape=(1, 13), dtype=int)
    dilated = img.erode(np.ones(shape=(3, 3), dtype=int)).dilate(np.ones(shape=(3, 3))).dilate(se).dilate(
        se.transpose())
    borders = dilated.subtract(dilated.erode(np.ones(shape=(3, 3), dtype=int)))
    result_data = img.data.copy()
    result = copy(img)

    for i in range(borders.data.shape[0]):
        for j in range(borders.data.shape[1]):
            if borders.data[i, j] == 1:
                result_data[i, j] = 1

    result.data = result_data

    return result

def remove_noise_median_mask(img):
    smoothing_start = time.time()
    img_result = img.apply_mask(MedianSpatialMask(size=3, overlap_strategy=OverlapStrategy.CROP,
                                                                  params={'order': 70}))
    smoothing_end = time.time()
    print(f'Smoothing time: {smoothing_end - smoothing_start} seconds.')

    return img_result

if __name__ == '__main__':
    print('Starting...')
    print('loading image...')
    img = load_as_ppm('../image_samples/noised/grupo_02_linhas_52_palavras_600.pbm')
    print('removing noise...')
    img_without_noised = remove_noise_median_mask(img)
    start_counting_column_time = time.time()
    print('counting columns...')
    number_of_columns = count_columns(img_without_noised)
    print('Number of columns: ' + str(number_of_columns))
    end_counting_column_time = time.time()
    print('time elapsed to count columns: ' + str(end_counting_column_time - start_counting_column_time) + ' seconds')
    start_counting_row_time = time.time()
    print('couting rows...')
    number_of_rows = count_rows(img_without_noised)
    end_counting_row_time = time.time()
    print('Number of rows: ' + str(number_of_rows))
    print('time elapsed to count rows: ' + str(end_counting_row_time - start_counting_row_time) + ' seconds')
    print('detecting words...')
    start_detecting_time = time.time()
    img_with_detected_words = detect_words(img_without_noised)
    end_detecting_time = time.time()
    print('time elapsed to detect words: ' + str(end_detecting_time - start_detecting_time) + ' seconds')
    vs.plot_images([
                    vs.PrintableAxe(img_with_detected_words, "number of columns: " + str(number_of_columns) +
                                   ' number of rows: ' + str(number_of_rows))], markers=True)