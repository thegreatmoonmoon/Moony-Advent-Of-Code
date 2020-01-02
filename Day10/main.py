"""
main.py
====================================
The core module for the Asteroid Finder
"""

import utilsfuncs as uf


if __name__ == "__main__":

    asteroidmap = uf.load_input("inputFiles/inputfile")

    asteroidmapmatrix = [[x for x in sublist] for sublist in asteroidmap]

    asteroidcoordinates = uf.array_lookup(asteroidmapmatrix, "#")

    maxv = 0
    for asteroidchecked in asteroidcoordinates:
        clearsightcounter = 0
        for asteroidcompared in asteroidcoordinates:
            if asteroidchecked == asteroidcompared:
                continue
            else:
                lineofsight = uf.line(asteroidchecked, asteroidcompared)
                if all(map(lambda x: False if x in asteroidcoordinates else True, lineofsight)):
                    clearsightcounter += 1
        print(f"Asteroid with coordinates {asteroidchecked} -> eye contact with {clearsightcounter} another ones")
        if clearsightcounter > maxv:
            maxv = clearsightcounter
            maxresult = (asteroidchecked, clearsightcounter)

    print("Best location to setup the monitoring station: ", maxresult)
