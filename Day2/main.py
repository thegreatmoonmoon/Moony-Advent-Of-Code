import classes
import utilsfuncs

if __name__ == '__main__':

    #load intcode from input file
    intcodelist = list(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))
    
    intcodelist[1] = 12
    intcodelist[2] = 2

    intcode = classes.Intcode(intcodelist)

    for item in iter(intcode):
        if item[1] == 1:
            intcode.adder(intcode[item[0]+1], intcode[item[0]+2], intcode[item[0]+3])
        elif item[1] == 2:
            intcode.multiplier(intcode[item[0]+1], intcode[item[0]+2], intcode[item[0]+3])    
        elif item[1] == 99:
            break
        else:
            print("Unexpected Opcode!")
            raise Exception
    
    print(intcode.get_intcode())

    

  