from collections import deque
from copy import deepcopy
from nonograms import is_solved
from nonograms import deduction, generate_possibilities, cross_out
from nonograms import matrix_to_output

"""We will fill the matrix with numbers 1 (definitely filled cell) and 0 (definitely empty cell).
At the beginning, we have a height x width matrix filled with -1."""


def solve(input: str):
    return backtrack(*process_input(input))


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


def ac3(matrix, row_possibilities, col_possibilities):
    """Solve using the AC3 algorithm, task 1"""
    to_check = deque(
        [("r", r) for r in range(len(matrix))]
        + [("c", c) for c in range(len(matrix[0]))]
    )

    while to_check:
        kind, index = to_check.popleft()
        if kind == "r":
            possibilities = row_possibilities[index]
        else:
            possibilities = col_possibilities[index]

        # if there are zero possibilities, abandon this path
        if not possibilities:
            raise IndexError("There cannot be zero possibilities!")

        conclusions = deduction(possibilities)

        for k, v in conclusions.items():
            if kind == "r" and matrix[index][k] == -1:
                matrix[index][k] = v
                cross_out(col_possibilities, k, index, v)
                if ("c", k) not in to_check:
                    to_check.append(("c", k))

            elif kind == "c" and matrix[k][index] == -1:
                matrix[k][index] = v
                cross_out(row_possibilities, k, index, v)
                if ("r", k) not in to_check:
                    to_check.append(("r", k))


def backtrack(matrix, row_possibilities, col_possibilities):
    # Deduce what can be deduced
    try:
        ac3(matrix, row_possibilities, col_possibilities)
    except IndexError:
        return False

    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == -1:
                # Recursion - if we have remaining pixels to deduce, take one of them,
                # fill it and check if it works. If not, it must be 0 and deduce further.
                new_matrix = deepcopy(matrix)  # DEEPCOPY OTHERWISE IT DOESN'T WORK......
                new_row_poss = row_possibilities.copy()
                new_col_poss = col_possibilities.copy()
                new_matrix[r][c] = 1
                cross_out(new_row_poss, r, c, 1)
                cross_out(new_col_poss, c, r, 1)

                solution = backtrack(new_matrix, new_row_poss, new_col_poss)
                if solution:
                    return solution

                matrix[r][c] = 0
                cross_out(row_possibilities, r, c, 0)
                cross_out(col_possibilities, c, r, 0)
                return backtrack(matrix, row_possibilities, col_possibilities)

    # If there are no uncertain pixels
    if is_solved(matrix, hint_rows, hint_cols):
        return matrix
    return False


with open("input.txt", "r") as input_file:
    input_data = input_file.read()

solution = solve(input_data)
output = matrix_to_output(solution)


with open("output.txt", "w") as output_file:
    output_file.write(output)
