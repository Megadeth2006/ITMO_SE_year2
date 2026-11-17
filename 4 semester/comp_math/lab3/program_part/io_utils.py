from __future__ import annotations

from program_part.models import IntegrationSolveResult, VariantReportResult
from program_part.number_utils import format_number, parse_real


def parse_integration_params(raw_params: dict) -> dict[str, float]:
    return {
        "a": parse_real(raw_params.get("a"), "a"),
        "b": parse_real(raw_params.get("b"), "b"),
        "eps": parse_real(raw_params.get("eps"), "eps"),
    }


def render_integration_report(result: IntegrationSolveResult) -> str:
    lines = [
        "Результаты вычисления",
        "",
        f"Функция: f(x) = {result.problem_expression}",
        f"Метод: {result.method_name}",
        f"Границы интегрирования: [{format_number(result.source_a, 6)}; {format_number(result.source_b, 6)}]",
        f"Точность: {format_number(result.epsilon, 6)}",
    ]

    if result.active_segments:
        lines.append(
            "Вычисляемые подынтервалы: "
            + ", ".join(f"[{format_number(segment.left, 6)}; {format_number(segment.right, 6)}]" for segment in result.active_segments)
        )

    if result.excluded_segments:
        lines.append(
            "Исключенные участки: "
            + ", ".join(f"[{format_number(segment.left, 6)}; {format_number(segment.right, 6)}]" for segment in result.excluded_segments)
        )

    lines.extend(result.singularity_notes)

    if result.borders_were_swapped:
        lines.append("Примечание: границы были переставлены местами, знак результата изменен.")

    lines.extend(
        [
            "",
            f"Значение интеграла: {format_number(result.approximation)}",
            f"Число разбиений: {result.subdivisions}",
            f"Оценка погрешности по правилу Рунге: {format_number(result.runge_error)}",
        ]
    )

    if result.rows:
        lines.extend(
            [
                "",
                "Таблица итераций:",
                f"{'n':>10} {'I_n':>18} {'I_2n':>18} {'R':>18}",
            ]
        )
        for row in result.rows:
            lines.append(
                f"{row.subdivisions:>10} "
                f"{format_number(row.current_value):>18} "
                f"{format_number(row.refined_value):>18} "
                f"{format_number(row.runge_error):>18}"
            )

    return "\n".join(lines)


def render_variant_report(result: VariantReportResult) -> str:
    lines = [
        "Вычислительная часть для варианта 3",
        "",
        f"Интеграл: [0;2] ({result.problem_expression}) dx",
        f"Точное значение: {format_number(result.exact_value)}",
        "",
        f"{'Метод':<35} {'I_прибл':>15} {'Абс. погр.':>15} {'Отн. погр., %':>15}",
    ]

    for row in result.rows:
        lines.append(
            f"{row.method_name:<35} "
            f"{format_number(row.approximation):>15} "
            f"{format_number(row.absolute_error):>15} "
            f"{format_number(row.relative_error_percent):>15}"
        )

    return "\n".join(lines)
