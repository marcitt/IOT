# this module gets the users text screen data

import pytesseract
from PIL import ImageGrab
import numpy as np

def detect_text():
    # first we need to get the user's screen information

    # temp hard-coded values
    width = 2560
    height = 1600

    img = ImageGrab.grab(bbox=(0, 0, width, height))
    np_img = np.array(img)

    text = pytesseract.image_to_string(np_img, lang="eng")

    # for initial implementation return simple word count
    return len(text.split())




