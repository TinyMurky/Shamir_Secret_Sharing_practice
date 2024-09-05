"""
This file will create a polynomial,
sample "k" point from it,
and get (y mod prime) from that polynomial
"""

import random

from .constants import DEFAULT_PRIME


def _eval_at(polynomial_coefficients: list[int], x, prime) -> int:
    """
    This function use iterated method to calculate "f(x) mod prime"
    mod will be calculate inside every step not after f(x) is calculated
    """

    accumulate: int = 0

    for coefficient in reversed(
        polynomial_coefficients
    ):  # reverse make sure it calculate from a_n to a_0
        accumulate *= x
        accumulate += coefficient
        accumulate %= prime
    return accumulate


def make_random_share(
    secret: int, threshold_of_key: int, shares_of_key: int, prime: int = DEFAULT_PRIME
) -> list[tuple[int, int]]:
    """
    :param secret: secret to divided into shares
    :param threshold_of_key: minimum number of shares needed to reconstruct the secret
    :param shares_of_key: number of shares to generate
    :param prime: prime number to mod polynomial
    """

    if threshold_of_key > shares_of_key:
        raise ValueError("Threshold of key must be less than or equal to shares of key")

    # Secret is the first coefficient of the polynomial
    # other coefficients are random between 0 and prime - 1
    # the max degree of polynomial is threshold_of_key - 1,
    # because we already have secret be our first coefficient
    polynomial_coefficients = [secret] + [
        random.SystemRandom().randint(0, prime - 1) for _ in range(threshold_of_key - 1)
    ]

    # x is 1 to shares_of_key + 1, y use _eval_at to calculate f(x) mod prime
    points = [
        (x, _eval_at(polynomial_coefficients, x, prime))
        for x in range(1, shares_of_key + 1)
    ]
    return points
