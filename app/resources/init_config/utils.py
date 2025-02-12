from sympy import isprime, primitive_root

def is_prime(n: int) -> bool:
    """Check if a number is a prime using sympy's isprime function."""
    return isprime(n)

def is_valid_generator(generator: int, prime: int) -> bool:
    """
    Check if a number is a valid generator for the given prime.

    A valid generator g should be a primitive root modulo prime.
    """
    if not is_prime(prime):
        return False

    try:
        return generator in {primitive_root(prime)}
    except ValueError:
        return False 

