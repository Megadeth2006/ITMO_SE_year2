from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from program_part.io_utils import parse_points_text
from program_part.models import DataPoint
from program_part.number_utils import format_decimal, parse_real
from program_part.plotting_utils import create_approximation_figure, create_placeholder_figure
from program_part.solver_service import build_variant_3_points, solve_approximations


TABLE_ROWS = 12
CONTROL_PANEL_WIDTH = 430


class ApproximationApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ЛР №4 — аппроксимация МНК")
        self.geometry("1300x820")
        self.minsize(1120, 690)

        self.canvas: FigureCanvasTkAgg | None = None
        self.last_report: str = ""
        self.x_entries: list[ttk.Entry] = []
        self.y_entries: list[ttk.Entry] = []
        self._build_layout()
        self._fill_variant_3_points()
        self._draw_placeholder()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        controls_host = ttk.Frame(self, width=CONTROL_PANEL_WIDTH, padding=(12, 12, 12, 12))
        controls_host.grid(row=0, column=0, sticky="ns")
        controls_host.grid_propagate(False)
        controls_host.grid_columnconfigure(0, weight=1)

        self._build_controls(controls_host)

        content = ttk.Frame(self, padding=(0, 12, 12, 12))
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(0, weight=3)
        content.grid_rowconfigure(1, weight=2)
        content.grid_columnconfigure(0, weight=1)

        self._build_plot_area(content)
        self._build_result_area(content)

    def _build_controls(self, parent: ttk.Frame) -> None:
        input_frame = ttk.LabelFrame(parent, text="Исходная таблица", padding=10)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        input_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(
            input_frame,
            text=(
                "Заполните от 8 до 12 строк. В каждой строке отдельно вводятся x_i и y_i. "
                "Пустые строки игнорируются. Поддерживаются десятичная точка и запятая."
            ),
            wraplength=385,
            justify="left",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 7))

        table_frame = ttk.Frame(input_frame)
        table_frame.grid(row=1, column=0, sticky="ew")
        table_frame.grid_columnconfigure(1, weight=1)
        table_frame.grid_columnconfigure(2, weight=1)

        ttk.Label(table_frame, text="№", anchor="center").grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Label(table_frame, text="x_i", anchor="center").grid(row=0, column=1, sticky="ew", padx=(0, 6))
        ttk.Label(table_frame, text="y_i", anchor="center").grid(row=0, column=2, sticky="ew")

        for row_index in range(TABLE_ROWS):
            ttk.Label(table_frame, text=str(row_index + 1), anchor="center").grid(
                row=row_index + 1,
                column=0,
                sticky="ew",
                padx=(0, 6),
                pady=1,
            )
            x_entry = ttk.Entry(table_frame, width=17)
            y_entry = ttk.Entry(table_frame, width=17)
            x_entry.grid(row=row_index + 1, column=1, sticky="ew", padx=(0, 6), pady=1)
            y_entry.grid(row=row_index + 1, column=2, sticky="ew", pady=1)
            self.x_entries.append(x_entry)
            self.y_entries.append(y_entry)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="ВАРИАНТ 3", command=self._fill_variant_3_points).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=(0, 5)
        )
        ttk.Button(button_frame, text="ЗАГРУЗИТЬ ИЗ ФАЙЛА", command=self.load_points_from_file).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=(0, 5)
        )
        ttk.Button(button_frame, text="ОЧИСТИТЬ ТАБЛИЦУ", command=self.clear_points_table).grid(
            row=1, column=0, columnspan=2, sticky="ew"
        )

        action_frame = ttk.LabelFrame(parent, text="Действия", padding=10)
        action_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        action_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(action_frame, text="ПОСТРОИТЬ АППРОКСИМАЦИИ", command=self.solve_action).grid(row=0, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(action_frame, text="СОХРАНИТЬ РЕЗУЛЬТАТ В TXT", command=self.save_report_action).grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(action_frame, text="СОХРАНИТЬ ГРАФИК В PNG", command=self.save_plot_action).grid(row=2, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(action_frame, text="ОЧИСТИТЬ РЕЗУЛЬТАТ", command=self.clear_output).grid(row=3, column=0, sticky="ew")

        info_frame = ttk.LabelFrame(parent, text="Что считает программа", padding=10)
        info_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        info_frame.grid_columnconfigure(0, weight=1)

        

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

        self.result_text = tk.Text(result_frame, wrap="none", font=("Consolas", 10))
        self.result_text.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll = ttk.Scrollbar(result_frame, orient="horizontal", command=self.result_text.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.result_text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    def _get_points_from_entries(self) -> list[DataPoint]:
        points: list[DataPoint] = []
        for index, (x_entry, y_entry) in enumerate(zip(self.x_entries, self.y_entries), start=1):
            raw_x = x_entry.get().strip()
            raw_y = y_entry.get().strip()

            if not raw_x and not raw_y:
                continue
            if not raw_x or not raw_y:
                raise ValueError(
                    f"Строка {index}: нужно заполнить оба поля — x_i и y_i, "
                    "либо оставить строку полностью пустой."
                )

            x = parse_real(raw_x, f"x_i в строке {index}")
            y = parse_real(raw_y, f"y_i в строке {index}")
            points.append(DataPoint(x=x, y=y))

        if not points:
            raise ValueError("Введите исходную таблицу: от 8 до 12 точек.")
        return points

    def _set_points_to_entries(self, points: list[DataPoint]) -> None:
        if len(points) > TABLE_ROWS:
            raise ValueError(f"В таблицу можно загрузить не больше {TABLE_ROWS} точек.")

        self.clear_points_table()
        for index, point in enumerate(points):
            self.x_entries[index].insert(0, format_decimal(point.x))
            self.y_entries[index].insert(0, format_decimal(point.y))

    def _fill_variant_3_points(self) -> None:
        self._set_points_to_entries(build_variant_3_points())

    def clear_points_table(self) -> None:
        for x_entry, y_entry in zip(self.x_entries, self.y_entries):
            x_entry.delete(0, "end")
            y_entry.delete(0, "end")

    def _draw_placeholder(self) -> None:
        self._set_figure(create_placeholder_figure())

    def _set_figure(self, figure) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.current_figure = figure
        self.canvas = FigureCanvasTkAgg(figure, master=self.plot_host)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _set_report(self, report: str) -> None:
        self.last_report = report
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", report)

    def clear_output(self) -> None:
        self.result_text.delete("1.0", "end")
        self.last_report = ""
        self._draw_placeholder()

    def load_points_from_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите файл с точками",
            filetypes=(
                ("Текстовые файлы", "*.txt *.csv"),
                ("Все файлы", "*.*"),
            ),
        )
        if not path:
            return

        try:
            file_path = Path(path)
            try:
                content = file_path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                content = file_path.read_text(encoding="cp1251")

            points = parse_points_text(content)
            self._set_points_to_entries(points)
        except Exception as error:
            messagebox.showerror("Ошибка загрузки", str(error))

    def solve_action(self) -> None:
        try:
            points = self._get_points_from_entries()
            result = solve_approximations(points)
            self._set_figure(create_approximation_figure(result))
            self._set_report(result.report)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def save_report_action(self) -> None:
        if not self.last_report:
            messagebox.showwarning("Нет результата", "Сначала выполните расчет.")
            return

        path = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".txt",
            filetypes=(("Текстовый файл", "*.txt"), ("Все файлы", "*.*")),
        )
        if not path:
            return

        try:
            Path(path).write_text(self.last_report, encoding="utf-8")
        except Exception as error:
            messagebox.showerror("Ошибка сохранения", str(error))

    def save_plot_action(self) -> None:
        if not hasattr(self, "current_figure"):
            messagebox.showwarning("Нет графика", "Сначала выполните расчет.")
            return

        path = filedialog.asksaveasfilename(
            title="Сохранить график",
            defaultextension=".png",
            filetypes=(("PNG", "*.png"), ("Все файлы", "*.*")),
        )
        if not path:
            return

        try:
            self.current_figure.savefig(path, dpi=160)
        except Exception as error:
            messagebox.showerror("Ошибка сохранения", str(error))


def main() -> None:
    app = ApproximationApp()
    app.mainloop()
