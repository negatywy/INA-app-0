import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

def real_to_bin(a, b, x_real, d):
    l = math.ceil(math.log2((b - a) / d + 1))
    real_to_int = (x_real - a) * (2**l - 1) / (b - a)
    int_to_bin = bin(int(round(real_to_int)))[2:].zfill(l)
    return int_to_bin

def f_x(x_real):
    return -(x_real + 1) * (x_real - 1) * (x_real - 2)

def min_f_x(a, b, d):
    min = f_x(a)
    x = a
    while x <= b:
        f = f_x(x)
        if f < min:
            min = f
        x += d
    return min

def max_f_x(a, b, d):
    max = f_x(a)
    x = a
    while x <= b:
        f = f_x(x)
        if f > max:
            max = f
        x += d
    return max

def g_x(x_real, a, b, d, max=True):
    if max:
        g = f_x(x_real) - min_f_x(a, b, d) + d
    else:
        g = -(f_x(x_real) - max_f_x(a, b, d)) + d
    return g

# Funkcja całościowa
def functions(a, b, x, d):
    try:
        xx = dictD[combobox_d.get()]
        f = f_x(x)
        g = g_x(x, a, b, d)

        return [
            round(x, xx),
            round(f, xx),
            round(g, xx)
        ]
    except ValueError:
        return [float('nan')] * 3

# wygenerowanie tabeli
def generate_table(a, b, N, d):
    results = []
    xx = dictD[combobox_d.get()] + 1

    for _ in range(N):
        x = round(random.uniform(a, b), xx)
        result = functions(a, b, x, d)
        results.append(result)

    return results

# obliczenie wartości dla losowych argumentów
def calculate():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        N = int(entry_N.get())
        d = float(combobox_d.get())
        xx = dictD[combobox_d.get()] + 1

        if a > b:
            messagebox.showerror("Błąd", "Liczba a musi być mniejsza lub równa b")
            return

        table_data = generate_table(a, b, N, d)
        show_table(table_data)

        g_sum = sum([row[2] for row in table_data]) 

        for row in table_data:
            row.append(round(row[2] / g_sum, xx))

        q_values = []
        q_sum = 0
        for row in table_data:
            p_value = row[3]
            q_sum += p_value
            q_values.append(q_sum)

        # fix for the rounding error
        q_values[-1] = 1.0

        for i, row in enumerate(table_data):
            row.append(round(q_values[i], xx))

        r_values = []
        for row in table_data:
            r_value = round(random.uniform(0, 1), xx)
            r_values.append(r_value)
            row.append(r_value)

        x_new_column = []
        x_bin_column = []
        for i in range(len(table_data)):
            if i == 0:
                q_prev = 0
            else:
                q_prev = q_values[i - 1]
            q_curr = q_values[i]
            r_value = r_values[i]

            if q_prev < r_value <= q_curr:
                selected_x = table_data[i][0]
                x_new_column.append(selected_x)
                # Perform binary conversion for the selected x
                x_bin = real_to_bin(a, b, selected_x, d)
                x_bin_column.append(x_bin)
            else:
                x_new_column.append("")
                x_bin_column.append("")

        # Append the new x and its binary representation to each row
        for i, row in enumerate(table_data):
            row.append(x_new_column[i])
            row.append(x_bin_column[i])

        # Show the updated table with new columns
        show_table(table_data)

    except ValueError:
        messagebox.showerror("Błąd", "Podano nieprawidłowe liczby")

# wypełnianie tabeli
def show_table(results):
    for row in table.get_children():
        table.delete(row)

    for index, entry in enumerate(results, start=1):
        table.insert("", "end", values=[index] + entry)

# wygnenerowanie okienka
root = tk.Tk()
root.title("Laboratorium 2: f(x)= -(x+1)(x-1)(x-2)")
root.state('zoomed')

# input a
label_a = tk.Label(root, text="Podaj a:")
label_a.grid(row=0, column=0, sticky='w', padx=5, pady=5)
entry_a = tk.Entry(root, width=10)
entry_a.grid(row=0, column=1, sticky='w', padx=5, pady=5)

# input b
label_b = tk.Label(root, text="Podaj b:")
label_b.grid(row=1, column=0, sticky='w', padx=5, pady=5)
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=1, column=1, sticky='w', padx=5, pady=5)

# input N
label_N = tk.Label(root, text="Podaj N:")
label_N.grid(row=2, column=0, sticky='w', padx=5, pady=5)
entry_N = tk.Entry(root, width=10)
entry_N.grid(row=2, column=1, sticky='w', padx=5, pady=5)

# input d
dictD = {
    "0.1": 1,
    "0.01": 2,
    "0.001": 3,
    "0.0001": 4
}
label_d = tk.Label(root, text="Wybierz d:")
label_d.grid(row=3, column=0, sticky='w', padx=5, pady=5)
combobox_d = ttk.Combobox(root, values=[0.1, 0.01, 0.001, 0.0001])
combobox_d.grid(row=3, column=1, sticky='w', padx=5, pady=5)
combobox_d.current(0)

# button
button = tk.Button(root, text="Oblicz", command=calculate)
button.grid(row=4, columnspan=2, padx=5, pady=10)

# table interface
columns = ["L.P.", "x(real)", "f(x)", "g(x)", "p", "q", "r", "new x", "x(bin)"]
table = ttk.Treeview(root, columns=columns, show="headings")
table.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

table.column("L.P.", width=40)
table.column("x(real)", width=80)
table.column("f(x)", width=80)
table.column("g(x)", width=80)
table.column("p", width=80)
table.column("q", width=80)
table.column("r", width=80)
table.column("new x", width=80)
table.column("x(bin)", width=100)

for col in columns:
    table.heading(col, text=col)

# launch the app
root.mainloop()
