import utilsfuncs as uf


def calculate_numer_of_digits(layerdata: list, digit: int) -> int:
    """Calculates the amount of specified digit occurrences in a nested iterable (depth = 2)"""
    return len(list(filter(lambda x: True if x == digit else False, 
                                            [ elem for sublist in layerdata for elem in sublist ])))

def calculate_zeroes_per_layer(layersdata: list) -> list:
    """Calculates the amount of zero digits in an iterable nested in an interable, nested in an iterable (depth = 3)"""
    amountofzeros = []
    for layer in layersdata:
        amountofzeros.append(calculate_numer_of_digits(layer, 0))
    
    return amountofzeros

def get_layer_with_fewest_zeroes(layersdata: list) -> list:
    """From a depth-3 nested iterable, retrieves an iterable that containes the fewest amount of zeroes"""
    zeroeslist = calculate_zeroes_per_layer(layersdata)
    
    return layersdata.__getitem__(zeroeslist.index(min(zeroeslist)))

def group_pixels_from_all_layers(layersdata: list, layerwidth: int = 25, layerhight: int = 6) -> list:
    """Flattens a multidimensional array so that points from each dimension that have the same position are stored in the output nested lists, in order"""
    
    return [ 
                [ imagelayer[i][j] for imagelayer in layersdata ] 
                    for i in range(0, layerhight) 
                    for j in range(0, layerwidth)
            ]

def retrieve_colours(pixeldata: list, **kwargs) -> list:
    """Iterates through nested lists, maps the lists to a particular colour as soon as a strong value (0, 1) is found.
    Takes the colours for 'zeroes' and 'ones' as keywords arguments. Returns a flat list of colourized 'pixels'."""
    colourized = []
    for pixel in pixeldata:
        for data in pixel:
            if data == 0:
                colourized.append(kwargs['zeroes'])
                break
            if data == 1:
                colourized.append(kwargs['ones'])
                break
            if data == 2:
                continue
    
    return colourized

def image_printer(imagedata: list, imagewidth: int = 25, imagehight: int = 6) -> None:
    """Groups the characters by specified width and hight. Prints the data row by row"""
    for imagetoprint in uf.grouper(uf.grouper(imagedata, imagewidth), imagehight):
        for row in imagetoprint:
            print("".join(row))
    
    return None


if __name__ == '__main__':

    #get raw transmissiondata as list of integers
    rawtransmissiondata = list(map(
                                    int, 
                                    [x for x in uf.load_input("/home/thegreatmoonmoon/GitRepos/moony-advent-of-code/Day8/inputFiles/inputfile")]
                                    ))

    #group transmissiondata in layers 25 digits wide by 6 digits tall 
    groupedtransmissiondata = list(uf.grouper(uf.grouper(rawtransmissiondata, 25), 6))

    #retrieve the layer with fewest zeroes
    layerwithfewestzeroes = get_layer_with_fewest_zeroes(groupedtransmissiondata)
    
    #calculate amount of ones and twos in the layer of interest
    amountofones = calculate_numer_of_digits(layerwithfewestzeroes, 1)
    amountoftwos = calculate_numer_of_digits(layerwithfewestzeroes, 2)

    #transform and colourize transmission data
    transformedtransmissiondata = group_pixels_from_all_layers(groupedtransmissiondata)
    colourizedtransmission = retrieve_colours(transformedtransmissiondata, zeroes=' ', ones=u"\u2588")

    #print results
    print("Number of 1 digits multiplied by the number of 2 digits in the layer with the fewest 0 digits equals: ", amountofones * amountoftwos)
    image_printer(colourizedtransmission)