from PIL import Image
from PIL.ImageEnhance import Contrast
import numpy as np
import random
import os

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--contrast',
                    default=1.5,
                    dest='contrast',
                    help='scale contrast of the input image',
                    type=float
                    )
parser.add_argument('-t', '--threshold_scale',
                    default=1.3,
                    dest='scale',
                    help='Change threshold scaling for ascii values',
                    type=float
                    )

parser.add_argument('-ms', '--max_size',
                    default=200,
                    dest='max_size',
                    help='Change the maximum dimension of the output',
                    type=int
                    )

args = parser.parse_args()

MAX_SIZE = args.max_size
SCALE = args.scale
CONTRAST = args.contrast

CHAR_MAP = {15*SCALE : ["##"],
            25*SCALE : ["#+", "+#"],
            35*SCALE : ["/#", "#/"],
            45*SCALE : ["\+", '+\\'],
            55*SCALE : ["++"],
            65*SCALE : ["+*", "*+"],
            75*SCALE : ["+*", "*+"],
            85*SCALE : ["**"],
            95*SCALE : ["*.", ".*"],
            105*SCALE : ["o.", '.o'],
            115*SCALE : [".."]}

def image_to_ascii(image_file: str) -> np.ndarray:
    original = Image.open(image_file).convert('L')
    if max(original.size) > MAX_SIZE:
        factor = int(max(original.size)/MAX_SIZE)
    else:
        factor = 1

    original = original.resize((int(original.size[0]/factor), int(original.size[1]/factor)))
    original = Contrast(original).enhance(CONTRAST)
    
    im_arr = np.array(original)
    

    ascii = "\n"

    for x in range(len(im_arr)):
        for y in range(len(im_arr[0])):
            for key in CHAR_MAP:
                if im_arr[x][y] < key:
                    ascii += random.choice(CHAR_MAP[key])
                    break
            else:
                ascii += '  '

        ascii = ascii.rstrip()
        ascii += "\n"

    return ascii


if __name__ == '__main__':
    for file in os.listdir("images"):
        ascii = image_to_ascii(os.path.join("images", file))
        with open(os.path.join("asciis", ''.join(file.split(".")[:-1])+".txt"), 'w+') as f:
            f.write(ascii)