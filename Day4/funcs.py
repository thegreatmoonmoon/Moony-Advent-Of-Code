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

def validate_for_adjacent_pairs_only(candidate):
    candidatestr = str(candidate)
    pairs = []
    endresults = []

    for i in range(0, len(candidatestr)):
        if i != len(candidatestr) - 1:
            if candidatestr[i] == candidatestr[i+1] or candidatestr[i] == candidatestr[i-1]:
                pairs.append(candidatestr[i])
        else:
            if candidatestr[i] == candidatestr[i-1]:
                pairs.append(candidatestr[i])
    
    results = {char:pairs.count(char) for char in pairs}
    
    for result in results:
        if results[result] == 2:
            endresults.append(True)
        else:
            endresults.append(False)

    return any(endresults)

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
    
    candidate = 112233
    assert validate_for_adjacent_pairs_only(candidate) == True

    candidate = 123444
    assert validate_for_adjacent_pairs_only(candidate) == False

    candidate = 111122
    assert validate_for_adjacent_pairs_only(candidate) == True