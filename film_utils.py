"""Add module which search movies in a csv-file."""

import csv


TITLE_IDX = 2
GENRE_IDX = 3
LENGTH_IDX = 1
YEAR_IDX = 0
POPULARITY_IDX = 7
MANDATORY_IDX = (GENRE_IDX, LENGTH_IDX, YEAR_IDX, POPULARITY_IDX)


def _iter_rows(path):
    """This function open a csv-file."""
    with open(path, encoding="Latin1") as csvfile:
        reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONE)
        try:
            next(reader)
            next(reader)
        except StopIteration:
            raise Exception("csv-file to short")
        yield from reader


def create_dict(row, append_popularity=False):
    """This function create a dictionary."""
    movie = {
        "Title": row[TITLE_IDX],
        "Genre": row[GENRE_IDX],
        "Length": int(row[LENGTH_IDX]),
        "Year": int(row[YEAR_IDX]),
    }
    if append_popularity:
        movie["popularity"] = int(row[POPULARITY_IDX])
    return movie


def search_title(path, title, all_results=True):
    """This function search a title in a csv-file."""
    movies_info = []
    if title == "":
        return movies_info

    for row in _iter_rows(path):
        if (row[TITLE_IDX] == "") or (row[LENGTH_IDX] == ""):
            continue
        elif title in row[TITLE_IDX]:
            movies_info.append(create_dict(row))

            if not all_results:
                break

    return movies_info


def get_genres(path):
    """This function search all movie genre in a csv-file."""
    return set(row[GENRE_IDX] for row in _iter_rows(path) if row[GENRE_IDX])


def get_popular_films(path):
    """This function show all popular movie from all genre."""
    movies = {}
    for row in _iter_rows(path):
        if any((row[idx] == "") for idx in MANDATORY_IDX):
            continue

        genre = row[GENRE_IDX]
        popularity = int(row[POPULARITY_IDX])
        if genre not in movies:
            movies[genre] = create_dict(row, append_popularity=True)
        else:
            actually_popularity = movies[genre]["popularity"]

            if ((popularity > actually_popularity) or
                    (popularity == actually_popularity) and
                    (int(row[YEAR_IDX]) > movies[genre]["Year"])):
                movies[genre] = create_dict(row, append_popularity=True)

    for value in movies.values():
        del value["popularity"]

    return movies
