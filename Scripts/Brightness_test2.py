from math import floor
from PIL import Image, ImageColor, ImageStat
from os import listdir
from decimal import Decimal
from pyperclip import copy


def rgb2hsBrightness(R, G, B, mod=1):
    R, G, B = R / 255, G / 255, B / 255

    """Brightness"""
    # The Average of the Smallest and Largest
    if mod == 1:
        L = (max(R, G, B) + min(R, G, B)) / 2
    # Luma
    elif mod == 2:
        L = 0.212 * R + 0.701 * G + 0.087 * B
    # Weighted Euclidean Norm of the [R, G, B] Vector
    elif mod == 3:
        L = (0.299 * (R ** 2) + 0.587 * (G ** 2) + 0.114 * (B ** 2)) ** 0.5

    """Hue"""
    V = max(R, G, B)
    C = V - min(R, G, B)
    if C == 0:
        H = 0
    elif V == R:
        H = ((G - B) / C) % 6
    elif V == G:
        H = 2 + (B - R) / C
    elif V == B:
        H = 4 + (R - G) / C

    """Saturation"""
    # Sl
    if L == 0 or L == 1:
        S = 0
    else:
        S = (V - L) / min(L, 1 - L)
    # # Sv
    # if V == 0:
    #     S = 0
    # else:
    #     S = C / V

    return H, S, L

def hsBrightness2rgb(H, S, L):
    C = (1 - abs(2 * L - 1)) * S
    X = C * (1 - abs(H % 2 - 1))

    if 0 <= H < 1:
        R1, G1, B1 = C, X, 0
    elif 1 <= H < 2:
        R1, G1, B1 = X, C, 0
    elif 2 <= H < 3:
        R1, G1, B1 = 0, C, X
    elif 3 <= H < 4:
        R1, G1, B1 = 0, X, C
    elif 4 <= H < 5:
        R1, G1, B1 = X, 0, C
    elif 5 <= H < 6:
        R1, G1, B1 = C, 0, X

    m = L - (C / 2)
    R, G, B = R1 + m, G1 + m, B1 + m
    R, G, B = map(lambda x: round_half_up(x * 255), (R, G, B))

    return R, G, B

def round_half_up(n, decimals=0):
    if type(n) is str and n.isdigit():
        if '.' in n:
            n = float(n)
        else:
            n = int(n)
    multiplier = 10 ** decimals
    return floor(n * multiplier + 0.5) / multiplier

def get_diff(position, L_first, mod):
    color = image.getpixel(position)
    _, _, L = rgb2hsBrightness(*color, mod)
    differ = 1 + (L - L_first) / L_first
    return round_half_up(differ, 3)



def apply_scale(color, scale, mod):
    B, G, R = (int(color[x:x + 2], 16) for x in (0, 2, 4))
    H, S, L = rgb2hsBrightness(R, G, B, mod)
    R, G, B = hsBrightness2rgb(H, S, min(L * scale, 1))
    return R, G, B


variant = 3
# variant = int(input())

path = r'D:\Torrents\Series\Mars Red\Image sequence\\'
# path = input(r'Full path to images sequence folder: ') + r'\\'
file_lst = listdir(path)
pos = (1101, 491)
# pos = tuple(map(int, input('Source color pixel position - x y: ').split()))
print("Parsing images brightnesses...")


image = Image.open(path + file_lst[0])
color_first = image.getpixel(pos)
_, _, l_first = rgb2hsBrightness(*color_first, variant)

diffs = []
for file in file_lst[1:]:
    image = Image.open(path + file)
    diff = get_diff(pos, l_first, variant)
    diffs.append(diff)


sign_color_first = input('Signs colors:\n')
tail = sign_color_first[:sign_color_first.find('H') + 1]
sign_color = sign_color_first.strip(tail)

with open('Brightness_var3_Sl.txt', 'w') as output:
    while sign_color:
        output.write(f'{tail}{sign_color}&\n')

        for diff in diffs:
            r, g, b = map(int, apply_scale(sign_color, diff, variant))
            output.write(f'{tail}{b:02X}{g:02X}{r:02X}&\n')

        sign_color = input().strip(tail)
