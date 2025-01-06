from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SecretTag(BaseModel):
    """Model for secret tags"""
    model_config = ConfigDict(
        strict=True,
        frozen=True
    )
    
    id: str
    slug: str
    name: str
    color: Optional[str] = None

class BaseSecret(BaseModel):
    """Infisical Secret"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True
    )

    id: str
    _id: str
    workspace: str
    environment: str
    version: int
    type: str
    secret_key: str = Field(alias="secretKey")
    secret_value: str = Field(alias="secretValue")
    secret_comment: str = Field(alias="secretComment")
    secret_reminder_note: Optional[str] = Field(None, alias="secretReminderNote")
    secret_reminder_repeat_days: Optional[int] = Field(None, alias="secretReminderRepeatDays")
    skip_multiline_encoding: Optional[bool] = Field(False, alias="skipMultilineEncoding")
    metadata: Optional[Any] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

class Import(BaseModel):
    """Model for imports section"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True
    )

    secret_path: str = Field(alias="secretPath")
    environment: str
    folder_id: Optional[str] = Field(None, alias="folderId")
    secrets: List[BaseSecret]

class SecretsResponse(BaseModel):
    """Complete response model for secrets API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    secrets: List[BaseSecret]
    imports: List[Import] = Field(default_factory=list)