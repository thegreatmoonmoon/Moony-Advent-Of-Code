import classes
import utilsfuncs
import itertools
from itertools import product
from functools import partial

if __name__ == '__main__':
    
    #load intcode from input file
    intcodelist = list(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))

    potentialinputs = list(itertools.permutations([0, 1, 2, 3, 4]))

    maxresult = 0
    for inputs in potentialinputs:

        amplifierA = classes.Amplifier("A", intcodelist, [0, inputs[0]])
        amplifierA.run_program()

        amplifierB = classes.Amplifier("B", intcodelist, [amplifierA.get_output(), inputs[1]])
        amplifierB.run_program()

        amplifierC = classes.Amplifier("C", intcodelist, [amplifierB.get_output(), inputs[2]])
        amplifierC.run_program()

        amplifierD = classes.Amplifier("D", intcodelist, [amplifierC.get_output(), inputs[3]])
        amplifierD.run_program()

        amplifierE = classes.Amplifier("E", intcodelist, [amplifierD.get_output(), inputs[4]])
        amplifierE.run_program()
        finaloutput = amplifierE.get_output()
        
        if finaloutput > maxresult:
            maxresult = finaloutput
            result = (finaloutput, inputs)


    print(result)

    

  