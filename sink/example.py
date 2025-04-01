from infisical_sdk import InfisicalSDKClient, SymmetricEncryption

import random
import base64
import string

sdkInstance = InfisicalSDKClient(host="http://localhost:8080")

MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_ID = "<client-id>"
MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_SECRET = "<client-secret>"

sdkInstance.auth.universal_auth.login(MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_ID, MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_SECRET)

SECRETS_PROJECT_ID = "8770e386-6392-4bfa-a377-a1e2d981668a"
SECRETS_ENVIRONMENT_SLUG = "staging"
KMS_PROJECT_ID = "c54edf7a-f861-4131-afdc-b0ad5faec5dc"


def random_string(length: int = 10) -> str:
    # Use only lowercase letters, numbers, and hyphens
    allowed_chars = string.ascii_lowercase + string.digits + '-'
    return ''.join(random.choices(allowed_chars, k=length))




################################################# SECRET TESTS #################################################

new_secret = sdkInstance.secrets.create_secret_by_name(
    secret_name=f"TEST_{random_string()}",
    project_id=SECRETS_PROJECT_ID,
    secret_path="/",
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_value=f"secret_value_{random_string()}",
    secret_comment=f"Optional comment_{random_string()}",
    skip_multiline_encoding=False,
    secret_reminder_repeat_days=30,  # Optional
    secret_reminder_note=f"Remember to update this secret_{random_string()}"  # Optional
)

print(f"Created secret: [key={new_secret.secretKey}] | [value={new_secret.secretValue}]")

updated_secret = sdkInstance.secrets.update_secret_by_name(
    current_secret_name=new_secret.secretKey,
    project_id=SECRETS_PROJECT_ID,
    secret_path="/",
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_value=f"new_secret_value_{random_string()}",
    secret_comment=f"Updated comment_{random_string()}",  # Optional
    skip_multiline_encoding=False,
    secret_reminder_repeat_days=10,  # Optional
    secret_reminder_note=f"Updated reminder note_{random_string()}",  # Optional
    new_secret_name=f"NEW_NAME_{random_string()}"  # Optional
)

print(f"Updated secret: [key={updated_secret.secretKey}] | [value={updated_secret.secretValue}]")
secret = sdkInstance.secrets.get_secret_by_name(
    secret_name=updated_secret.secretKey,
    project_id=SECRETS_PROJECT_ID,
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_path="/",
    expand_secret_references=True,
    include_imports=True,
    version=None  # Optional
)

print(f"Retrieved secret: [key={secret.secretKey}] | [value={secret.secretValue}]")


all_secrets = sdkInstance.secrets.list_secrets(
    project_id=SECRETS_PROJECT_ID,
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_path="/",
    expand_secret_references=True,
    include_imports=True
)

if len(all_secrets.secrets) != 1:
    raise Exception("Expected 1 secret, got {}".format(len(all_secrets.secrets)))


# Print all secret keys
for idx, secret in enumerate(all_secrets.secrets):
    print(f"Listed secrets key {idx}: [{secret.secretKey}] | [value={secret.secretValue}]")

deleted_secret = sdkInstance.secrets.delete_secret_by_name(
    secret_name=updated_secret.secretKey,
    project_id=SECRETS_PROJECT_ID,
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_path="/"
)

print(f"Deleted secret: [key={deleted_secret.secretKey}] | [value={deleted_secret.secretValue}]")

################################################# KMS TESTS #################################################

kms_key = sdkInstance.kms.create_key(
    name=f"test-key-{random_string()}",
    project_id=KMS_PROJECT_ID,
    encryption_algorithm=SymmetricEncryption.AES_GCM_256,
    description=f"Optional description_{random_string()}"
)

print(f"Created KMS key: [key={kms_key.id}] | [name={kms_key.name}]")


plantext = "Hello, world!"

encrypted = sdkInstance.kms.encrypt_data(
    key_id=kms_key.id,
    base64EncodedPlaintext=base64.b64encode(plantext.encode()).decode()
)

print(f"Encrypted: {encrypted}")

decrypted = sdkInstance.kms.decrypt_data(
    key_id=kms_key.id,
    ciphertext=encrypted
)

print(f"Decrypted: {base64.b64decode(decrypted.encode()).decode()}")

key_by_id = sdkInstance.kms.get_key_by_id(
    key_id=kms_key.id
)

print(f"Key by ID: {key_by_id}")

key_by_name = sdkInstance.kms.get_key_by_name(
    key_name=kms_key.name,
    project_id=KMS_PROJECT_ID
)

print(f"Key by Name: {key_by_name}")

list_keys = sdkInstance.kms.list_keys(
    project_id=KMS_PROJECT_ID
)

print(f"List keys: {list_keys}")


deleted_key = sdkInstance.kms.delete_key(
    key_id=kms_key.id
)

print(f"Deleted key: {deleted_key}")