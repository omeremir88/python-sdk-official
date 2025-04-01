from infisical_sdk import InfisicalSDKClient

import time

SECRETS_PROJECT_ID = "8770e386-6392-4bfa-a377-a1e2d981668a"
SECRETS_ENVIRONMENT_SLUG = "dev"

MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_ID = "<client-id>"
MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_SECRET = "<client-secret>"
SITE_URL = "http://localhost:8080"

cache_enabled_client = InfisicalSDKClient(host=SITE_URL, cache_ttl=10)
cache_enabled_client.auth.universal_auth.login(MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_ID, MACHINE_IDENTITY_UNIVERSAL_AUTH_CLIENT_SECRET)



single_secret_cached = cache_enabled_client.secrets.get_secret_by_name(
    secret_name="TEST",
    project_id=SECRETS_PROJECT_ID,
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_path="/",
    expand_secret_references=True,
    include_imports=True)


time_start_cache_enabled = time.time()
# Running in loop 10 times or the time is so small that python messes up the print (which is a great sign for us!)
for i in range(10):
  single_secret_cached = cache_enabled_client.secrets.get_secret_by_name(
      secret_name="TEST",
      project_id=SECRETS_PROJECT_ID,
      environment_slug=SECRETS_ENVIRONMENT_SLUG,
      secret_path="/",
      expand_secret_references=True,
      include_imports=True)
time_end_cache_enabled = time.time()
print(f"[CACHE ENABLED] Time taken: {time_end_cache_enabled - time_start_cache_enabled} seconds")


print("Sleeping for 10 seconds")
time.sleep(10)


print("Getting secret again")
time_start_cache_enabled = time.time()
single_secret_cached = cache_enabled_client.secrets.get_secret_by_name(
    secret_name="TEST",
    project_id=SECRETS_PROJECT_ID,
    environment_slug=SECRETS_ENVIRONMENT_SLUG,
    secret_path="/",
    expand_secret_references=True,
    include_imports=True)
time_end_cache_enabled = time.time()
print(f"[CACHE EXPIRED] Time taken: {time_end_cache_enabled - time_start_cache_enabled} seconds")



