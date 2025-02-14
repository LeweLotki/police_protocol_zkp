from pydantic import BaseModel, Field
import uuid

class SendMessageRequest(BaseModel):
    """Schema for sending an encrypted message."""
    server_id: str = Field(..., example=str(uuid.uuid4()))
    message: str = Field(..., example="EncryptedMessageHere")

class SendMessageResponse(BaseModel):
    """Schema for response after sending a message."""
    message: str = "Message sent successfully"

class VerifyMessageRequest(BaseModel):
    """Schema for verifying a Schnorr proof for a message."""
    server_id: str
    message: str

class VerifyMessageResponse(BaseModel):
    """Schema for response after message verification."""
    message: str

