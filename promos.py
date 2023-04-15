BY_ITEM = 'promo-per-item'
BY_TRX = 'promo-per-transaction'


def get_promo(promo_name):
    """
    Get the promo function associated with the specified promo code.

    Parameters:
    -----------
    promo_name : str
        The promo code to look up.

    Returns:
    --------
    The promo function associated with the specified promo code. If the specified promo code is not recognized,
    the default promo function (promo_per_item) is returned.
    """
    if promo_name == BY_TRX:
        return promo_per_transaction
    return promo_per_item  # default promo


def no_promo_total(items):
    """
    Calculate the total cost of all items in the transaction without applying any promo code.

    Parameters:
    -----------
    items : dict
        A dictionary of items in the transaction, where the keys are the names of the items and the values are `Item` objects.

    Returns:
    --------
    The total cost of all items in the transaction.
    """
    return sum(item.qty * item.price for item in items.values())


def promo_per_transaction(items):
    """
    Calculate the final price and discount for the transaction based on a per-transaction promo code.

    Parameters:
    -----------
    items : dict
        A dictionary of items in the transaction, where the keys are the names of the items and the values are `Item` objects.

    Returns:
    --------
    A tuple containing the final price and discount for the transaction, respectively.
    """
    total_cost = no_promo_total(items)
    discount = 0

    if total_cost > 500_000:
        discount = 0.07
    elif total_cost > 300_000:
        discount = 0.06
    elif total_cost > 200_000:
        discount = 0.05

    final_price = total_cost * (1 - discount)

    return final_price, discount


def promo_per_item(items):
    """
    Calculate the final price and discount for the transaction based on a per-item promo code.

    Parameters:
    -----------
    items : dict
        A dictionary of items in the transaction, where the keys are the names of the items and the values are `Item` objects.

    Returns:
    --------
    A tuple containing the final price and discount for the transaction, respectively.
    """
    final_price = 0

    for item in items.values():
        subtotal = item.qty * item.price
        discount = 0
        if subtotal > 500_000:
            discount = 0.07
        elif subtotal > 300_000:
            discount = 0.06
        elif subtotal > 200_000:
            discount = 0.05

        final_price += subtotal * (1 - discount)

    total_cost = no_promo_total(items)
    discount = 0
    if total_cost > 0:
        discount = (total_cost - final_price)/total_cost

    return final_price, discount
