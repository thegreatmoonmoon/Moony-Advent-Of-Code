"""
utilsfuncs.py
====================================
Contains utility functions utilized by the classes or the main module of the Intcode Computer
"""

import functools


def load_input(filepath):
    """Function to return a list of input variables from file"""
    with open(filepath, "r") as inputfile:
        return inputfile.read().split(",")


def retrieve_params(f):
    """Decorator to retrieve program command attributes, depending on their parameters
    (position:0, immediate:1, relative:2).
    Parameter names the decorator will modify:
        firstread
        secondread
        write
        write_output"""

    attributecodes = {
            'position': 0,
            'immediate': 1,
            'relative': 2
            }

    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        modifiedkwargs = {}
        for kwarg in kwargs:
            if kwarg in ("write"):
                if kwargs[kwarg][1] in (attributecodes['position'],
                                        attributecodes['immediate']):
                    modifiedkwargs[kwarg] = kwargs[kwarg][0][1]
                elif kwargs[kwarg][1] == attributecodes['relative']:
                    modifiedkwargs[kwarg] = self._relativebase.currentindex + kwargs[kwarg][0][1]
            elif kwarg in ("firstread", "secondread", "write_output"):
                if kwargs[kwarg][1] == attributecodes['position']:
                    modifiedkwargs[kwarg] = self._intcodeoutput[kwargs[kwarg][0][1]]
                elif kwargs[kwarg][1] == attributecodes['immediate']:
                    modifiedkwargs[kwarg] = kwargs[kwarg][0][1]
                elif kwargs[kwarg][1] == attributecodes['relative']:
                    modifiedkwargs[kwarg] = self._intcodeoutput[self._relativebase.currentindex + kwargs[kwarg][0][1]]
            else:
                modifiedkwargs[kwarg] = kwargs[kwarg]
        return f(self, *args, **modifiedkwargs)

    return wrap
