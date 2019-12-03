import classes
import utilsfuncs
from itertools import product

if __name__ == '__main__':
    
    for x, y in product(range(0,100), range(0, 100)):
        
        #load intcode from input file
        intcodelist = list(map(int, utilsfuncs.load_input("inputFiles/inputfile.csv")))
        
        intcodelist[1] = x
        intcodelist[2] = y

        intcode = classes.Intcode(intcodelist)

        try:
            for item in iter(intcode):
                if item[1] == 1:
                    intcode.adder(intcode[item[0]+1], intcode[item[0]+2], intcode[item[0]+3])
                elif item[1] == 2:
                    intcode.multiplier(intcode[item[0]+1], intcode[item[0]+2], intcode[item[0]+3])    
                elif item[1] == 99:
                    break
                else:
                    break
        except IndexError:
            continue

        if intcode.get_intcode()[0] == 19690720:
            print("noun: {0}, verb: {1}".format(x,y))
            break
    

    

  