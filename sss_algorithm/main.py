"""
Main logic
"""
from sss_algorithm.sss.constants import DEFAULT_PRIME
from sss_algorithm.sss.generate_share import make_random_share
from sss_algorithm.sss.recover_key import recover_secret
def start():
    """
    Start
    """
    _secret = 1234
    shares = make_random_share(_secret, 3, 5, DEFAULT_PRIME)

    print(f"Secret: {_secret}")
    print('Shares:')
    if shares:
        for share in shares:
            print('  ', f"key: (x: {share[0]}, y: {share[1]})")
    
    recovered_secret = recover_secret(shares)
    print(f"Recovered secret: {recovered_secret}")