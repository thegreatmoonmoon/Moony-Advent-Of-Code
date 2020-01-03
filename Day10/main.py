"""
main.py
====================================
The core module for the Asteroid Finder
"""

import utilsfuncs as uf
import collections
from typing import OrderedDict, Union


def line_of_sight_finder(coordinates: list) -> tuple:
    """For each of the asteroids, render a straight line of sight to the other ones.
    If the line points do not corelate with any of the asteroids, increase the counter.
    Store the coordinates of the asteroid with the greatest counter."""

    maxv = 0
    for asteroidchecked in asteroidcoordinates:
        clearsightcounter = 0
        for asteroidcompared in asteroidcoordinates:
            if asteroidchecked == asteroidcompared:
                continue
            else:
                lineofsight = uf.line(asteroidchecked, asteroidcompared)
                if all(
                    map(
                        lambda x: False if x in asteroidcoordinates else True,
                        lineofsight,
                    )
                ):
                    clearsightcounter += 1
        # print(f"Asteroid with coordinates {asteroidchecked} -> eye contact with {clearsightcounter} another ones")
        if clearsightcounter > maxv:
            maxv = clearsightcounter
            maxresult = (asteroidchecked, clearsightcounter)

    return maxresult


def group_asteroids_by_angle(referalpoint: tuple, coordinates: list) -> OrderedDict:
    """For each of the coordinates passed to the function, an angle of the heading from the referal point is
    calculated and returned as degrees between the y-axis and the coordinate. Angle increases clockwise.
    Function returns an OrderedDict, with angles as keys and nested tuples of absolute coordinates, relative
    coordinates, and the diagonal distance" between the referalpoint and coordinate."""
    anglegrouper = {}
    for asteroidchecked in coordinates:
        if asteroidchecked == referalpoint:
            continue
        relativecoordinates = uf.relative_coordinates(referalpoint, asteroidchecked)
        relativeangle = uf.calculate_angle(*relativecoordinates)
        try:
            anglegrouper[relativeangle].append(
                (
                    asteroidchecked,
                    relativecoordinates,
                    uf.diagonal_distance((0, 0), relativecoordinates),
                )
            )
        except KeyError:
            anglegrouper[relativeangle] = [
                (
                    asteroidchecked,
                    relativecoordinates,
                    uf.diagonal_distance((0, 0), relativecoordinates),
                )
            ]

    return collections.OrderedDict(sorted(anglegrouper.items()))


def sort_dict_values(
    unsortdict: Union[dict, OrderedDict], key, reverse=True
) -> Union[dict, OrderedDict]:
    """Function to sort dictionary values by the passed key, reversed by default"""

    for item in unsortdict:
        unsortdict[item].sort(key=key, reverse=reverse)

    return None


if __name__ == "__main__":

    asteroidmap = uf.load_input("inputFiles/inputfile")

    asteroidmapmatrix = [[x for x in sublist] for sublist in asteroidmap]

    asteroidcoordinates = uf.array_lookup(asteroidmapmatrix, "#")

    monitoringstation = line_of_sight_finder(asteroidcoordinates)
    monitoringstationloc = monitoringstation[0]

    print("Best location to setup the monitoring station: ", monitoringstation)

    sortedanglegrouper = group_asteroids_by_angle(
        monitoringstationloc, asteroidcoordinates
    )

    sort_dict_values(sortedanglegrouper, lambda x: x[2])

    i = 1
    while True:
        for anglegroup in sortedanglegrouper:
            try:
                asteroidtoobliterate = sortedanglegrouper[anglegroup].pop()
            except IndexError:
                continue
            if i == 200:
                twohundredsthvaporization = asteroidtoobliterate
            print(
                f"{i}. Obliterating asteroid with coordinates {asteroidtoobliterate[0]}, relative coordinates {asteroidtoobliterate[1]}, at angle {anglegroup}"
            )
            i += 1

        print("Full laser rotation completed, checking if another run necessary...")
        if any(
            map(lambda x: True if len(x) > 0 else False, sortedanglegrouper.values())
        ):
            continue
        else:
            print("Armageddon completed, no more asteroids.")
            break

    print(
        f"The lucky asteroid vaporized as the 200th is located at: {twohundredsthvaporization[0]}"
    )
