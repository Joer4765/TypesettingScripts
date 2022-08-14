with open('Brightness.txt') as file1, open('Brightness_2.txt') as file2, open('Brightness_compare.txt', 'w') as output:
    for line1, line2 in zip(file1, file2):
        print(line1.strip('\n'), line2, sep=' ' * 2, file=output, end='')