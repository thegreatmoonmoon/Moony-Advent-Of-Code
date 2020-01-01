import classes
import utilsfuncs
import itertools


def main(program: tuple, inputA: int = 1, inputs: list = [9, 8, 7, 6, 5]):
    """Starts the BOOST computer.
    InputA default value equals 1 (Test Mode)"""
    
    boostruntime = classes.Runtime("BOOST", program)
    
    boostruntimerun = boostruntime.run_program([inputA,])

    while True:
    
        try:
            next(boostruntimerun)
    
        except StopIteration:
            print("StopIteration!")
            break

    return boostruntime.get_output()

if __name__ == '__main__':
    
    #load intcode from input file
    intcodetuple = tuple(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))

    lastprogramoutput = main(inputA=2, program=intcodetuple)
    
    print("Last program output: ", lastprogramoutput)
  