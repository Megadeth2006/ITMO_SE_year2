import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from solver_service import EQUATIONS, solve_odu

class OduApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Решение оду численное")
        self.geometry("1300x800")
        
        self.current_result = None
        self.visibility_vars = {}
        
        self._build_layout()
        self._init_plot()

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = ttk.LabelFrame(self, text="Параметры ОДУ", padding=15)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        ttk.Label(left_frame, text="Уравнение:").pack(anchor="w", pady=(0, 5))
        self.eq_cb = ttk.Combobox(left_frame, values=[eq.display_name for eq in EQUATIONS], state="readonly", width=25)
        self.eq_cb.current(0)
        self.eq_cb.pack(fill="x", pady=(0, 15))
        
        fields = [("x0", "0.0"), ("y0", "1.0"), ("xn", "1.0"), ("Шаг h", "0.1"), ("Точность ε", "0.001")]
        self.entries = {}
        
        for label, default in fields:
            f = ttk.Frame(left_frame)
            f.pack(fill="x", pady=5)
            ttk.Label(f, text=label, width=10).pack(side="left")
            ent = ttk.Entry(f)
            ent.insert(0, default)
            ent.pack(side="left", fill="x", expand=True)
            self.entries[label] = ent
            
        ttk.Button(left_frame, text="Рассчитать", command=self.calculate).pack(fill="x", pady=20)

        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(0, weight=3)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # график 
        top_right = ttk.Frame(right_frame)
        top_right.grid(row=0, column=0, sticky="nsew")
        top_right.grid_columnconfigure(0, weight=1)
        
        self.plot_frame = ttk.Frame(top_right, relief="solid", borderwidth=1)
        self.plot_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        checkbox_frame = ttk.LabelFrame(top_right, text="Отображение графиков", padding=10)
        checkbox_frame.grid(row=0, column=1, sticky="ns")
        
        self.visibility_vars["Точное решение"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Точное решение", variable=self.visibility_vars["Точное решение"], command=self.update_plot).pack(anchor="w", pady=2)
        
        for name in ["Метод Эйлера", "Рунге-Кутта 4", "Метод Милна"]:
            self.visibility_vars[name] = tk.BooleanVar(value=True)
            ttk.Checkbutton(checkbox_frame, text=name, variable=self.visibility_vars[name], command=self.update_plot).pack(anchor="w", pady=2)

        # таблички внизу
        bottom_right = ttk.Frame(right_frame)
        bottom_right.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        bottom_right.grid_columnconfigure(0, weight=2)
        bottom_right.grid_columnconfigure(1, weight=1)
        
        val_frame = ttk.LabelFrame(bottom_right, text="Таблица значений", padding=5)
        val_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.val_tree = ttk.Treeview(val_frame, columns=("x", "exact", "euler", "rk4", "milne"), show="headings", height=8)
        for col, text in zip(self.val_tree["columns"], ["x", "Точное", "Эйлер", "Рунге-Кутта", "Милн"]):
            self.val_tree.heading(col, text=text)
            self.val_tree.column(col, width=80, anchor="center")
        self.val_tree.pack(fill="both", expand=True)
        
        # таблица погрешностей
        err_frame = ttk.LabelFrame(bottom_right, text="Оценка погрешности", padding=5)
        err_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.err_tree = ttk.Treeview(err_frame, columns=("method", "error", "crit"), show="headings", height=8)
        self.err_tree.heading("method", text="Метод")
        self.err_tree.heading("error", text="Погрешность")
        self.err_tree.heading("crit", text="Критерий")
        self.err_tree.column("method", width=100)
        self.err_tree.column("error", width=100, anchor="center")
        self.err_tree.column("crit", width=150)
        self.err_tree.pack(fill="both", expand=True)

    def _init_plot(self):
        self.figure = Figure(dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.canvas.draw()

    def _get_float_val(self, field_name):
        """Вспомогательный метод для безопасного получения числа с поддержкой запятой"""
        raw_str = self.entries[field_name].get()
        # Заменяем запятую на точку перед конвертацией
        return float(raw_str.replace(',', '.'))

    def calculate(self):
        try:
            eq_idx = self.eq_cb.current()
            x0 = self._get_float_val("x0")
            y0 = self._get_float_val("y0")
            xn = self._get_float_val("xn")
            h = self._get_float_val("Шаг h")
            eps = self._get_float_val("Точность ε")
            
            if h <= 0 or xn <= x0:
                raise ValueError("Некорректный интервал или шаг. Шаг должен быть > 0, а xn > x0.")
            if eps <= 0:
                raise ValueError("Точность должна быть больше 0.")
            if eps < 1e-6:
                raise ValueError("Слишком высокая точность! Возможны зависания из-за метода Эйлера.\nВведите ε >= 0.000001")
                
            self.current_result = solve_odu(eq_idx, x0, y0, xn, h, eps)
            self.update_plot()
            self.update_tables()
            
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", f"Проверьте правильность введенных данных.\n{str(ve)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка:\n{str(e)}")

    def update_plot(self):
        self.ax.clear()
        self.ax.grid(True, linestyle="--", alpha=0.6)
        
        if not self.current_result:
            self.canvas.draw()
            return
            
        res = self.current_result
        has_lines = False  
        
        if self.visibility_vars["Точное решение"].get():
            self.ax.plot(res.exact_xs, res.exact_ys, color="black", linewidth=2, label="Точное решение")
            has_lines = True
            
        for m in res.methods_results:
            if self.visibility_vars[m.name].get():
                self.ax.plot(m.xs, m.ys, color=m.color, marker='o', markersize=4, linestyle='-', linewidth=1.5, label=m.name)
                has_lines = True
                
        if has_lines:
            self.ax.legend(loc="best")
            
        self.figure.tight_layout()
        self.canvas.draw()

    def update_tables(self):
        self.val_tree.delete(*self.val_tree.get_children())
        self.err_tree.delete(*self.err_tree.get_children())
        
        if not self.current_result:
            return
            
        res = self.current_result
        x0 = self._get_float_val("x0")
        y0 = self._get_float_val("y0")
        xn = self._get_float_val("xn")
        h = self._get_float_val("Шаг h")
        
       
        n_steps = int(round((xn - x0) / h))
        base_xs = [x0 + i * h for i in range(n_steps + 1)]
        
       
        for bx in base_xs:
            exact_val = res.equation.exact(bx, x0, y0)
            row = [f"{bx:.4f}", f"{exact_val:.6f}"]
            
            for m in res.methods_results:
            
                best_idx = min(range(len(m.xs)), key=lambda k: abs(m.xs[k] - bx))
                row.append(f"{m.ys[best_idx]:.6f}")
                
            self.val_tree.insert("", "end", values=row)
            

        for m in res.methods_results:
            self.err_tree.insert("", "end", values=(m.name, f"{m.error:.8f}", m.error_criterion))