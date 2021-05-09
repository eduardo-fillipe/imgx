import numpy as np
from imgx.image_types.image import PPMImage


def load_as_ppm(file_path: str) -> PPMImage:
    with open(file_path, 'r') as file:
        lines = list(map(lambda x: x.rstrip(), file.readlines()))
        img_type = lines[0]

        img_comments: list[str] = []
        comment: str = lines[1]
        index = 1
        while comment.startswith('#'):
            img_comments.append(comment[1:])
            index += 1
            comment = lines[index]

        dimensions = [int(i) for i in lines[index].split(' ')]
        img_dimensions = (dimensions[0], dimensions[1])
        index += 1

        max_pixel_color = int(lines[index])
        index += 1

        data = list(map(lambda x: str(x).split(' '), lines[index:]))
        payload = np.array([int(color) for colors in data for color in colors if len(color) > 0])

        img_channels_number = 1
        if img_type == 'P3':
            img_channels_number = 3

        name_index = file_path.split('/')
        name = file_path if len(name_index) == 0 else name_index[-1]

        result = PPMImage(name, file_path, img_type, img_dimensions, max_pixel_color,
                          channels_number=img_channels_number, comments=img_comments, raw_data=payload)
        return result
