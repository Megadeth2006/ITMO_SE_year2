from __future__ import annotations

from dataclasses import dataclass

from program_part.integration_methods import (
    middle_rectangles,
    newton_cotes_for_six_parts,
    simpson_method,
    trapezoid_method,
)
from program_part.integration_problems import FUNCTIONS, METHODS, VARIANT_3_FUNCTION_CODE
from program_part.io_utils import parse_integration_params, render_integration_report, render_variant_report
from program_part.models import (
    IntegrationMethod,
    IntegrationProblem,
    IntegrationSegment,
    IntegrationSolveResult,
    IterationRow,
    VariantReportResult,
    VariantReportRow,
)


INITIAL_SUBDIVISIONS = 4
MAX_SUBDIVISIONS = 1_000_000


@dataclass
class _IntervalInfo:
    left: float
    right: float
    sign: int


def _normalize_interval(left: float, right: float) -> _IntervalInfo:
    if left <= right:
        return _IntervalInfo(left, right, 1)
    return _IntervalInfo(right, left, -1)


def _adjust_subdivisions(method: IntegrationMethod, subdivisions: int) -> int:
    if method.code == "5" and subdivisions % 2 != 0:
        return subdivisions + 1
    return subdivisions


def _calculate_runge_error(current_value: float, refined_value: float, order: int) -> float:
    return abs(refined_value - current_value) / (2 ** order - 1)


def _validate_interval(problem: IntegrationProblem, left: float, right: float) -> None:
    if not problem.interval_validator(left, right):
        raise ValueError("Выбранная функция не определена на заданном отрезке.")


def _build_segments(problem: IntegrationProblem, left: float, right: float) -> tuple[list[IntegrationSegment], list[IntegrationSegment], list[str]]:
    if problem.code != "5":
        return [IntegrationSegment(left, right)], [], []

    if left == 0.0 or right == 0.0:
        raise ValueError("Для функции 1 / x интеграл на отрезке с границей в точке разрыва не существует.")

    if left < 0.0 < right:
        radius = min(-left, right)
        excluded_segment = IntegrationSegment(-radius, radius)
        active_segments: list[IntegrationSegment] = []

        if left < -radius:
            active_segments.append(IntegrationSegment(left, -radius))
        if right > radius:
            active_segments.append(IntegrationSegment(radius, right))

        notes = [
            "Обнаружен разрыв второго рода в точке x = 0.",
            "Симметричный участок вокруг точки разрыва исключен по условию главного значения.",
        ]

        if not active_segments:
            notes.append("После исключения симметричного участка вклад интеграла равен 0.")

        return active_segments, [excluded_segment], notes

    return [IntegrationSegment(left, right)], [], []


def _integrate_on_segments(
    problem: IntegrationProblem,
    method: IntegrationMethod,
    segments: list[IntegrationSegment],
    subdivisions: int,
) -> float:
    total = 0.0
    for segment in segments:
        total += method.integrator(problem.function, segment.left, segment.right, subdivisions)
    return total


def _integrate_with_runge(
    problem: IntegrationProblem,
    method: IntegrationMethod,
    segments: list[IntegrationSegment],
    epsilon: float,
) -> tuple[float, int, float, list[IterationRow]]:
    rows: list[IterationRow] = []
    subdivisions = _adjust_subdivisions(method, INITIAL_SUBDIVISIONS)

    while subdivisions <= MAX_SUBDIVISIONS:
        current_value = _integrate_on_segments(problem, method, segments, subdivisions)
        doubled_subdivisions = _adjust_subdivisions(method, subdivisions * 2)

        if doubled_subdivisions > MAX_SUBDIVISIONS:
            break

        refined_value = _integrate_on_segments(problem, method, segments, doubled_subdivisions)
        runge_error = _calculate_runge_error(current_value, refined_value, method.order)
        rows.append(IterationRow(subdivisions, current_value, refined_value, runge_error))

        if runge_error <= epsilon:
            return refined_value, doubled_subdivisions, runge_error, rows

        subdivisions = doubled_subdivisions

    raise ValueError(
        f"Не удалось достичь заданной точности. Превышено ограничение по числу разбиений ({MAX_SUBDIVISIONS})."
    )


def solve_integral(method_code: str, problem: IntegrationProblem, raw_params: dict) -> IntegrationSolveResult:
    params = parse_integration_params(raw_params)
    source_a = params["a"]
    source_b = params["b"]
    epsilon = params["eps"]

    if epsilon <= 0:
        raise ValueError("Точность eps должна быть положительной.")

    if source_a == source_b:
        result = IntegrationSolveResult(
            method_code=method_code,
            method_name=METHODS[method_code].name,
            problem_name=problem.name,
            problem_expression=problem.expression,
            approximation=0.0,
            runge_error=0.0,
            subdivisions=0,
            report="",
            rows=[],
            source_a=source_a,
            source_b=source_b,
            normalized_a=source_a,
            normalized_b=source_b,
            epsilon=epsilon,
            borders_were_swapped=False,
            active_segments=[],
            excluded_segments=[],
            singularity_notes=[],
        )
        result.report = render_integration_report(result)
        return result

    interval = _normalize_interval(source_a, source_b)
    _validate_interval(problem, interval.left, interval.right)

    method = METHODS.get(method_code)
    if method is None:
        raise ValueError("Неизвестный метод численного интегрирования.")

    active_segments, excluded_segments, singularity_notes = _build_segments(problem, interval.left, interval.right)

    if active_segments:
        approximation, subdivisions, runge_error, rows = _integrate_with_runge(
            problem,
            method,
            active_segments,
            epsilon,
        )
    else:
        approximation = 0.0
        subdivisions = 0
        runge_error = 0.0
        rows = []

    if interval.sign < 0:
        approximation = -approximation

    result = IntegrationSolveResult(
        method_code=method.code,
        method_name=method.name,
        problem_name=problem.name,
        problem_expression=problem.expression,
        approximation=approximation,
        runge_error=runge_error,
        subdivisions=subdivisions,
        report="",
        rows=rows,
        source_a=source_a,
        source_b=source_b,
        normalized_a=interval.left,
        normalized_b=interval.right,
        epsilon=epsilon,
        borders_were_swapped=interval.sign < 0,
        active_segments=active_segments,
        excluded_segments=excluded_segments,
        singularity_notes=singularity_notes,
    )
    result.report = render_integration_report(result)
    return result


def _build_variant_row(method_name: str, approximation: float, exact_value: float) -> VariantReportRow:
    absolute_error = abs(exact_value - approximation)
    relative_error_percent = absolute_error / abs(exact_value) * 100.0
    return VariantReportRow(method_name, approximation, absolute_error, relative_error_percent)


def build_variant_3_report() -> VariantReportResult:
    problem = FUNCTIONS[VARIANT_3_FUNCTION_CODE]
    a = 0.0
    b = 2.0
    exact_value = 4.0 / 3.0

    rows = [
        _build_variant_row("Формула Ньютона-Котеса (n = 6)", newton_cotes_for_six_parts(problem.function, a, b), exact_value),
        _build_variant_row("Средние прямоугольники (n = 10)", middle_rectangles(problem.function, a, b, 10), exact_value),
        _build_variant_row("Трапеции (n = 10)", trapezoid_method(problem.function, a, b, 10), exact_value),
        _build_variant_row("Симпсон (n = 10)", simpson_method(problem.function, a, b, 10), exact_value),
    ]

    result = VariantReportResult(
        problem_name=problem.name,
        problem_expression=problem.expression,
        a=a,
        b=b,
        exact_value=exact_value,
        rows=rows,
        report="",
    )
    result.report = render_variant_report(result)
    return result
