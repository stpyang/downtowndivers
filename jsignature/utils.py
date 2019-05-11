"""
    Very inspired by zivezab's django-autograph
    https://github.com/zivezab/django-autograph/blob/master/autograph/utils.py
"""
import json
from itertools import chain
from PIL import Image, ImageDraw, ImageOps

AA = 5  # super sampling gor antialiasing


def draw_signature(data, as_file=False):
    """ Draw signature based on lines stored in json_string.
        `data` can be a json object (list in fact) or a json string
        if `as_file` is True, a temp file is returned instead of Image instance
    """

    if isinstance(data, str):
        drawing = json.loads(data)
    elif isinstance(data, list):
        drawing = data
    else:
        raise ValueError

    # Compute box
    width = max(chain(*[d['x'] for d in drawing])) + 10
    height = max(chain(*[d['y'] for d in drawing])) + 10

    # Draw image
    image = Image.new("RGBA", (width*AA, height*AA))
    draw = ImageDraw.Draw(image)
    for line in drawing:
        len_line = len(line['x'])
        points = [(line['x'][i]*AA, line['y'][i]*AA)
                  for i in range(0, len_line)]
        draw.line(points, fill="#000", width=2*AA)
    image = ImageOps.expand(image)
    # Smart crop
    bbox = image.getbbox()
    if bbox:
        image.crop(bbox)

    image.thumbnail((width, height), Image.ANTIALIAS)

    if as_file:
        ret = image._dump(format='PNG')
    else:
        ret = image

    return ret
