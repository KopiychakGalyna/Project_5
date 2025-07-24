# Projekt 5: Vylepšený task manager 

## Popis projektu

Aplikace pro správu úkolů s ukládáním dat do MySQL databáze. Program umožňuje přidávat, zobrazovat, aktualizovat a mazat úkoly
přes jednoduché menu v terminálu. Všechny operace pracují přímo s databází a je možné je automatizovaně testovat.

## Funkcionalita

- **Přidání úkolu** – Zadání názvu a popisu, stav se nastaví automaticky na "Nezahájeno".
- **Zobrazení úkolů** – Výpis všech úkolů, možnost filtrování podle stavu („Nezahájeno“, „Probíhá“).
- **Aktualizace úkolu** – Změna stavu vybraného úkolu na „Probíhá“ nebo „Hotovo“.
- **Odstranění úkolu** – Smazání úkolu podle ID.
- **Automatizované testy** – Testování všech hlavních funkcí pomocí pytest a testovací databáze.

## Závislosti
- Python 3.10+
- mysql-connector-python
- pytest

Instalace:
   pip install mysql-connector-python pytest

## Struktura databáze

```sql
CREATE TABLE ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(100) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
);


Soubory projektu:
main.py – Spouští aplikaci s menu a volá všechny základní funkce (přidání, výpis, aktualizace, mazání úkolů).

repository.py – Obsahuje veškerou logiku pro práci s databází (CRUD operace).

db.py – Připojení k MySQL databázi.

test_db.py – Automatizované testy pomocí pytest (pozitivní i negativní scénáře).

config.py nebo .env – Nastavení přístupu k databázi (název DB, heslo, uživatel…).

První spuštění:
Vytvoř si MySQL databázi:
Například task_manager (produkční) a test_task_manager (testovací).

Nastav přístupové údaje:
V souboru .env, config.py nebo přímo v kódu (dle implementace).

Spusť program:
   python main.py

Spuštění testů:
Testy používají testovací databáza
   pytest test_db.py



