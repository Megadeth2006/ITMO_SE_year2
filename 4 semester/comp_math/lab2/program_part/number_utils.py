from __future__ import annotations

import math


def parse_real(value: object, field_name: str) -> float:
    if isinstance(value, (int, float)):
        result = float(value)
    elif isinstance(value, str):
        normalized = value.strip().replace(" ", "").replace(",", ".")
        if not normalized:
            raise ValueError(f"Поле «{field_name}» не заполнено.")
        try:
            result = float(normalized)
        except ValueError as error:
            raise ValueError(f"Поле «{field_name}» должно содержать число.") from error
    else:
        raise ValueError(f"Поле «{field_name}» имеет неподдерживаемый тип данных.")

    if not math.isfinite(result):
        raise ValueError(f"Поле «{field_name}» должно содержать конечное число.")
    return result


def format_number(value: float) -> str:
    return str(value)
