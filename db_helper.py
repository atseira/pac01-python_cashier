import sqlite3
from tabulate import tabulate

DB_FILENAME = "orders.db"

TABLE_TRANSACTIONS = '''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_harga_rp INTEGER,
    diskon_persen INTEGER,
    harga_final_rp INTEGER
);'''

TABLE_ORDER_DETAILS = '''
CREATE TABLE IF NOT EXISTS order_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    nama_item TEXT,
    jumlah_item INTEGER,
    harga_item INTEGER,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);'''


def singleton(cls):
    """
    A decorator to turn a class into a singleton.

    Parameters:
    -----------
    cls : class
        The class to be turned into a singleton.

    Returns:
    --------
    A new function that creates and returns the singleton instance of the class. If the singleton instance has already
    been created, the existing instance is returned instead of creating a new one.
    """
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return get_instance


@singleton
class SQLiteConnector:
    """
    A class that creates a SQLite connection and cursor, and ensures that only one instance of the class is ever created.
    """

    def __init__(self):
        self.connection = sqlite3.connect(DB_FILENAME)
        self.cursor = self.connection.cursor()


def get_conn_cursor():
    """
    Creates a connection to the SQLite database and returns the connection and cursor.

    Usage:
    - Call the get_conn_cursor() function to create a connection to the SQLite database and return the connection
      and cursor objects.
    - This function uses the @singleton decorator to ensure that only one instance of the SQLiteConnector class is ever
      created.
    - To use the connection and cursor, simply unpack the return value of the function into separate variables:
        conn, cursor = get_conn_cursor()
    """
    sqlc = SQLiteConnector()
    return sqlc.connection, sqlc.cursor
    # print table content named orders in sqlite3


def create_tables():
    """
    Creates two tables in the SQLite database: 'transactions' and 'order_details' using SQL query constant defined at beginning of code.
    """
    conn, cursor = get_conn_cursor()
    cursor.execute(TABLE_TRANSACTIONS)
    cursor.execute(TABLE_ORDER_DETAILS)
    conn.commit()



def show_table_transactions():
    """
    Prints the contents of the 'transactions' table in the SQLite database using tabulate.
    """
    _, cursor = get_conn_cursor()
    # Select all rows from the "orders" table
    cursor.execute("SELECT * FROM transactions")

    # Fetch all results and assign them to a variable
    rows = cursor.fetchall()

    # Get the column names from the cursor's description attribute
    headers = [desc[0] for desc in cursor.description]

    # Print the table using tabulate
    print(tabulate(rows, headers=headers))

def show_detailed_transactions():
    """
    Prints the contents of the 'transactions' table joined with 'order_details' table in the SQLite database.
    """
    _, cursor = get_conn_cursor()

    cursor.execute('''
        SELECT transactions.id, total_harga_rp, diskon_persen, harga_final_rp, nama_item, jumlah_item, harga_item
        FROM transactions
        RIGHT JOIN order_details
        ON transactions.id = order_details.transaction_id;
    ''')

    # Fetch all results and assign them to a variable
    rows = cursor.fetchall()

    # Get the column names from the cursor's description attribute
    headers = [desc[0] for desc in cursor.description]

    # Print the table using tabulate
    print(tabulate(rows, headers=headers))



def drop_tables():
    conn, cursor = get_conn_cursor()
    cursor.execute('DROP TABLE IF EXISTS transactions')
    cursor.execute('DROP TABLE IF EXISTS order_details')
    conn.commit()


def delete_tables_data():
    conn, cursor = get_conn_cursor()
    cursor.execute('DELETE FROM transactions')
    cursor.execute('DELETE FROM order_details')
    conn.commit()


def insert_transaction(total, discount, final):
    """
    Inserts a new row into the 'transactions' table in the SQLite database.

    Args:
    - total (int): the total cost of the transaction in Indonesian rupiah, before any discounts
    - discount (float): the discount percentage applied to the transaction (0.0-1.0)
    - final (int): the final cost of the transaction in Indonesian rupiah, after any discounts

    Returns:
    - int: the ID of the new row inserted into the 'transactions' table
    """
    conn, cursor = get_conn_cursor()
    cursor.execute('INSERT INTO transactions (total_harga_rp, diskon_persen, harga_final_rp) VALUES (?, ?, ?)',
                   (total, discount, final))
    conn.commit()
    return cursor.lastrowid


def insert_order_detail(transaction_id, name, qty, price):
    """
    Inserts a new row into the 'order_details' table in the SQLite database.

    Args:
    - transaction_id (int): the ID of the transaction to which this order detail belongs
    - name (str): the name of the item ordered
    - qty (int): the quantity of the item ordered
    - price (int): the price of the item ordered in Indonesian rupiah
    """
    conn, cursor = get_conn_cursor()
    cursor.execute('INSERT INTO order_details (transaction_id, nama_item, jumlah_item, harga_item) VALUES (?, ?, ?, ?)',
                   (transaction_id, name, qty, price))
    conn.commit()
