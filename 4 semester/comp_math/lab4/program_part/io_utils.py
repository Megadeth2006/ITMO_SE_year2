from __future__ import annotations

import re

from program_part.models import ApproximationSolveResult, DataPoint
from program_part.number_utils import format_decimal, format_number, parse_real


_SPLIT_BY_SPACES_OR_SEMICOLON = re.compile(r"[;\s]+")


def _split_data_line(line: str) -> list[str]:
    if ";" in line or "\t" in line or " " in line:
        return [part for part in _SPLIT_BY_SPACES_OR_SEMICOLON.split(line.strip()) if part]

    # Supports simple CSV lines like 1.5,2.3 without conflicting with decimal comma.
    if line.count(",") == 1 and "." in line:
        return [part.strip() for part in line.split(",")]

    return [line.strip()]


def parse_points_text(text: str) -> list[DataPoint]:
    points: list[DataPoint] = []
    expected_count: int | None = None

    meaningful_lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not meaningful_lines:
        raise ValueError("Введите таблицу точек: каждая строка должна содержать x и y.")

    first_parts = _split_data_line(meaningful_lines[0])
    if len(first_parts) == 1:
        try:
            maybe_count = int(first_parts[0])
        except ValueError:
            maybe_count = None
        if maybe_count is not None and len(meaningful_lines) > 1:
            expected_count = maybe_count
            meaningful_lines = meaningful_lines[1:]

    for line_number, line in enumerate(meaningful_lines, start=1 if expected_count is None else 2):
        parts = _split_data_line(line)
        if len(parts) != 2:
            raise ValueError(
                f"Строка {line_number}: нужно указать ровно два значения — x и y. "
                "Пример: -1,2; -0,9460737937"
            )
        x = parse_real(parts[0], f"x в строке {line_number}")
        y = parse_real(parts[1], f"y в строке {line_number}")
        points.append(DataPoint(x=x, y=y))

    if expected_count is not None and expected_count != len(points):
        raise ValueError(f"В первой строке указано {expected_count} точек, а фактически введено {len(points)}.")

    return points


def points_to_table_text(points: list[DataPoint]) -> str:
    return "\n".join(f"{format_decimal(point.x)}; {format_decimal(point.y)}" for point in points)


def render_approximation_report(result: ApproximationSolveResult) -> str:
    lines: list[str] = []
    lines.append("Результаты аппроксимации методом наименьших квадратов")
    lines.append("")
    lines.append(f"Количество точек: {len(result.points)}")
    lines.append(f"Лучшая аппроксимирующая функция: {result.best_result.name}")
    lines.append(f"Вид функции: {result.best_result.expression}")
    lines.append(f"Минимальное среднеквадратичное отклонение: {format_number(result.best_result.standard_deviation)}")
    lines.append(f"Коэффициент корреляции Пирсона для линейной зависимости: {format_number(result.pearson_correlation)}")
    lines.append("")

    lines.append("Исходная таблица:")
    lines.append(f"{'i':>3} {'x_i':>18} {'y_i':>18}")
    for index, point in enumerate(result.points, start=1):
        lines.append(f"{index:>3} {format_decimal(point.x):>18} {format_decimal(point.y):>18}")
    lines.append("")

    lines.append("Сводная таблица по функциям:")
    lines.append(f"{'Функция':<38} {'S':>16} {'СКО':>16} {'R^2':>16}")
    for approximation in result.results:
        if approximation.is_applicable:
            lines.append(
                f"{approximation.name:<38} "
                f"{format_number(approximation.deviation_measure):>16} "
                f"{format_number(approximation.standard_deviation):>16} "
                f"{format_number(approximation.determination):>16}"
            )
        else:
            lines.append(f"{approximation.name:<38} {'не применима':>50}")
    lines.append("")

    for approximation in result.results:
        lines.append("=" * 78)
        lines.append(approximation.name)
        if not approximation.is_applicable:
            lines.append(f"Не построена: {approximation.error_message}")
            lines.append("")
            continue

        lines.append(f"Вид: {approximation.expression}")
        if approximation.coefficients:
            coefficient_text = ", ".join(
                f"{name} = {format_number(value)}" for name, value in approximation.coefficients.items()
            )
            lines.append(f"Коэффициенты: {coefficient_text}")
        lines.append(f"S = {format_number(approximation.deviation_measure)}")
        lines.append(f"Среднеквадратичное отклонение = {format_number(approximation.standard_deviation)}")
        lines.append(f"R^2 = {format_number(approximation.determination)}. {approximation.quality_message}")
        lines.append("")
        lines.append(f"{'i':>3} {'x_i':>14} {'y_i':>14} {'phi(x_i)':>18} {'epsilon_i':>18}")
        for index, (point, phi, epsilon) in enumerate(
            zip(result.points, approximation.phi_values, approximation.epsilon_values),
            start=1,
        ):
            lines.append(
                f"{index:>3} "
                f"{format_decimal(point.x):>14} "
                f"{format_decimal(point.y):>14} "
                f"{format_number(phi):>18} "
                f"{format_number(epsilon):>18}"
            )
        lines.append("")

    return "\n".join(lines)
