import utilsfuncs as uf


if __name__ == '__main__':

    #get raw transmissiondata as list of integers
    rawtransmissiondata = list(map(int, [x for x in uf.load_input("inputFiles/inputfile")]))

    #group transmissiondata in layers 25 digits wide by 6 digits tall 
    groupedtransmissiondata = list(uf.grouper(uf.grouper(rawtransmissiondata, 25), 6))

    #calculate amount of zeroes for each of the layers
    amountofzeros = []
    for layer in groupedtransmissiondata:
        amountofzeros.append(len(list(filter(lambda x: True if x == 0 else False, 
                                            [ elem for sublist in layer for elem in sublist]))))

    #retrieve the layer with the least amount of zeroes
    layerofinterest = groupedtransmissiondata.__getitem__(amountofzeros.index(min(amountofzeros)))

    #calculate amount of ones and twos in the layer of interest
    amountofones = len(list(filter(lambda x: True if x == 1 else False, 
                                            [ elem for sublist in layerofinterest for elem in sublist])))
    amountoftwos = len(list(filter(lambda x: True if x == 2 else False, 
                                            [ elem for sublist in layerofinterest for elem in sublist])))

    print("Number of 1 digits multiplied by the number of 2 digits in the layer with the fewest 0 digits equals: ", amountofones * amountoftwos)