from math import floor


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return floor(n * multiplier + 0.5) / multiplier


with open('Brightness.txt', 'r+') as file:
    for line in file:
        separator = line.rfind('.') - 1
        n1 = line[:separator]
        n2 = line[separator:]
        # print('{:.2f}     {:.2f}'.format(*map(lambda x: round_half_up(float(x), 2), [n1, n2])))
        print('{:.2f}       {:.2f}'.format(*map(float, [n1, n2])))
