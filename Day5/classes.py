import functools

class Intcode():
    """Intcode class"""
    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(intcode)) #intcode enumerated (position, value)
        self._intcodeoutput = Intcodeoutput(intcode)

    def __iter__(self):
        """Returns Opcode custom iterator object"""
        return IntcodeIterator(self)

    def __getitem__(self, key):
        return self._intcodeenumed[key]
    
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
        self._programinput = int(input("Please provide program input: "))
        self._intcodeoutput.setter(write[1], self._programinput)

    def take_output(self, write):
        if write[1] == 0:
            print("Output value is {}".format(self._intcodeoutput.get_intcodeoutput()[write[0][1]]))
        elif write[1] == 1:
            print("Output value is {}".format(write[0][1]))

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
    """Custom Opcode iterator object"""
    def __init__(self, intcodeobj):
        """OpcodeIterator constructor with reference to Opcode object"""
        self._intcodeobj = intcodeobj
        self._index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        """Returns a next value, depending on the instruction"""
        currentintcode = list(enumerate(self._intcodeobj.get_intcode()))
        if self._index < (len(currentintcode)):
            opcode = currentintcode[self._index]
            if Intcode.get_opcode(opcode[1]) in (1, 2):
                self._index += 4
            else:
                self._index += 2
            return opcode
        raise StopIteration

if __name__ == '__main__':

    #exampleprogram = [1,9,10,3,2,3,11,0,99,30,40,50]
    #exampleprogramresult = [3500,9,10,70,2,3,11,0,99,30,40,50]
    inputoutputtest = [3, 0, 4, 0, 99]
    inputoutputresults = [13, 0, 4, 0, 99] #provided input value = 13


    intcode = Intcode(inputoutputtest)

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
            elif parsedopcode[0] == 99:
                break
            else:
                print("Unexpected Opcode!")
                raise Exception
    except IndexError:
        print("Something's rather wrong...")

        
    print(intcode.get_intcode())
    assert intcode.get_intcode() == inputoutputresults
   