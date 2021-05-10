from imgx.io.load import load_as_ppm
from imgx.io.save import save_as_ppm
from imgx.io import visualization as vf
from imgx.io.visualization import PrintableAxe

if __name__ == '__main__':
    img = load_as_ppm('../image_samples/lua.pgm')
    save_as_ppm(img, 'same_image.ppm')
    save_as_ppm(img.negative(), 'negative.ppm')
    save_as_ppm(img.threshold(), 'threshold.ppm')

    vf.plot_images([
        PrintableAxe(img, 'Normal'),
        # PrintableAxe(img.negative(), 'Negative'),
        # PrintableAxe(img.threshold(), 'Threshold')
        ]
    )
