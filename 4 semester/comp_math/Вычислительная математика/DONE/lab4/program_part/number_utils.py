from __future__ import annotations

from decimal import Decimal, InvalidOperation


def parse_real(value: object, field_name: str) -> Decimal:
    """Parse a real number without limiting the number of entered digits.

    The GUI accepts both a dot and a comma as the decimal separator.
    The value is stored as Decimal first, then numerical algorithms convert it
    to float only at the calculation stage.
    """
    if isinstance(value, Decimal):
        result = value
    elif isinstance(value, (int, float)):
        result = Decimal(str(value))
    elif isinstance(value, str):
        normalized = value.strip().replace(" ", "").replace(",", ".")
        if not normalized:
            raise ValueError(f"Поле «{field_name}» не заполнено.")
        try:
            result = Decimal(normalized)
        except InvalidOperation as error:
            raise ValueError(f"Поле «{field_name}» должно содержать число.") from error
    else:
        raise ValueError(f"Поле «{field_name}» имеет неподдерживаемый тип данных.")

    if not result.is_finite():
        raise ValueError(f"Поле «{field_name}» должно содержать конечное число.")
    return result


def decimal_to_float(value: Decimal, field_name: str) -> float:
    result = float(value)
    if result == float("inf") or result == float("-inf"):
        raise ValueError(f"Число в поле «{field_name}» слишком велико для вычислений.")
    return result


def format_decimal(value: Decimal) -> str:
    normalized = value.normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text if text else "0"


def format_number(value: float | int | None, significant_digits: int = 12) -> str:
    if value is None:
        return "—"
    return f"{float(value):.{significant_digits}g}"
