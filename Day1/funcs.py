from math import floor
from functools import reduce

def fuel_calculator(mass):
    """Function to return required fuel, takes mass as the only argument"""  
    return (floor(mass / 3) - 2)


def fuel_totalizer(*args):
    """Function to return the total of all arguments provided""" 
    total = 0
    for arg in args:
        total += arg
    return total

def load_input(filepath):
    """Function to return a list of input variables from file"""  
    inputlist = []
    with open(filepath, "r") as inputfile:
        for line in inputfile:
            inputlist.append(line.rstrip())
    return inputlist


if __name__ == "__main__":
    
    #function test variables
    testinput = [12, 14, 1969, 100756]
    testoutput = [2, 2, 654, 33583]
    testsum = 34241
    inputfilelist = ["123", "321", "213", "231"]

    #function tests
    assert list(map(fuel_calculator, testinput)) == testoutput
    assert reduce(fuel_totalizer, testoutput) == testsum

    assert reduce(fuel_totalizer, [1,0]) == 1
    assert reduce(fuel_totalizer, [5,]) == 5

    assert load_input("test_input.csv") == inputfilelist
