from imgx.types.image import Image, ImageColorType


def save_as_ppm(img: Image, output_file: str):
    with open(output_file, 'w') as file:
        img_type = 'P1'
        if img.color_type == ImageColorType.SHADES_OF_GRAY:
            img_type = 'P2'
        elif img.color_type == ImageColorType.RGB:
            img_type = 'P3'

        file.write(f'{img_type}\n')

        for comment in img.comments:
            file.write(f'#{comment}\n')

        file.write(f'{img.dimensions[1]} {img.dimensions[0]}\n')

        file.write(f'{img.max_channel_color}\n')

        c = 0
        s = ''
        if img.color_type == ImageColorType.BINARY:
            data = img.data.reshape(-1)
            for color in data:
                s += f'{color}'
                c += 1
                if c == 70:
                    s += '\n'
                    c = 0
            file.write(s)
        else:
            for color in img.data.reshape(-1):
                file.write(f'{color}\n')

        file.write('\n')
