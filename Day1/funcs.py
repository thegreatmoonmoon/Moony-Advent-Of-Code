from math import floor
from functools import reduce

def fuel_calculator(mass):
    """Function to return required fuel, takes mass as the only argument"""  
    return (floor(mass / 3) - 2)

def fuel_calculator_recursive(mass):
    """Recursive function to return required fuel, takes into account the mass of fuel itself"""  
    if fuel_calculator(mass) < 0:
        return 0
    else:
        return fuel_calculator(mass) + fuel_calculator_recursive(fuel_calculator(mass))

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
    testoutput2 = [2, 2, 966, 50346]
    testsum = 34241
    inputfilelist = ["123", "321", "213", "231"]

    #function tests
    assert list(map(fuel_calculator, testinput)) == testoutput
    assert reduce(fuel_totalizer, map(fuel_calculator, testinput)) == testsum

    assert reduce(fuel_totalizer, [1,0]) == 1
    assert reduce(fuel_totalizer, [5,]) == 5

    assert load_input("inputFiles/test_input.csv") == inputfilelist
    
    assert list(map(fuel_calculator_recursive, testinput)) == testoutput2