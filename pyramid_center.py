'''Python training'''


def main(height):
    '''Return list with #-Pyramid centered'''
    pyramid = []
    for index in range(1, height + 1):
        pyramid.append(('#' * (index + (index - 1))).center(((height * 2) - 1), ' '))
    return pyramid
