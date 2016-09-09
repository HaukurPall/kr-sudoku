from sudoku_gen import construct_puzzle_solution, pluck

def create_a_puzzle(filled_spaces=22):
    a_puzzle_solution = construct_puzzle_solution()
    result, number_of_cells = pluck(a_puzzle_solution, filled_spaces)
    return result


def write_puzzle_to_disk(puzzle):
    stringified = stringify_puzzle(puzzle)
    name = str(hash(stringified))
    f = open('resources/' + name, 'w')
    f.write(stringified)
    f.close()


def stringify_puzzle(puzzle):
    string = ''
    for box in puzzle:
        for number in box:
            string += str(number)
    return string

def find_options_for_row(boxNr, numberNr, puzzle):
    startingBox = boxNr/3
    return {1}

def find_options_for_column(boxNr, numberNr, puzzle):
    return {1}

def find_options_for_box(boxNr, numberNr, puzzle):
    return {1}

def find_options_for(boxNr, numberNr, puzzle):
    all_options = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    options = all_options.intersection(find_options_for_row(boxNr, numberNr, puzzle))
    options = options.intersection(find_options_for_column(boxNr, numberNr, puzzle))
    options = options.intersection(find_options_for_box(boxNr, numberNr, puzzle))

"""
Converts an un set number to a set of possibilites. I.e. 0 to a {1,2,3,..}
"""
def add_guess_sets(puzzle):
    for boxNr, box in enumerate(puzzle):
        for numberNr, number in enumerate(box):
            if number == 0:
                options = find_options_for(boxNr, numberNr, puzzle)

puzzle = create_a_puzzle(22)
write_puzzle_to_disk(puzzle)
