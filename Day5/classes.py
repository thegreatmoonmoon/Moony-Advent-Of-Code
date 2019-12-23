import functools

class Intcode():
    """Intcode class"""
    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(intcode)) #intcode enumerated (position, value)
        self._intcodeoutput = Intcodeoutput(intcode)

    def __iter__(self):
        """Returns Opcode custom iterator object"""
        self._intcodeiterator = IntcodeIterator(self)
        return self._intcodeiterator

    def __getitem__(self, key):
        return list(enumerate(self.get_intcode()))[key]
    
    #staticmethods for opcode with parameters parsing
    @staticmethod
    def get_opcode(number):
        return int(round((number/10) % 10 * 10))

    @staticmethod
    def get_param1(number):
        return int((number/100) % 10)

    @staticmethod
    def get_param2(number):
        return int(number/1000)

    @staticmethod
    def get_param3(number):
        return int(number/10000)

    def adder(self, firstread, secondread, write):
        """Adds together numbers read from two positions and stores the result in a third position."""
        write_p = write[0][1]
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        write_v = (firstread_v + secondread_v)

        self._intcodeoutput.setter(write_p, write_v)

    def multiplier(self, firstread, secondread, write):
        """Multiplies the two inputs instead of adding them."""
        write_p = write[0][1]
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        write_v = (firstread_v * secondread_v)

        self._intcodeoutput.setter(write_p, write_v)

    def take_input(self, write):
        """Takes a single integer as input and saves it to the position given by its only parameter."""
        self._programinput = int(input("Please provide program input: "))
        self._intcodeoutput.setter(write[1], self._programinput)

    def take_output(self, write):
        """Outputs the value of its only parameter."""
        if write[1] == 0:
            print("Output value is {}".format(self._intcodeoutput.get_intcodeoutput()[write[0][1]]))
        elif write[1] == 1:
            print("Output value is {}".format(write[0][1]))

    def jump_if_true(self, firstread, secondread):
        """If the first parameter is non-zero, it sets the instruction pointer 
        to the value from the second parameter. Otherwise, it does nothing."""
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
            
        if firstread_v != 0:
            self._intcodeiterator.modify_index_pointer(secondread_v)
        else:
            self._intcodeiterator.manually_move_index(3)

    def jump_if_false(self, firstread, secondread):
        """If the first parameter is zero, it sets the instruction pointer 
        to the value from the second parameter. Otherwise, it does nothing."""
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        
        if firstread_v == 0:
            self._intcodeiterator.modify_index_pointer(secondread_v)
        else:
            self._intcodeiterator.manually_move_index(3)

    def less_than(self, firstread, secondread, write):
        """if the first parameter is less than the second parameter, it stores 1
        in the position given by the third parameter. Otherwise, it stores 0."""
        write_p = write[0][1]
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]

        if firstread_v < secondread_v:
            self._intcodeoutput.setter(write_p, 1)
        else:
            self._intcodeoutput.setter(write_p, 0)

    def equal(self, firstread, secondread, write):
        """if the first parameter is equal to the second parameter, it stores 1 
        in the position given by the third parameter. Otherwise, it stores 0"""
        write_p = write[0][1]
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]

        if firstread_v == secondread_v:
            self._intcodeoutput.setter(write_p, 1)
        else:
            self._intcodeoutput.setter(write_p, 0)

    def get_intcode(self):
        return self._intcodeoutput.get_intcodeoutput()

class Intcodeoutput():
    """Intcode output observer class"""
    def __init__(self, intcode):
        self._intcode = intcode

    def __getitem__(self, key):
        return self._intcode[key]

    def setter(self, position, value):
        self._intcode[position] = value 

    def get_intcodeoutput(self):
        return self._intcode
    
class IntcodeIterator():
    """Custom Intcode iterator object"""
    def __init__(self, intcodeobj):
        """IntcodeIterator constructor with reference to Intcode object"""
        self._intcodeobj = intcodeobj
        self._index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next value, depending on the instruction"""
        currentintcode = list(enumerate(self._intcodeobj.get_intcode()))
        if self._index < (len(currentintcode)):
            opcode = currentintcode[self._index]
            if Intcode.get_opcode(opcode[1]) in (1, 2, 7, 8):
                self._index += 4
            elif Intcode.get_opcode(opcode[1]) in (3, 4):
                self._index += 2
            else:
                return opcode
            return opcode
        raise StopIteration

    def modify_index_pointer(self, newpointervalue):
        """Sets the iterator index to a new value"""
        self._index = newpointervalue
    
    def manually_move_index(self, numberofplaces):
        """Moves the iterator index by specific number of places"""
        self._index = self._index + numberofplaces


if __name__ == '__main__':

    exampleprogram = [1,9,10,3,2,3,11,0,99,30,40,50]
    exampleprogramresult = [3500,9,10,70,2,3,11,0,99,30,40,50]
    inputoutputtest = [3, 0, 4, 0, 99]
    inputoutputresults = [13, 0, 4, 0, 99] #provided input value = 13
    jumptestposition = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    jumptestimmediate = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    comparisontest1 = [3,9,8,9,10,9,4,9,99,-1,8]
    comparisontest2 = [3,9,7,9,10,9,4,9,99,-1,8]
    comparisontest3 = [3,3,1108,-1,8,3,4,3,99]
    comparisontest4 = [3,3,1107,-1,8,3,4,3,99]
    largerprogram = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]


    intcode = Intcode(largerprogram)

    opcodeparsing = (Intcode.get_opcode, 
                    Intcode.get_param1, 
                    Intcode.get_param2, 
                    Intcode.get_param3)

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
            elif parsedopcode[0] == 5:
                intcode.jump_if_true((intcode[item[0]+1], parsedopcode[1]),
                                     (intcode[item[0]+2], parsedopcode[2]))
            elif parsedopcode[0] == 6:
                intcode.jump_if_false((intcode[item[0]+1], parsedopcode[1]),
                                     (intcode[item[0]+2], parsedopcode[2]))
            elif parsedopcode[0] == 7:
                intcode.less_than((intcode[item[0]+1], parsedopcode[1]),
                                   (intcode[item[0]+2], parsedopcode[2]),
                                   (intcode[item[0]+3], parsedopcode[3]))
            elif parsedopcode[0] == 8:
                intcode.equal((intcode[item[0]+1], parsedopcode[1]),
                                   (intcode[item[0]+2], parsedopcode[2]),
                                   (intcode[item[0]+3], parsedopcode[3]))                                                
            elif parsedopcode[0] == 99:
                break
            else:
                print("Unexpected Opcode!")
                raise Exception
    except IndexError:
        print("Something's rather wrong...")

        
    print(intcode.get_intcode())
    #assert intcode.get_intcode() == inputoutputresults
   