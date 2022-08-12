from math import floor
from PIL import Image, ImageColor, ImageStat
from os import listdir
from decimal import Decimal


def brightness(im_file, variant=2):
    # Favourite variant - 2
    im = Image.open(im_file)

    # Average pixel brightness.
    if variant == 1:
        im = im.convert('L')
        stat = ImageStat.Stat(im)
        return stat.mean[0]

    # RMS pixel brightness.
    if variant == 2:
        im = im.convert('L')
        stat = ImageStat.Stat(im)
        return stat.rms[0]

    # Average pixels, then transform to "perceived brightness".
    if variant == 3:
        stat = ImageStat.Stat(im)
        r, g, b = stat.mean
        return (0.299 * (r ** 2) + 0.587 * (g ** 2) + 0.114 * (b ** 2)) ** 0.5

    # RMS of pixels, then transform to "perceived brightness".
    if variant == 4:
        stat = ImageStat.Stat(im)
        r, g, b = stat.rms
        return (0.299 * (r ** 2) + 0.587 * (g ** 2) + 0.114 * (b ** 2)) ** 0.5

    # Calculate "perceived brightness" of pixels, then return average.
    if variant == 5:
        stat = ImageStat.Stat(im)
        gs = ((0.299 * (r ** 2) + 0.587 * (g ** 2) + 0.114 * (b ** 2)) ** 0.5
              for r, g, b in im.getdata())
        return sum(gs) / stat.count[0]


def round_half_up(n, decimals=0):
    if type(n) is not float and n.isdigit():
        n = float(n)
    multiplier = 10 ** decimals
    return floor(n * multiplier + 0.5) / multiplier


path = r'D:\Torrents\Series\Mars Red\Image sequence\\'
file_lst = listdir(path)


print("Parsing images' brightness...")
variants = [2]
first = [brightness(path + file_lst[0], i) for i in variants]
values = [[] for i in variants]

with open('Brightness.txt', 'w') as output:
    # print(*(1 for _ in range(len(variants))), file=output)
    for i, file in enumerate(file_lst):
        for j, variant in enumerate(variants):
            value = brightness(path + file, variant)
            value = 1 + (value - first[j]) / first[j]
            output.write(f'{value:.2f}    ')
            # output.write(str(round_half_up(value)).center(10))
        output.write('\n')
        print(f'{i + 1} frame completed.')


