"""Functions for tracking poker hands and assorted card tasks.

Python list documentation: https://docs.python.org/3/tutorial/datastructures.html
"""


def get_rounds(number):
    """Create a list containing the current and next two round numbers.

    :param number: int - current round number.
    :return: list - current round and the two that follow.
    """
    return [number, number + 1, number + 2]


def concatenate_rounds(rounds_1, rounds_2):
    """Concatenate two lists of round numbers.

    :param rounds_1: list - first rounds played.
    :param rounds_2: list - second set of rounds played.
    :return: list - all rounds played.
    """
    return rounds_1 + rounds_2


def list_contains_round(rounds, number):
    """Check if the list of rounds contains the specified number.

    :param rounds: list - rounds played.
    :param number: int - round number.
    :return: bool - was the round played?
    """
    return number in rounds


def card_average(hand):
    """Calculate and returns the average card value from the list.

    :param hand: list - cards in hand.
    :return: float - average value of the cards in the hand.
    """
    if not hand:
        return 0.0
    return sum(hand) / len(hand)


def approx_average_is_average(hand):
    """Return if the (average of first and last card values) OR ('middle' card) == calculated average.

    :param hand: list - cards in hand.
    :return: bool - does one of the approximate averages equal the `true average`?
    """
    # calculate the average of the hand
    actual_average = sum(hand) / len(hand)
    # calculate the average of the first and last card
    first_average = (hand[0] + hand[-1]) / 2
    # calculate the average of the middle card
    median = hand[len(hand) // 2]
    # check if either of the two averages is equal to the actual average
    return actual_average in (first_average, median)


def average_even_is_average_odd(hand):
    """Return if the (average of even indexed card values) == (average of odd indexed card values).

    :param hand: list - cards in hand.
    :return: bool - are even and odd averages equal?
    """
    even_sum = 0
    even_count = 0
    odd_sum = 0
    odd_count = 0

    for idx, card in enumerate(hand):
        if idx % 2 == 0:
            even_sum += card
            even_count += 1
        else:
            odd_sum += card
            odd_count += 1

    if odd_count == 0:
        return False

    return (even_sum / even_count) == (odd_sum / odd_count)


def maybe_double_last(hand):
    """Multiply a Jack card value in the last index position by 2.

    :param hand: list - cards in hand.
    :return: list - hand with Jacks (if present) value doubled.
    """
    if not hand:
        return []
    # check if the last card is a Jack
    if hand[-1] == 11:
        # double the value of the last card
        hand[-1] *= 2
    return hand