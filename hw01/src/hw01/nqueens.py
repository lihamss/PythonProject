from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Sequence, Tuple


BoardSolution = Tuple[int, ...]


@dataclass(frozen=True, slots=True)
class NQueensResult:
    n: int
    solutions: Tuple[BoardSolution, ...]

    def __len__(self) -> int:  # pragma: no cover
        return len(self.solutions)


def solve_n_queens(n: int) -> List[BoardSolution]:
    """
    返回所有解。每个解用长度为 n 的元组表示：solution[row] = col。
    """
    return list(iter_n_queens_solutions(n))


def iter_n_queens_solutions(n: int) -> Iterator[BoardSolution]:
    """
    生成所有解。每个解用长度为 n 的元组表示：solution[row] = col。
    """
    _validate_n(n)
    if n == 0:
        yield ()
        return

    full_mask = (1 << n) - 1
    placement: List[int] = [-1] * n

    def backtrack(row: int, cols: int, diag1: int, diag2: int) -> Iterator[BoardSolution]:
        if row == n:
            yield tuple(placement)
            return

        available = ~(cols | diag1 | diag2) & full_mask
        while available:
            bit = available & -available
            available -= bit

            col = (bit.bit_length() - 1)
            placement[row] = col

            yield from backtrack(
                row + 1,
                cols | bit,
                (diag1 | bit) << 1,
                (diag2 | bit) >> 1,
            )

    yield from backtrack(0, 0, 0, 0)


def solve(n: int) -> NQueensResult:
    """返回包含全部解的结果对象。"""
    sols = tuple(iter_n_queens_solutions(n))
    return NQueensResult(n=n, solutions=sols)


def format_solution(solution: Sequence[int]) -> str:
    """
    将解格式化为棋盘字符串（'Q' 表示皇后，'.' 表示空位）。
    """
    n = len(solution)
    rows: List[str] = []
    for r, c in enumerate(solution):
        if not (0 <= c < n):
            raise ValueError(f"invalid column at row {r}: {c}")
        rows.append("." * c + "Q" + "." * (n - c - 1))
    return "\n".join(rows)


def is_valid_solution(solution: Sequence[int]) -> bool:
    """校验解是否满足：每行/列至多一个皇后，且无对角线冲突。"""
    n = len(solution)
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    for r, c in enumerate(solution):
        if not isinstance(c, int):
            return False
        if not (0 <= c < n):
            return False
        if c in cols:
            return False
        d1 = r - c
        d2 = r + c
        if d1 in diag1 or d2 in diag2:
            return False
        cols.add(c)
        diag1.add(d1)
        diag2.add(d2)
    return True


def _validate_n(n: int) -> None:
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 0:
        raise ValueError("n must be >= 0")

