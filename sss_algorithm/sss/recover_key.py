"""
This code will recover secret from shares
"""

from typing import Generator
from .constants import DEFAULT_PRIME

def _extended_gcd(a: int, n: int) -> tuple[int, int]:
    """
    This will calculate "Modular multiplicative inverse" by extended Euclidean algorithm
    check https://zh.wikipedia.org/wiki/%E6%A8%A1%E5%8F%8D%E5%85%83%E7%B4%A0 for more information

    When a*x + n*y = 1, x is the modular multiplicative inverse of a will be x
    """

    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while n != 0:
        quot = a // n
        a, n = n, a % n
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y

    # last_x is the modular multiplicative inverse of a
    return last_x, last_y

def _divmod(num: int, den: int, prime: int) -> int:
    """Compute num / den mod prime

    this will make sure the following equation hold:
    den * _divmod(num, den, prime) % prime == num

    what we want is to help lagrange interpolation of:
        (num/den) mod prime
    be easily calculated with "Modular multiplicative inverse" of den
    """
    inv, _ = _extended_gcd(den, prime)
    return num * inv

def _lagrange_interpolation(x: int, x_shares: list[int], y_shares: list[int], prime: int) -> int:
    """
    This function will calculate lagrange interpolation for x
    """

    len_of_shares = len(x_shares)
    assert len_of_shares == len(set(x_shares)), "x_shares must be unique"

    def PI(vals:Generator[int, None, None] | list[int]) -> int :
        """
        upper-case PI -- product of inputs
        """
        accumulate = 1
        for v in vals:
            accumulate *= v
        return accumulate

    nums:list[int] = []  # avoid inexact division, nums is the product of (x - x_j) for all j != i
    dens: list[int] = []  # dens is the product of (x_i - x_j) for all j != i
    for i in range(len_of_shares):
        others = list(x_shares)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))

    den = PI(dens) # product of all dens, 可以當作是每個差值為了一起計算，分母進行的通分

    # nums[i] * den * y_shares[i] % prime 是 lagrange 需要 sum(y * (x - x_1) * ... * (x - x_n) / (x_i - x_1) * ... * (x_i - x_n))
    # 所以 nums[i]代表在 i 的 分子的乘積, den代表通分, y 代表 shares_i的被mod prime的y值
    # 把nums[i] * den * y_shares[i] % prime 和 dens[i] 代入_divmod, 就是相當於 進行模數除法運算, 並且把結果加總
    num = sum([_divmod(nums[i] * den * y_shares[i] % prime, dens[i], prime)
               for i in range(len_of_shares)])

    return (_divmod(num, den, prime) + prime) % prime # make sure the value is in range of prime

def recover_secret(shares: list[tuple[int, int]], prime: int = DEFAULT_PRIME) -> int:
    """
    :param shares: list of shares
    :param prime: prime number to mod polynomial
    """
    x_shares, y_shares = zip(*shares)
    return _lagrange_interpolation(0, x_shares, y_shares, prime)
