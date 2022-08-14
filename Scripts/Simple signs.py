from datetime import timedelta
import re

path = r'D:\Torrents\Series\Inou Battle Within Everyday Life [1080p;H265] (2014)\Subs\E02\Inou Battle Within Everyday ' \
       r'Life - 02 SIGNS CLEANED'
ex = '.ass'

with open(f'{path}{ex}', encoding='Utf-8') as input_file:
    file = [line.rstrip('\n').split(',', maxsplit=9) for line in input_file]

tail = file[:file.index(['[Events]']) + 2]
file = file[file.index(['[Events]']) + 2:]


def parts(line):
    text = line[9][line[9].rfind('}') + 1:]
    start = [float(i) for i in line[1].split(':')]
    start = start[0] * 360000 + start[1] * 6000 + start[2] * 100
    end = [float(i) for i in line[2].split(':')]
    end = end[0] * 360000 + end[1] * 6000 + end[2] * 100
    return {'text': text, 'start': start, 'end': end}


def all_text():
    for line in file:
        text = parts(line)['text']
        print(text)
    exit()


def letters_concatenate(file):
    concatenated = []
    text_pr = ''
    file.sort(key=lambda x: [x[1], x[0]])
    for line in file:
        text = parts(line)['text']
        if len(text) == 1 and len(text_pr) == 1:
            concatenated[-1][-1] += text
        else:
            concatenated.append(line)
        text_pr = text
    return concatenated


def lines_concatenate(file):
    concatenated, text_pr, end_pr = [], '', 0
    file.sort(key=lambda x: [x[9][x[9].rfind('}') + 1:], x[1]])
    for line in file:
        text, start, end = parts(line)['text'], parts(line)['start'], parts(line)['end']
        if text == text_pr and (abs(start - end_pr) <= 8 or end == end_pr):
            concatenated[-1][2] = str(timedelta(milliseconds=end * 10)).rstrip('0')
        else:
            concatenated.append(line)
        text_pr, end_pr = text, end

    return concatenated


file = letters_concatenate(file)
file = lines_concatenate(file)
file.sort(key=lambda x: [x[1], x[9][x[9].rfind('}') + 1:]])

with open(f'{path}_concatenated{ex}', mode='w', encoding='utf-8') as output_file:
    output_file.writelines('\n'.join([','.join(line) for line in tail]) + '\n')
    output_file.writelines('\n'.join([','.join(line) for line in file]))

# with open(f'{path}_concatenated{ex}', mode='r', encoding='utf-8') as output_file:
#     print(output_file.readlines())
