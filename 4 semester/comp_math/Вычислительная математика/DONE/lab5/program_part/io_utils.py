from __future__ import annotations

import re

from models import DataPoint
from number_utils import parse_real

_SPLIT_BY_SPACES_OR_SEMICOLON = re.compile(r"[;\s]+")


def _split_data_line(line: str) -> list[str]:
    if ";" in line or "\t" in line or " " in line:
        return [part for part in _SPLIT_BY_SPACES_OR_SEMICOLON.split(line.strip()) if part]

    if line.count(",") == 1 and "." in line:
        return [part.strip() for part in line.split(",")]

    return [line.strip()]


def parse_points_text(text: str) -> list[DataPoint]:
    points: list[DataPoint] = []
    expected_count: int | None = None

    meaningful_lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not meaningful_lines:
        raise ValueError("Файл пуст или не содержит таблицы точек.")

    first_parts = _split_data_line(meaningful_lines[0])
    if len(first_parts) == 1:
        try:
            maybe_count = int(first_parts[0])
        except ValueError:
            maybe_count = None
        if maybe_count is not None and len(meaningful_lines) > 1:
            expected_count = maybe_count
            meaningful_lines = meaningful_lines[1:]

    # парсим сами точки
    for line_number, line in enumerate(meaningful_lines, start=1 if expected_count is None else 2):
        parts = _split_data_line(line)
        if len(parts) != 2:
            raise ValueError(
                f"Строка {line_number}: нужно указать ровно два значения — x и y. "
                "Пример: 1.1; 0.2234"
            )
        x = parse_real(parts[0], f"x в строке {line_number}")
        y = parse_real(parts[1], f"y в строке {line_number}")
        points.append(DataPoint(x=x, y=y))

    if expected_count is not None and expected_count != len(points):
        raise ValueError(f"В первой строке указано {expected_count} точек, а фактически введено {len(points)}.")

    return points