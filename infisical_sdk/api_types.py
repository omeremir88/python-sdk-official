from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class ApprovalStatus(str, Enum):
    """Enum for approval status"""
    OPEN = "open"
    APPROVED = "approved"
    REJECTED = "rejected"


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
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


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


class ListSecretsResponse(BaseModel):
    """Complete response model for secrets API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    secrets: List[BaseSecret]
    imports: List[Import] = Field(default_factory=list)


class CreateSecretResponse(BaseModel):
    """Response model for create secret API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    secret: BaseSecret


class UpdateSecretResponse(BaseModel):
    """Response model for update secret API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    secret: BaseSecret


class DeleteSecretResponse(BaseModel):
    """Response model for delete secret API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    secret: BaseSecret


class MachineIdentityLoginResponse(BaseModel):
    """Response model for machine identity login API"""
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
    )

    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    access_token_max_ttl: int = Field(alias="accessTokenMaxTTL")
    token_type: str = Field(alias="tokenType")
