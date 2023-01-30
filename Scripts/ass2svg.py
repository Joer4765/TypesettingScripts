import re


def ass_to_svg(infilename):
    with open(infilename, 'r', encoding='Utf-8') as f:
        lines = f.readlines()
    paths = []
    for line in lines:
        color_search = re.search("\\\\1{0,1}c&H([a-zA-Z0-9]+)&", line)
        c = color_search[1]
        color = c[4:6] + c[2:4] + c[0:2]
        path_search = re.search("}([-.a-zA-Z0-9 ]+)", line)
        p = path_search[1]
        path = re.sub("m", "M", p)
        path = re.sub("l", "L", path)
        path = re.sub("b", "C", path)
        p_str = f"<path d=\"{path}\" fill=\"#{color}\"/>"
        paths.append(p_str)
    paths_str = "".join(paths)
    bp = f"<svg height=\"1080\" width=\"1920\">{paths_str}</svg>"
    print(bp)


ass_to_svg(r'D:\Torrents\Series\Kubo-san wa Mob wo Yurusanai\Sub\Ukr\Signs\text.txt')
