from imgx.types.image import Image


def save_as_ppm(img: Image, output_file: str):
    with open(output_file, 'w') as file:
        img_type = 'P1'
        if img.channels_number >= 3:
            img_type = 'P3'
        elif img.max_channel_color > 1:
            img_type = 'P2'

        file.write(f'{img_type}\n')

        for comment in img.comments:
            file.write(f'#{comment}\n')

        file.write(f'{img.dimensions[0]} {img.dimensions[1]}\n')

        file.write(f'{img.max_channel_color}\n')

        for color in img.data.reshape(-1):
            file.write(f'{color}\n')

        file.write('\n')
