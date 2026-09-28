import json
from types import SimpleNamespace

import httpx

from app.services.wechat import WeChatMiniProgramClient


def test_wechat_client_exchanges_both_codes_and_caches_access_token():
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path == "/sns/jscode2session":
            assert request.url.params["appid"] == "wx-test-app"
            assert request.url.params["secret"] == "test-mini-program-secret"
            assert request.url.params["js_code"] == "login-code"
            return httpx.Response(200, json={"openid": "openid-1"}, request=request)
        if request.url.path == "/cgi-bin/token":
            assert request.url.params["grant_type"] == "client_credential"
            return httpx.Response(
                200,
                json={"access_token": "access-token", "expires_in": 7200},
                request=request,
            )
        if request.url.path == "/wxa/business/getuserphonenumber":
            assert request.method == "POST"
            assert request.url.params["access_token"] == "access-token"
            assert json.loads(request.content) in ({"code": "phone-code"}, {"code": "next-phone-code"})
            return httpx.Response(
                200,
                json={
                    "errcode": 0,
                    "phone_info": {
                        "phoneNumber": "+8613800138000",
                        "purePhoneNumber": "13800138000",
                        "countryCode": "86",
                    },
                },
                request=request,
            )
        raise AssertionError(f"Unexpected WeChat request: {request.url}")

    settings = SimpleNamespace(
        wechat_miniprogram_app_id="wx-test-app",
        wechat_miniprogram_app_secret="test-mini-program-secret",
        wechat_request_timeout_seconds=10,
    )
    client = WeChatMiniProgramClient(settings)
    client.close()
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    try:
        assert client.exchange_login_code("login-code") == "openid-1"
        assert client.get_phone_number("phone-code").canonical == "+8613800138000"
        assert client.get_phone_number("next-phone-code").canonical == "+8613800138000"
    finally:
        client.close()

    assert [request.url.path for request in requests] == [
        "/sns/jscode2session",
        "/cgi-bin/token",
        "/wxa/business/getuserphonenumber",
        "/wxa/business/getuserphonenumber",
    ]
