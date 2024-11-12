import sqlite3
import time
import hashlib
import os

# Funkcija za kreiranje i inicijalizaciju baze podataka
def init_db():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            account_number TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            token TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# Funkcija za dodavanje korisnika
def add_user(cursor, name, account_number, password):
    cursor.execute('''
        INSERT INTO clients (name, account_number, password) 
        VALUES (?, ?, ?)
    ''', (name, account_number, password))

# Funkcija za validaciju korisnika
def validate_user(cursor, account_number, password):
    cursor.execute('''
        SELECT id FROM clients WHERE account_number = ? AND password = ?
    ''', (account_number, password))
    return cursor.fetchone()

# Funkcija za generisanje tokena
def generate_token():
    return hashlib.sha256(os.urandom(64)).hexdigest()

# Funkcija za ažuriranje tokena u bazi podataka
def update_token(cursor, user_id, token):
    cursor.execute('''
        UPDATE clients SET token = ? WHERE id = ?
    ''', (token, user_id))

def main():
    conn, cursor = init_db()

    # Dodavanje tri proizvoljna korisnika
    users = [
        ('Marko Markovic', '12345', 'pass123'),
        ('Jovan Jovanovic', '67890', 'pass456'),
        ('Ana Anic', '54321', 'pass789')
    ]
    for user in users:
        try:
            add_user(cursor, *user)
        except sqlite3.IntegrityError:
            pass  # Ignorišemo grešku ako korisnik već postoji

    conn.commit()

    # Zahtev za unos broja računa i šifre
    account_number = input('Unesite broj računa: ')
    password = input('Unesite šifru: ')

    # Validacija korisnika
    user = validate_user(cursor, account_number, password)
    if user:
        user_id = user[0]
        token = generate_token()
        update_token(cursor, user_id, token)
        conn.commit()
        print(f'Pristup uspešan. Vaš token je: {token}')
    else:
        print('Greška: Neispravan broj računa ili šifra.')

    # Zatvaranje konekcije
    conn.close()

if __name__ == '__main__':
    main()
