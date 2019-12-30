import classes
import utilsfuncs
import itertools
from itertools import product
from functools import partial


def main(inputA: int = 0, inputs: list = [9, 8, 7, 6, 5], program: tuple = (3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5)):
    """Coordinates amplifier coroutines to create feedback loop A->B->C->D->E->A. Breakes the loop once one of the 
    amplifiers raises StopIteration exception (at opcode 99) and returns the output value of the last amplifier.
    - takes initial input for the first amplifier
    - takes phase input parameters for all 5 amplifiers"""
    
    amplifierA = classes.Amplifier("A", program)
    amplifierB = classes.Amplifier("B", program)
    amplifierC = classes.Amplifier("C", program)
    amplifierD = classes.Amplifier("D", program)
    amplifierE = classes.Amplifier("E", program)

    runA = amplifierA.run_program([inputA, inputs[0]])
    inputB = next(runA)
    runB = amplifierB.run_program([inputB, inputs[1]])
    inputC = next(runB)
    runC = amplifierC.run_program([inputC, inputs[2]])
    inputD = next(runC)
    runD = amplifierD.run_program([inputD, inputs[3]])
    inputE = next(runD)
    runE = amplifierE.run_program([inputE, inputs[4]])
    inputA = next(runE)


    while inputA is not None:
        
        try:
            inputB = runA.send([inputA])
    
            inputC = runB.send([inputB])

            inputD = runC.send([inputC])

            inputE = runD.send([inputD])

            inputA = runE.send([inputE])
        
        except StopIteration:
            print("Feedback loop ended!")
            break

    return amplifierE.get_output()


if __name__ == '__main__':
    
    #load intcode from input file
    intcodetuple = tuple(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))

    #create potential phase permutations
    potentialinputs = list(itertools.permutations([5, 6, 7, 8, 9]))

    maxresult = 0
    for inputs in potentialinputs:    
    
        lastamplifieroutput = main(inputA=0, inputs=inputs, program=intcodetuple)
    
        if lastamplifieroutput > maxresult:
            maxresult = lastamplifieroutput
            result = (lastamplifieroutput, inputs)

    
    print("Highest potential feedback loop result: ", result)

    

  