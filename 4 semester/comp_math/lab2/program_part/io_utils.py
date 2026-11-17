from __future__ import annotations

import json
from pathlib import Path

from program_part.models import ChordRow, EquationProblem, IterationRow, NewtonSystemRow, SecantRow, SystemProblem
from program_part.number_utils import format_number, parse_real


def read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return parse_real(raw, prompt.rstrip(": "))
        except ValueError as error:
            print(error)


def read_int(prompt: str, allowed: set[str] | None = None) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Введите значение.")
            continue
        if allowed is not None and value not in allowed:
            print(f"Недопустимое значение. Ожидается одно из: {', '.join(sorted(allowed))}.")
            continue
        return value


def load_json_config(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON: {error.msg}") from error
    if not isinstance(data, dict):
        raise ValueError("JSON-файл должен содержать объект с параметрами.")
    return data


def output_report(text: str, destination: str, path: str | None = None) -> None:
    if destination == "1":
        print()
        print(text)
        return

    if not path:
        raise ValueError("Не указан путь для сохранения результата.")
    Path(path).write_text(text, encoding="utf-8")
    print(f"Результат сохранен в файл: {path}")


def read_equation_params_keyboard() -> dict:
    return {
        "a": read_float("Введите левую границу интервала a: "),
        "b": read_float("Введите правую границу интервала b: "),
        "eps": read_float("Введите точность eps: "),
    }


def read_system_params_keyboard() -> dict:
    return {
        "x0": read_float("Введите начальное приближение x0: "),
        "y0": read_float("Введите начальное приближение y0: "),
        "eps": read_float("Введите точность eps: "),
    }


def print_equation_menu(equations: dict[str, EquationProblem]) -> None:
    print("Доступные уравнения:")
    for key, problem in equations.items():
        print(f"  {key}. {problem.name}: {problem.expression} = 0")


def print_system_menu(systems: dict[str, SystemProblem]) -> None:
    print("Доступные системы:")
    for key, problem in systems.items():
        print(f"  {key}. {problem.name}: {problem.expression}")


def _header_lines(title: str, problem_text: str, meta_lines: list[str]) -> list[str]:
    return [title, problem_text, *meta_lines, "", "Таблица итераций:"]


def render_chord_report(problem: EquationProblem, root: float, rows: list[ChordRow], meta: dict) -> str:
    lines = _header_lines(
        "Метод хорд",
        f"Уравнение: {problem.expression} = 0",
        [
            f"Интервал: [{format_number(meta['a'])}, {format_number(meta['b'])}]",
            f"Фиксированный конец: {format_number(meta['fixed'])}",
            f"Начальное приближение: {format_number(meta['x0'])}",
            f"Точность: {format_number(meta['eps'])}",
        ],
    )
    for row in rows:
        lines.append(
            f"{row.k:2d}: x_k={format_number(row.xk)}, x_k+1={format_number(row.xk1)}, "
            f"f(x_k+1)={format_number(row.fxk1)}, |dx|={format_number(row.delta)}"
        )
    lines.extend(
        [
            "",
            f"Найденный корень: {format_number(root)}",
            f"Значение функции в корне: {format_number(problem.f(root))}",
            f"Количество итераций: {len(rows)}",
        ]
    )
    return "\n".join(lines)


def render_secant_report(problem: EquationProblem, root: float, rows: list[SecantRow], meta: dict) -> str:
    lines = _header_lines(
        "Метод секущих",
        f"Уравнение: {problem.expression} = 0",
        [
            f"Интервал: [{format_number(meta['a'])}, {format_number(meta['b'])}]",
            f"Начальные приближения: x0={format_number(meta['x0'])}, x1={format_number(meta['x1'])}",
            f"Точность: {format_number(meta['eps'])}",
        ],
    )
    for row in rows:
        lines.append(
            f"{row.k:2d}: x_k-1={format_number(row.xk_1)}, x_k={format_number(row.xk)}, "
            f"x_k+1={format_number(row.xk1)}, f(x_k+1)={format_number(row.fxk1)}, "
            f"|dx|={format_number(row.delta)}"
        )
    lines.extend(
        [
            "",
            f"Найденный корень: {format_number(root)}",
            f"Значение функции в корне: {format_number(problem.f(root))}",
            f"Количество итераций: {len(rows)}",
        ]
    )
    return "\n".join(lines)


def render_iteration_report(problem: EquationProblem, root: float, rows: list[IterationRow], meta: dict) -> str:
    lines = _header_lines(
        "Метод простой итерации",
        f"Уравнение: {problem.expression} = 0",
        [
            f"Интервал: [{format_number(meta['a'])}, {format_number(meta['b'])}]",
            f"Начальное приближение: {format_number(meta['x0'])}",
            f"lambda: {format_number(meta['lambda'])}",
            f"q: {format_number(meta['q'])}",
            f"Точность: {format_number(meta['eps'])}",
        ],
    )
    for row in rows:
        lines.append(
            f"{row.k:2d}: x_k={format_number(row.xk)}, x_k+1={format_number(row.xk1)}, "
            f"f(x_k+1)={format_number(row.fxk1)}, |dx|={format_number(row.delta)}"
        )
    lines.extend(
        [
            "",
            f"Найденный корень: {format_number(root)}",
            f"Значение функции в корне: {format_number(problem.f(root))}",
            f"Количество итераций: {len(rows)}",
        ]
    )
    return "\n".join(lines)


def render_newton_system_report(problem: SystemProblem, root: tuple[float, float], rows: list[NewtonSystemRow], meta: dict) -> str:
    x, y = root
    lines = _header_lines(
        "Метод Ньютона для системы",
        f"Система: {problem.expression}",
        [
            f"Начальное приближение: x0={format_number(meta['x0'])}, y0={format_number(meta['y0'])}",
            f"Точность: {format_number(meta['eps'])}",
        ],
    )
    for row in rows:
        lines.append(
            f"{row.k:2d}: (x_k, y_k)=({format_number(row.xk)}, {format_number(row.yk)}) -> "
            f"({format_number(row.xk1)}, {format_number(row.yk1)}), "
            f"|dx|={format_number(row.dx)}, |dy|={format_number(row.dy)}, "
            f"F1={format_number(row.f1_next)}, F2={format_number(row.f2_next)}"
        )
    lines.extend(
        [
            "",
            f"Найденное решение: x={format_number(x)}, y={format_number(y)}",
            f"Проверка F1(x, y)={format_number(problem.f1(x, y))}",
            f"Проверка F2(x, y)={format_number(problem.f2(x, y))}",
            f"Количество итераций: {len(rows)}",
        ]
    )
    return "\n".join(lines)


def parse_equation_params(raw_params: dict) -> dict:
    return {
        "a": parse_real(raw_params.get("a"), "a"),
        "b": parse_real(raw_params.get("b"), "b"),
        "eps": parse_real(raw_params.get("eps"), "eps"),
    }


def parse_system_params(raw_params: dict) -> dict:
    return {
        "x0": parse_real(raw_params.get("x0"), "x0"),
        "y0": parse_real(raw_params.get("y0"), "y0"),
        "eps": parse_real(raw_params.get("eps"), "eps"),
    }
