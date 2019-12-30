import itertools


def load_input(filepath):
    """Function to return a list of input variables from file"""  
    with open(filepath, "r") as inputfile:
            return inputfile.read()

def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF GXX
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)