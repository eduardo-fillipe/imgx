import numpy as np

from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vs
from imgx.types.image import Image
from imgx.mask.masks import MedianSpatialMask, OverlapStrategy


def remove_noise(img: Image) -> Image:
    pass


if __name__ == '__main__':
    normal_img = load_as_ppm('image_samples/lorem_s12_c02_just.pbm')
    img_just_noise = load_as_ppm('image_samples/lorem_s12_c02_just_noise.pbm')
    img_just_smooth = img_just_noise.apply_mask(MedianSpatialMask(size=3, overlap_strategy=OverlapStrategy.CROP,
                                                                  params={'order': 70}))

    save_as_ppm(img_just_smooth, 'img_just_smooth.pbm')
    vs.plot_images([vs.PrintableAxe(normal_img, "Normal Image"),
                    vs.PrintableAxe(img_just_noise, "Noised Image"),
                    vs.PrintableAxe(img_just_smooth, "Smoothed Image")], markers=True)
