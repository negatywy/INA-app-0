import numpy as np
import math
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

def real_to_bin(a, b, x_real, d):
    l = math.ceil(math.log2((b - a) / d + 1))
    real_to_int = (x_real - a) * (2**l - 1) / (b - a)
    int_to_bin = bin(int(round(real_to_int)))[2:].zfill(l)
    return int_to_bin

def bin_to_real(a, b, x_bin, d):
    l = len(x_bin)
    bin_to_int = int(x_bin, 2)
    int_to_real = bin_to_int * (b - a) / (2**l - 1) + a
    return round(int_to_real, int(-math.log10(d)))

def f_x(x_real):
    return (x_real % 1) * (np.cos(20 * np.pi * x_real) - np.sin(x_real))

def steepest_ascent(a, b, d, T):
    l = math.ceil(math.log2((b - a) / d + 1))
    current_real = round(random.uniform(a, b), int(-math.log10(d)))
    current_bin = real_to_bin(a, b, current_real, d)
    best_real, best_bin = current_real, current_bin
    best_f = f_x(current_real)
    
    history = [(current_real, current_bin, best_f)]
    
    for t in range(T):
        local_max = False
        
        while not local_max:
            neighbors = []
            for i in range(l):
                new_bin = list(current_bin)
                new_bin[i] = '1' if new_bin[i] == '0' else '0'
                neighbors.append("".join(new_bin))
            
            # Evaluate neighbors
            neighbor_values = [(bin_to_real(a, b, n_bin, d), f_x(bin_to_real(a, b, n_bin, d))) for n_bin in neighbors]
            best_neighbor = max(neighbor_values, key=lambda x: x[1])
            
            if best_neighbor[1] > best_f:
                current_real, best_f = best_neighbor
                current_bin = real_to_bin(a, b, current_real, d)
                history.append((current_real, current_bin, best_f))
            else:
                local_max = True
        
        # Restart from a new point
        current_real = round(random.uniform(a, b), int(-math.log10(d)))
        current_bin = real_to_bin(a, b, current_real, d)
    
    return history

# Parameters
a, b = -4, 12
d = 0.001
T = 100

history = steepest_ascent(a, b, d, T)

# Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Steepest Ascent Results")
    
    # Treeview setup
    columns = ("X Real", "Binary", "f(X)")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    
    # Insert data
    for real, binary, value in history:
        tree.insert("", "end", values=(real, binary, value))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    root.mainloop()

# Plot results
x_vals = [x[0] for x in history]
f_vals = [x[2] for x in history]

# plt.plot(x_vals, f_vals, marker='o')
# plt.xlabel("x_real")
# plt.ylabel("f(x_real)")
# plt.title("Function Optimization using Steepest Ascent")
# plt.show()

# wygnenerowanie okienka
root = tk.Tk()
root.title("f(x)= x MOD 1 *cos(20π*x) – sin(x)")
root.state('zoomed')

# input a
label_a = tk.Label(root, text="Podaj a:")
label_a.grid(row=0, column=0, sticky='w', padx=5, pady=5)
entry_a = tk.Entry(root, width=10)
entry_a.grid(row=0, column=1, sticky='w', padx=5, pady=5)
entry_a.insert(0, "-4")

# input b
label_b = tk.Label(root, text="Podaj b:")
label_b.grid(row=0, column=2, sticky='w', padx=5, pady=5)
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=0, column=3, sticky='w', padx=5, pady=5)
entry_b.insert(0, "12")

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
combobox_d.current(2)

# input T
label_T = tk.Label(root, text="Podaj T:")
label_T.grid(row=3, column=2, sticky='w', padx=5, pady=5)
entry_T = tk.Entry(root, width=10)
entry_T.grid(row=3, column=3, sticky='w', padx=5, pady=5)

# buttons
button = tk.Button(root, text="Oblicz", command=create_gui)
button.grid(row=5, columnspan=2, padx=10, pady=10)


# test_button = tk.Button(root, text="Testy", command=show_test)
# test_button.grid(row=5, column=5, padx=10, pady=10)

# table data
columns = ["L.P.", "x(real)", "x(bin)", "f(x)", "Percentage"]
table = ttk.Treeview(root, columns=columns, show="headings", height=20)
table.grid(row=6, column=0, columnspan=3, padx=5, pady=10)

table.column("L.P.", width=40)
table.column("x(real)", width=80)
table.column("x(bin)", width=110)
table.column("f(x)", width=80)
table.column("Percentage", width=100)

for col in columns:
    table.heading(col, text=col)

# test table data
# test_columns = ["L.P.", "zbiór", "f avg(x)"]
# table_test = ttk.Treeview(root, columns=test_columns, show="headings", height=20)
# table_test.grid(row=6, column=4, columnspan=3, padx=5, pady=10)

# table_test.column("L.P.", width=50)
# table_test.column("zbiór", width=180)
# table_test.column("f avg(x)", width=90)

# for col in test_columns:
#     table_test.heading(col, text=col)

# launch the app
root.mainloop()