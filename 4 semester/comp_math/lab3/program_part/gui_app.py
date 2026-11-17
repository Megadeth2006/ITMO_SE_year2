from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from program_part.integration_problems import FUNCTIONS, METHODS, VARIANT_3_FUNCTION_CODE
from program_part.plotting_utils import create_integration_figure, create_placeholder_figure
from program_part.solver_service import build_variant_3_report, solve_integral


class IntegrationApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Численное интегрирование")
        self.geometry("1250x780")
        self.minsize(1000, 650)

        self.function_choice = tk.StringVar(value=VARIANT_3_FUNCTION_CODE)
        self.method_choice = tk.StringVar(value="5")

        self.canvas: FigureCanvasTkAgg | None = None
        self._build_layout()
        self._draw_placeholder()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        controls_host = ttk.Frame(self, padding=(12, 12, 6, 12))
        controls_host.grid(row=0, column=0, sticky="ns")
        controls_host.grid_rowconfigure(0, weight=1)
        controls_host.grid_columnconfigure(0, weight=1)

        self._build_scrollable_controls(controls_host)

        content = ttk.Frame(self, padding=(0, 12, 12, 12))
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(0, weight=3)
        content.grid_rowconfigure(1, weight=2)
        content.grid_columnconfigure(0, weight=1)

        self._build_plot_area(content)
        self._build_result_area(content)

    def _build_scrollable_controls(self, parent: ttk.Frame) -> None:
        canvas = tk.Canvas(parent, width=360, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="ns")
        scrollbar.grid(row=0, column=1, sticky="ns")

        controls = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=controls, anchor="nw")

        def update_scroll_region(_: object = None) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_inner(event: tk.Event) -> None:
            canvas.itemconfigure(window_id, width=event.width)

        controls.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_inner)

        def on_mousewheel(event: tk.Event) -> None:
            delta = -1 if event.delta > 0 else 1
            canvas.yview_scroll(delta, "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self._build_controls(controls)

    def _build_controls(self, parent: ttk.Frame) -> None:
        function_frame = ttk.LabelFrame(parent, text="Выбор функции", padding=10)
        function_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        for code, problem in FUNCTIONS.items():
            ttk.Radiobutton(
                function_frame,
                text=f"{code}. f(x) = {problem.expression}",
                variable=self.function_choice,
                value=code,
            ).pack(anchor="w", pady=2)

        method_frame = ttk.LabelFrame(parent, text="Метод и параметры", padding=10)
        method_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        for code, method in METHODS.items():
            ttk.Radiobutton(
                method_frame,
                text=method.name,
                variable=self.method_choice,
                value=code,
            ).pack(anchor="w", pady=2)

        self.entry_a = self._labeled_entry(method_frame, "Левая граница a:", "0")
        self.entry_b = self._labeled_entry(method_frame, "Правая граница b:", "2")
        self.entry_eps = self._labeled_entry(method_frame, "Точность eps:", "0.001")

        ttk.Button(method_frame, text="ВЫЧИСЛИТЬ ИНТЕГРАЛ", command=self.solve_integral_action).pack(fill="x", pady=(10, 4))
        ttk.Button(method_frame, text="ОЧИСТИТЬ", command=self.clear_output).pack(fill="x")

        # variant_frame = ttk.LabelFrame(parent, text="Вычислительная часть", padding=10)
        # variant_frame.grid(row=2, column=0, sticky="ew", pady=(18, 10))

        # ttk.Label(
        #     variant_frame,
        #     text="Вариант 3: [0; 2], f(x) = -x^3 - x^2 + x + 3",
        #     wraplength=300,
        #     justify="left",
        # ).pack(anchor="w", pady=(0, 8))
        # ttk.Button(
        #     variant_frame,
        #     text="ПОКАЗАТЬ ОТЧЕТ ВАРИАНТА 3",
        #     command=self.show_variant_report_action,
        # ).pack(fill="x")

    def _labeled_entry(self, parent: ttk.Frame, label: str, default: str) -> ttk.Entry:
        ttk.Label(parent, text=label).pack(anchor="w", pady=(6, 0))
        entry = ttk.Entry(parent)
        entry.pack(fill="x")
        entry.insert(0, default)
        return entry

    def _build_plot_area(self, parent: ttk.Frame) -> None:
        plot_frame = ttk.Frame(parent, relief="solid", padding=6)
        plot_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_host = plot_frame

    def _build_result_area(self, parent: ttk.Frame) -> None:
        result_frame = ttk.Frame(parent, relief="solid", padding=6)
        result_frame.grid(row=1, column=0, sticky="nsew")
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        self.result_text = tk.Text(result_frame, wrap="word", font=("Consolas", 10))
        self.result_text.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=scroll.set)

    def _draw_placeholder(self) -> None:
        self._set_figure(create_placeholder_figure())

    def _set_figure(self, figure) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(figure, master=self.plot_host)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _set_report(self, report: str) -> None:
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", report)

    def clear_output(self) -> None:
        self.result_text.delete("1.0", "end")
        self._draw_placeholder()

    def solve_integral_action(self) -> None:
        try:
            problem = FUNCTIONS[self.function_choice.get()]
            result = solve_integral(
                self.method_choice.get(),
                problem,
                {
                    "a": self.entry_a.get(),
                    "b": self.entry_b.get(),
                    "eps": self.entry_eps.get(),
                },
            )
            figure = create_integration_figure(
                problem,
                result.normalized_a,
                result.normalized_b,
                segments=result.active_segments,
                excluded_segments=result.excluded_segments,
                approximation=result.approximation,
            )
            self._set_figure(figure)
            self._set_report(result.report)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def show_variant_report_action(self) -> None:
        try:
            problem = FUNCTIONS[VARIANT_3_FUNCTION_CODE]
            result = build_variant_3_report()
            figure = create_integration_figure(problem, result.a, result.b, approximation=result.exact_value)
            self._set_figure(figure)
            self._set_report(result.report)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))


def main() -> None:
    app = IntegrationApp()
    app.mainloop()
