import pytest
from db import connect_to_db
from repository import pridat_ukol, aktualizovat_ukol, odstranit_ukol

@pytest.fixture
def db_conn():
    """
    Fixture pro vytvoření a uzavření připojení k testovací databázi.
    """
    conn = connect_to_db(testing=True)
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def clear_ukoly(db_conn):
    """
    Fixture, která před každým testem vyčistí tabulku ukoly.
    Zaručuje, že testy jsou na prázdné databázi.
    """
    cursor = db_conn.cursor()
    cursor.execute("TRUNCATE TABLE ukoly")
    db_conn.commit()
    cursor.close()

def test_pridat_ukol_pozitivni(db_conn) -> None:
    """
    Ověřuje, že úkol lze úspěšně přidat do databáze.
    """
    pridat_ukol("Test Úkol", "Testovací popis", conn=db_conn)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test Úkol",))
    vysledek = cursor.fetchone()
    assert vysledek is not None
    cursor.close()

def test_pridat_ukol_negativni(db_conn) -> None:
    """
    Testuje, že pokud zadám prázdný název nebo popis, funkce vyhodí chybu.
    """
    with pytest.raises(ValueError):
        pridat_ukol("", "", conn=db_conn)

def test_aktualizovat_ukol_pozitivni(db_conn) -> None:
    """
    Přidá úkol a následně ověří, že stav úkolu lze změnit na 'Hotovo'.
    """
    pridat_ukol("Aktualizace Úkol", "Popis", conn=db_conn)
    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Aktualizace Úkol",))
    ukol_id = cursor.fetchone()[0]
    aktualizovat_ukol(ukol_id, "Hotovo", conn=db_conn)
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = cursor.fetchone()[0]
    assert stav == "Hotovo"
    cursor.close()

def test_aktualizovat_ukol_negativni(db_conn) -> None:
    """
    Zkouší změnit stav u neexistujícího úkolu a ověří, že se vyhodí výjimka.
    """
    neexistujici_id = 99999
    with pytest.raises(Exception):
        aktualizovat_ukol(neexistujici_id, "Hotovo", conn=db_conn)

def test_odstranit_ukol_pozitivni(db_conn) -> None:
    """
    Přidá úkol, smaže ho a ověří, že už v databázi neexistuje.
    """
    pridat_ukol("Smazat Úkol", "Popis", conn=db_conn)
    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Smazat Úkol",))
    ukol_id = cursor.fetchone()[0]
    odstranit_ukol(ukol_id, conn=db_conn)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    vysledek = cursor.fetchone()
    assert vysledek is None
    cursor.close()

def test_odstranit_ukol_negativni(db_conn) -> None:
    """
    Pokusí se smazat neexistující úkol. Ověří, že funkce neskončí chybou a v databázi nic není.
    """
    neexistujici_id = 99999
    odstranit_ukol(neexistujici_id, conn=db_conn)
    cursor = db_conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    pocet = cursor.fetchone()[0]
    assert pocet == 0
    cursor.close()
