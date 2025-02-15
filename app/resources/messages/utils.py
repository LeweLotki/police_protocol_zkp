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
    # Step 1: Choose a random nonce (r)
    r = random.randint(1, prime - 1)

    # Step 2: Compute commitment C = g^r mod p
    commitment = pow(generator, r, prime)

    # Step 3: Compute challenge c = H(commitment, public_key^r mod p, H(message))
    public_key = pow(generator, private_key, prime)  # Compute public key y = g^x mod p
    challenge = hash_value(commitment, pow(public_key, r, prime), hash_value(message))

    # Step 4: Compute response s = r + c * x mod (p-1)
    proof = (r + challenge * private_key) % (prime - 1)

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

    # ✅ Ensure proof and commitment are integers
    proof = int(proof)
    commitment = int(commitment)
    challenge = int(challenge)
    public_key = int(public_key)
    prime = int(prime)
    generator = int(generator)

    # Step 1: Compute g^s mod p
    left_side = pow(generator, proof, prime)

    # Step 2: Compute y^c * r mod p
    right_side = (pow(public_key, challenge, prime) * commitment) % prime

    # Step 3: Check if proof is valid
    return left_side == right_side

