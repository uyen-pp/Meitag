
from PIL import UnidentifiedImageError
from PIL import Image

def check_image(path):
    try:
        Image.open(path)
    except UnidentifiedImageError:
        return False
    except IsADirectoryError:
        return False
    return True

def read_image(path):
    try:
        image = Image.open(path)
    except UnidentifiedImageError:
        return None
    except IsADirectoryError:
        return None
    return image

