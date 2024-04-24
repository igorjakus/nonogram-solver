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
    """Jeżeli w każdym wariancie na i-tej pozycji jest val to na i-tej pozycji musi być val"""
    sure = {}
    for i in range(len(possibilities[0])):
        v = possibilities[0][i]
        if all(possibilities[j][i] == v for j in range(len(possibilities))):
            sure[i] = v
    return sure


def cross_out(possibilities: list, index: int, bit: int, new_value: int):
    """Wykreśla z ORYGINALNEJ LISTY POSSIBILITIES, te które nie spełniają
    nowowydedukowanych wartości."""
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
    """Zamienia macierz będącą rozwiązaniem na odpowiedni obrazek jak w sprawdzaczce"""
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
    """Bierze input i przetwarza na odpowiednie wartości w polach:
    - matrix to dotychczasowe rozwiazanie
    - hint_rows/cols przechowuje dane nam hinty
    - rows/cols_estimation to estymacja dla kazdego wiersza/kolumny ile potrzeba ruchow zeby naprawic"""
    tab = input.split("\n")[:-1]  # usuwamy \n z końca
    height, width = map(int, tab[0].split(" "))

    global hint_rows
    global hint_cols

    # wskazowki podane w inpucie, przesuwamy o 1 bo odczytaliśmy już width i height
    hint_rows = [[int(y) for y in x.split(" ")] for x in tab[1 : height + 1]]
    hint_cols = [[int(y) for y in x.split(" ")] for x in tab[height + 1 :]]

    # inicjalizacja macierzy
    matrix = [[-1 for __ in range(width)] for __ in range(height)]

    # policz możliwości dla każdego wiersza i każdej kolumny
    # trochę wolne ale mamy max. 25 x 25 więc powinno być OK
    row_possibilities = {
        r: generate_possibilities(width, hint) for r, hint in enumerate(hint_rows)
    }
    col_possibilities = {
        c: generate_possibilities(height, hint) for c, hint in enumerate(hint_cols)
    }
    return matrix, row_possibilities, col_possibilities
