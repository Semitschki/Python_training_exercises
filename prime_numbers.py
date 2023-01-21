"""Counts the prime-numbers in a list."""


def main(numbers):
    """This function counts the prime-numbers."""
    primes = list()
    for number in numbers:
        if(number <= 1) or (number == 4):
            continue

        for div in range(2, int(number * 0.5)):
            if number % div == 0:
                break
        else:
            primes.append(number)
    return len(primes)
