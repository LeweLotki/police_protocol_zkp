from pydantic import BaseModel, Field
from typing import Optional


class InitConfigCreate(BaseModel):
    """Schema for creating a new initial configuration (prime & generator)."""
    
    prime: int = Field(..., example=23, description="A large prime number used for ZKP.")
    generator: int = Field(..., example=5, description="A generator corresponding to the prime.")

    class Config:
        json_schema_extra = {
            "example": {
                "prime": 23,
                "generator": 5
            }
        }


class InitConfigResponse(BaseModel):
    """Schema for responding with the stored initial configuration."""
    
    prime: int
    generator: int
    message: Optional[str] = "Prime and generator set successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "prime": 23,
                "generator": 5,
                "message": "Prime and generator set successfully"
            }
        }

