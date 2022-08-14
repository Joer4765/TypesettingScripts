import re

string = r'{\blur1\bord0\fs150\fnKuenstler 165 Original\c&H3C1F53&\4c&HBDE2FF&\3c&H54267D&\pos(1062.26,' \
         r'468.16)\yshad2\fscx55\fscy55}К{\c&H3F2058&\4c&HC7E6FF&}о{\c&H41215C&\4c&HCBE7FF&}р{' \
         r'\c&H442161&\4c&HCEE9FF&}о{' \
         r'\c&H472266&\4c&HD1EAFF&}л{\c&H49236A&\4c&HD3EBFF&}ь {\c&H4C246F&\4c&HD7EDFF&}д{\c&H4E2573&\4c&HD9EDFF&}у{' \
         r'\c&H512678&\4c&HDAEEFF&}р{\c&H54267D&\4c&HDCEFFF&}н{\c&H562781&\4c&HDEEFFF&}і{\c&H592886&\4c&HDFF0FF&}в '


def split(s, sep=' '):
    st, last_i = set(), len(s) + 2
    for i, l in enumerate(s):
        if l in sep:
            if i - last_i > 1:
                st.add(s[last_i + 1:i])
            last_i = i
    return st


def extract_color(lst, color='c'):
    colors = set()
    for e in lst:
        if f'{color}&' in e:
            colors.add(e)


arr = split(string, '\\{}')
extract_color(arr)


# print(re.sub(new_color, old_color, line))