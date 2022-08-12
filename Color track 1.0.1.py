from math import floor
from PIL import Image, ImageColor, ImageStat
from os import listdir
from re import sub


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return floor(float(n) * multiplier + 0.5) / multiplier


def image_color(im_path, rec, mod):
    im = Image.open(im_path)
    im = im.crop(rec)
    stat = ImageStat.Stat(im)
    if mod == 0:
        return stat.mean
    elif mod == 1:
        return stat.rms


def get_diff(color_orig, color):
    return tuple(map(lambda x, x_orig: round_half_up(1 + (x - x_orig) / x_orig, 3), color, color_orig))


def apply_scale(color, differ):
    B, G, R = tuple(int(color[x:x + 2], 16) for x in (0, 2, 4))
    return tuple(map(lambda x, multiplier: min(int(round_half_up(x * multiplier)), 255), (R, G, B), differ))


def split_set(s, sep=' '):
    st, last_i = set(), 0
    for i, l in enumerate(s):
        if l in sep:
            if s[i - 1] not in sep and last_i:
                st.add(s[last_i + 1:i])
            last_i = i
    return st or set(s[last_i:]) or set(s)


def extract_color(lst, color='c'):
    colors = set()
    for e in lst:
        if f'{color}&' in e:
            colors.add(e)
    return colors


# adjust_mod = int(input('0 - add color mod, 1 - multiply color mod: '))
image_color_mod = 1
# image_color_mod = int(input('0 - avg image color, 1 - rms image color: '))

path = r'E:\Torrents\Series\Mars Red\clip\\'
# path = input(r'Full path to images sequence folder: ') + r'\\'
im_lst = listdir(path)
in_files = listdir()
clip = r'\clip(620.32,444.53,631.98,461.3)'
# clip = input(r'Clip points (e.g. \clip(81,44.33,128,68.67) or x1,y1,x2,y2): ')
if clip.isascii():
    if 'clip' in clip:
        clip = clip.lstrip(r'\clip(').rstrip(')')
    clip = tuple(int(round_half_up(x)) for x in clip.split(','))

print("Parsing images brightnesses...")
color_first = image_color(path + im_lst[0], clip, image_color_mod)
diffs = []
for im_name in im_lst[1:]:
    diff = get_diff(color_first, image_color(path + im_name, clip, image_color_mod))
    diffs.append(diff)


color_type = input('Enter what color to track (e.g. c, 2c, 3c, 4c): ')

line = input('Paste colors or lines:\n')

with open(f'RGB_scale_{["avg", "rms"][image_color_mod]}.txt', 'w') as output:
    while line:
        print(line, file=output)

        line_colors = list(filter(lambda x: x[:len(color_type)] == color_type, split_set(line, '\\{}')))
        for diff in diffs:
            new_line = str(line)

            for color in line_colors:
                r, g, b = apply_scale(color.strip(f'{color_type}&H'), diff)
                new_color = fr'{color_type}&H{b:02X}{g:02X}{r:02X}&'
                new_line = sub(color, new_color, new_line)

            print(new_line, file=output)
        line = input()
