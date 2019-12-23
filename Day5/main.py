import classes
import utilsfuncs
from itertools import product
from functools import partial

if __name__ == '__main__':
    
    #load intcode from input file
    intcodelist = list(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))

    intcode = classes.Intcode(intcodelist)

    opcodeparsing = (classes.Intcode.get_opcode, 
                             classes.Intcode.get_param1, 
                             classes.Intcode.get_param2, 
                             classes.Intcode.get_param3)

    try:
        for item in iter(intcode):

            parsedopcode = [f(item[1]) for f in opcodeparsing]

            if parsedopcode[0] == 1:
                intcode.adder((intcode[item[0]+1], parsedopcode[1]),
                              (intcode[item[0]+2], parsedopcode[2]),
                              (intcode[item[0]+3], parsedopcode[3]))
            elif parsedopcode[0] == 2:
                intcode.multiplier((intcode[item[0]+1], parsedopcode[1]),
                                   (intcode[item[0]+2], parsedopcode[2]),
                                   (intcode[item[0]+3], parsedopcode[3]))
            elif parsedopcode[0] == 3:
                intcode.take_input((intcode[item[0]+1]))
            elif parsedopcode[0] == 4:
                intcode.take_output((intcode[item[0]+1], parsedopcode[1]),)
            elif parsedopcode[0] == 99:
                break
            else:
                print("Unexpected Opcode!")
                raise Exception
    except IndexError:
        print("Something's rather wrong...")
    

    

  