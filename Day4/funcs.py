def candidate_generator(startrange, endrange):
    candidate = startrange
    while candidate <= endrange:
        yield candidate
        candidate += 1

def validate_for_adjacent(candidate):
    candidatestr = str(candidate)
    previous = 'x'
    for char in candidatestr:
        if char == previous:
            return True
        previous = char
    return False

def validate_for_increase(candidate):
    candidatestr = str(candidate)
    previous = '0'
    for char in candidatestr:
        if int(char) < int(previous):
            return False
        previous = char
    return True
    

if __name__ == "__main__":
    
    testpack = [validate_for_adjacent, validate_for_increase]
    
    candidate = 111111
    results = (map(lambda test: test(candidate), testpack))
    
    assert all(results) == True

    candidate = 223450
    results = (map(lambda test: test(candidate), testpack))
    
    assert all(results) == False

    candidate = 123789
    results = (map(lambda test: test(candidate), testpack))
    
    assert all(results) == False
    

