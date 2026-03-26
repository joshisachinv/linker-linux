from typing import Tuple

def num_to_col_letters(n: int) -> str:
    if n < 0: return "A"
    result = []
    while True:
        n, r = divmod(n, 26)
        result.append(chr(ord('A') + r))
        if n == 0: break
        n -= 1
    return ''.join(reversed(result))

def cell_address(row: int, col: int) -> str:
    return f"{num_to_col_letters(col)}{row + 1}"

def col_letters_to_num(s: str) -> int:
    s = s.strip().upper()
    total = 0
    for ch in s:
        if 'A' <= ch <= 'Z':
            total = total * 26 + (ord(ch) - ord('A') + 1)
    return max(0, total - 1)

def parse_cell_address(addr: str) -> Tuple[int, int]:
    addr = addr.strip().upper()
    i = 0
    while i < len(addr) and addr[i].isalpha(): i += 1
    col_letters, row_digits = addr[:i], addr[i:]
    try:
        return max(0, int(row_digits) - 1), col_letters_to_num(col_letters)
    except:
        return (0, 0)