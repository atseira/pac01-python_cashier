from tabulate import tabulate

from db_helper import create_tables, insert_transaction, insert_order_detail
import promos


class Item:
    """
    A class representing an item with a quantity and a price.

    Attributes:
    -----------
    qty : int
        The quantity of the item.
    price : int
        The price of the item.
    """

    def __init__(self, qty, price):
        self.qty = qty
        self.price = price

    def update_qty(self, qty):
        self.qty = qty

    def update_price(self, price):
        self.price = price

    def __str__(self):
        return f"[{self.qty}, {self.price}]"


class Transaction:
    """
    A class representing a transaction with a list of items, a promo code, and methods for managing the transaction.

    Attributes:
    -----------
    items : dict
        A dictionary of items in the transaction, where the keys are the names of the items and the values are `Item` objects.
    promo : str
        The promo code to be applied to the transaction.
    """

    def __init__(self):
        self.items = {}
        self.promo = None
        create_tables()

    def insert_to_db(self, total, discount, final):
        transaction_id = insert_transaction(total, discount, final)
        for name, item in self.items.items():
            insert_order_detail(transaction_id, name, item.qty, item.price)

    def add_item(self, name, qty, price):
        """
        Add an item to the transaction.

        Parameters:
        -----------
        name : str
            The name of the item to be added.
        qty : int
            The quantity of the item to be added.
        price : int
            The price of the item to be added.

        Returns:
        --------
        None
        """
        if isinstance(name, str) and isinstance(qty, int) and isinstance(price, int):
            self.items[name] = Item(qty, price)
            print(f"Pemesanan sudah benar: {{'{name}': {self.items[name]}}}")
        else:
            print("Terdapat kesalahan input data")

    def update_item_name(self, old_name, new_name):
        self.items[new_name] = self.items.pop(old_name)

    def update_item_qty(self, name, qty):
        self.items[name].update_qty(qty)

    def update_item_price(self, name, price):
        self.items[name].update_price(price)

    def delete_item(self, name):
        self.items.pop(name)

    def reset_transaction(self):
        self.items = {}
        print("Semua item berhasil di-delete!")

    def check_order(self):
        """
        Print a table showing the items in the transaction and their quantities and prices.

        Returns:
        --------
        None
        """
        # Extract the data into a list of tuples
        data = [(name, item.qty, item.price, item.qty*item.price)
                for name, item in self.items.items()]

        # Print the table using tabulate
        print(tabulate(data, headers=["Item", "Qty", "Price"]))

    def set_promo(self, promo):
        self.promo = promo

    def check_out(self):
        """
        Calculate the final total and discount for the transaction, apply the promo code (there is a default),
        and insert the transaction and order details into the database.

        Returns:
        --------
        None
        """
        promo_function = promos.get_promo(self.promo)
        total = promos.no_promo_total(self.items)
        final, discount = promo_function(self.items)
        discount_percent = discount * 100
        self.check_order()
        print(f"Total harga: {total:,}")
        print(f"% diskon: {discount_percent:.2f}%")
        print(f"Harga final: {final:,}")
        self.insert_to_db(total, discount_percent, final)

    def __str__(self):
        item_str = ", ".join(f"'{key}': {value}" for key,
                             value in self.items.items())
        return f"{{{item_str}}}"
