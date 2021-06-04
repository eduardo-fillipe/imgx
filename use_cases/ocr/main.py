from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy
import time


if __name__ == '__main__':
    load_normal_start = time.time()
    normal_img = load_as_ppm('image_samples/lorem_s12_c02_just.pbm')
    load_normal_end = time.time()
    load_noise_start = time.time()
    img_just_noise = load_as_ppm('image_samples/lorem_s12_c02_just_noise.pbm')
    load_noise_end = time.time()
    smoothing_start = time.time()
    img_just_smooth = img_just_noise.apply_mask(MedianSpatialMask(size=3, overlap_strategy=OverlapStrategy.CROP,
                                                                  params={'order': 70}))
    smoothing_end = time.time()
    save_result_start = time.time()
    save_as_ppm(img_just_smooth, 'img_just_smooth.pbm')
    save_result_end = time.time()

    print(f'Normal Image load time: {load_normal_end - load_normal_start} seconds.')
    print(f'Noised Image load time: {load_noise_end - load_noise_start} seconds.')
    print(f'Smoothing time: {smoothing_end - smoothing_start} seconds.')
    print(f'Saving time: {save_result_end - save_result_start   } seconds.')

    vs.plot_images([vs.PrintableAxe(normal_img, "Normal Image"),
                    vs.PrintableAxe(img_just_noise, "Noised Image"),
                    vs.PrintableAxe(img_just_smooth, "Smoothed Image")], markers=True)
