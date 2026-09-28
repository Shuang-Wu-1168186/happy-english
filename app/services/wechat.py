"""Server-side verification for WeChat Mini Program sign-in credentials."""

import re
import threading
from dataclasses import dataclass
from time import monotonic

import httpx


class WeChatMiniProgramError(Exception):
    """Base class for errors returned while verifying WeChat credentials."""


class WeChatCredentialError(WeChatMiniProgramError):
    """The short-lived code sent by the Mini Program is invalid or expired."""


class WeChatServiceError(WeChatMiniProgramError):
    """WeChat or this application's Mini Program configuration is unavailable."""


@dataclass(frozen=True)
class VerifiedPhoneNumber:
    """A phone number returned by WeChat and the forms used for legacy lookups."""

    canonical: str
    lookup_values: tuple[str, ...]
    normalized_lookup_values: tuple[str, ...]


def _digits(value) -> str:
    return "".join(re.findall(r"\d", str(value or "")))


def verified_phone_number(phone_info: dict) -> VerifiedPhoneNumber:
    """Convert WeChat's phone payload to E.164 without trusting client input."""
    raw = str(phone_info.get("phoneNumber") or "").strip()
    local_number = _digits(phone_info.get("purePhoneNumber"))
    country_code = _digits(phone_info.get("countryCode"))
    raw_digits = _digits(raw)

    if local_number and country_code:
        canonical = f"+{country_code}{local_number}"
    elif raw.startswith("+"):
        canonical = f"+{raw_digits}"
    else:
        raise WeChatServiceError("WeChat returned an incomplete phone number.")

    if not re.fullmatch(r"\+[1-9]\d{6,14}", canonical):
        raise WeChatServiceError("WeChat returned an invalid phone number.")

    values = []

    def add_value(value):
        value = str(value or "").strip()
        if value and value not in values:
            values.append(value)

    add_value(canonical)
    add_value(raw)
    add_value(raw_digits)
    add_value(local_number)
    add_value(canonical[1:])
    if country_code:
        add_value(f"00{canonical[1:]}")

    normalized_values = []

    def add_normalized(value):
        value = _digits(value)
        if value and value not in normalized_values:
            normalized_values.append(value)

    for value in values:
        add_normalized(value)

    return VerifiedPhoneNumber(
        canonical=canonical,
        lookup_values=tuple(values),
        normalized_lookup_values=tuple(normalized_values),
    )


class WeChatMiniProgramClient:
    """Small synchronous client for the two WeChat APIs used by phone sign-in."""

    CODE_TO_SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"
    ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    PHONE_NUMBER_URL = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"
    ACCESS_TOKEN_ERROR_CODES = {40001, 40014, 42001}
    CREDENTIAL_ERROR_CODES = {40029, 40163}

    def __init__(self, settings):
        self.app_id = settings.wechat_miniprogram_app_id.strip()
        self.app_secret = settings.wechat_miniprogram_app_secret.strip()
        self._client = httpx.Client(timeout=httpx.Timeout(settings.wechat_request_timeout_seconds))
        self._access_token = ""
        self._access_token_expires_at = 0.0
        self._access_token_lock = threading.Lock()

    def close(self):
        self._client.close()

    def exchange_login_code(self, login_code: str) -> str:
        self._require_configuration()
        payload = self._request(
            "GET",
            self.CODE_TO_SESSION_URL,
            params={
                "appid": self.app_id,
                "secret": self.app_secret,
                "js_code": login_code,
                "grant_type": "authorization_code",
            },
        )
        self._raise_for_api_error(payload)
        openid = payload.get("openid")
        if not isinstance(openid, str) or not openid:
            raise WeChatServiceError("WeChat did not return a Mini Program identity.")
        return openid

    def get_phone_number(self, phone_code: str) -> VerifiedPhoneNumber:
        self._require_configuration()
        for attempt in range(2):
            access_token = self._get_access_token()
            payload = self._request(
                "POST",
                self.PHONE_NUMBER_URL,
                params={"access_token": access_token},
                json={"code": phone_code},
            )
            error_code = self._api_error_code(payload)
            if error_code in self.ACCESS_TOKEN_ERROR_CODES and attempt == 0:
                self._invalidate_access_token(access_token)
                continue
            self._raise_for_api_error(payload)
            phone_info = payload.get("phone_info")
            if not isinstance(phone_info, dict):
                raise WeChatServiceError("WeChat did not return a phone number.")
            return verified_phone_number(phone_info)
        raise WeChatServiceError("WeChat access token could not be refreshed.")

    def _require_configuration(self):
        if not self.app_id or not self.app_secret:
            raise WeChatServiceError("WeChat Mini Program login is not configured.")

    def _get_access_token(self) -> str:
        with self._access_token_lock:
            if self._access_token and monotonic() < self._access_token_expires_at:
                return self._access_token
            payload = self._request(
                "GET",
                self.ACCESS_TOKEN_URL,
                params={
                    "grant_type": "client_credential",
                    "appid": self.app_id,
                    "secret": self.app_secret,
                },
            )
            self._raise_for_api_error(payload)
            access_token = payload.get("access_token")
            try:
                expires_in = int(payload.get("expires_in", 0))
            except (TypeError, ValueError):
                expires_in = 0
            if not isinstance(access_token, str) or not access_token or expires_in <= 0:
                raise WeChatServiceError("WeChat did not return an access token.")
            self._access_token = access_token
            self._access_token_expires_at = monotonic() + max(expires_in - 60, 1)
            return access_token

    def _invalidate_access_token(self, access_token: str):
        with self._access_token_lock:
            if self._access_token == access_token:
                self._access_token = ""
                self._access_token_expires_at = 0.0

    def _request(self, method: str, url: str, **kwargs) -> dict:
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise WeChatServiceError("Unable to reach WeChat.") from exc
        if not isinstance(payload, dict):
            raise WeChatServiceError("WeChat returned an invalid response.")
        return payload

    @staticmethod
    def _api_error_code(payload: dict) -> int:
        try:
            return int(payload.get("errcode", 0))
        except (TypeError, ValueError):
            return -1

    def _raise_for_api_error(self, payload: dict):
        error_code = self._api_error_code(payload)
        if not error_code:
            return
        if error_code in self.CREDENTIAL_ERROR_CODES:
            raise WeChatCredentialError("The WeChat code is invalid or expired.")
        raise WeChatServiceError("WeChat rejected the request.")
