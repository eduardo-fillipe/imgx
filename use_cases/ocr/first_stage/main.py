from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy
import time


def executar(normal_image_path, noised_image_path) :
    load_normal_start = time.time()
    normal_img = load_as_ppm(normal_image_path)
    load_normal_end = time.time()
    load_noise_start = time.time()
    img_just_noise = load_as_ppm(noised_image_path)
    load_noise_end = time.time()
    smoothing_start = time.time()
    img_just_smooth = img_just_noise.apply_mask(MedianSpatialMask(size=3, overlap_strategy=OverlapStrategy.CROP,
                                                                  params={'order': 70}))
    smoothing_end = time.time()
    save_result_start = time.time()
    save_as_ppm(img_just_smooth, normal_image_path.replace('normal', 'result', 1))
    save_result_end = time.time()

    print(f'Normal Image load time: {load_normal_end - load_normal_start} seconds.')
    print(f'Noised Image load time: {load_noise_end - load_noise_start} seconds.')
    print(f'Smoothing time: {smoothing_end - smoothing_start} seconds.')
    print(f'Saving time: {save_result_end - save_result_start} seconds.')

    vs.plot_images([vs.PrintableAxe(normal_img, "Normal Image"),
                    vs.PrintableAxe(img_just_noise, "Noised Image"),
                    vs.PrintableAxe(img_just_smooth, "Smoothed Image")], markers=True)


if __name__ == '__main__':
    print(f'first test case is starting')
    executar('../image_samples/normal/grupo_02_linhas_46_palavras_300.pbm', 'image_samples/noised/grupo_02_linhas_46_palavras_300.pbm')
    print(f'second test case is starting')
    executar('../image_samples/normal/grupo_02_linhas_48_palavras_500.pbm', 'image_samples/noised/grupo_02_linhas_48_palavras_500.pbm')
    print(f'third test case is starting')
    executar('../image_samples/normal/grupo_02_linhas_52_palavras_600.pbm', 'image_samples/noised/grupo_02_linhas_52_palavras_600.pbm')

