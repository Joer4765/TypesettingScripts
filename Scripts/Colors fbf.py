from PIL import Image
from os import listdir
from pyperclip import copy


path = r'E:\Torrents\Series\Mars Red\Image sequence E11\\'
file_list = listdir(path)
# pos = tuple(map(int, input('x y: ').split()))

pos = (1165, 488)
phylum = input('Номер кольору: ') + 'c'


def rgb_to_ass(r, g, b):
    return '{:02X}{:02X}{:02X}'.format(b, g, r)
    # return format(b, '02X') + format(g, '02X') + format(r, '02X')


def get_colors(pos, files):
    result = []
    for file in files:
        image = Image.open(path + file)
        color = image.getpixel(pos)
        color = fr'\{phylum}&H{rgb_to_ass(*color)}&'
        result.append(color)
    return result


print('Збираю кольори...')
colors = get_colors(pos, file_list)
s = '\n'.join(colors)
copy(s)
print('Кольори зібрано і скопійовано до буфера обміну.')
