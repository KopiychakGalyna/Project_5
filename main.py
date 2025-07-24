"""
projekt_5: pátý projekt do Engeto Online Python Akademie

author: Galyna Kopiychak
email: galynakopiychak@outlook.com
"""

from repository import vytvoreni_tabulky, pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol

def hlavni_menu():
    """
    Hlavní menu pro správu úkolů.
    """
    while True:
        print("\nHlavní nabídka - Zobrazit možnosti:")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyberte možnost (1-5): ").strip()

        if volba == '1':
            # Přidání nového úkolu
            nazev = input("Zadejte název úkolu: ").strip()
            popis = input("Zadejte popis úkolu: ").strip()
            try:
                pridat_ukol(nazev, popis)
                print("Úkol byl úspěšně přidán.")
            except Exception as e:
                print(f"Chyba při přidání úkolu: {e}")

        elif volba == '2':
            # Zobrazení úkolů
            while True:
                filtr = input("Chcete zobrazit jen nezahájené/probíhající úkoly? (a/n): ").strip().lower()
                if filtr in ('a', 'n'):
                    break
                print("Zadejte prosím pouze 'a' (ano) nebo 'n' (ne).")

            filtrovat_otevrene = filtr == 'a'
            ukoly = zobrazit_ukoly(only_open=filtrovat_otevrene)
            if not ukoly:
                print("Žádné úkoly nejsou uložené.")
            else:
                print("\nSeznam úkolů:")
                for u in ukoly:
                    print(f"{u[0]}. {u[1]} – {u[2]} | Stav: {u[3]}")

        elif volba == '3':
            # Změna stavu úkolu
            ukoly = zobrazit_ukoly()
            if not ukoly:
                print("Žádné úkoly nejsou uloženy.")
                continue

            print("\nSeznam úkolů:")
            for u in ukoly:
                print(f"{u[0]}. {u[1]} | Stav: {u[3]}")

            try:
                ukol_id = int(input("Zadejte ID úkolu ke změně stavu: ").strip())

                # Kontrola, zda zadané ID existuje v seznamu úkolů
                if not any(u[0] == ukol_id for u in ukoly):
                    print("Úkol s tímto ID neexistuje! Zkuste to znovu.")
                    continue

                print("1. Probíhá\n2. Hotovo")
                stav_volba = input("Zadejte nový stav (1 nebo 2): ").strip()
                novy_stav = "Probíhá" if stav_volba == '1' else "Hotovo" if stav_volba == '2' else None
                if novy_stav is None:
                    print("Neplatná volba stavu.")
                    continue

                aktualizovat_ukol(ukol_id, novy_stav)
                print("Stav úkolu byl úspěšně změněn.")
            except ValueError:
                print("Zadané ID musí být číslo.")
            except Exception as e:
                print(f"Chyba při změně stavu: {e}")

        elif volba == '4':
            # Odstranění úkolu
            ukoly = zobrazit_ukoly()
            if not ukoly:
                print("Žádné úkoly nejsou uložené.")
                continue

            print("\nSeznam úkolů:")
            for u in ukoly:
                print(f"{u[0]}. {u[1]} | Stav: {u[3]}")

            try:
                ukol_id = int(input("Zadejte ID úkolu k odstranění: ").strip())

                # Kontrola, zda ID existuje
                if not any(u[0] == ukol_id for u in ukoly):
                    print("Úkol s tímto ID neexistuje! Zkuste to znovu.")
                    continue

                # CYKLUS pro potvrzení mazání
                while True:
                    potvrzeni = input(f"Opravdu chcete odstranit úkol {ukol_id}? (a/n): ").strip().lower()
                    if potvrzeni in ('a', 'n'):
                        break
                    print("Zadejte prosím pouze 'a' (ano) nebo 'n' (ne).")

                if potvrzeni == 'a':
                    deleted = odstranit_ukol(ukol_id)
                    if deleted:
                        print("Úkol byl odstraněn.")
                else:
                    print("Mazání zrušeno.")

            except ValueError:
                print("Zadané ID musí být číslo.")
            except Exception as e:
                print(f"Chyba při mazání úkolu: {e}")

        elif volba == '5':
            # Ukončení programu
            print("Ukončuji program...")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()
