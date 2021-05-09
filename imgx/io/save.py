from imgx.types.image import PPMImage


def save_as_ppm(img: PPMImage, output_file: str):
    with open(output_file, 'w') as file:
        file.write(f'{img.ppm_type}\n')

        for comment in img.comments:
            file.write(f'#{comment}\n')

        file.write(f'{img.dimensions[0]} {img.dimensions[1]}\n')

        file.write(f'{img.max_pixel_color}\n')

        for color in img.raw_data:
            file.write(f'{color}\n')

        file.write('\n')
