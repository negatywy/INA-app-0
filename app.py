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
            row.append(round(row[2] / g_sum, 2))

        q_values = []
        q_sum = 0
        for row in table_data:
            p_value = row[3]
            q_sum += p_value
            q_values.append(q_sum)

        # fix for the rounding error
        q_values[-1] = 1.0

        for i, row in enumerate(table_data):
            row.append(round(q_values[i], 2))

        r_values = []
        for row in table_data:
            r_value = round(random.uniform(0, 1), 2)
            r_values.append(r_value)
            row.append(r_value)

        x_selection = []
        x_bin_selection = []

        for i in range(len(table_data)):
            j = 0
            while j < len(q_values) and r_values[i] > q_values[j]:
                j += 1
            selected_x = table_data[j][0]
            x_selection.append(selected_x)
            selected_x_bin = real_to_bin(a, b, selected_x, d)
            x_bin_selection.append(selected_x_bin)


        for i, row in enumerate(table_data):
            row.append(x_selection[i])
            row.append(x_bin_selection[i])

        r2_values = []
        for row in table_data:
            r2_value = round(random.uniform(0, 1), 2)
            r2_values.append(r2_value)
            row.append(r2_value)

        pk = float(entry_pk.get())
        if 0 > pk or pk > 1:
            messagebox.showerror("Błąd", "pk musi zawierać się w przedziale [0; 1]")
            return
        
        for row in table_data:
            if row[8] <= pk:
                parent = row[7]
                row.append(parent)
            else:
                row.append('nan')
        
        l = math.ceil(math.log2((b - a) / d + 1))

        parents_data = [row for row in table_data if row[9] != 'nan']
        if len(parents_data) % 2 != 0:
            parents_data = parents_data[:-1]

        pc_values = []
        for _ in range(0, len(parents_data), 2):
            pc = int(random.uniform(1, l - 1))
            pc_values.extend([pc, pc])

        pc_index = 0
        for row in table_data:
            if row[9] != 'nan'and pc_index < len(pc_values):
                row.append(pc_values[pc_index])
                pc_index += 1
            else:
                row.append('nan')

        children_binaries = []
        for i in range(0, len(parents_data), 2):
            parent1_bin = str(parents_data[i][7])
            parent2_bin = str(parents_data[i+1][7])
            pc = pc_values[i]

            child1_bin = parent1_bin[:pc] + parent2_bin[pc:]
            child2_bin = parent2_bin[:pc] + parent1_bin[pc:]

            children_binaries.append(child1_bin)
            children_binaries.append(child2_bin)

        child_index = 0
        for row in table_data:
            if row[9] != 'nan' and child_index < len(children_binaries):
                row.append(children_binaries[child_index])
                child_index += 1
            else:
                row.append('nan')
        
        for row in table_data:
            if row[10] != 'nan':
                row.append(row[11])
            else:
                row.append(row[7])

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
label_b.grid(row=0, column=2, sticky='w', padx=5, pady=5)
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=0, column=3, sticky='w', padx=5, pady=5)

# input N
label_N = tk.Label(root, text="Podaj N:")
label_N.grid(row=1, column=0, sticky='w', padx=5, pady=5)
entry_N = tk.Entry(root, width=10)
entry_N.grid(row=1, column=1, sticky='w', padx=5, pady=5)

# input pk
label_pk = tk.Label(root, text="Podaj pk:")
label_pk.grid(row=1, column=2, sticky='w', padx=5, pady=5)
entry_pk = tk.Entry(root, width=10)
entry_pk.grid(row=1, column=3, sticky='w', padx=5, pady=5)

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
columns = ["L.P.", "x(real)", "f(x)", "g(x)", "p", "q", "r", "x sel", "x(bin)", "r2", "parent", "pc", "child", "new gen"]
table = ttk.Treeview(root, columns=columns, show="headings")
table.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

table.column("L.P.", width=40)
table.column("x(real)", width=60)
table.column("f(x)", width=60)
table.column("g(x)", width=60)
table.column("p", width=40)
table.column("q", width=40)
table.column("r", width=40)
table.column("x sel", width=60)
table.column("x(bin)", width=100)
table.column("r2", width=40)
table.column("parent", width=80)
table.column("pc", width=40)
table.column("child", width=80)
table.column("new gen", width=80)

for col in columns:
    table.heading(col, text=col)

# launch the app
root.mainloop()
