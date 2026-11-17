from __future__ import annotations
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from io_utils import parse_points_text
from models import DataPoint
from number_utils import format_decimal, parse_real, format_number
from plotting_utils import draw_interpolation_on_figure, draw_placeholder
from solver_service import build_variant_3_points, solve_interpolation, generate_from_function

TABLE_ROWS = 10

class InterpolationApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ЛИнтерполяция")
        self.geometry("1400x850")
        
        self.x_entries: list[ttk.Entry] = []
        self.y_entries: list[ttk.Entry] = []
        self.loaded_file_points: list[DataPoint] = []
        
        self._build_layout()
        self._fill_variant_3()
        self.target_x_entry.insert(0, "1.121")
        
        
        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_host)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        draw_placeholder(self.figure)
        self.canvas.draw()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # левая колонка
        controls = ttk.Frame(self, width=380, padding=10)
        controls.grid(row=0, column=0, sticky="ns")
        
        self.notebook = ttk.Notebook(controls)
        self.notebook.pack(fill="x", pady=5)
        
    
        tab_table = ttk.Frame(self.notebook)
        self.notebook.add(tab_table, text="Таблица")
        
        table_frame = ttk.Frame(tab_table, padding=5)
        table_frame.pack(fill="x")
        ttk.Label(table_frame, text="x_i").grid(row=0, column=0)
        ttk.Label(table_frame, text="y_i").grid(row=0, column=1)
        for i in range(TABLE_ROWS):
            ex = ttk.Entry(table_frame, width=15)
            ey = ttk.Entry(table_frame, width=15)
            ex.grid(row=i+1, column=0, padx=2, pady=2)
            ey.grid(row=i+1, column=1, padx=2, pady=2)
            self.x_entries.append(ex)
            self.y_entries.append(ey)
        ttk.Button(tab_table, text="Загрузить Вариант 3", command=self._fill_variant_3).pack(fill="x", pady=5)

      
        tab_file = ttk.Frame(self.notebook)
        self.notebook.add(tab_file, text="Из файла")
        ttk.Button(tab_file, text="Выбрать файл .txt", command=self.load_file).pack(fill="x", pady=10)
        self.file_label = ttk.Label(tab_file, text="Файл не выбран", foreground="gray")
        self.file_label.pack(pady=5)

      
        tab_func = ttk.Frame(self.notebook)
        self.notebook.add(tab_func, text="Из функции")
        ttk.Label(tab_func, text="Функция:").pack(anchor="w")
        self.func_cb = ttk.Combobox(tab_func, values=["sin(x)", "cos(x)", "x^2 - 3x"], state="readonly")
        self.func_cb.current(0)
        self.func_cb.pack(fill="x", pady=2)
        
        f_params = ttk.Frame(tab_func)
        f_params.pack(fill="x", pady=5)
        ttk.Label(f_params, text="a:").grid(row=0, column=0)
        self.func_a = ttk.Entry(f_params, width=8); self.func_a.insert(0, "0")
        self.func_a.grid(row=0, column=1, padx=5)
        ttk.Label(f_params, text="b:").grid(row=0, column=2)
        self.func_b = ttk.Entry(f_params, width=8); self.func_b.insert(0, "3.14")
        self.func_b.grid(row=0, column=3, padx=5)
        ttk.Label(f_params, text="Точек:").grid(row=1, column=0, pady=5)
        self.func_n = ttk.Entry(f_params, width=8); self.func_n.insert(0, "5")
        self.func_n.grid(row=1, column=1, pady=5)

        # Искомая точка
        target_frame = ttk.LabelFrame(controls, text="Искомая точка", padding=5)
        target_frame.pack(fill="x", pady=15)
        ttk.Label(target_frame, text="X = ").pack(side="left")
        self.target_x_entry = ttk.Entry(target_frame)
        self.target_x_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(controls, text="ВЫЧИСЛИТЬ", command=self.solve).pack(fill="x", pady=5)

        # правая колонка
        self.paned = ttk.PanedWindow(self, orient="vertical")
        self.paned.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


        self.plot_host = ttk.Frame(self.paned, relief="solid")
        self.paned.add(self.plot_host, weight=3)


        self.res_notebook = ttk.Notebook(self.paned)
        self.paned.add(self.res_notebook, weight=2)


        results_frame = ttk.Frame(self.res_notebook, padding=5)
        self.res_notebook.add(results_frame, text="Результаты")
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_columnconfigure(1, weight=1)

        left_frame = ttk.Frame(results_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        ttk.Label(results_frame, text="Результаты вычислений:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        self.res_tree = ttk.Treeview(left_frame, columns=("method", "value"), show="headings", height=6)
        self.res_tree.heading("method", text="Метод")
        self.res_tree.heading("value", text="Значение")
        self.res_tree.column("method", width=250, anchor="w")
        self.res_tree.column("value", width=150, anchor="w")
        self.res_tree.pack(fill="both", expand=True)


        right_frame = ttk.Frame(results_frame)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        ttk.Label(results_frame, text="Ограничения методов:", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", pady=5)

        self.status_tree = ttk.Treeview(right_frame, columns=("method", "status", "reason"), show="headings", height=6)
        self.status_tree.heading("method", text="Метод")
        self.status_tree.heading("status", text="Статус")
        self.status_tree.heading("reason", text="Причина")
        self.status_tree.column("method", width=200, anchor="w")
        self.status_tree.column("status", width=100, anchor="w")
        self.status_tree.column("reason", width=250, anchor="w")
        self.status_tree.pack(fill="both", expand=True)

        self.status_tree.tag_configure('success', foreground='green')
        self.status_tree.tag_configure('error', foreground='red')


        table_res_frame = ttk.Frame(self.res_notebook)
        self.res_notebook.add(table_res_frame, text="Таблица разностей")
        table_res_frame.grid_rowconfigure(0, weight=1)
        table_res_frame.grid_columnconfigure(0, weight=1)

        self.diff_tree = ttk.Treeview(table_res_frame, show="headings", height=7)
        self.diff_tree.grid(row=0, column=0, sticky="nsew")
        tree_y_scroll = ttk.Scrollbar(table_res_frame, orient="vertical", command=self.diff_tree.yview)
        tree_y_scroll.grid(row=0, column=1, sticky="ns")
        tree_x_scroll = ttk.Scrollbar(table_res_frame, orient="horizontal", command=self.diff_tree.xview)
        tree_x_scroll.grid(row=1, column=0, sticky="ew")
        self.diff_tree.configure(yscrollcommand=tree_y_scroll.set, xscrollcommand=tree_x_scroll.set)

    def _fill_variant_3(self):
        for ex, ey in zip(self.x_entries, self.y_entries):
            ex.delete(0, "end"); ey.delete(0, "end")
        for i, p in enumerate(build_variant_3_points()):
            self.x_entries[i].insert(0, format_decimal(p.x))
            self.y_entries[i].insert(0, format_decimal(p.y))

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8")
                self.loaded_file_points = parse_points_text(content)
                self.file_label.config(text=f"Загружено {len(self.loaded_file_points)} точек", foreground="green")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def solve(self):
        try:
            tab_idx = self.notebook.index(self.notebook.select())
            points = []
            
            if tab_idx == 0:
                for ex, ey in zip(self.x_entries, self.y_entries):
                    rx, ry = ex.get().strip(), ey.get().strip()
                    if rx and ry:
                        points.append(DataPoint(parse_real(rx, "x"), parse_real(ry, "y")))
            elif tab_idx == 1:
                if not self.loaded_file_points: raise ValueError("Файл не загружен!")
                points = self.loaded_file_points
            elif tab_idx == 2:
                a = float(self.func_a.get())
                b = float(self.func_b.get())
                n = int(self.func_n.get())
                points = generate_from_function(self.func_cb.get(), a, b, n)

            target_x = parse_real(self.target_x_entry.get(), "Искомый X")
            result = solve_interpolation(points, target_x)
            

            self.res_tree.delete(*self.res_tree.get_children())
            self.status_tree.delete(*self.status_tree.get_children())

            for res in result.results:
                val_str = format_number(res.calculated_value, 6) if res.is_applicable else "N/A"
                self.res_tree.insert("", "end", values=(res.name, val_str))

                status = "Доступен" if res.is_applicable else "Недоступен"
                tag = "success" if res.is_applicable else "error"
                reason = "Любые узлы" if res.name == "Многочлен Лагранжа" else ("Условия выполнены" if res.is_applicable else res.error_message)
                self.status_tree.insert("", "end", values=(res.name, status, reason), tags=(tag,))

  
            self.diff_tree.delete(*self.diff_tree.get_children())
            diffs = result.finite_differences if result.finite_differences else result.divided_differences
            if diffs:
                n_points = len(diffs)
                cols = ["i", "y"] + [f"Δ^{k}" for k in range(1, n_points)]
                self.diff_tree["columns"] = cols
                for col in cols:
                    self.diff_tree.heading(col, text=col)
                    self.diff_tree.column(col, width=90, anchor="center")
                
                for i in range(n_points):
                    row_values = [str(i)]
                    for k in range(n_points):
                        if i < len(diffs[k]):
                            row_values.append(format_number(diffs[k][i], 5))
                        else:
                            row_values.append("")
                    self.diff_tree.insert("", "end", values=row_values)
            
  
            draw_interpolation_on_figure(self.figure, result)
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    app = InterpolationApp()
    app.mainloop()