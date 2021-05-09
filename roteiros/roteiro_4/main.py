from imgx.io.load import load_as_ppm
from imgx.io import visualization as vs
from imgx.mask.masks import AverageSpatialMask, MedianSpatialMask, IdentitySpatialMask

if __name__ == '__main__':
    img = load_as_ppm('../image_samples/pimentoes.pgm')
    size = 11
    vs.plot_images([
        vs.PrintableAxe(img, "ORIGINAL"),
        vs.PrintableAxe(img.apply_mask(IdentitySpatialMask()), "IDENTITY"),
        vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size)), "AVERAGE"),
        vs.PrintableAxe(img.apply_mask(MedianSpatialMask(size=size, params={'order': 0})), f"MEDIAN: {0}"),
        vs.PrintableAxe(img.apply_mask(MedianSpatialMask(size=size)), f"MEDIAN"),
        vs.PrintableAxe(img.apply_mask(MedianSpatialMask(size=size, params={'order': 100})), f"MEDIAN: {100}")
    ], title=f'Spatial Smoothing Masks applied to: {img.name}')

    # vs.plot_images([
    #     vs.PrintableAxe(img, "ORIGINAL"),

    #     vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size, overlap_strategy=OverlapStrategy.PADDING_MAX)),
    #                     "AVERAGE: PADDING_MIN"),
    #     vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size, overlap_strategy=OverlapStrategy.PADDING_MAX)),
    #                     "AVERAGE: PADDING_MAX"),
    #     vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size, overlap_strategy=OverlapStrategy.PADDING_MEAN)),
    #                     "AVERAGE: PADDING_MEAN"),
    #     vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size, overlap_strategy=OverlapStrategy.CROP)),
    #                     "AVERAGE: CROP"),
    #     vs.PrintableAxe(img.apply_mask(AverageSpatialMask(size=size, overlap_strategy=OverlapStrategy.PARTIAL_APPLY)),
    #                     "AVERAGE: PARTIAL_APPLY"),
    # ])
