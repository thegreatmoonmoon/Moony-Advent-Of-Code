import utilsfuncs


def count_oribits_recur(body, orbitmap):
    #filter for orbiting body match, make it a list
    bodyfilter = list(filter(lambda x: x if x[1] == body else None, orbitmap))
    if len(bodyfilter) == 0:
        return 0
    else:
        return count_oribits_recur(bodyfilter[0][0], orbitmap) + 1



if __name__ == '__main__':

    orbitmap = utilsfuncs.load_input("inputFiles/inputfile.csv")
    orbitmapdenormalized = [y for x in orbitmap for y in x]
    uniquebodies = set(orbitmapdenormalized)


    orbits = 0
    for body in uniquebodies:
        orbits += count_oribits_recur(body, orbitmap)

    print(orbits)