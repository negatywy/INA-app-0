import random
import numpy as np

pm = 0.05

x_bin = []
for i in range(10):
    y = int(random.uniform(0, 6))
    x = np.array(['0'] * y + ['1'] * (6 - y))
    np.random.shuffle(x)
    x_bin.append(x)

for row in x_bin:
    gene = -1
    print("x_bin: ", row)
    for i in range(6):
        r_value = round(random.uniform(0, 1), 4)
        if r_value <= pm:
            if gene == -1:
                gene = i+1
            else:
                gene = str(gene) + ', ' + str(i+1)
                #x_bin = mutate(x_bin, i)
        elif gene == -1 and i == 5:
            gene = 'nan'
        print("R: ", r_value, " Gen: ", gene)
    print("--------------------")