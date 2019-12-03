import funcs

if __name__ == "__main__":

    #load input variables from file and convert to int
    inputlist = list(map(int, funcs.load_input("calc_input.csv")))
    
    #pass input variables to totalizer function and get the result
    result = funcs.fuel_totalizer(*list(map(funcs.fuel_calculator, inputlist)))

    #print the result
    print(result)