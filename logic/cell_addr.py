from typing import Tuple

def num_to_col_letters(n: int) -> str:
    """
    Converts 0-based column index to Excel letters (e.g., 0 -> A, 25 -> Z, 26 -> AA).
    """
    if n < 0: return "A"
    result = []
    while True:
        n, r = divmod(n, 26)
        result.append(chr(ord('A') + r))
        if n == 0:
            break
        n -= 1
    return ''.join(reversed(result))

def col_letters_to_num(s: str) -> int:
    """
    Converts Excel letters back to 0-based column index (e.g., A -> 0, B -> 1).
    """
    if not s: return 0
    s = s.strip().upper()
    total = 0
    for ch in s:
        if 'A' <= ch <= 'Z':
            total = total * 26 + (ord(ch) - ord('A') + 1)
    return max(0, total - 1)

def cell_address(row: int, col: int) -> str:
    """
    Combines 0-based row and column into a standard Excel address (e.g., 0,0 -> A1).
    """
    return f"{num_to_col_letters(col)}{row + 1}"

def parse_cell_address(addr: str) -> Tuple[int, int]:
    """
    Splits an Excel address like 'B10' into (row 9, col 1).
    """
    if not addr: return (0, 0)
    addr = addr.strip().upper()
    
    # Find where the letters end and numbers begin
    i = 0
    while i < len(addr) and addr[i].isalpha():
        i += 1
        
    col_letters = addr[:i]
    row_digits = addr[i:]
    
    try:
        row = int(row_digits) - 1 if row_digits else 0
        col = col_letters_to_num(col_letters)
        return max(0, row), col
    except ValueError:
        return (0, 0)