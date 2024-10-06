import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

# Funkcje matematyczne do obliczeń
def funkcje_matematyczne(x, d):
    try:
        sin_x = math.sin(x)
        cos_x = math.cos(sin_x)  # cos przyjmuje wynik sin
        tan_x = math.tan(cos_x)   # tan przyjmuje wynik cos
        sqrt_x = math.sqrt(abs(tan_x))  # sqrt przyjmuje wynik tan
        x_d = tan_x ** d           # x^d przyjmuje wynik tan
        ln_x = math.log(abs(x_d)) if x_d != 0 else float('nan')  # ln przyjmuje wynik x^d

        return [sin_x, cos_x, tan_x, sqrt_x, x_d, ln_x]
    except ValueError:
        return [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')]

# Funkcja do generowania tabeli
def generuj_tabele(a, b, N, d):
    wyniki = []
    for _ in range(N):
        x = round(random.uniform(a, b), 3)
        funkcje = funkcje_matematyczne(x, d)
        wyniki.append([x] + funkcje)  # Dodaj x na początku
    return wyniki

# Obsługa przycisku "Licz"
def oblicz():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        N = int(entry_N.get())
        d = float(combobox_d.get())

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

    for index, wynik in enumerate(wyniki, start=1):
        tabela.insert("", "end", values=[index] + wynik)  # Dodaj numer wiersza

# Tworzenie okna
root = tk.Tk()
root.title("Aplikacja do obliczeń matematycznych")
root.geometry("450x300")  # Ustawia rozmiar okna na 450x300 pikseli

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
columns = ["L.P.", "x", "sin(x)", "cos(sin(x))", "tan(cos(sin(x)))", "sqrt(|tan(cos(sin(x)))|)", "tan(cos(sin(x)))^d", "ln(|tan(cos(sin(x)))^d|)"]
tabela = ttk.Treeview(root, columns=columns, show="headings")
tabela.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

# Ustawienie szerokości kolumn tabeli
tabela.column("L.P.", width=40)  # Szerokość kolumny L.P.
tabela.column("x", width=40)  # Szerokość kolumny x
tabela.column("sin(x)", width=60)  # Szerokość kolumny sin(x)
tabela.column("cos(sin(x))", width=90)  # Szerokość kolumny cos(sin(x))
tabela.column("tan(cos(sin(x)))", width=120)  # Szerokość kolumny tan(cos(sin(x)))
tabela.column("sqrt(|tan(cos(sin(x)))|)", width=90)  # Szerokość kolumny sqrt
tabela.column("tan(cos(sin(x)))^d", width=90)  # Szerokość kolumny x^d
tabela.column("ln(|tan(cos(sin(x)))^d|)", width=90)  # Szerokość kolumny ln

# Ustawienia nagłówków tabeli
for col in columns:
    tabela.heading(col, text=col)

# Uruchomienie aplikacji
root.mainloop()
