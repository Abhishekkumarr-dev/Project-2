"""
Advanced Scientific Calculator using Tkinter
Author: Abhishek Kumarr
"""

import math
import tkinter as tk
from tkinter import ttk

# ---------- CONSTANTS ---------- #
LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}


# ---------- LENGTH CONVERTER TOP-LEVEL ---------- #
class LengthConverter(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Length Converter")
        self.resizable(False, False)
        self.geometry("+620+150")
        self.configure(bg="#f0f0f0")

        # --- widgets --- #
        lbl_font = ("Segoe UI", 11)
        entry_font = ("Consolas", 12)

        tk.Label(self, text="From:", font=lbl_font, bg="#f0f0f0").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.from_var = tk.StringVar(value="cm")
        self.from_combo = ttk.Combobox(self, values=list(LENGTH_UNITS.keys()), width=8, textvariable=self.from_var, state="readonly")
        self.from_combo.grid(row=0, column=1, padx=8, pady=8)
        self.from_combo.bind("<<ComboboxSelected>>", self.calculate)

        self.from_entry = tk.Entry(self, font=entry_font, width=14, justify="center")
        self.from_entry.grid(row=0, column=2, padx=8, pady=8)
        self.from_entry.bind("<KeyRelease>", self.calculate)

        tk.Label(self, text="To:", font=lbl_font, bg="#f0f0f0").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.to_var = tk.StringVar(value="m")
        self.to_combo = ttk.Combobox(self, values=list(LENGTH_UNITS.keys()), width=8, textvariable=self.to_var, state="readonly")
        self.to_combo.grid(row=1, column=1, padx=8, pady=8)
        self.to_combo.bind("<<ComboboxSelected>>", self.calculate)

        self.to_entry = tk.Entry(self, font=entry_font, width=14, justify="center", state="normal")
        self.to_entry.grid(row=1, column=2, padx=8, pady=8)
        self.to_entry.bind("<KeyRelease>", self.calculate_reverse)

        # --- close button --- #
        tk.Button(self, text="Close", command=self.destroy, width=10).grid(row=2, column=0, columnspan=3, pady=10)

    # ---------- conversion logic ---------- #
    def calculate(self, *_):
        try:
            val = float(self.from_entry.get())
        except ValueError:
            self.to_entry.delete(0, tk.END)
            return
        from_unit = LENGTH_UNITS[self.from_var.get()]
        to_unit = LENGTH_UNITS[self.to_var.get()]
        result = val * from_unit / to_unit
        self.to_entry.delete(0, tk.END)
        self.to_entry.insert(0, str(result))

    def calculate_reverse(self, *_):
        try:
            val = float(self.to_entry.get())
        except ValueError:
            self.from_entry.delete(0, tk.END)
            return
        from_unit = LENGTH_UNITS[self.from_var.get()]
        to_unit = LENGTH_UNITS[self.to_var.get()]
        result = val * to_unit / from_unit
        self.from_entry.delete(0, tk.END)
        self.from_entry.insert(0, str(result))


# ---------- MAIN CALCULATOR ---------- #
class SciCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Scientific Calculator")
        self.resizable(False, False)
        self.geometry("+400+100")

        # ---- Display ---- #
        self.expr = tk.StringVar()
        self.history = tk.StringVar()
        self.make_display()

        # ---- Buttons ---- #
        self.make_buttons()

        # ---- Keyboard ---- #
        self.bind("<Return>", lambda e: self.on_equal())
        self.bind("<KP_Enter>", lambda e: self.on_equal())
        self.bind("<BackSpace>", lambda e: self.on_backspace())
        self.bind("<Escape>", lambda e: self.on_all_clear())

    # ---------- GUI Construction ---------- #
    def make_display(self):
        top = tk.Frame(self)
        top.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        tk.Label(top, textvariable=self.history, font=("Segoe UI", 10), fg="grey", anchor="e").pack(fill="x")
        entry = tk.Entry(top, textvariable=self.expr, font=("Consolas", 22), bd=5, relief="sunken", justify="right")
        entry.pack(fill="x")
        entry.focus()

    def make_buttons(self):
        # fmt: off
        buttons = [
            ("AC", 1, 0, 1, self.on_all_clear, "lightcoral"),
            ("C",  1, 1, 1, self.on_clear, "lightcoral"),
            ("⌫", 1, 2, 1, self.on_backspace, "orange"),
            ("/",  1, 3, 1, lambda: self.append("/"), "lightblue"),
            ("π",  1, 4, 1, lambda: self.append(str(math.pi)), "lightgreen"),
            ("e",  1, 5, 1, lambda: self.append(str(math.e)), "lightgreen"),

            ("7", 2, 0, 1, lambda: self.append("7")),
            ("8", 2, 1, 1, lambda: self.append("8")),
            ("9", 2, 2, 1, lambda: self.append("9")),
            ("*", 2, 3, 1, lambda: self.append("*"), "lightblue"),
            ("x²", 2, 4, 1, lambda: self.wrap("**2"), "lightgreen"),
            ("√",  2, 5, 1, lambda: self.wrap("sqrt(", ")"), "lightgreen"),

            ("4", 3, 0, 1, lambda: self.append("4")),
            ("5", 3, 1, 1, lambda: self.append("5")),
            ("6", 3, 2, 1, lambda: self.append("6")),
            ("-", 3, 3, 1, lambda: self.append("-"), "lightblue"),
            ("sin", 3, 4, 1, lambda: self.wrap("sin(", ")"), "lightgreen"),
            ("cos", 3, 5, 1, lambda: self.wrap("cos(", ")"), "lightgreen"),

            ("1", 4, 0, 1, lambda: self.append("1")),
            ("2", 4, 1, 1, lambda: self.append("2")),
            ("3", 4, 2, 1, lambda: self.append("3")),
            ("+", 4, 3, 1, lambda: self.append("+"), "lightblue"),
            ("tan", 4, 4, 1, lambda: self.wrap("tan(", ")"), "lightgreen"),
            ("ln",  4, 5, 1, lambda: self.wrap("log(", ")"), "lightgreen"),

            ("0", 5, 0, 1, lambda: self.append("0")),
            (".", 5, 1, 1, lambda: self.append(".")),
            ("±", 5, 2, 1, self.on_plusminus),
            ("=", 5, 3, 1, self.on_equal, "lightblue"),
            ("log", 5, 4, 1, lambda: self.wrap("log10(", ")"), "lightgreen"),
            ("Length", 5, 5, 1, self.open_length_converter, "gold"),

            ("(", 6, 0, 1, lambda: self.append("(")),
            (")", 6, 1, 1, lambda: self.append(")")),
            ("%", 6, 2, 1, lambda: self.append("%")),
            ("1/x", 6, 3, 1, lambda: self.wrap("1/"), "lightgreen"),
            ("|x|", 6, 4, 1, lambda: self.wrap("abs(", ")"), "lightgreen"),
            ("xʸ", 6, 5, 1, lambda: self.append("**"), "lightgreen"),
        ]
        # fmt: on

        for (txt, r, c, w, cmd, *color) in buttons:
            tk.Button(
                self,
                text=txt,
                width=5 if w == 1 else 10,
                height=2,
                font=("Segoe UI", 12),
                bg=color[0] if color else "gainsboro",
                fg="black",
                command=cmd,
                bd=3,
                relief="raised",
            ).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i + 1, weight=1)

    # ---------- Logic Helpers ---------- #
    def append(self, text):
        self.expr.set(self.expr.get() + str(text))

    def wrap(self, before, after=""):
        current = self.expr.get()
        self.expr.set(current + before + after)
        widget = self.focus_get()
        if isinstance(widget, tk.Entry):
            widget.icursor(len(current) + len(before))

    def on_plusminus(self):
        current = self.expr.get()
        buf = ""
        for ch in reversed(current):
            if ch in "0123456789.":
                buf = ch + buf
            else:
                break
        if not buf:
            return
        num = float(buf)
        new = str(-num)
        self.expr.set(current[: -len(buf)] + new)

    def on_clear(self):
        self.expr.set("")

    def on_all_clear(self, *_):
        self.expr.set("")
        self.history.set("")

    def on_backspace(self, *_):
        self.expr.set(self.expr.get()[:-1])

    # ---------- Error handling ---------- #
    def _show_error(self):
        self.history.set("")
        self.expr.set("Error")
        e = self.focus_get()
        if isinstance(e, tk.Entry):
            e.config(foreground="red")
        self.bind("<KeyPress>", self._reset_colour, "+")

    def _reset_colour(self, *_):
        e = self.focus_get()
        if isinstance(e, tk.Entry):
            e.config(foreground="black")
        self.unbind("<KeyPress>", self._reset_colour)

    def on_equal(self, *_):
        expr = self.expr.get().strip()
        if not expr:
            return
        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log,
            "log10": math.log10,
            "sqrt": math.sqrt,
            "exp": math.exp,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
        }
        try:
            result = eval(expr, {"__builtins__": None}, safe_dict)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.history.set(f"{expr} =")
            self.expr.set(str(result))
        except Exception:
            self._show_error()

    # ---------- Length converter ---------- #
    def open_length_converter(self):
        LengthConverter(self)


# ---------- Run ---------- #
if __name__ == "__main__":
    SciCalc().mainloop()