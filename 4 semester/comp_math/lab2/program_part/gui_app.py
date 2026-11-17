from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from program_part.equation_problems import EQUATIONS
from program_part.plotting_utils import create_equation_figure, create_system_figure
from program_part.solver_service import solve_equation, solve_system
from program_part.system_problems import SYSTEMS


class SolverApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Nonlinear Equations & Systems Solver")
        self.geometry("1250x780")
        self.minsize(1000, 650)

        self.equation_choice = tk.StringVar(value="1")
        self.method_choice = tk.StringVar(value="2")
        self.system_choice = tk.StringVar(value="1")

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
        content.grid_rowconfigure(1, weight=1)
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
        equation_frame = ttk.LabelFrame(parent, text="Выбор уравнения", padding=10)
        equation_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        for key, problem in EQUATIONS.items():
            ttk.Radiobutton(
                equation_frame,
                text=problem.expression + " = 0",
                variable=self.equation_choice,
                value=key,
            ).pack(anchor="w", pady=2)

        method_frame = ttk.LabelFrame(parent, text="Метод и параметры уравнения", padding=10)
        method_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Radiobutton(method_frame, text="Метод хорд", variable=self.method_choice, value="2").pack(anchor="w", pady=2)
        ttk.Radiobutton(method_frame, text="Метод секущих", variable=self.method_choice, value="4").pack(anchor="w", pady=2)
        ttk.Radiobutton(method_frame, text="Метод простой итерации", variable=self.method_choice, value="5").pack(anchor="w", pady=2)

        self.entry_a = self._labeled_entry(method_frame, "Левая граница a:", "0") # type: ignore
        self.entry_b = self._labeled_entry(method_frame, "Правая граница b:", "1") # type: ignore
        self.entry_eps = self._labeled_entry(method_frame, "Точность eps:", "0.01") # type: ignore

        ttk.Button(method_frame, text="РЕШИТЬ УРАВНЕНИЕ", command=self.solve_equation_action).pack(fill="x", pady=(10, 4))
        ttk.Button(method_frame, text="ОЧИСТИТЬ", command=self.clear_output).pack(fill="x")

        system_frame = ttk.LabelFrame(parent, text="Выбор системы", padding=10)
        system_frame.grid(row=2, column=0, sticky="ew", pady=(18, 10))

        for key, problem in SYSTEMS.items():
            ttk.Radiobutton(
                system_frame,
                text=problem.expression,
                variable=self.system_choice,
                value=key,
            ).pack(anchor="w", pady=2)

        system_params_frame = ttk.LabelFrame(parent, text="Параметры системы", padding=10)
        system_params_frame.grid(row=3, column=0, sticky="ew")

        self.entry_x0 = self._labeled_entry(system_params_frame, "Начальное x0:", "0,5") # type: ignore
        self.entry_y0 = self._labeled_entry(system_params_frame, "Начальное y0:", "0,5") # type: ignore
        self.entry_system_eps = self._labeled_entry(system_params_frame, "Точность eps:", "0,001") # type: ignore

        ttk.Button(system_params_frame, text="РЕШИТЬ СИСТЕМУ", command=self.solve_system_action).pack(fill="x", pady=(10, 4))
        ttk.Button(system_params_frame, text="ОЧИСТИТЬ", command=self.clear_output).pack(fill="x")

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
        self.canvas: FigureCanvasTkAgg | None = None

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
        figure = Figure(figsize=(7.0, 4.8), dpi=100)
        axis = figure.add_subplot(111)
        axis.set_xlim(0, 1)
        axis.set_ylim(0, 1)
        axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
        self._set_figure(figure)

    def _set_figure(self, figure: Figure) -> None:
        if self.canvas is not None:
            widget = self.canvas.get_tk_widget()
            widget.destroy()
        self.canvas = FigureCanvasTkAgg(figure, master=self.plot_host)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _set_report(self, report: str) -> None:
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", report)

    def clear_output(self) -> None:
        self.result_text.delete("1.0", "end")
        self._draw_placeholder()

    def solve_equation_action(self) -> None:
        try:
            problem = EQUATIONS[self.equation_choice.get()]
            result = solve_equation(
                self.method_choice.get(),
                problem,
                {
                    "a": self.entry_a.get(),
                    "b": self.entry_b.get(),
                    "eps": self.entry_eps.get(),
                },
            )
            figure = create_equation_figure(problem, result.a, result.b, root=result.root)
            self._set_figure(figure)
            self._set_report(result.report)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def solve_system_action(self) -> None:
        try:
            problem = SYSTEMS[self.system_choice.get()]
            result = solve_system(
                problem,
                {
                    "x0": self.entry_x0.get(),
                    "y0": self.entry_y0.get(),
                    "eps": self.entry_system_eps.get(),
                },
            )
            figure = create_system_figure(problem, result.x0, result.y0, root=result.root)
            self._set_figure(figure)
            self._set_report(result.report)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))


def main() -> None:
    app = SolverApp()
    app.mainloop()
