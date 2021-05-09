from imgx.image_io.load import load_as_ppm
from imgx.image_io import visualization as vf

if __name__ == '__main__':
    img = load_as_ppm('../image_samples/pimentoes.pgm')
    print(img.get_pixel_histogram())
    vf.plot_histogram(img)
