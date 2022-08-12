import subprocess
from os import listdir, chdir, system

path = r"E:\Torrents\Series\Gankutsuou\[WSE] Gankutsuou The Count of Monte Cristo [BD x264 720p FLAC][Dual Audio]"
files = listdir(path)
sub_count = 2
ext = '.mkv'
chdir(path)
for file in files:
    if ext in file:
        command = f'mkvmerge -i "{file}"'
        s = subprocess.check_output(command)
        arr = str(s).split('\\n')
        for i in arr:
            if "subtitles" in i:
                ID = i[i.find('ID') + 3]
                command = f'mkvextract tracks "{file}" {ID}:"Subs\\{ID}_{file.strip(ext)}.ass"'
                system(command)

