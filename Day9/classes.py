import functools
import itertools

class Intcode():
    """Intcode class"""
    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(list(intcode))) #intcode enumerated (position, value)
        self._intcodeoutput = Intcodeoutput(list(intcode))
        self._relativebase = RelativeBase()

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
        return int(number/1000) % 10

    @staticmethod
    def get_param3(number):
        return int(number/10000)

    def adder(self, firstread, secondread, write):
        """Adds together numbers read from two positions and stores the result in a third position."""
        if write[1] in (0, 1):
            write_p = write[0][1]
        elif write[1] == 2:
            write_p = self._relativebase.currentindex + write[0][1]
            
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]
        write_v = (firstread_v + secondread_v)

        self._intcodeoutput.setter(write_p, write_v)

    def multiplier(self, firstread, secondread, write):
        """Multiplies the two inputs instead of adding them."""
        if write[1] in (0, 1):
            write_p = write[0][1]
        elif write[1] == 2:
            write_p = self._relativebase.currentindex + write[0][1]
            
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]
        write_v = (firstread_v * secondread_v)

        self._intcodeoutput.setter(write_p, write_v)

    def take_input(self, write, inputvalue):
        """Takes a single integer as input and saves it to the position given by its only parameter."""
        if write[1] in (0, 1):
            self._intcodeoutput.setter(write[0][1], inputvalue)
        elif write[1] == 2:
            self._intcodeoutput.setter(self._relativebase.currentindex + write[0][1], inputvalue)

    def take_output(self, write):
        """Outputs the value of its only parameter."""
        if write[1] == 0:
            return (self._intcodeoutput.get_intcodeoutput()[write[0][1]])
        elif write[1] == 1:
            return (write[0][1])
        elif write[1] == 2:
            return (self._intcodeoutput.get_intcodeoutput()[self._relativebase.currentindex + write[0][1]])

    def jump_if_true(self, firstread, secondread):
        """If the first parameter is non-zero, it sets the instruction pointer 
        to the value from the second parameter. Otherwise, it does nothing."""
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]
            
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
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]
        
        if firstread_v == 0:
            self._intcodeiterator.modify_index_pointer(secondread_v)
        else:
            self._intcodeiterator.manually_move_index(3)

    def less_than(self, firstread, secondread, write):
        """if the first parameter is less than the second parameter, it stores 1
        in the position given by the third parameter. Otherwise, it stores 0."""
        if write[1] in (0, 1):
            write_p = write[0][1]
        elif write[1] == 2:
            write_p = self._relativebase.currentindex + write[0][1]
            
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]

        if firstread_v < secondread_v:
            self._intcodeoutput.setter(write_p, 1)
        else:
            self._intcodeoutput.setter(write_p, 0)

    def equal(self, firstread, secondread, write):
        """if the first parameter is equal to the second parameter, it stores 1 
        in the position given by the third parameter. Otherwise, it stores 0"""
        if write[1] in (0, 1):
            write_p = write[0][1]
        elif write[1] == 2:
            write_p = self._relativebase.currentindex + write[0][1]
        
        if firstread[1] == 0:
            firstread_v = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            firstread_v = firstread[0][1]
        elif firstread[1] == 2:
            firstread_v = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]
        
        if secondread[1] == 0:
            secondread_v = self._intcodeoutput[secondread[0][1]]
        elif secondread[1] == 1:
            secondread_v = secondread[0][1]
        elif secondread[1] == 2:
            secondread_v = self._intcodeoutput[self._relativebase.currentindex + secondread[0][1]]

        if firstread_v == secondread_v:
            self._intcodeoutput.setter(write_p, 1)
        else:
            self._intcodeoutput.setter(write_p, 0)

    def adjust_relative_base(self, firstread):
        """adjusts the relative base by the value of its only parameter. The relative 
        base increases (or decreases, if the value is negative) by the value of the parameter."""

        if firstread[1] == 0:
            self._relativebase.currentindex = self._intcodeoutput[firstread[0][1]]
        elif firstread[1] == 1:
            self._relativebase.currentindex = firstread[0][1]
        elif firstread[1] == 2:
            self._relativebase.currentindex = self._intcodeoutput[self._relativebase.currentindex + firstread[0][1]]

    def get_intcode(self):
        return self._intcodeoutput.get_intcodeoutput()

class Intcodeoutput():
    """Intcode output observer class"""
    def __init__(self, intcode):
        self._intcode = intcode
        self._extendedmemorymodule = {}

    def __getitem__(self, key):
        try:
            return self._intcode[key]
        except IndexError:
            #look for the value in the extended memory module
            if key < 0:
                raise IndexError("Extended memory address cannot be a negative number!")
            else:
                return self._access_extended_memory(key)

    def setter(self, position, value):
        try:
            self._intcode[position] = value 
        except IndexError:
            if position < 0:
                raise IndexError("Extended memory address cannot be a negative number!")
            else:
                self._write_extended_memory(position, value)

    def get_intcodeoutput(self):
        return self._intcode

    def _access_extended_memory(self, key):
        try:
            return self._extendedmemorymodule[key]
        except KeyError:
            return 0

    def _write_extended_memory(self, position, value):
        self._extendedmemorymodule[position] = value    
    
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
            elif Intcode.get_opcode(opcode[1]) in (3, 4, 9):
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

class RelativeBase():
    def __init__(self):
        self._currentindex = 0

    @property
    def currentindex(self):
        return self._currentindex

    @currentindex.setter
    def currentindex(self, offset):
        self._currentindex = self._currentindex + offset

class Runtime():
    """Runtime class"""
    def __init__(self, name, intcode):
        self.name = name
        self.intcode = Intcode(intcode)
        self.params = []
        self.output = None

    def run_program(self, params):
        """Main coroutine generator for the Runtime class. Takes params at the initialization which are consumed by input opcode 3. 
        Further, params to be modified via the .send() method. Yields output value (at opcode 4)."""
        opcodeparsing = (Intcode.get_opcode, 
                    Intcode.get_param1, 
                    Intcode.get_param2, 
                    Intcode.get_param3)
        self.params = params
        try:
            for item in iter(self.intcode):

                parsedopcode = [f(item[1]) for f in opcodeparsing]

                if parsedopcode[0] == 1:
                    self.intcode.adder((self.intcode[item[0]+1], parsedopcode[1]),
                                  (self.intcode[item[0]+2], parsedopcode[2]),
                                  (self.intcode[item[0]+3], parsedopcode[3]))
                elif parsedopcode[0] == 2:
                    self.intcode.multiplier((self.intcode[item[0]+1], parsedopcode[1]),
                                       (self.intcode[item[0]+2], parsedopcode[2]),
                                       (self.intcode[item[0]+3], parsedopcode[3]))
                elif parsedopcode[0] == 3:
                    print("taking input ", self.params, " by ", self.name)
                    self.intcode.take_input((self.intcode[item[0]+1], parsedopcode[1]), self.params.pop())
                elif parsedopcode[0] == 4:
                    self.output = self.intcode.take_output((self.intcode[item[0]+1], parsedopcode[1]),)
                    print("giving output: ", self.output, " by ", self.name)
                    self.params = yield self.output
                elif parsedopcode[0] == 5:
                    self.intcode.jump_if_true((self.intcode[item[0]+1], parsedopcode[1]),
                                         (self.intcode[item[0]+2], parsedopcode[2]))
                elif parsedopcode[0] == 6:
                    self.intcode.jump_if_false((self.intcode[item[0]+1], parsedopcode[1]),
                                         (self.intcode[item[0]+2], parsedopcode[2]))
                elif parsedopcode[0] == 7:
                    self.intcode.less_than((self.intcode[item[0]+1], parsedopcode[1]),
                                       (self.intcode[item[0]+2], parsedopcode[2]),
                                       (self.intcode[item[0]+3], parsedopcode[3]))
                elif parsedopcode[0] == 8:
                    self.intcode.equal((self.intcode[item[0]+1], parsedopcode[1]),
                                       (self.intcode[item[0]+2], parsedopcode[2]),
                                       (self.intcode[item[0]+3], parsedopcode[3]))
                elif parsedopcode[0] == 9:
                    self.intcode.adjust_relative_base((self.intcode[item[0]+1], parsedopcode[1]),)                                                
                elif parsedopcode[0] == 99:
                    break
                else:
                    print("Unexpected Opcode! {}".format(parsedopcode[0]))
                    raise ValueError
        except IndexError:
            print("Something's rather wrong...")
        return None

    def get_output(self):
        return self.output

def main(program: tuple, inputA: int = 1, inputs: list = [9, 8, 7, 6, 5]):
    """Starts the BOOST computer.
    InputA default value equals 1 (Test Mode)"""
    
    boostruntime = Runtime("BOOST", program)
    
    boostruntimerun = boostruntime.run_program([inputA,])

    while True:
    
        try:
            next(boostruntimerun)
    
        except StopIteration:
            print("StopIteration!")
            break

    return boostruntime.get_output()


if __name__ == '__main__':

    #exampleprogram = (109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99)
    #exampleprogram = (1102,34915192,34915192,7,4,7,99,0)
    exampleprogram = (104,1125899906842624,99)


    lastprogramoutput = main(inputA=1, program=exampleprogram)
    
    print("Last program output: ", lastprogramoutput)

    assert lastprogramoutput == (1125899906842624)