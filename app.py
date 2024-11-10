import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import numpy as np
import matplotlib.pyplot as plt

def real_to_bin(a, b, x_real, d):
    l = math.ceil(math.log2((b - a) / d + 1))
    real_to_int = (x_real - a) * (2**l - 1) / (b - a)
    int_to_bin = bin(int(round(real_to_int)))[2:].zfill(l)
    return int_to_bin

def bin_to_real(a, b, x_bin, xx, l):
    bin_to_int = int(x_bin, 2)
    int_to_real = bin_to_int*(b-a)/(2**l - 1) + a
    return round(int_to_real, xx)

def f_x(x_real):
    return (x_real % 1) * (np.cos(20 * np.pi * x_real) - np.sin(x_real))

def g_x(x_real, a, b, d): 
    step = int((b-a)/d)
    x_values = np.linspace(a, b, step)
    f_values = f_x(x_values)

    min_value = np.min(f_values)
    g = f_x(x_real) - min_value + d
    return g

# Funkcja całościowa
def functions(a, b, x, d):
    try:
        xx = dictD[combobox_d.get()]
        f = f_x(round(x, xx))
        g = g_x(x, a, b, d)

        return [
            round(x, xx),
            round(f, xx),
            round(g, xx)
        ]
    except ValueError:
        return [float('nan')] * 3

# wygenerowanie tabeli
def generate_table(a, b, N, d, x_T):
    results = []
    xx = dictD[combobox_d.get()] + 1

    for i in range(N):
        if x_T == 'nan':
            x = round(random.uniform(a, b), xx)
        else:
            x = x_T[i]
        result = functions(a, b, x, d)
        results.append(result)

    return results

def selection(table_data, a, b, d, pk):
    r_values = generate_r(table_data)
    x_selection = []
    x_bin_selection = []
    q_values = [row[4] for row in table_data]

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

    r2_values = generate_r(table_data)
        
    for row in table_data:
        if row[8] <= pk:
            parent = row[7]
            row.append(parent)
        else:
            row.append('-')

def generate_r(table_data):
    r_values = []
    for row in table_data:
        r_value = round(random.uniform(0, 1), 2)
        r_values.append(r_value)
        row.append(r_value)
    return r_values

def crossing(table_data, l):
    parents = [row for row in table_data if row[9] != '-']
    if len(parents) % 2 != 0:
         parents = parents[:-1]

    pc_values = []
    for _ in range(0, len(parents), 2):
        pc = int(random.uniform(1, l - 1))
        pc_values.extend([pc, pc])

    pc_index = 0
    for row in table_data:
        if row[9] != '-'and pc_index < len(pc_values):
            row.append(pc_values[pc_index])
            pc_index += 1
        else:
            row.append('-')

    children = []
    for i in range(0, len(parents), 2):
        parent1 = str(parents[i][7])
        parent2 = str(parents[i+1][7])
        pc = pc_values[i]

        child1 = parent1[:pc] + parent2[pc:]
        child2 = parent2[:pc] + parent1[pc:]

        children.append(child1)
        children.append(child2)

    child_index = 0
    for row in table_data:
        if row[9] != '-' and child_index < len(children):
            row.append(children[child_index])
            child_index += 1
        else:
            row.append('-')
        
    for row in table_data:
        if row[10] != '-':
            row.append(row[11])
        else:
            row.append(row[7])

def mutate(x_bin, i):
    new_bit = "1" if x_bin[i] == "0" else "0"
    mutated = list(x_bin)
    mutated[i] = new_bit
    mutated_str = ''.join(mutated)
    return mutated_str

def mutation(table_data, l, pm, a, b, xx):
    for row in table_data:
        gene = -1
        x_bin = row[12]
        for i in range(l):
            r_value = round(random.uniform(0, 1), 5)
            if r_value <= pm:
                if gene == -1:
                    gene = i+1
                else:
                    gene = str(gene) + ', ' + str(i+1)
                x_bin = mutate(x_bin, i)
            elif gene == -1 and i == l-1:
                gene = '-'
        row.append(gene)
        row.append(x_bin)
        x_real = bin_to_real(a, b, x_bin, xx, l)
        row.append(x_real)
        fx = round(f_x(x_real), xx)
        row.append(fx)

def calculate_summary(table_data, generation):
    f_values = [row[1] for row in table_data]
    min_f = min(f_values)
    max_f = max(f_values)
    avg_f = sum(f_values) / len(f_values)
    return [generation, min_f, max_f, round(avg_f, 2)]

def plot_summary(summary):
    generations = [row[0] for row in summary]
    min_values = [row[1] for row in summary]
    max_values = [row[2] for row in summary]
    avg_values = [row[3] for row in summary]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, min_values, label='Min f(x)', marker='o')
    plt.plot(generations, max_values, label='Max f(x)', marker='o')
    plt.plot(generations, avg_values, label='Avg f(x)', marker='o')
    
    plt.xlabel('Pokolenie')
    plt.ylabel('f(x)')
    plt.title('Wykres podsumowujący wartości f(x) dla pokoleń')
    plt.legend()
    plt.grid(True)
    plt.show()

# obliczenie wartości dla losowych argumentów
def calculate():
    try:
        T = int(entry_T.get())
        if T <= 0:
            messagebox.showerror("Błąd", "Liczba pokoleń T musi być dodatnia")
            return

        a = int(entry_a.get())
        b = int(entry_b.get())
        N = int(entry_N.get())
        d = float(combobox_d.get())
        xx = dictD[combobox_d.get()]
        l = math.ceil(math.log2((b - a) / d + 1))
        pk = float(entry_pk.get())
        pm = float(entry_pm.get())

        table_data = generate_table(a, b, N, d, 'nan')
        global summary
        summary = []
        
        for j in range(T):
            g_sum = sum([row[2] for row in table_data]) 
            for row in table_data:
                row.append(round(row[2] / g_sum, 2))

            q_values = []
            q_sum = 0
            for row in table_data:
                p_value = row[3]
                q_sum += p_value
                q_values.append(q_sum)
            q_values[-1] = 1.0

            for i, row in enumerate(table_data):
                row.append(round(q_values[i], 2))

            elite = None
            if elita.get():
                table_data.sort(key=lambda row: row[1], reverse=True)
                elite = table_data[0]

            selection(table_data, a, b, d, pk)
            crossing(table_data, l)
            mutation(table_data, l, pm, a, b, xx)

            if elita.get():
                changed = int(random.uniform(0, N - 1))
                while (table_data[changed][16] > elite[1]):
                    changed = int(random.uniform(0, N - 1))
                table_data[changed] = elite

            x_T = [row[15] for row in table_data]
            if j < (T-1): 
                table_data = generate_table(a, b, N, d, x_T)

            summary.append(calculate_summary(table_data, j + 1))
            print("summary ", j+1, ": ")
            print(summary)

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
root.title("f(x)= x MOD 1 *cos(20π*x) – sin(x)")
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

# input pm
label_pm = tk.Label(root, text="Podaj pm:")
label_pm.grid(row=3, column=2, sticky='w', padx=5, pady=5)
entry_pm = tk.Entry(root, width=10)
entry_pm.grid(row=3, column=3, sticky='w', padx=5, pady=5)

# input T
label_T = tk.Label(root, text="Podaj T:")
label_T.grid(row=4, column=0, sticky='w', padx=5, pady=5)
entry_T = tk.Entry(root, width=10)
entry_T.grid(row=4, column=1, sticky='w', padx=5, pady=5)

# elita
elita = tk.BooleanVar(value=True)
label_elita = tk.Label(root, text="Elita:")
label_elita.grid(row=4, column=2, sticky='w', padx=5, pady=5)
checkbox_elita = tk.Checkbutton(root, variable=elita)
checkbox_elita.grid(row=4, column=3, sticky='w', padx=5, pady=5)

# buttons
button = tk.Button(root, text="Oblicz", command=calculate)
button.grid(row=5, columnspan=2, padx=10, pady=10)

plot_button = tk.Button(root, text="Pokaż wykres", command=lambda: plot_summary(summary))
plot_button.grid(row=5, column=2, padx=10, pady=10)

# table interface
columns = ["L.P.", "x(real)", "f(x)", "g(x)", "p", "q", "r", "x sel", "x(bin)", "r2", "parent", "pc", "child", "new gen", "gene", "x(bin)2", "x(real)2", "f(x)2"]
table = ttk.Treeview(root, columns=columns, show="headings", height=20)
table.grid(row=6, column=0, columnspan=6, padx=5, pady=10)

table.column("L.P.", width=40)
table.column("x(real)", width=60)
table.column("f(x)", width=60)
table.column("g(x)", width=60)
table.column("p", width=40)
table.column("q", width=40)
table.column("r", width=40)
table.column("x sel", width=60)
table.column("x(bin)", width=110)
table.column("r2", width=40)
table.column("parent", width=110)
table.column("pc", width=40)
table.column("child", width=110)
table.column("new gen", width=110)
table.column("gene", width=60)
table.column("x(bin)2", width=110)
table.column("x(real)2", width=60)
table.column("f(x)2", width=60)

for col in columns:
    table.heading(col, text=col)

# launch the app
root.mainloop()
