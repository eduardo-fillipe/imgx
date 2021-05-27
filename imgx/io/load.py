import numpy as np
from imgx.types.image import Image, ImageColorType as Ct


def get_type_from_bpm(bpm_type: str) -> Ct:
    if bpm_type == 'P1':
        return Ct.BINARY

    if bpm_type == 'P2':
        return Ct.SHADES_OF_GRAY

    if bpm_type == 'P3':
        return Ct.RGB

    raise ValueError("Invalid bmp_type.")


def load_as_ppm(file_path: str) -> Image:
    with open(file_path, 'r') as file:
        lines = list(map(lambda x: x.rstrip(), file.readlines()))
        img_type = lines[0]

        color_type: Ct = get_type_from_bpm(img_type)
        img_channels_number = 1
        if color_type == Ct.RGB:
            img_channels_number = 3

        img_comments: list[str] = []
        comment: str = lines[1]
        index = 1
        while comment.startswith('#'):
            img_comments.append(comment[1:])
            index += 1
            comment = lines[index]

        dimensions = [int(i) for i in lines[index].split(' ')]
        dimensions[0], dimensions[1] = dimensions[1], dimensions[0]
        index += 1

        if color_type == Ct.BINARY:
            max_pixel_color = 1
        else:
            max_pixel_color = int(lines[index])
            index += 1

        data = list(map(lambda x: str(x).split(' ')
                        if color_type != Ct.BINARY
                        else list(filter(lambda c: c in ['1', '0'], list(x))),
                    lines[index:]))
        payload = np.array([int(color) for colors in data for color in colors if len(color) > 0])

        result_payload = payload.reshape((dimensions[0], dimensions[1])) if img_channels_number == 1 \
            else payload.reshape((dimensions[0], dimensions[1], img_channels_number))

        name_index = file_path.split('/')
        name = file_path if len(name_index) == 0 else name_index[-1]

        result_img = Image(data=result_payload, max_channel_color=max_pixel_color, color_type=color_type,
                           name=name,
                           origin_file_path=file_path,
                           comments=img_comments)
        return result_img
