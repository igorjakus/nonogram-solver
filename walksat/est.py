from functools import cache


def estimation(row, hints):
    # change to tuple to hash properly :)
    return estimate_row(tuple(row), tuple(hints))


@cache  # memoization for entire rows and hints
def estimate_row(row_tuple, hints_tuple):
    # cast to appropriate lists
    row = list(row_tuple)
    hints = list(hints_tuple)

    @cache  # memoization inside the row and hint estimation calculation
    def backtrack(start, hint_index):
        if hint_index == len(hints):
            return sum(row[start:])

        hint = hints[hint_index]
        min_changes = float("inf")

        # how many bits need to be set where the hint is
        bit_changes = sum(bit == 0 for bit in row[start : start + hint])

        # length - (remaining hints + remaining spaces - no gaps at the front and back)
        end = len(row) - (sum(hints[hint_index:]) + len(hints) - hint_index - 2) 
        for i in range(start, end):
            if i != start:
                bit_changes += row[i + hint - 1] == 0
                bit_changes += 1 if row[i - 1] == 1 else -1

            help = backtrack(i + hint + 1, hint_index + 1)

            if i + hint < len(row) and row[i + hint] == 1:
                min_changes = min(min_changes, bit_changes + 1 + help)
            else:
                min_changes = min(min_changes, bit_changes + help)

        return min_changes

    return backtrack(0, 0)
