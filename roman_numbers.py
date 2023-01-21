"""Change arabic-numbers in to regular-numbers."""

ROMAN = ("I", "V", "X", "L", "C", "D", "M")


def main(number):
    """This function change arabic-numbers in to regular-numbers."""
    index = 0
    exception_count = ""
    if number > 3000:
        return "Number is wrong"

    while number:
        exception = ""
        cipher = number % 10
        if cipher == 4:
            exception += ROMAN[index] + ROMAN[index + 1]
        elif cipher == 9:
            exception += ROMAN[index] + ROMAN[index + 2]
        else:

            if cipher >= 5:
                exception += ROMAN[index + 1]
                cipher -= 5

            while cipher > 0:
                exception += ROMAN[index]
                cipher -= 1

        number = number // 10
        exception_count = exception + exception_count
        index += 2

    return exception_count
