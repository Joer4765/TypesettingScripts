from re import split, search, sub


tag_values = (123.234, 123.23)
tag_name = 'fsp'
text = r'{\blur0.6\pos(1061.7,522.44)\alpha&H00&\fsp16\c&HDDE6E5&\1a&H00&\fscx168\fscy168}Приречення'
print(sub(fr'{tag_name}.*?(?=[\\}}])', fr'{tag_name}{tag_values}'.replace(' ', ''), text))
