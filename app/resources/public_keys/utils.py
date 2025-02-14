import random
from sympy import isprime

def generate_private_key(prime: int) -> int:
    """Generate a private key that is a random number between 2 and prime-2."""
    if not isprime(prime):
        raise ValueError("Prime number is not valid")
    return random.randint(2, prime - 2)

def compute_public_key(generator: int, private_key: int, prime: int) -> int:
    """Compute the public key using modular exponentiation: g^x mod p."""
    return pow(generator, private_key, prime)

