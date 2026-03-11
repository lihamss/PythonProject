import pytest

from hw01.nqueens import format_solution, is_valid_solution, iter_n_queens_solutions, solve_n_queens


@pytest.mark.parametrize(
    ("n", "expected_count"),
    [
        (0, 1),  # empty board
        (1, 1),
        (2, 0),
        (3, 0),
        (4, 2),
        (8, 92),
    ],
)
def test_solution_counts(n: int, expected_count: int) -> None:
    sols = solve_n_queens(n)
    assert len(sols) == expected_count


def test_solutions_are_valid_and_unique_for_8() -> None:
    sols = solve_n_queens(8)
    assert len(sols) == 92
    assert all(is_valid_solution(s) for s in sols)
    assert len(set(sols)) == len(sols)


def test_iter_and_solve_match() -> None:
    n = 6
    a = list(iter_n_queens_solutions(n))
    b = solve_n_queens(n)
    assert a == b


def test_format_solution_round_trip_validation() -> None:
    sol = solve_n_queens(4)[0]
    board = format_solution(sol)
    lines = board.splitlines()
    assert len(lines) == 4
    assert all(len(line) == 4 for line in lines)
    assert sum(line.count("Q") for line in lines) == 4
    assert is_valid_solution(sol)


def test_invalid_n_rejected() -> None:
    with pytest.raises(ValueError):
        solve_n_queens(-1)
    with pytest.raises(TypeError):
        solve_n_queens(8.0)  # type: ignore[arg-type]

