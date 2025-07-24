import mysql.connector
from mysql.connector import Error
from config import load_config

def connect_to_db(config=None, testing=False):
    if config is None:
        config = load_config(testing=testing)

    if testing and "test" not in config["database"].lower():
            raise RuntimeError("Varovani: Pri testovani musis pouzit testovaci DB")

    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print(f"Pripojeni k databazi {config['database']} bylo uspesne")
            return conn
    except Error as e:
        print(f"Chyba pripojeni k databazi: {e}")
        return None





