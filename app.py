import numpy as np
import math
import random
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
            for i in range(l):  # Flip each bit once to create neighbors
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

# Save to file
with open("results.txt", "w") as file:
    for real, binary, value in history:
        file.write(f"{real}, {binary}, {value}\n")

# Plot results
x_vals = [x[0] for x in history]
f_vals = [x[2] for x in history]

plt.plot(x_vals, f_vals, marker='o')
plt.xlabel("x_real")
plt.ylabel("f(x_real)")
plt.title("Function Optimization using Steepest Ascent")
plt.show()
