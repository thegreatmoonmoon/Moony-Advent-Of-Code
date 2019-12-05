from funcs import validate_for_increase, validate_for_adjacent, candidate_generator, validate_for_adjacent_pairs_only

if __name__ == "__main__":
    
    testpack = [validate_for_increase, validate_for_adjacent, validate_for_adjacent_pairs_only]
    counter = 0

    for candidate in candidate_generator(307237, 769058):
        results = (map(lambda test: test(candidate), testpack))
        if all(results):
            counter += 1

    print(counter)