from typing import Tuple


def num_to_col_letters(n: int) -> str:
    """Convert zero-based column index to Excel column letters."""
    if n < 0:
        raise ValueError("Column index must be >= 0")

    result = []
    while True:
        n, r = divmod(n, 26)
        result.append(chr(ord("A") + r))
        if n == 0:
            break
        n -= 1

    return "".join(reversed(result))


def cell_address(row: int, col: int) -> str:
    """Convert zero-based row/column indexes to Excel cell address."""
    if row < 0 or col < 0:
        raise ValueError("Row and column indexes must be >= 0")

    return f"{num_to_col_letters(col)}{row + 1}"


def col_letters_to_num(s: str) -> int:
    """Convert Excel column letters to zero-based column index."""
    s = s.strip().upper()
    if not s or not s.isalpha():
        raise ValueError("Column letters must contain only A-Z")

    total = 0
    for ch in s:
        total = total * 26 + (ord(ch) - ord("A") + 1)

    return total - 1


def parse_cell_address(addr: str) -> Tuple[int, int]:
    """Convert Excel cell address like B3 to zero-based (row, col)."""
    addr = addr.strip().upper()
    if not addr:
        raise ValueError("Cell address cannot be empty")

    i = 0
    while i < len(addr) and addr[i].isalpha():
        i += 1

    col_letters = addr[:i]
    row_digits = addr[i:]

    if not col_letters or not row_digits or not row_digits.isdigit():
        raise ValueError(f"Invalid cell address: {addr}")

    row = int(row_digits) - 1
    col = col_letters_to_num(col_letters)

    if row < 0:
        raise ValueError(f"Invalid row in cell address: {addr}")

    return row, col