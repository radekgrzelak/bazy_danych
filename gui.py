import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funkcja do inicjalizacji bazy danych i tworzenia tabel
def inicjalizuj_baze():
    conn = sqlite3.connect('biblioteka.db')
    cursor = conn.cursor()

    # Tworzenie tabeli Uczniowie, jeśli nie istnieje
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Uczniowie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imie TEXT NOT NULL,
        nazwisko TEXT NOT NULL,
        klasa TEXT
    )
    ''')

    # Sprawdzenie, czy kolumna 'ksiazka' istnieje, a jeśli nie, dodaj ją
    cursor.execute("PRAGMA table_info(Uczniowie)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    if 'ksiazka' not in column_names:
        cursor.execute("ALTER TABLE Uczniowie ADD COLUMN ksiazka TEXT")

    conn.commit()
    conn.close()


# Funkcja do połączenia z bazą danych
def polacz_z_baza():
    return sqlite3.connect('biblioteka.db')

# Funkcja do dodawania ucznia
def dodaj_ucznia():
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    klasa = entry_klasa.get()

    if imie and nazwisko and klasa:
        conn = polacz_z_baza()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Uczniowie (imie, nazwisko, klasa) VALUES (?, ?, ?)", (imie, nazwisko, klasa))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Uczeń został dodany!")
        entry_imie.delete(0, tk.END)
        entry_nazwisko.delete(0, tk.END)
        entry_klasa.delete(0, tk.END)
        wyswietl_uczniow()
    else:
        messagebox.showwarning("Błąd", "Wypełnij wszystkie pola!")

# Funkcja do wypożyczania książki przez ucznia
def wypozycz_ksiazke():
    wybrany_uczen = listbox_uczniowie.get(tk.ACTIVE)
    ksiazka = entry_ksiazka.get()

    if wybrany_uczen and ksiazka:
        uczen_id = wybrany_uczen.split(",")[0].split(":")[1].strip()
        conn = polacz_z_baza()
        cursor = conn.cursor()
        cursor.execute("UPDATE Uczniowie SET ksiazka = ? WHERE id = ?", (ksiazka, uczen_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", f"Uczeń wypożyczył książkę: {ksiazka}")
        entry_ksiazka.delete(0, tk.END)
        wyswietl_uczniow()
    else:
        messagebox.showwarning("Błąd", "Wybierz ucznia i wprowadź tytuł książki!")

# Funkcja do usuwania ucznia
def usun_ucznia():
    wybrany_uczen = listbox_uczniowie.get(tk.ACTIVE)
    if wybrany_uczen:
        uczen_id = wybrany_uczen.split(",")[0].split(":")[1].strip()
        odpowiedz = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć ucznia o ID {uczen_id}?")
        if odpowiedz:
            conn = polacz_z_baza()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Uczniowie WHERE id = ?", (uczen_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukces", "Uczeń został usunięty!")
            wyswietl_uczniow()
    else:
        messagebox.showwarning("Błąd", "Wybierz ucznia do usunięcia!")

# Funkcja do wyświetlania listy uczniów
def wyswietl_uczniow():
    conn = polacz_z_baza()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Uczniowie")
    uczniowie = cursor.fetchall()
    conn.close()

    listbox_uczniowie.delete(0, tk.END)
    for uczen in uczniowie:
        wypozyczona_ksiazka = uczen[4] if uczen[4] else "Brak książki"
        listbox_uczniowie.insert(tk.END, f"ID: {uczen[0]}, Imię: {uczen[1]}, Nazwisko: {uczen[2]}, Klasa: {uczen[3]}, Książka: {wypozyczona_ksiazka}")

# Inicjalizacja bazy danych przy starcie programu
inicjalizuj_baze()

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("System Zarządzania Biblioteką Szkolną")

# Ramka do dodawania ucznia
frame_dodaj_ucznia = tk.LabelFrame(root, text="Dodaj ucznia", padx=10, pady=10)
frame_dodaj_ucznia.pack(padx=10, pady=10, fill="x")

tk.Label(frame_dodaj_ucznia, text="Imię:").grid(row=0, column=0, sticky="w")
entry_imie = tk.Entry(frame_dodaj_ucznia)
entry_imie.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_dodaj_ucznia, text="Nazwisko:").grid(row=1, column=0, sticky="w")
entry_nazwisko = tk.Entry(frame_dodaj_ucznia)
entry_nazwisko.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_dodaj_ucznia, text="Klasa:").grid(row=2, column=0, sticky="w")
entry_klasa = tk.Entry(frame_dodaj_ucznia)
entry_klasa.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_dodaj_ucznia, text="Dodaj ucznia", command=dodaj_ucznia).grid(row=3, column=0, columnspan=2, pady=10)

# Ramka do wypożyczania książki
frame_wypozycz_ksiazke = tk.LabelFrame(root, text="Wypożycz książkę", padx=10, pady=10)
frame_wypozycz_ksiazke.pack(padx=10, pady=10, fill="x")

tk.Label(frame_wypozycz_ksiazke, text="Tytuł książki:").grid(row=0, column=0, sticky="w")
entry_ksiazka = tk.Entry(frame_wypozycz_ksiazke)
entry_ksiazka.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_wypozycz_ksiazke, text="Wypożycz książkę", command=wypozycz_ksiazke).grid(row=1, column=0, columnspan=2, pady=10)

# Ramka do wyświetlania listy uczniów
frame_uczniowie = tk.LabelFrame(root, text="Lista uczniów", padx=10, pady=10)
frame_uczniowie.pack(padx=10, pady=10, fill="both", expand=True)

listbox_uczniowie = tk.Listbox(frame_uczniowie)
listbox_uczniowie.pack(fill="both", expand=True)

# Przycisk do usuwania ucznia
tk.Button(frame_uczniowie, text="Usuń ucznia", command=usun_ucznia).pack(pady=10)

# Inicjalne wyświetlenie listy uczniów
wyswietl_uczniow()

# Uruchomienie głównej pętli aplikacji
root.mainloop()
