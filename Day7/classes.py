import functools
import itertools

class Intcode():
    """Intcode class"""
    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(list(intcode))) #intcode enumerated (position, value)
        self._intcodeoutput = Intcodeoutput(list(intcode))

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

    def take_input(self, write, inputvalue):
        """Takes a single integer as input and saves it to the position given by its only parameter."""
        self._intcodeoutput.setter(write[1], inputvalue)

    def take_output(self, write):
        """Outputs the value of its only parameter."""
        if write[1] == 0:
            return (self._intcodeoutput.get_intcodeoutput()[write[0][1]])
        elif write[1] == 1:
            return (write[0][1])

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

class Amplifier():
    """Amplifier class"""
    def __init__(self, name, intcode):
        self.name = name
        self.intcode = Intcode(intcode)
        self.params = []
        self.output = None

    def run_program(self, params):
        """Main coroutine generator for the Amplifier class. Takes params at the initialization which are consumed by input opcode 3. 
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
                    self.intcode.take_input((self.intcode[item[0]+1]), self.params.pop())
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

def main(inputA: int = 0, inputs: list = [9, 8, 7, 6, 5], program: tuple = (3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5)):
    """Coordinates amplifier coroutines to create feedback loop A->B->C->D->E->A. Breakes the loop once one of the 
    amplifiers raises StopIteration exception (at opcode 99) and returns the output value of the last amplifier.
    - takes initial input for the first amplifier
    - takes phase input parameters for all 5 amplifiers"""
    
    amplifierA = Amplifier("A", program)
    amplifierB = Amplifier("B", program)
    amplifierC = Amplifier("C", program)
    amplifierD = Amplifier("D", program)
    amplifierE = Amplifier("E", program)

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
            print("StopIteration!")
            break

    return amplifierE.get_output()


if __name__ == '__main__':

    #exampleprogram = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    #exampleprogram = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    #exampleprogram = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    #exampleprogram = (3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5)
    exampleprogram = (3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10)
    
    potentialinputs = list(itertools.permutations([5, 6, 7, 8, 9]))

    maxresult = 0
    for inputs in potentialinputs:    
    
        lastamplifieroutput = main(inputA=0, inputs=inputs, program=exampleprogram)
    
        if lastamplifieroutput > maxresult:
            maxresult = lastamplifieroutput
            result = (lastamplifieroutput, inputs)

    
    print(result)
    assert result == (18216, (9, 7, 8, 5, 6))