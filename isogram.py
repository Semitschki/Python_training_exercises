'''Checking string for isogram.'''


def main(input_string):
    '''Isogram check.'''
    return len(input_string.lower()) == len(set(input_string.lower()))
