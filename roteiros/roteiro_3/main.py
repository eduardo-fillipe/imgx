from imgx.io.load import load_as_ppm
from imgx.io import visualization as vf

if __name__ == '__main__':
    img = load_as_ppm('../image_samples/lua.pgm')

    vf.plot_histogram(img.histogram_equalized())
    vf.plot_images([vf.PrintableAxe(img, 'Normal'), vf.PrintableAxe(img.histogram_equalized(), 'Histogram equalized')])
    # vf.plot_histogram(img.histogram_equalized(), True)
