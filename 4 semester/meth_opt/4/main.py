from AnalyticalMethod import main as analytical_method
from CoordinateDescent import main as coordinate_descent
from FastestDescent import main as fastest_descent
from GradientDescent import main as gradient_descent


def run_all_methods():
    methods = [
        ("Analytical Method", analytical_method),
        ("Coordinate Descent", coordinate_descent),
        ("Fastest Descent", fastest_descent),
        ("Gradient Descent", gradient_descent),
    ]

    for title, method in methods:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
        method()


if __name__ == "__main__":
    run_all_methods()
