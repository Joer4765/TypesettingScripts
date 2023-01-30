from shutil import rmtree
from Transitions import t2fr, rgb2ass
from PIL import Image
from os import listdir, makedirs, path
from pyperclip import copy
from subprocess import run, PIPE, DEVNULL


def get_images(video_path, start_time, frames_count, folder=r'images'):
    print('Getting images...')
    result = run([
        'mpv',
        f'{video_path}',
        '--start=' + start_time,
        '--hr-seek=yes',
        '--sid=no',
        f'--frames={frames_count}',
        '--vo=image',
        '--vo-image-format=png',
        fr'--vo-image-outdir={path.dirname(path.abspath(__file__))}\{folder}',
    ], stdout=DEVNULL, encoding='utf-8')
    with open(f'{folder}/../log.txt', 'w') as log:
        print(video_path, start_time, frames_count, file=log, sep='\n')
    return result.stdout


def get_color(pos, file_path):
    image = Image.open(file_path)
    color = image.getpixel(pos)
    return color


start = 0
video_path = r'D:\Torrents\Series\Kubo-san wa Mob wo Yurusanai\Videos\ASW\[ASW] Kubo-san wa Mob wo Yurusanai - 01 [' \
             r'1080p HEVC][8E4CD0BE].mkv'
images_path = r'images'
makedirs(images_path, exist_ok=True)

start_time = '0:22:02.84'
frames_count = 51
reference_pos = (1022, 1078)

if not listdir(images_path):
    get_images(video_path, start_time, frames_count)
else:
    try:
        with open(f'{images_path}/../log.txt', 'r') as log:
            line = log.readline()
            if not line or line == '\n':
                get_images(video_path, start_time, frames_count)
            else:
                log_video_path, log_start_time, log_frames_count = line, log.readline(), int(log.readline())
                start_frame, log_start_frame = t2fr(start_time), t2fr(log_start_time)
                if start_frame >= log_start_frame and start_frame + frames_count <= log_start_frame + log_frames_count \
                        and video_path == log_video_path.strip('\n'):
                    start = start_frame - log_start_frame
                else:
                    get_images(video_path, start_time, frames_count)
    except IOError:
        get_images(video_path, start_time, frames_count)


images_list = listdir(images_path)
track_path = r'track.txt'

color_number = input('Color number: ') + 'c'
print('Getting colors...')
s = ''
try:
    with open(track_path, 'r') as track_file:
        while (line := track_file.readline()) != 'Position\n':
            pass
        track_file.readline()
        line = list(map(lambda x: round(float(x)), track_file.readline().split()))
        track_pos = (line[1], line[2])
        for image in images_list[start:-1]:
            s += f'\\{color_number}{rgb2ass(*get_color(reference_pos, f"{images_path}/{image}"))}\n'
            prev_track_pos = track_pos
            line = list(map(lambda x: round(float(x)), track_file.readline().split()))
            track_pos = (line[1], line[2])
            diff = (track_pos[0] - prev_track_pos[0], track_pos[1] - prev_track_pos[1])
            reference_pos = (reference_pos[0] + diff[0], reference_pos[1] + diff[1])
        s += f'\\{color_number}{rgb2ass(*get_color(reference_pos, f"{images_path}/{image}"))}\n'

except IOError:
    for image in images_list:
        s += f'\\{color_number}{rgb2ass(*get_color(reference_pos, f"{images_path}/{image}"))}\n'

copy(s)
print('Gotten colors:\n', s)
print('Copied to clipboard.')
delete = input('Delete encoded images? (y/n)\n')
if delete == 'y':
    rmtree(images_path)
