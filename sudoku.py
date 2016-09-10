from sudoku_gen import construct_puzzle_solution, pluck
from sudoku_to_dag import Sudoku, Cell


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


if __name__ == "__main__":
    puzzle = create_a_puzzle(22)
    sudoku = Sudoku(puzzle)

    print sudoku.count_all_possibilities()

    #write_puzzle_to_disk(puzzle)
