def load_input(filepath):
    """Function to return a list of input variables from file"""  
    inputlist = []
    with open(filepath, "r") as inputfile:
        for line in inputfile:
            inputlist.append(line.rstrip().split(","))
    return inputlist