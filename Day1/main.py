import funcs

if __name__ == "__main__":

    #load input variables from file and convert to int
    inputlist = list(map(int, funcs.load_input("inputFiles/calc_input.csv")))
    
    #map input variables to fuel calculator, pass it to totalizer function and get the result
    result = funcs.fuel_totalizer(*map(funcs.fuel_calculator, inputlist))

    #map input variables to fuel calculator recursive, pass it to totalizer function and get the result
    result2 = funcs.fuel_totalizer(*map(funcs.fuel_calculator_recursive, inputlist))

    #print the result
    print(result)
    print(result2)