from collections import deque
from copy import deepcopy
from nonograms import is_solved
from nonograms import deduction, generate_possibilities, cross_out
from nonograms import matrix_to_output

"""Będziemy macierz wypełniać liczbami 1 (na pewno zamazane pole), oraz 0 (na pewno puste pole).
Na początku mamy macierz height x width wypełnioną samymi -1."""


def solve(input: str):
    return backtrack(*process_input(input))


def process_input(input):
    """Bierze input i przetwarza na odpowiednie§ wartości w polach:
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


def ac3(matrix, row_possibilities, col_possibilities):
    """Rozwiązujemy algorytmem ac3, zadanie 1"""
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

        # jak jest zero możliwości to trzeba porzucić tą ścieżkę
        if not possibilities:
            raise IndexError("Nie może być zero możliwości!")

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
    # Wydedukuj co się da
    try:
        ac3(matrix, row_possibilities, col_possibilities)
    except IndexError:
        return False

    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == -1:
                # Rekurencja - jeżeli mamy pozostałe pixele do wydedukowania to weź jeden z nich,
                # zamaż i sprawdź czy działa. Jeżeli nie to musi być tam 0 i dedukuj dalej.
                new_matrix = deepcopy(matrix)  # DEEPCOPY INACZEJ NIE DZIALA ......
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

    # Jeżeli nie ma żadnych pixeli niepewnych
    if is_solved(matrix, hint_rows, hint_cols):
        return matrix
    return False


with open("input.txt", "r") as input_file:
    input_data = input_file.read()

solution = solve(input_data)
output = matrix_to_output(solution)


with open("output.txt", "w") as output_file:
    output_file.write(output)
