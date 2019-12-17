from collections import deque


def calculate_stars(size):
    return range(1, size, 2)

def calculate_spaces(size):
    return reversed(range(0, int(size/2)))

def setup_green_area(stars):
    def setup_black_area(spaces):
            return zip(stars, spaces)
    return setup_black_area

def dont_forget_the_trunk(size):
    for _ in range(0, int(size*0.1)):
            print("{}{}".format(' ' * int(size/2/2), '*' * int(size/2 + 1)))

def grow_a_tree(size):
    deque(map(lambda x: print(' ' * x[1], '*' * x[0]), setup_green_area(calculate_stars(size))(calculate_spaces(size))))
    dont_forget_the_trunk(size)


grow_a_tree(100)
