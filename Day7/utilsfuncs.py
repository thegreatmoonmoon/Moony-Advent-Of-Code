def load_input(filepath):
    """Function to return a list of input variables from file"""  
    with open(filepath, "r") as inputfile:
            return inputfile.read().split(",")