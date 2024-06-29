from random import randint, choice, random
from walksat.est import estimation


class NonogramSolver:
    def __init__(self, input: str):
        """Takes input and processes it into appropriate fields:
        - matrix is the current solution
        - hint_rows/cols stores the given hints
        - rows/cols_estimation is an estimation for each row/column of how many moves are needed to solve"""
        tab = input.split("\n")[:-1]  # remove \n from the end
        height, width = map(int, tab[0].split(" "))

        # hints given in the input, shift by 1 because we have already read width and height
        self.hint_rows = [[int(y) for y in x.split(" ")] for x in tab[1 : height + 1]]
        self.hint_cols = [[int(y) for y in x.split(" ")] for x in tab[height + 1 :]]

        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.matrix = [[randint(0, 1) for _ in range(self.width)] for _ in range(self.height)]
        self.rows_estimation = {r: estimation(self.matrix[r], self.hint_rows[r]) for r in range(self.height)}
        self.cols_estimation = {c: estimation(self.get_col(c), self.hint_cols[c]) for c in range(self.width)}

    def get_col(self, col_index):
        return [self.matrix[y][col_index] for y in range(self.height)]

    def bad_rows(self):
        return [row for row, est in self.rows_estimation.items() if est != 0]

    def bad_cols(self):
        return [col for col, est in self.cols_estimation.items() if est != 0]

    def is_solved(self):
        return not self.bad_rows() and not self.bad_cols()

    def est_diff(self, r, c):
        self.matrix[r][c] ^= 1
        new_row_est = estimation(self.matrix[r], self.hint_rows[r])
        new_col_est = estimation(self.get_col(c), self.hint_cols[c])
        self.matrix[r][c] ^= 1
        return (new_row_est - self.rows_estimation[r]) + (new_col_est - self.cols_estimation[c])

    def best_pixel_in_scope(self, iterable_rows, iterable_cols):
        """Returns the best pixel among rows x columns given in the argument,
        if several are optimal, choose one of them randomly"""
        min_diff = float("inf")
        best_pixels = [(choice(iterable_rows), choice(iterable_cols))]

        for r in iterable_rows:
            for c in iterable_cols:
                diff = self.est_diff(r, c)

                if diff < min_diff:
                    min_diff = diff
                    best_pixels = [(r, c)]
                elif diff == min_diff:
                    best_pixels.append((r, c))

        return choice(best_pixels)  

    def pick_pixel(self):
        bad_rows = self.bad_rows()
        bad_cols = self.bad_cols()

        if bad_rows and random() >= 0.5:
            bad_row = [choice(bad_rows)]
            return self.best_pixel_in_scope(bad_row, range(self.width))
        elif bad_cols:
            bad_col = [choice(bad_cols)]
            return self.best_pixel_in_scope(range(self.height), bad_col)
        else:
            row = randint(0, self.height - 1)
            col = randint(0, self.width - 1)
            return (row, col)

    def make_move(self, pixel):
        row, col = pixel
        self.matrix[row][col] ^= 1
        self.rows_estimation[row] = estimation(self.matrix[row], self.hint_rows[row])
        self.cols_estimation[col] = estimation(self.get_col(col), self.hint_cols[col])

    def solve(self):
        counter = 0
        while not self.is_solved():
            if counter % (self.height * self.width * 15) == 0:
                self.reset()

            pixel = self.pick_pixel()
            self.make_move(pixel)
            counter += 1

        print(counter)
        return self.matrix


def matrix_to_output(matrix):
    """Converts the solution matrix into the appropriate picture format as in the checker"""
    out = ""
    for row in matrix:
        for x in row:
            out += "#" if x == 1 else "."
        out += "\n"
    return out


with open("zad_input.txt", "r") as input_file:
    solver = NonogramSolver(input_file.read())

solution = solver.solve()
output = matrix_to_output(solution)

with open("zad_output.txt", "w") as output_file:
    output_file.write(output)
