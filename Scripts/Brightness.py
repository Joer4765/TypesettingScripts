from PIL import Image, ImageColor, ImageStat
from os import listdir
from colorsys import hsv_to_rgb, rgb_to_hsv, hls_to_rgb, rgb_to_hls
from pyperclip import copy
import math


def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


def percentage(lst):
    origin, result = lst[0], [1]
    for i in range(1, len(lst)):
        result.append(1 + (lst[i] - origin) / origin)
    return result


def brightness_scale(R, G, B, scale, mod):

    def convert(decimals):
        return tuple(round(i * 255) for i in decimals)

    if mod == 0:
        H, L, S = rgb_to_hls(R / 255, G / 255, B / 255)
        return convert(hls_to_rgb(H, min([L * scale, 1]), S))
    if mod == 1:
        H, S, V = rgb_to_hsv(R / 255, G / 255, B / 255)
        return convert(hls_to_rgb(H, S, min([V * scale, 1])))


def rgb2ass(R, G, B):
    return '{:02X}{:02X}{:02X}'.format(int(B), int(G), int(R))



def matrix2text(matrix):
    s = '\n'.join(['\n'.join(lst) for lst in matrix])
    return s


# path = rf"{input('Path to images: ')}"
path = r'D:\Torrents\Series\[InariDuB] Червоний Марс [1080p]\Image sequence\\'
file_list = listdir(path)

values = []
print('Parsing images...')
for file in file_list:
    image = Image.open(path + file)
    values.append(calculate_brightness(image))
values = percentage(values)

mod, color, frames = int(input('HLS lightness - 0, HSV value - 1: ')), input('Colors:\n'), []
tail = color[:color.find('H') + 1]
color = color.strip(tail)
while True:
    if color:
        frame = []
        for value in values:
            b, g, r = ImageColor.getcolor(f"#{color}", "RGB")
            illuminated_rgb = brightness_scale(r, g, b, value, mod)
            illuminated_ass = rgb2ass(*illuminated_rgb)
            frame.append(tail + illuminated_ass + '&')
        frames.append(frame)
        color = input().strip(tail)
    else:
        break

copy(matrix2text(frames))
print('Brightness applied.\nNew colors copied to clip board.')
