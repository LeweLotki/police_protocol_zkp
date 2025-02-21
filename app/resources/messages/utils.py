import hashlib
import random

def hash_value(*args) -> int:
    """
    Computes a cryptographic hash of the given values using SHA-256.
    Converts the hash to an integer.
    """
    combined = "".join(str(arg) for arg in args)
    return int(hashlib.sha256(combined.encode()).hexdigest(), 16)

def generate_schnorr_proof(message: str, private_key: int, prime: int, generator: int) -> tuple:
    """
    Generates a Schnorr proof for a given message.

    :param message: The message being sent.
    :param private_key: The sender's private key.
    :param prime: The prime modulus.
    :param generator: The generator.
    :return: (commitment, proof, challenge)
    """
    q = (prime - 1) // 2  # Approximate order of the subgroup

    r = random.randint(1, q - 1)  # Random nonce

    # Compute commitment C = g^r mod p
    commitment = pow(generator, r, prime)

    # Compute challenge c = H(commitment, public_key, H(message))
    public_key = pow(generator, private_key, prime)
    challenge = hash_value(commitment, public_key, hash_value(message)) % q

    # Compute response s = r + c * x mod q
    proof = (r + challenge * private_key) % q  # ✅ Fix: use q instead of prime

    return commitment, proof, challenge

def verify_schnorr_proof(
    message: str,
    commitment: int,
    proof: int,
    challenge: int,
    public_key: int,
    prime: int,
    generator: int
) -> bool:
    """
    Verifies a Schnorr proof.
    """
    q = (prime - 1) // 2  # Approximate order of the subgroup

    # Convert inputs to integers
    proof = int(proof)
    commitment = int(commitment)
    challenge = int(challenge)
    public_key = int(public_key)
    prime = int(prime)
    generator = int(generator)

    # Compute left-side: g^s mod p
    left_side = pow(generator, proof, prime)

    # Compute right-side: y^c * r mod p
    right_side = (pow(public_key, challenge, prime) * commitment) % prime

    print(f"Computed left-side: {left_side}")
    print(f"Expected right-side: {right_side}")
    print(f"Verification result: {left_side == right_side}")

    return left_side == right_side

