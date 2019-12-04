from itertools import product
import pprint
import utilsfuncs


def get_key_list(val, diction): 
    keylist = []
    for key, value in diction.items(): 
        if val == value: 
            keylist.append(key)
    return keylist 


if __name__ == "__main__":
    
    exampleinstructions1 = [['R8', 'U5', 'L5', 'D3'], ['U7', 'R6', 'D4', 'L4']]
    exampleinstructions2 = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'], ['U62','R66','U55','R34','D71','R55','D58','R83']]
    exampleinstructions3 = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]

    instructions = utilsfuncs.load_input("inputFiles/inputfile.csv")

    wiregrid = dict()
    wirestamp = 0
    distances = []

    for wire in instructions:
        x = 0
        y = 0
        wirestamp += 1
        for instruction in wire:
            if instruction[0] == 'R':
                for i in range(0, int(instruction[1:])):
                    x += 1
                    try:
                        value = wiregrid[(x, y)]
                        value.append(wirestamp)
                        wiregrid[(x, y)] = value
                    except:
                        wiregrid[(x, y)] = [wirestamp]
            elif instruction[0] == 'U':
                for i in range(0, int(instruction[1:])):
                    y += 1
                    try:
                        value = wiregrid[(x, y)]
                        value.append(wirestamp)
                        wiregrid[(x, y)] = value
                    except:
                        wiregrid[(x, y)] = [wirestamp]
            elif instruction[0] == 'L':
                for i in range(0, int(instruction[1:])):
                    x -= 1
                    try:
                        value = wiregrid[(x, y)]
                        value.append(wirestamp)
                        wiregrid[(x, y)] = value
                    except:
                        wiregrid[(x, y)] = [wirestamp]
            elif instruction[0] == 'D':
                for i in range(0, int(instruction[1:])):
                    y -= 1
                    try:
                        value = wiregrid[(x, y)]
                        value.append(wirestamp)
                        wiregrid[(x, y)] = value
                    except:
                        wiregrid[(x, y)] = [wirestamp]

    for crossing in get_key_list([1, 2], wiregrid):
        
        print(crossing)
        distances.append(abs(crossing[0]) + abs(crossing[1]))

    print(min(distances))
