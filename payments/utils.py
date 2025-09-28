import hmac
import hashlib
import base64

def generate_signature(payload: dict, secret_key: str, signed_fields: str) -> str:
    """
    Generate HMAC-SHA256 signature for eSewa.
    """
    signed_data = []
    for field in signed_fields.split(","):
        signed_data.append(f"{field}={payload[field]}")
    signed_string = ",".join(signed_data)

    digest = hmac.new(
        secret_key.encode("utf-8"),
        signed_string.encode("utf-8"),
        hashlib.sha256
    ).digest()

    return base64.b64encode(digest).decode("utf-8")
