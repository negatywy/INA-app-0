import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

# Funkcje matematyczne do obliczeń
def funkcje_matematyczne(x, d):
    return {
        'sin(x)': math.sin(x),
        'cos(x)': math.cos(x),
        'tan(x)': math.tan(x),
        'sqrt(|x|)': math.sqrt(abs(x)),
        'x^d': x ** d,
        'ln(|x|)': math.log(abs(x)) if x != 0 else float('nan')
    }

# Funkcja do generowania tabeli
def generuj_tabele(a, b, N, d):
    wyniki = []
    for _ in range(N):
        x = random.randint(a, b)
        funkcje = funkcje_matematyczne(x, d)
        wyniki.append([x] + list(funkcje.values()))
    return wyniki

# Obsługa przycisku "Licz"
def oblicz():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        N = int(entry_N.get())
        d = int(combobox_d.get())

        if a > b:
            messagebox.showerror("Błąd", "Liczba a musi być mniejsza lub równa liczbie b")
            return

        tabela_wynikow = generuj_tabele(a, b, N, d)
        wyswietl_tabele(tabela_wynikow)

    except ValueError:
        messagebox.showerror("Błąd", "Proszę podać prawidłowe liczby")

# Funkcja do wyświetlenia wyników w tabeli
def wyswietl_tabele(wyniki):
    for row in tabela.get_children():
        tabela.delete(row)

    for wynik in wyniki:
        tabela.insert("", "end", values=wynik)

# Tworzenie okna
root = tk.Tk()
root.title("Aplikacja do obliczeń matematycznych")
root.geometry("400x300")  # Ustawia rozmiar okna na 400x300 pikseli

# Etykiety i pola wejściowe
label_a = tk.Label(root, text="Podaj a:")
label_a.grid(row=0, column=0, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej
entry_a = tk.Entry(root, width=10)  # Ustawia szerokość pola na 10 znaków
entry_a.grid(row=0, column=1, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej

label_b = tk.Label(root, text="Podaj b:")
label_b.grid(row=1, column=0, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej
entry_b = tk.Entry(root, width=10)  # Ustawia szerokość pola na 10 znaków
entry_b.grid(row=1, column=1, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej

label_N = tk.Label(root, text="Podaj N:")
label_N.grid(row=2, column=0, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej
entry_N = tk.Entry(root, width=10)  # Ustawia szerokość pola na 10 znaków
entry_N.grid(row=2, column=1, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej

label_d = tk.Label(root, text="Wybierz d:")
label_d.grid(row=3, column=0, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej
combobox_d = ttk.Combobox(root, values=[0.1, 0.01, 0.001, 0.0001])
combobox_d.grid(row=3, column=1, sticky='w', padx=5, pady=5)  # Wyrównanie do lewej
combobox_d.current(0)

# Przycisk
button = tk.Button(root, text="Licz", command=oblicz)
button.grid(row=4, columnspan=2, padx=5, pady=10)

# Tabela wyników
columns = ["x", "sin(x)", "cos(x)", "tan(x)", "sqrt(|x|)", "x^d", "ln(|x|)"]
tabela = ttk.Treeview(root, columns=columns, show="headings")
tabela.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

# Ustawienie szerokości kolumn tabeli
tabela.column("x", width=40)  # Szerokość kolumny x
tabela.column("sin(x)", width=60)  # Szerokość kolumny sin(x)
tabela.column("cos(x)", width=60)  # Szerokość kolumny cos(x)
tabela.column("tan(x)", width=60)  # Szerokość kolumny tan(x)
tabela.column("sqrt(|x|)", width=70)  # Szerokość kolumny sqrt(|x|)
tabela.column("x^d", width=60)  # Szerokość kolumny x^d
tabela.column("ln(|x|)", width=70)  # Szerokość kolumny ln(|x|)

# Ustawienia nagłówków tabeli
for col in columns:
    tabela.heading(col, text=col)

# Uruchomienie aplikacji
root.mainloop()
