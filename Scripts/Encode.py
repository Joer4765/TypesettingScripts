from pprint import pprint
from os import system
from pymediainfo import MediaInfo
from glob import iglob
from os import path, makedirs


class Mode:
    def __init__(self, code: int):
        self.sub = code == 0
        self.dub = code == 1
        self.sub_type = ['full', 'signs'][code]

    def check_subs(self, sub_name):
        return self.sub_type in path.basename(sub_name).casefold()


def encode_options(options):
    return ' '.join(
        '--{}="{}"'.format(str(key).replace('_', '-'), str(val)) if val else '' for key, val in options.items())


def encode(input_file, **kwargs):
    command = f'mpv "{input_file}" {encode_options(kwargs)}'
    system(command)


def define_file(files, file_type):
    if not files:
        print(f'There is no {file_type}.')
        print(f'{file_type.capitalize()} excluded.')
        return
    elif len(files) > 1:
        for i, file in enumerate(files):
            print(f'{file_type.capitalize()} {i}: {path.basename(file)}')
        print()
        try:
            choose = files[int(input(f'Choose a {file_type}: '))]
            print()
            return choose
        except:
            print(f'{file_type.capitalize()} excluded.')
            return
    else:
        choose = files[0]
        print(f'Chosen {file_type} is {choose}\n')
        return choose


SCRIPT_DIRECTORY = path.dirname(path.abspath(__file__))
matching_formats = {
    'video': [
        'mkv',
        'mp4',
        'avi'
    ],
    'audio': [
        'aac',
        'flac',
        'opus',
        'ac3'
    ],
    'sub': [
        'ass',
        'srt'
    ]
}

mode = Mode(int(input('0 - sub,  1 - dub: ')))
print()
episode = input('Episode number: ')
print()
matched = {
    'video': [],
    'audio': [],
    'sub': []
}

for file_path in iglob(SCRIPT_DIRECTORY + f'/**/*[E _]{episode:>02}[ _]*', recursive=True):
    file_format = (file_path[file_path.rfind('.') + 1:])
    if file_format in matching_formats['video']:
        matched['video'].append(file_path)
    elif mode.dub and file_format in matching_formats['audio']:
        matched['audio'].append(file_path)
    elif mode.check_subs(file_path) and file_format in matching_formats['sub']:
        matched['sub'].append(file_path)

defined_video = define_file(matched['video'], 'video')
output_dir = f'{path.dirname(defined_video)}/../Encoded/'
makedirs(output_dir, exist_ok=True)
output_video_path = f'{output_dir}{path.basename(defined_video)[:-4]}_{mode.sub_type}.mp4'

media_info = MediaInfo.parse(defined_video)
video_audio_tracks = media_info.audio_tracks
audio_id = len(video_audio_tracks) + 1

if mode.sub:
    defined_audio = None
    if audio_id > 2:
        for audio in video_audio_tracks:
            print(f'Track {audio.stream_identifier}: {audio.other_language[0]}')
        print()
        try:
            audio_id = int(input(f'Choose an audio: '))
            print()
        except:
            print(f'Audio excluded.')
    else:
        audio_id = 1
else:
    defined_audio = define_file(matched['audio'], 'audio')

defined_sub = define_file(matched['sub'], 'sub')
sub_id = len(media_info.text_tracks) + 1 if defined_sub else 'no'

encode(defined_video,
       audio_file=defined_audio,
       aid=audio_id,
       vf='format=yuv420p,fps=23.976',
       o=output_video_path,
       ovcopts="profile=main,level=4.1,crf=23",
       sub_file=defined_sub,
       sid=sub_id,
       )
