import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

def functions(a, b, x, d):
    l = math.ceil(math.log2((b-a)/d + 1))
    try:
        real_to_int = (x-a)*(2**l - 1)/(b-a)
        int_to_bin = bin(int(round(real_to_int)))[2:]
        bin_to_int = int(str(int_to_bin), 2)
        int_to_real = bin_to_int*(b-a)/(2**l - 1) + a
        f_x = -(int_to_real+1)*(int_to_real-1)*(int_to_real-2)

        return [
            round(real_to_int, 3),
            int_to_bin,            # Keep as string
            bin_to_int,            # Keep as int (you can convert to float if needed)
            round(int_to_real, 3),
            round(f_x, 3)
        ]
    except ValueError:
        return [float('nan')] * 5

def generate_table(a, b, N, d):
    results = []
    for _ in range(N):
        x = round(random.uniform(a, b), 3)
        result = functions(a, b, x, d)
        results.append([x] + result)
    return results

def calculate():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        N = int(entry_N.get())
        d = float(combobox_d.get())

        if a > b:
            messagebox.showerror("Błąd", "Liczba a musi być mniejsza lub równa liczbie b")
            return

        table = generate_table(a, b, N, d)
        show_table(table)

    except ValueError:
        messagebox.showerror("Błąd", "Proszę podać prawidłowe liczby")

def show_table(results):
    for row in table.get_children():
        table.delete(row)

    for index, entry in enumerate(results, start=1):
        table.insert("", "end", values=[index] + entry)

root = tk.Tk()
root.title("Laboratorium 1")
root.geometry("600x500")

label_a = tk.Label(root, text="Podaj a:")
label_a.grid(row=0, column=0, sticky='w', padx=5, pady=5)
entry_a = tk.Entry(root, width=10)
entry_a.grid(row=0, column=1, sticky='w', padx=5, pady=5)

label_b = tk.Label(root, text="Podaj b:")
label_b.grid(row=1, column=0, sticky='w', padx=5, pady=5)
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=1, column=1, sticky='w', padx=5, pady=5)

label_N = tk.Label(root, text="Podaj N:")
label_N.grid(row=2, column=0, sticky='w', padx=5, pady=5)
entry_N = tk.Entry(root, width=10)
entry_N.grid(row=2, column=1, sticky='w', padx=5, pady=5)

label_d = tk.Label(root, text="Wybierz d:")
label_d.grid(row=3, column=0, sticky='w', padx=5, pady=5)
combobox_d = ttk.Combobox(root, values=[0.1, 0.01, 0.001, 0.0001])
combobox_d.grid(row=3, column=1, sticky='w', padx=5, pady=5)
combobox_d.current(0)

button = tk.Button(root, text="Licz", command=calculate)
button.grid(row=4, columnspan=2, padx=5, pady=10)

columns = ["L.P.", "x(real)", "x(int)", "x(bin)", "x(int)2", "x(real)2", "f(x)"]
table = ttk.Treeview(root, columns=columns, show="headings")
table.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

table.column("L.P.", width=40)
table.column("x(real)", width=80)
table.column("x(int)", width=80)
table.column("x(bin)", width=80)
table.column("x(int)2", width=80)
table.column("x(real)2", width=80)
table.column("f(x)", width=80)

for col in columns:
    table.heading(col, text=col)

# launch the app
root.mainloop()
