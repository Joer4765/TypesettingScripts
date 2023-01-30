from Transitions import t2fr, fr2t

path = r'E:\Torrents\Series\Arknights - Reimei Zensou\Sub\Ukr\Full\Arknights - Reimei Zensou - 01 - ukr.ass'
with open(f'{path}', 'r+', encoding='Utf-8') as input_file:
    framerate = 24000 / 1001
    fields = ('Layer', 'Start', 'End', 'Style', 'Actor', 'MarginL', 'MarginR', 'MarginV', 'Effect', 'Text')
    while line := input_file.readline():
        cur_pos = input_file.tell()
        if 'fbf' in line:
            components = dict(zip(fields, line[10:-1].split(',', maxsplit=9)))
            components['Start'] = fr2t(t2fr(components['Start'], framerate) + int(components['Actor']) - 1,
                                       framerate)
            components['End'] = fr2t(t2fr(components['Start'], framerate) + 1, framerate)
            input_file.seek(prev_pos + 12)
            input_file.write(f'{components["Start"]},{components["End"]}')
            input_file.seek(cur_pos)
        prev_pos = cur_pos
