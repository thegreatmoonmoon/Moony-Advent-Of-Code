import funcs

if __name__ == "__main__":

    #load input variables from file and convert to int
    inputlist = list(map(int, funcs.load_input("calc_input.csv")))
    
    #map input variables to fuel calculator and then to totalizer function and get the result
    result = funcs.fuel_totalizer(*list(map(funcs.fuel_calculator, inputlist)))

    #map input variables to fuel calculator 2 and then to totalizer function and get the result
    result2 = funcs.fuel_totalizer(*list(map(funcs.fuel_calculator2, inputlist)))

    #print the result
    print(result)
    print(result2)