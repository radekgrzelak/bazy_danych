CREATE TABLE Uczniowie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    klasa TEXT
);

CREATE TABLE Kategorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    nazwa TEXT NOT NULL
);

CREATE TABLE Autorzy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL
);

CREATE TABLE Wydawcy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    nazwa TEXT NOT NULL
);

CREATE TABLE Ksiazki (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    tytul TEXT NOT NULL,
    kategoria_id INTEGER,
    autor_id INTEGER,
    wydawca_id INTEGER,
    FOREIGN KEY (kategoria_id) REFERENCES Kategorie(id),
    FOREIGN KEY (autor_id) REFERENCES Autorzy(id),
    FOREIGN KEY (wydawca_id) REFERENCES Wydawcy(id)
);

CREATE TABLE Wypozyczenia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Używamy AUTOINCREMENT bez myślnika
    uczen_id INTEGER,
    ksiazka_id INTEGER,
    data_wypozyczenia DATE,
    data_zwrotu DATE,
    FOREIGN KEY (uczen_id) REFERENCES Uczniowie(id),
    FOREIGN KEY (ksiazka_id) REFERENCES Ksiazki(id)
);
