class Intcode():
    """Intcode class"""
    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(intcode))
        self._intcodeoutput = Intcodeoutput(intcode)

    def __iter__(self):
        """Returns Opcode custom iterator object"""
        return IntcodeIterator(self)

    def __getitem__(self, key):
        return self._intcodeenumed[key]

    def adder(self, firstread, secondread, write):
        firstread_v = firstread[1]
        secondread_v = secondread[1]
        write_p = write[1]
        write_v = (self._intcodeoutput[firstread_v] + self._intcodeoutput[secondread_v])

        self._intcodeoutput.setter(write_p, write_v)

    def multiplier(self, firstread, secondread, write):
        firstread_v = firstread[1]
        secondread_v = secondread[1]
        write_p = write[1]
        write_v = (self._intcodeoutput[firstread_v] * self._intcodeoutput[secondread_v])

        self._intcodeoutput.setter(write_p, write_v)

    def get_intcode(self):
        return self._intcodeoutput.get_intcodeoutput()

class Intcodeoutput():
    """Intcode output class"""
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
        """Returns a next value, iterated by 4 positions"""
        if self._index < (len(self._intcodeobj._intcodeenumed)):
            opcode = self._intcodeobj._intcodeenumed[self._index]
            self._index += 4
            return opcode
        raise StopIteration

if __name__ == '__main__':

    exampleprogram = [1,9,10,3,2,3,11,0,99,30,40,50]
    exampleprogramresult = [3500,9,10,70,2,3,11,0,99,30,40,50]

    intcode = Intcode(exampleprogram)

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

    assert intcode.get_intcode() == exampleprogramresult
   