from re import sub, search, split


def t2fr(t, framerate=24000 / 1001):
    h, m, s = t.split(':')
    return round((int(h) * 3600 + int(m) * 60 + float(s) - 0.02) * framerate)


def fr2t(frame, framerate=24000 / 1001):
    seconds = frame / framerate
    return f'{seconds // 3600:.0f}:{seconds // 60 % 60:02.0f}:{seconds % 60 + 0.02:05.2f)}'


def rgb2ass(r, g, b):
    return f'&H{b:02X}{g:02X}{r:02X}&'


def get_simple_tag(text, tag):
    if tag in text:
        return float(search(fr'\\{tag}.*?[\\}}]', text).group()[len(tag) + 1:-1])


def get_complex_tag(text, tag):
    if tag in text:
        return tuple(float(i) for i in split(r'[^\d.]', search(fr'\\{tag}.*?[\\}}]', text).group()) if i)


def paste_tags(text, tag_name, tag_values):
    if tag_name in text:
        return sub(fr'{tag_name}.*?(?=[\\}}])', fr'{tag_name}{tag_values}'.replace(' ', ''), text)
    return fr'{{\{tag_name}{tag_values}{text[1:]}'
