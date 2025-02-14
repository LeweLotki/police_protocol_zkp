def generate_schnorr_proof(message: str) -> str:
    """Mocks Schnorr proof generation for a given message."""
    return f"MOCK_PROOF_{hash(message)}"

def verify_schnorr_proof(message: str, proof: str) -> bool:
    """Mocks Schnorr proof verification."""
    expected_proof = generate_schnorr_proof(message)
    return proof == expected_proof

