class Cell:
    # set of possible values
    values = []
    # reference to the whole sudoku
    sudoku = {}
    # row and column indexes
    row = 0
    column = 0

    final_value = 0

    # initialize the cell with every possible value
    def __init__(self, row, column, sudoku):
        self.values = []
        for i in range(1, sudoku.SIZE + 1):
            self.values.append(i)
        self.sudoku = sudoku
        self.row = row
        self.column = column

    # returns the set of possible values for the cell
    def get_possibilities(self):
        return self.values

    def remove_number(self, number):
        try:
            self.values.remove(number)
            return True
        except:
            return False

    # removes a possibility, if only one is remaining, calls the 'insert number' function,
    # otherwise if there's no value left, it throws an exception
    def remove_possibility(self, number):
        if self.remove_number(number):
            if len(self.values) == 0:
                raise
            elif len(self.values) == 1:
                self.sudoku.insert_number(self.row, self.column, self.values[0])

    # true if there's only one value left
    def is_fixed(self):
        return self.final_value != 0

    def print_possibilities(self):
        if len(self.values) == 1:
            print (str(self.final_value) + '  '),
        else:
            print ('?' + str(len(self.values)) + ' '),

    def set_number(self, number):
        if number not in self.values:
            raise
        if self.final_value == 0:
            self.values = []
            self.values.append(number)
            self.final_value = number
        else:
            raise


class Sudoku:
    # size of the sector and number of sectors
    BASE_SIZE = 3
    SIZE = BASE_SIZE * BASE_SIZE

    # Row first then columns
    grid = []

    # initialize empty sudoku
    def __init__(self):
        self.grid.insert(0, {})
        for i in range(1, self.SIZE + 1):
            row = [{}]
            for j in range(1, self.SIZE + 1):
                cell = Cell(i, j, self)
                row.insert(j, cell)
            self.grid.insert(i, row)

    # insert number 'number' on row 'row' and column 'column'
    def insert_number(self, row, column, number):
        self.grid[row][column].set_number(number)
        self.remove_in_column(row, column, number)
        self.remove_in_row(row, column, number)
        self.remove_in_sector(row, column, number)
        self.check_trivials()

    # removes the inserted number in the specified row (except for the the specified column)
    def remove_in_row(self, row, column, number):
        i = 0
        for cell in self.grid[row]:
            if i > 0:
                if i != column:
                    cell.remove_possibility(number)
            i += 1

    # removes the inserted number in the specified column (except for the the specified row)
    def remove_in_column(self, row, column, number):
        for j in range(1, self.SIZE + 1):
            cell_row = self.grid[j]
            cell = cell_row[column]
            if j != row:
                cell.remove_possibility(number)

    # removes the inserted number in the corresponding sector (except for the the specified row and column)
    def remove_in_sector(self, row, column, number):
        base_row = (row - 1) // 3
        base_column = (column - 1) // 3
        for i in range(1, self.BASE_SIZE + 1):
            for j in range(1, self.BASE_SIZE + 1):
                x = base_row * self.BASE_SIZE + i
                y = base_column * self.BASE_SIZE + j
                cell = self.grid[x][y]
                if x != row or y != column:
                    cell.remove_possibility(number)

    def print_possibilities(self):
        for i in range(1, self.SIZE + 1):
            for j in range(1, self.SIZE + 1):
                self.grid[i][j].print_possibilities()
            print

    def check_trivials(self):
        self.check_rows()
        self.check_columns()
        self.check_sectors()

    def check_rows(self):
        for row in range(1, self.SIZE + 1):
            i = 0
            numbers = {}
            for cell in self.grid[row]:
                if i > 0:
                    possibilities = cell.get_possibilities()
                    for possibility in possibilities:
                        if possibility not in numbers.keys():
                            numbers[possibility] = []
                        numbers[possibility].append(cell)
                i += 1

            for i in range(1, self.SIZE + 1):
                if len(numbers[i]) == 1:
                    if not numbers[i][0].is_fixed():
                        self.insert_number(numbers[i][0].row, numbers[i][0].column, i)
                elif len(numbers[i]) == 0:
                    raise

    def check_columns(self):
        for column in range(1, self.SIZE + 1):
            numbers = {}
            for j in range(1, self.SIZE + 1):
                cell_row = self.grid[j]
                cell = cell_row[column]
                possibilities = cell.get_possibilities()
                for possibility in possibilities:
                    if possibility not in numbers.keys():
                        numbers[possibility] = []
                    numbers[possibility].append(cell)

            for i in range(1, self.SIZE + 1):
                if len(numbers[i]) == 1:
                    if not numbers[i][0].is_fixed():
                        self.insert_number(numbers[i][0].row, numbers[i][0].column, i)
                elif len(numbers[i]) == 0:
                    raise

    def check_sectors(self):
        for base_row in range(0, self.BASE_SIZE):
            for base_column in range(0, self.BASE_SIZE):
                numbers = {}
                for i in range(1, self.BASE_SIZE + 1):
                    for j in range(1, self.BASE_SIZE + 1):
                        x = base_row * self.BASE_SIZE + i
                        y = base_column * self.BASE_SIZE + j
                        cell = self.grid[x][y]
                        possibilities = cell.get_possibilities()
                        for possibility in possibilities:
                            if possibility not in numbers:
                                numbers[possibility] = []
                            numbers[possibility].append(cell)

                for i in range(1, self.SIZE + 1):
                    if len(numbers[i]) == 1:
                        if not numbers[i][0].is_fixed():
                            self.insert_number(numbers[i][0].row, numbers[i][0].column, i)
                    elif len(numbers[i]) == 0:
                        raise


def sudoku_to_dag(input_sudoku):
    sudoku = Sudoku()
    sudoku.insert_number(1, 1, 7)
    sudoku.insert_number(1, 2, 1)
    sudoku.insert_number(1, 3, 6)
    sudoku.insert_number(1, 5, 3)
    sudoku.insert_number(1, 6, 8)
    sudoku.insert_number(1, 9, 9)

    sudoku.insert_number(2, 5, 9)
    sudoku.insert_number(2, 6, 5)
    sudoku.insert_number(2, 7, 6)
    sudoku.insert_number(2, 8, 7)

    sudoku.insert_number(3, 1, 5)
    sudoku.insert_number(3, 2, 9)
    sudoku.insert_number(3, 4, 7)
    sudoku.insert_number(3, 8, 3)
    sudoku.insert_number(3, 9, 4)

    sudoku.insert_number(4, 1, 1)
    sudoku.insert_number(4, 4, 9)
    sudoku.insert_number(4, 6, 6)
    sudoku.insert_number(4, 7, 7)
    sudoku.insert_number(4, 9, 3)

    sudoku.insert_number(5, 1, 9)
    sudoku.insert_number(5, 3, 3)
    sudoku.insert_number(5, 4, 1)
    sudoku.insert_number(5, 7, 5)
    sudoku.insert_number(5, 8, 2)

    sudoku.insert_number(6, 2, 2)
    sudoku.insert_number(6, 3, 7)
    sudoku.insert_number(6, 4, 5)
    sudoku.insert_number(6, 5, 8)
    sudoku.insert_number(6, 7, 1)

    sudoku.insert_number(7, 3, 1)
    sudoku.insert_number(7, 4, 3)
    sudoku.insert_number(7, 5, 7)
    sudoku.insert_number(7, 6, 9)
    sudoku.insert_number(7, 8, 8)

    sudoku.insert_number(8, 1, 8)

    sudoku.print_possibilities()


if __name__ == "__main__":
    sudoku_to_dag({})
