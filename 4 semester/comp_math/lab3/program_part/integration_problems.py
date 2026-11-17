from __future__ import annotations

import math

from program_part.integration_methods import (
    left_rectangles,
    middle_rectangles,
    right_rectangles,
    simpson_method,
    trapezoid_method,
)
from program_part.models import IntegrationMethod, IntegrationProblem


def _any_interval(_left: float, _right: float) -> bool:
    return True


def _allow_with_service_handling(_left: float, _right: float) -> bool:
    return True


FUNCTIONS: dict[str, IntegrationProblem] = {
    "1": IntegrationProblem(
        code="1",
        name="Вариант 3",
        expression="-x^3 - x^2 + x + 3",
        function=lambda x: -x ** 3 - x ** 2 + x + 3.0,
        interval_validator=_any_interval,
    ),
    "2": IntegrationProblem(
        code="2",
        name="Квадратичная функция",
        expression="x^2",
        function=lambda x: x ** 2,
        interval_validator=_any_interval,
    ),
    "3": IntegrationProblem(
        code="3",
        name="Синус",
        expression="sin(x)",
        function=math.sin,
        interval_validator=_any_interval,
    ),
    "4": IntegrationProblem(
        code="4",
        name="Экспонента",
        expression="exp(x)",
        function=math.exp,
        interval_validator=_any_interval,
    ),
    "5": IntegrationProblem(
        code="5",
        name="Гипербола",
        expression="1 / x",
        function=lambda x: 1.0 / x,
        interval_validator=_allow_with_service_handling,
    ),
}


METHODS: dict[str, IntegrationMethod] = {
    "1": IntegrationMethod("1", "Метод левых прямоугольников", 1, left_rectangles),
    "2": IntegrationMethod("2", "Метод правых прямоугольников", 1, right_rectangles),
    "3": IntegrationMethod("3", "Метод средних прямоугольников", 2, middle_rectangles),
    "4": IntegrationMethod("4", "Метод трапеций", 2, trapezoid_method),
    "5": IntegrationMethod("5", "Метод Симпсона", 4, simpson_method),
}


VARIANT_3_FUNCTION_CODE = "1"
