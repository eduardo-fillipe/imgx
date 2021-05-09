from imgx.image_io.load import load_as_ppm
from imgx.image_io.save import save_as_ppm
from imgx.image_io import visualization as vf
from imgx.image_io.visualization import PrintableAxe

if __name__ == '__main__':
    img = load_as_ppm('../image_samples/pimentoes.pgm')
    save_as_ppm(img.negative(), 'negative.ppm')
    save_as_ppm(img.threshold(), 'threshold.ppm')

    vf.plot_images([
        PrintableAxe(img, 'Normal'),
        PrintableAxe(img.negative(), 'Negative'),
        PrintableAxe(img.threshold(), 'Threshold')]
    )
