"""Auth adapters for IAM or Entra."""
from typing import Optional


AUTH_MODE = "{{ cookiecutter.auth }}"  # iam | entra


def verify_request(auth_header: Optional[str]) -> bool:
    """Very thin placeholder verifier.

    - iam: accept when header is present (simulates IAM authorizer)
    - entra: accept when header starts with "Bearer " (simulates JWT)
    - none: always allow
    """
    mode = AUTH_MODE
    if mode == "iam":
        return bool(auth_header)
    if mode == "entra":
        return bool(auth_header and auth_header.lower().startswith("bearer "))
    return True

