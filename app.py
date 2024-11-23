import numpy as np
import math
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

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
    return round((x_real % 1) * (np.cos(20 * np.pi * x_real) - np.sin(x_real)), 3)

def steepest_ascent(a, b, d, T):
    l = math.ceil(math.log2((b - a) / d + 1))
    current_real = round(random.uniform(a, b), int(-math.log10(d)))
    current_bin = real_to_bin(a, b, current_real, d)
    best_real, best_bin = current_real, current_bin
    best_f = f_x(current_real)
    
    all_f_values = []  # Track all f(x) values
    iteration_values = []  # Track best f(x) of each iteration
    
    for _ in range(T):
        local_max = False
        while not local_max:
            neighbors = []
            for i in range(l):
                new_bin = list(current_bin)
                new_bin[i] = '1' if new_bin[i] == '0' else '0'
                neighbors.append("".join(new_bin))
            
            neighbor_values = [(bin_to_real(a, b, n_bin, d), f_x(bin_to_real(a, b, n_bin, d))) for n_bin in neighbors]
            all_f_values.append([val[1] for val in neighbor_values])  # Track all neighbors' values
            
            best_neighbor = max(neighbor_values, key=lambda x: x[1])
            if best_neighbor[1] > best_f:
                current_real, best_f = best_neighbor
                current_bin = real_to_bin(a, b, current_real, d)
            else:
                local_max = True
        
        iteration_values.append(best_f)  # Record the best value of this iteration
        current_real = round(random.uniform(a, b), int(-math.log10(d)))
        current_bin = real_to_bin(a, b, current_real, d)
    
    return best_real, best_bin, best_f, all_f_values, iteration_values

def calculate():
    a = float(entry_a.get())
    b = float(entry_b.get())
    d = float(combobox_d.get())
    T = int(entry_T.get())
    
    best_real, best_bin, best_f, all_f_values, iteration_values = steepest_ascent(a, b, d, T)
    
    # Clear the table and insert the best solution
    for row in table.get_children():
        table.delete(row)
    table.insert("", "end", values=(best_real, best_bin, best_f))
    
    # Plot results
    plt.figure(figsize=(10, 6))
    
    # Plot all intermediate f(x) values
    for step_f_values in all_f_values:
        plt.plot(step_f_values, marker='.', linestyle='--', alpha=0.5)
    
    # Plot the best f(x) evolution
    plt.plot(iteration_values, marker='o', color='red', linewidth=2, label='Best f(x)')
    
    plt.xlabel("Iteration Steps")
    plt.ylabel("f(x)")
    plt.title("Function Optimization: Steepest Ascent Algorithm")
    plt.legend()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("f(x) = (x MOD 1) * cos(20πx) – sin(x)")
root.state('zoomed')

label_a = tk.Label(root, text="Podaj a:")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(root, width=10)
entry_a.grid(row=0, column=1, padx=5, pady=5)
entry_a.insert(0, "-4")

label_b = tk.Label(root, text="Podaj b:")
label_b.grid(row=0, column=2, padx=5, pady=5)
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=0, column=3, padx=5, pady=5)
entry_b.insert(0, "12")

label_d = tk.Label(root, text="Wybierz d:")
label_d.grid(row=1, column=0, padx=5, pady=5)
combobox_d = ttk.Combobox(root, values=[0.1, 0.01, 0.001, 0.0001])
combobox_d.grid(row=1, column=1, padx=5, pady=5)
combobox_d.current(2)

label_T = tk.Label(root, text="Podaj T:")
label_T.grid(row=1, column=2, padx=5, pady=5)
entry_T = tk.Entry(root, width=10)
entry_T.grid(row=1, column=3, padx=5, pady=5)
entry_T.insert(0, "30")

button = tk.Button(root, text="Oblicz", command=calculate)
button.grid(row=2, columnspan=4, pady=10)

columns = ["x(real)", "x(bin)", "f(x)"]
table = ttk.Treeview(root, columns=columns, show="headings", height=20)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)
table.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()