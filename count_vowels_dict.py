"""Count the vowels and return in a dictionary."""


VOWELS = "aiuoe"


def main(word):
    """Count the vowels and return in a dictionary."""
    vowel_dictionary = {}
    for vowel in VOWELS:
        vowel_dictionary[vowel] = word.lower().count(vowel)
    return vowel_dictionary
