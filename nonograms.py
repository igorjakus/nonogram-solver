def generate_possibilities(row_length: int, hints: list):
    """5, [3] -> [[1,1,1,0,0], [0,1,1,1,0], [0,0,1,1,1]]"""

    def backtrack(start, hint_index):
        if hint_index == len(hints):
            return [[0] * (row_length - start)]

        possibilities = []

        for s in range(start, row_length - sum(hints[hint_index:]) - (len(hints) - hint_index) + 2):
            if hint_index < len(hints) - 1:
                row = [0] * (s - start) + [1] * hints[hint_index] + [0]
                new_possibilities = backtrack(s + hints[hint_index] + 1, hint_index + 1)
            else:
                row = [0] * (s - start) + [1] * hints[hint_index]
                new_possibilities = backtrack(s + hints[hint_index], hint_index + 1)

            possibilities += [row + np for np in new_possibilities]

        return possibilities

    return backtrack(0, 0)


def deduction(possibilities):
    """If in every variant at the i-th position there is a value, then at the i-th position it must be that value"""
    sure = {}
    for i in range(len(possibilities[0])):
        v = possibilities[0][i]
        if all(possibilities[j][i] == v for j in range(len(possibilities))):
            sure[i] = v
    return sure


def cross_out(possibilities: list, index: int, bit: int, new_value: int):
    """Cross out from the ORIGINAL LIST OF POSSIBILITIES those that do not meet
    the newly deduced values."""
    possibilities[index] = list(filter(lambda xs: xs[bit] == new_value, possibilities[index]))


def get_col(matrix, col_index):
    return [matrix[y][col_index] for y in range(len(matrix))]


def make_hint(row):
    hint = []
    streak = 0
    for x in row:
        if x == 1:
            streak += 1
        elif streak > 0:
            hint.append(streak)
            streak = 0
    if streak > 0:
        hint.append(streak)
    return hint


def is_good(row, hint):
    return hint == make_hint(row)


def is_solved(matrix, hints_rows, hints_cols):
    for i in range(len(hints_rows)):
        if not is_good(matrix[i], hints_rows[i]):
            return False
    for i in range(len(hints_cols)):
        if not is_good(get_col(matrix, i), hints_cols[i]):
            return False
    return True


def matrix_to_output(matrix):
    """Converts the solution matrix into the appropriate picture format as in the checker"""
    out = ""
    for row in matrix:
        for x in row:
            if x == 1:
                out += "#"
            elif x == 0:
                out += "."
            else:
                out += "?"
        out += "\n"
    return out


def process_input(input):
    """Takes the input and processes it into appropriate fields:
    - matrix is the current solution
    - hint_rows/cols stores the given hints
    - rows/cols_estimation is an estimation for each row/column of how many moves are needed to solve"""
    tab = input.split("\n")[:-1]  # remove \n from the end
    height, width = map(int, tab[0].split(" "))

    global hint_rows
    global hint_cols

    # hints given in the input, shift by 1 because we have already read width and height
    hint_rows = [[int(y) for y in x.split(" ")] for x in tab[1 : height + 1]]
    hint_cols = [[int(y) for y in x.split(" ")] for x in tab[height + 1 :]]

    # initialize the matrix
    matrix = [[-1 for __ in range(width)] for __ in range(height)]

    # calculate possibilities for each row and each column
    # a bit slow but we have max. 25 x 25 so it should be OK
    row_possibilities = {
        r: generate_possibilities(width, hint) for r, hint in enumerate(hint_rows)
    }
    col_possibilities = {
        c: generate_possibilities(height, hint) for c, hint in enumerate(hint_cols)
    }
    return matrix, row_possibilities, col_possibilities
