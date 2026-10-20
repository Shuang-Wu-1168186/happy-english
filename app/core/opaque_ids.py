"""Authenticated opaque identifiers for the public HTTP boundary.

Database primary keys stay integers inside the application. The API exposes
only AES-SIV-encrypted, URL-safe tokens so a client cannot infer or enumerate
database identifiers. AES-SIV keeps the same ID stable across responses, which
lets clients compare and reuse an identifier without ever seeing its integer.
Tokens deliberately have no expiry because they are used in bookmarks and
long-lived learner progress records.
"""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESSIV


OPAQUE_ID_PREFIX = "hei1_"


class OpaqueIdError(ValueError):
    """Raised when an external identifier is malformed or has been tampered with."""


def _aessiv_key(secret: str) -> bytes:
    if not secret:
        raise ValueError("External identifier secret must not be empty.")
    return hashlib.sha512(f"happyenglish-external-id-v1:{secret}".encode()).digest()


@dataclass(frozen=True)
class OpaqueIdCodec:
    """Encrypt and authenticate positive database IDs without exposing their value."""

    secret: str
    previous_secrets: tuple[str, ...] = ()
    _ciphers: tuple[AESSIV, ...] = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "_ciphers",
            tuple(AESSIV(_aessiv_key(secret)) for secret in (self.secret, *self.previous_secrets)),
        )

    @staticmethod
    def is_token(value: object) -> bool:
        return isinstance(value, str) and value.startswith(OPAQUE_ID_PREFIX)

    def encode(self, identifier: int) -> str:
        if isinstance(identifier, bool) or not isinstance(identifier, int) or identifier <= 0:
            raise ValueError("Only positive integer database identifiers can be encoded.")
        encrypted = self._ciphers[0].encrypt(
            f"v1:{identifier}".encode(), [b"happyenglish:external-id:v1"]
        )
        return OPAQUE_ID_PREFIX + base64.urlsafe_b64encode(encrypted).decode().rstrip("=")

    def decode(self, value: object) -> int:
        if not self.is_token(value):
            raise OpaqueIdError("Identifier must be an opaque token.")
        token = value[len(OPAQUE_ID_PREFIX) :]
        padded = token + "=" * (-len(token) % 4)
        try:
            encrypted = base64.urlsafe_b64decode(padded.encode())
        except (ValueError, UnicodeEncodeError) as error:
            raise OpaqueIdError("Identifier is invalid or has been tampered with.") from error
        for cipher in self._ciphers:
            try:
                payload = cipher.decrypt(encrypted, [b"happyenglish:external-id:v1"]).decode()
            except (InvalidTag, UnicodeDecodeError):
                continue
            version, separator, raw_identifier = payload.partition(":")
            if version != "v1" or separator != ":" or not raw_identifier.isdecimal():
                continue
            identifier = int(raw_identifier)
            if identifier > 0:
                return identifier
        raise OpaqueIdError("Identifier is invalid or has been tampered with.")


def codec_from_settings(settings) -> OpaqueIdCodec:
    """Build the current codec and accept configured historical keys for rotation."""

    secret = settings.external_id_secret or settings.secret_key
    return OpaqueIdCodec(secret, tuple(settings.external_id_previous_secrets))
