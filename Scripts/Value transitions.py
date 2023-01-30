from pyonfx import *
from Transitions import get_complex_tag, get_simple_tag, paste_tags

io = Ass(r"Input.ass", keep_original=False)
meta, styles, lines = io.get_data()

tags = {}
for line in lines:
    if line.start_time == lines[0].start_time:
        text = line.raw_text
        orig_pos = get_complex_tag(text, 'pos')
        orig_fsp = get_simple_tag(text, 'fsp')
        orig_fscx = get_simple_tag(text, 'fscx') or 100
        orig_fscy = get_simple_tag(text, 'fscy') or 100
    text = line.raw_text
    pos = get_complex_tag(text, 'pos')

    if not pos:
        continue
    tags['pos'] = (orig_pos[0], pos[1])
    tags['fsp'] = orig_fsp * (orig_pos[0] / pos[0]) ** 10
    # tags['fscx'] = orig_fscx * (pos[1] / orig_pos[1]) ** 3
    # tags['fscy'] = orig_fscy * (pos[1] / orig_pos[1]) ** 3
    for name, value in tags.items():
        text = paste_tags(text, name, value)
    line.text = text
    io.write_line(line)

io.save()
io.open_aegisub()
