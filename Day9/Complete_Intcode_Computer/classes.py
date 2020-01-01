"""
classes.py
====================================
Contains all class objects utilized by the Intcode Computer
"""

import utilsfuncs


class Intcode:
    """Intcode class"""

    def __init__(self, intcode):
        """Opcode class constructor with enumerator"""
        self._intcodeenumed = list(enumerate(list(intcode)))  # intcode enumerated (position, value)
        self._intcodeoutput = Intcodeoutput(list(intcode))
        self._relativebase = RelativeBase()

    def __iter__(self):
        """Magic dunder method to return Opcode custom iterator object"""
        self._intcodeiterator = IntcodeIterator(self)
        return self._intcodeiterator

    def __getitem__(self, key):
        """Magic dunder method to allow object indexing by key"""
        return list(enumerate(self.get_intcode()))[key]

    @staticmethod
    def get_opcode(number):
        """Static method to retrieve an opcode from intcode value. Returns two last digits"""
        return int(round((number / 10) % 10 * 10))

    @staticmethod
    def get_param1(number):
        """Static method to retrieve the first parameter from intcode value. Returns hundreds digit"""
        return int((number / 100) % 10)

    @staticmethod
    def get_param2(number):
        """Static method to retrieve the second parameter from intcode value. Returns thousends digit"""
        return int(number / 1000) % 10

    @staticmethod
    def get_param3(number):
        """Static method to retrieve the third parameter from intcode value. Returns tens thousends digit"""
        return int(number / 10000)

    @utilsfuncs.retrieve_params
    def adder(self, firstread, secondread, write):
        """Adds together numbers read from two positions and stores the result in a third position."""
        write_p = write
        write_v = firstread + secondread

        self._intcodeoutput.setter(write_p, write_v)

    @utilsfuncs.retrieve_params
    def multiplier(self, firstread, secondread, write):
        """Multiplies the two inputs instead of adding them."""
        write_p = write
        write_v = firstread * secondread

        self._intcodeoutput.setter(write_p, write_v)

    @utilsfuncs.retrieve_params
    def take_input(self, write, inputvalue):
        """Takes a single integer as input and saves it to the position given by its only parameter."""
        self._intcodeoutput.setter(write, inputvalue)

    @utilsfuncs.retrieve_params
    def take_output(self, write_output):
        """Outputs the value of its only parameter."""

        return write_output

    @utilsfuncs.retrieve_params
    def jump_if_true(self, firstread, secondread):
        """If the first parameter is non-zero, it sets the instruction pointer
        to the value from the second parameter. Otherwise, it does nothing."""
        if firstread != 0:
            self._intcodeiterator.modify_index_pointer(secondread)
        else:
            self._intcodeiterator.manually_move_index(3)

    @utilsfuncs.retrieve_params
    def jump_if_false(self, firstread, secondread):
        """If the first parameter is zero, it sets the instruction pointer
        to the value from the second parameter. Otherwise, it does nothing."""
        if firstread == 0:
            self._intcodeiterator.modify_index_pointer(secondread)
        else:
            self._intcodeiterator.manually_move_index(3)

    @utilsfuncs.retrieve_params
    def less_than(self, firstread, secondread, write):
        """if the first parameter is less than the second parameter, it stores 1
        in the position given by the third parameter. Otherwise, it stores 0."""
        if firstread < secondread:
            self._intcodeoutput.setter(write, 1)
        else:
            self._intcodeoutput.setter(write, 0)

    @utilsfuncs.retrieve_params
    def equal(self, firstread, secondread, write):
        """if the first parameter is equal to the second parameter, it stores 1
        in the position given by the third parameter. Otherwise, it stores 0"""
        if firstread == secondread:
            self._intcodeoutput.setter(write, 1)
        else:
            self._intcodeoutput.setter(write, 0)

    @utilsfuncs.retrieve_params
    def adjust_relative_base(self, firstread):
        """adjusts the relative base by the value of its only parameter. The relative
        base increases (or decreases, if the value is negative) by the value of the parameter."""
        self._relativebase.currentindex = firstread

    def get_intcode(self):
        return self._intcodeoutput.get_intcodeoutput()


class Intcodeoutput:
    """Intcode output observer class"""

    def __init__(self, intcode):
        self._intcode = intcode
        self._extendedmemorymodule = {}

    def __getitem__(self, key):
        """Magic dunder method to get intcode output by key.
        First, tries to get an item from 'memory' initially assigned to the program.
        If the above fails, tries to access an item from 'extended memory', using onjeect's private method"""
        try:
            return self._intcode[key]
        except IndexError:
            # look for the value in the extended memory module
            if key < 0:
                raise IndexError("Extended memory address cannot be a negative number!")
            else:
                return self._access_extended_memory(key)

    def setter(self, position, value):
        """Method to set a value in the program's 'memory'. First, tries to set the value at a position
        initially assign to the program.
        If the above fails, assignes the value in the 'extended memory' data struct"""
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


class IntcodeIterator:
    """Custom Intcode iterator object"""

    def __init__(self, intcodeobj) -> None:
        """IntcodeIterator constructor with reference to Intcode object"""
        self._intcodeobj = intcodeobj
        self._index = 0

    def __iter__(self):
        """Magic dunder method to allow for iterating over the object"""
        return self

    def __next__(self):
        """Magic dunder method to return the next iterator value, depending on the instruction.
        Additionally, modifies the index by appropriate number, depending on the instruction"""
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

    def modify_index_pointer(self, newpointervalue: int) -> None:
        """Sets the iterator index to a new value"""
        self._index = newpointervalue

    def manually_move_index(self, numberofplaces: int) -> None:
        """Moves the iterator index by specific number of places"""
        self._index = self._index + numberofplaces


class RelativeBase:
    """Object to initialize, store, retrieve, and modify program's relative base point
    Uses property decorators for attribute retrieval and modification"""

    def __init__(self) -> None:
        self._currentindex = 0

    @property
    def currentindex(self) -> int:
        return self._currentindex

    @currentindex.setter
    def currentindex(self, offset) -> None:
        self._currentindex = self._currentindex + offset


class Runtime:
    """Runtime class"""

    def __init__(self, name: str, intcode: tuple) -> None:
        self.name = name
        self.intcode = Intcode(intcode)
        self.params = []
        self.output = None

    def run_program(self, params: list) -> None:
        """Main coroutine generator for the Runtime class. Takes params at the initialization which are consumed by input
        opcode 3. Further params to be modified via the .send() method. Yields output value (at opcode 4)."""
        opcodeparsing = (
            Intcode.get_opcode,  # set a sequence of functions to retrieve opcode+params from intcode value
            Intcode.get_param1,
            Intcode.get_param2,
            Intcode.get_param3,
        )
        self.params = params
        try:
            for item in iter(self.intcode):

                parsedopcode = [f(item[1]) for f in opcodeparsing]

                if parsedopcode[0] == 1:
                    self.intcode.adder(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                        write=(self.intcode[item[0] + 3], parsedopcode[3]),
                    )
                elif parsedopcode[0] == 2:
                    self.intcode.multiplier(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                        write=(self.intcode[item[0] + 3], parsedopcode[3]),
                    )
                elif parsedopcode[0] == 3:
                    print("taking input ", self.params, " by ", self.name)
                    self.intcode.take_input(
                        write=(self.intcode[item[0] + 1], parsedopcode[1]), inputvalue=self.params.pop()
                    )
                elif parsedopcode[0] == 4:
                    self.output = self.intcode.take_output(write_output=(self.intcode[item[0] + 1], parsedopcode[1]),)
                    print("giving output: ", self.output, " by ", self.name)
                    self.params = yield self.output
                elif parsedopcode[0] == 5:
                    self.intcode.jump_if_true(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                    )
                elif parsedopcode[0] == 6:
                    self.intcode.jump_if_false(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                    )
                elif parsedopcode[0] == 7:
                    self.intcode.less_than(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                        write=(self.intcode[item[0] + 3], parsedopcode[3]),
                    )
                elif parsedopcode[0] == 8:
                    self.intcode.equal(
                        firstread=(self.intcode[item[0] + 1], parsedopcode[1]),
                        secondread=(self.intcode[item[0] + 2], parsedopcode[2]),
                        write=(self.intcode[item[0] + 3], parsedopcode[3]),
                    )
                elif parsedopcode[0] == 9:
                    self.intcode.adjust_relative_base(firstread=(self.intcode[item[0] + 1], parsedopcode[1]),)
                elif parsedopcode[0] == 99:
                    break
                else:
                    print("Unexpected Opcode! {}".format(parsedopcode[0]))
                    raise ValueError
        except IndexError:
            print("Something's rather wrong... Null pointer?")
        return None

    def get_output(self) -> int:
        return self.output


if __name__ == "__main__":

    def main(program: tuple, inputA: int = 1, inputs: list = [9, 8, 7, 6, 5]):
        """Starts the BOOST computer.
        InputA default value equals 1 (Test Mode)"""

        boostruntime = Runtime("BOOST", program)

        boostruntimerun = boostruntime.run_program([inputA, ])

        while True:

            try:
                next(boostruntimerun)
            except StopIteration:
                print("StopIteration!")
                break

        return boostruntime.get_output()

    # exampleprogram = (109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99)
    exampleprogram = (1102, 34915192, 34915192, 7, 4, 7, 99, 0)
    # exampleprogram = (104,1125899906842624,99)

    lastprogramoutput = main(inputA=1, program=exampleprogram)

    print("Last program output: ", lastprogramoutput)

    assert len(str(lastprogramoutput)) == 16
