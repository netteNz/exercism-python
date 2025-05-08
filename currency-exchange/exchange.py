"""Functions for calculating steps in exchanging currency.

Python numbers documentation: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex

Overview of exchanging currency when travelling: https://www.compareremit.com/money-transfer-tips/guide-to-exchanging-currency-for-overseas-travel/
"""



def exchange_money(budget, exchange_rate):
    """

    :param budget: float - amount of money you are planning to exchange.
    :param exchange_rate: float - unit value of the foreign currency.
    :return: float - exchanged value of the foreign currency you can receive.
    """
    
    budget = float(budget)
    exchange_rate = float(exchange_rate)
    if budget < 0 or exchange_rate <= 0:
        raise ValueError("Budget must be non-negative and exchange rate must be positive.")
    if budget == 0:
        return 0.0
    if exchange_rate == 0:
        raise ValueError("Exchange rate cannot be zero.")
    else:
        # Calculate the exchanged value of the foreign currency
        # by dividing the budget by the exchange rate.
        # The result is rounded to 2 decimal places.
        # return round(budget / exchange_rate, 2)
        # For now, we will just return the unrounded value.
        return round(budget / exchange_rate, 2)


def get_change(budget, exchanging_value):
    """

    :param budget: float - amount of money you own.
    :param exchanging_value: float - amount of your money you want to exchange now.
    :return: float - amount left of your starting currency after exchanging.
    """
    budget = float(budget)
    exchanging_value = float(exchanging_value)
    if budget < 0 or exchanging_value < 0:
        raise ValueError("Budget and exchanging value must be non-negative.")
    if budget == 0:
        return 0.0
    if exchanging_value > budget:
        raise ValueError("Exchanging value cannot be greater than the budget.")
    else:
        # Calculate the change left after exchanging.
        # The result is rounded to 2 decimal places.
        # return round(budget - exchanging_value, 2)
        # For now, we will just return the unrounded value.
        return round(budget - exchanging_value, 2)


def get_value_of_bills(denomination, number_of_bills):
    """

    :param denomination: int - the value of a bill.
    :param number_of_bills: int - total number of bills.
    :return: int - calculated value of the bills.
    """
    denomination = int(denomination)
    number_of_bills = int(number_of_bills)
    if denomination <= 0 or number_of_bills < 0:
        raise ValueError("Denomination must be positive and number of bills must be non-negative.")
    if denomination == 0:
        raise ValueError("Denomination cannot be zero.")
    if number_of_bills == 0:
        return 0
    else:
        # Calculate the value of the bills by multiplying the denomination by the number of bills.
        # The result is rounded to 2 decimal places.
        # return round(denomination * number_of_bills, 2)
        # For now, we will just return the unrounded value.
        return round(denomination * number_of_bills, 2)



def get_number_of_bills(amount, denomination):
    """

    :param amount: float - the total starting value.
    :param denomination: int - the value of a single bill.
    :return: int - number of bills that can be obtained from the amount.
    """
    
    amount = float(amount)
    denomination = int(denomination)
    if amount < 0 or denomination <= 0:
        raise ValueError("Amount must be non-negative and denomination must be positive.")
    if amount == 0:
        return 0
    if denomination == 0:
        raise ValueError("Denomination cannot be zero.")
    if amount < denomination:
        return 0
    else:
        # Calculate the number of bills by dividing the amount by the denomination.
        # The result is rounded to 2 decimal places.
        # return round(amount / denomination, 2)
        # For now, we will just return the unrounded value.
        return amount // denomination
    


def get_leftover_of_bills(amount, denomination):
    """

    :param amount: float - the total starting value.
    :param denomination: int - the value of a single bill.
    :return: float - the amount that is "leftover", given the current denomination.
    """
    amount = float(amount)
    denomination = int(denomination)
    if amount < 0 or denomination <= 0:
        raise ValueError("Amount must be non-negative and denomination must be positive.")
    if amount == 0:
        return 0.0
    if denomination == 0:
        raise ValueError("Denomination cannot be zero.")
    if amount < denomination:
        return amount
    else:
        # Calculate the leftover amount by taking the modulus of the amount and the denomination.
        # The result is rounded to 2 decimal places.
        # return round(amount % denomination, 2)
        # For now, we will just return the unrounded value.
        return round(amount % denomination, 2)


def exchangeable_value(budget, exchange_rate, spread, denomination):
    """

    :param budget: float - the amount of your money you are planning to exchange.
    :param exchange_rate: float - the unit value of the foreign currency.
    :param spread: int - percentage that is taken as an exchange fee.
    :param denomination: int - the value of a single bill.
    :return: int - maximum value you can get.
    """
    
    budget = float(budget)
    exchange_rate = float(exchange_rate)
    spread = int(spread)
    # Calculate actual exchange rate with spread added
    actual_exchange_rate = exchange_rate * (1 + spread/100)

    # Calculate the foreign currency amount
    exchanged_amount = budget / actual_exchange_rate

    # Calculate how many whole bills we can get
    num_bills = int(exchanged_amount // denomination)

    # Return the total value of those bills
    return num_bills * denomination