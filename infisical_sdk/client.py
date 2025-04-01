from .infisical_requests import InfisicalRequests

from infisical_sdk.resources import Auth
from infisical_sdk.resources import V3RawSecrets
from infisical_sdk.resources import KMS

from infisical_sdk.util import SecretsCache

class InfisicalSDKClient:
    def __init__(self, host: str, token: str = None, cache_ttl: int | None = 300):
        self.host = host
        self.access_token = token

        self.api = InfisicalRequests(host=host, token=token)
        self.cache = SecretsCache(cache_ttl)
        self.auth = Auth(self.api, self.set_token)
        self.secrets = V3RawSecrets(self.api, self.cache)
        self.kms = KMS(self.api)

    def set_token(self, token: str):
        """
        Set the access token for future requests.
        """
        self.api.set_token(token)
        self.access_token = token

    def get_token(self):
        """
        Set the access token for future requests.
        """
        return self.access_token

