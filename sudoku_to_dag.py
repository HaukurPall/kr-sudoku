from graph_tool.all import *
import matplotlib

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
    def __init__(self, row, column, sudoku, possibilities=[], final_value=0):
        if possibilities == []:
            self.values = []
            for i in range(1, sudoku.SIZE + 1):
                self.values.append(i)
        else:
            self.values = possibilities[:]
        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.final_value = final_value

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

    def get_state(self):
        if not self.is_fixed():
            return '?'
        else:
            return str(self.final_value) + '-'


class Sudoku:
    # size of the sector and number of sectors
    BASE_SIZE = 3
    SIZE = BASE_SIZE * BASE_SIZE

    # count of inserted numbers
    count = 0

    # Row first then columns
    grid = []

    # initialize empty sudoku
    def __init__(self, grid=[], count=0):
        if grid == []:
            self.grid.insert(0, {})
            for i in range(1, self.SIZE + 1):
                row = [{}]
                for j in range(1, self.SIZE + 1):
                    cell = Cell(i, j, self)
                    row.insert(j, cell)
                self.grid.insert(i, row)
            count = 0
        else:
            self.grid = grid
            self.count = count

    # insert number 'number' on row 'row' and column 'column'
    def insert_number(self, row, column, number):
        self.grid[row][column].set_number(number)
        self.count += 1
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

    def is_complete(self):
        return self.count == self.SIZE * self.SIZE

    def encode(self):
        string = ''
        for i in range(1, self.SIZE + 1):
            for j in range(1, self.SIZE + 1):
                string += self.grid[i][j].get_state()
        return string

    def create_copy(self):
        grid = [{}]
        c = self.count
        sudoku = Sudoku(grid=grid, count=c)
        for i in range(1, self.SIZE + 1):
            row = [{}]
            for j in range(1, self.SIZE + 1):
                cell = Cell(self.grid[i][j].row, self.grid[i][j].column, sudoku,
                            possibilities=self.grid[i][j].get_possibilities(), final_value=self.grid[i][j].final_value)
                row.append(cell)
            grid.append(row)
        return sudoku


class SudokuNodeManager:
    sudoku_nodes = {}
    incorrect_solutions_count = 0
    correct_solutions_count = 0

    def __init__(self):
        self.incorrect_solutions_count = 0
        self.correct_solutions_count = 0

    def add_sudoku_node(self, sudoku_node):
        key = sudoku_node.encode()
        if key in self.sudoku_nodes.keys():
            return self.sudoku_nodes[key]
        else:
            self.sudoku_nodes[key] = sudoku_node
            if sudoku_node.sudoku.is_complete():
                self.correct_solutions_count += 1
            return None

    def get_nodes_number(self):
        return len(self.sudoku_nodes.keys())

    def get_sudoku_node(self, key):
        return self.sudoku_nodes[key]

    def add_incorrect_solution(self):
        self.incorrect_solutions_count += 1

    def get_incorrect_solutions_count(self):
        return self.incorrect_solutions_count

    def get_correct_soultuins_count(self):
        return self.correct_solutions_count


class Move:
    row = 0
    column = 0
    number = 0

    def __init__(self, row, column, number):
        self.row = row
        self.column = column
        self.number = number

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_number(self):
        return self.number


class SudokuNode:
    paths = {}
    sudoku = {}
    sudoku_manager = {}
    leaf = False

    def __init__(self, sudoku, sudoku_manager):
        self.sudoku = sudoku
        self.sudoku_manager = sudoku_manager
        self.paths = {"incorrect": []}

    def encode(self):
        return self.sudoku.encode()

    def compute(self):
        computed = self.sudoku_manager.add_sudoku_node(self)
        if not computed:
            for i in range(1, self.sudoku.SIZE):
                for j in range(1, self.sudoku.SIZE):
                    possibilities = self.sudoku.grid[i][j].get_possibilities()
                    if len(possibilities) > 1:
                        for possibility in possibilities:
                            sudoku = self.sudoku.create_copy()
                            sudoku_node = {}
                            try:
                                sudoku.insert_number(i, j, possibility)
                                sudoku_node = SudokuNode(sudoku, self.sudoku_manager)
                                key = sudoku.encode()
                                if key not in self.paths.keys():
                                    self.paths[key] = []
                                self.paths[key].append(Move(i, j, possibility))
                                sudoku_node.compute()

                            except:
                                self.sudoku_manager.add_incorrect_solution()



    def print_graph(self):
        graph = Graph()

        node_map = {}
        for node in self.sudoku_manager.sudoku_nodes:
            node_map[node] = graph.add_vertex()

        nodes = [self]
        visited = set()
        edges = set()
        while len(nodes) > 0:
            print len(nodes)
            node = nodes.pop()
            for key in self.paths.keys():
                link_from = node.sudoku.encode()
                link_to = key
                if (link_from, link_to) not in edges:
                    if link_to in node_map.keys():
                        graph.add_edge(node_map[link_from], node_map[link_to])
                        edges.add((link_from, link_to))
                        if link_to not in visited:
                            nodes.append(self.sudoku_manager.get_sudoku_node(link_to))
                            visited.add(link_to)
                    else:
                        fail = graph.add_vertex()
                        graph.add_edge(node_map[link_from], fail)
                        pass


                else:
                    pass

        print "here"
        graph_draw(graph, output_size=(1000, 1000), vertex_text=graph.vertex_index, output="graph.png")


def sudoku_to_dag(input_sudoku):
    sudoku_node_manager = SudokuNodeManager()

    sudoku = Sudoku()
    sudoku.insert_number(1, 1, 7)
    sudoku.insert_number(1, 2, 1)
    sudoku.insert_number(1, 3, 6)
    sudoku.insert_number(1, 6, 8)
    sudoku.insert_number(1, 9, 9)

    sudoku.insert_number(2, 5, 9)
    sudoku.insert_number(2, 6, 5)
    sudoku.insert_number(2, 7, 6)
    sudoku.insert_number(2, 8, 7)

    sudoku.insert_number(3, 1, 5)
    sudoku.insert_number(3, 2, 9)
    sudoku.insert_number(3, 8, 3)
    sudoku.insert_number(3, 9, 4)

    sudoku.insert_number(4, 1, 1)
    sudoku.insert_number(4, 4, 9)
    sudoku.insert_number(4, 6, 6)
    sudoku.insert_number(4, 7, 7)
    sudoku.insert_number(4, 9, 3)

    #sudoku.insert_number(5, 1, 9)
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

    sudoku_node = SudokuNode(sudoku, sudoku_node_manager)
    sudoku_node.compute()



    print ("There are {} correct solutions, {} intermediate nodes and {} incorrect possibilities".format(
        sudoku_node_manager.get_correct_soultuins_count(),
        sudoku_node_manager.get_nodes_number(),
        sudoku_node_manager.get_incorrect_solutions_count()))

    sudoku_node.print_graph()


if __name__ == "__main__":
    sudoku_to_dag({})
