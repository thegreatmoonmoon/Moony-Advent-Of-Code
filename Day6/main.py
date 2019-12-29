import utilsfuncs


def count_orbits_recur(body, orbitmap):
    #filter for orbiting body match, make it a list
    bodyfilter = list(filter(lambda x: x if x[1] == body else None, orbitmap))
    if len(bodyfilter) == 0:
        return 0
    else:
        return count_orbits_recur(bodyfilter[0][0], orbitmap) + 1

def count_orbits_to_specific_recur(body, orbitmap, stoppoint):
    #filter for orbiting body match, make it a list
    bodyfilter = list(filter(lambda x: x if x[1] == body else None, orbitmap))
    if bodyfilter[0] == stoppoint:
        return 0
    else:
        return count_orbits_to_specific_recur(bodyfilter[0][0], orbitmap, stoppoint) + 1

def path_to_COM(currentorbit, orbitmap, path_appender):
    pathfilter = list(filter(lambda x: x if x[1] == currentorbit else None, orbitmap))
    if currentorbit != 'COM':
        path_appender(pathfilter[0])
        return path_to_COM(pathfilter[0][0], orbitmap, path_appender)
    else:
        return None

def list_builder_factory():
    """Function factory with a closure list attribute"""
    builtlist = []
    def list_appender(element):
        """Appends an element to the outer funtion list, returns True"""
        builtlist.append(element)
        return True
    return list_appender

def get_first_common(list1, list2):
    """Get the first element from list1 that also exists in list2"""
    for i in list1:
        if i in list2:
            return i
    return None


if __name__ == '__main__':

    orbitmap = utilsfuncs.load_input("inputFiles/inputfile.csv")
    orbitmapdenormalized = [y for x in orbitmap for y in x]
    uniquebodies = set(orbitmapdenormalized)

    YOU_path_store = list_builder_factory()
    SAN_path_store = list_builder_factory()

    path_to_COM('YOU', orbitmap, YOU_path_store)
    path_to_COM('SAN', orbitmap, SAN_path_store)

    firstcommon = get_first_common(YOU_path_store.__closure__[0].cell_contents, SAN_path_store.__closure__[0].cell_contents)
    print(count_orbits_to_specific_recur('YOU', orbitmap, firstcommon) + count_orbits_to_specific_recur('SAN', orbitmap, firstcommon) - 2) #minus 2 to get a distance between the objects YOU and SAN are orbiting, instead of the direct distance between YOU and SAN