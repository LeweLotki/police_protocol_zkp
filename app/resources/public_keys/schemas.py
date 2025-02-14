from pydantic import BaseModel, Field
import uuid

class PublicKeyCreate(BaseModel):
    """Schema for sending a public key."""
    server_id: str = Field(default_factory=lambda: str(uuid.uuid4()), example=str(uuid.uuid4()))
    public_key: int = Field(..., example=10)

class PublicKeyResponse(BaseModel):
    """Schema for retrieving a stored public key."""
    server_id: str
    public_key: int

class PublicKeyCalculationRequest(BaseModel):
    """Schema for calculating public key from private key."""
    prime: int = Field(..., example=23)
    generator: int = Field(..., example=5)

class PublicKeyCalculationResponse(BaseModel):
    """Schema for returning the calculated public key and private key (for testing)."""
    public_key: int
    private_key: int  # This should not be stored in the database

