# Production API security baseline

The public API uses encrypted identifiers, signed sessions, CSRF protection,
role checks, and a reverse proxy. The production baseline adds transport,
host, rate, and session-revocation controls.

## Required environment values

Set these in the production `.env` without committing the file:

```dotenv
APP_ENV=production
COOKIE_SECURE=true
CORS_ORIGINS=["https://happylingo.cn","https://www.happylingo.cn"]
TRUSTED_HOSTS=["happylingo.cn","www.happylingo.cn","api.happylingo.cn","127.0.0.1","localhost"]
API_DOCS_ENABLED=false
APP_SESSION_SECONDS=604800
```

Android requests identify themselves with `HappyLingo-Android/`; their signed
session is valid for seven days. Browser sessions continue to use
`SESSION_SECONDS` (12 hours by default).

Use a dedicated `EXTERNAL_ID_SECRET` in production. Keep the previous key in
`EXTERNAL_ID_PREVIOUS_SECRETS` during a rotation so active opaque identifiers
continue to decode.

## Server files

Install the files in `deploy/nginx` as follows:

| Repository file | Server target |
| --- | --- |
| `00_happy_english_security.conf` | `/etc/nginx/conf.d/00_happy_english_security.conf` |
| `happy_english_security_headers.conf` | `/etc/nginx/snippets/happy_english_security_headers.conf` |
| `happy_english_api_proxy.conf` | `/etc/nginx/snippets/happy_english_api_proxy.conf` |
| `happy_english.conf` | `/etc/nginx/conf.d/happy_english.conf` |
| `deploy/systemd/happy_english.service` | `/etc/systemd/system/happy_english.service` |

Test Nginx with `nginx -t` before reloading it. The systemd unit binds
Uvicorn to `127.0.0.1`; only Nginx should accept public API traffic.
The Nginx snippets also keep request bodies out of access logs, enforce the
HTTPS security headers, and rate-limit authentication, upload, and audio
generation endpoints.

## Session revocation migration

Run `sql/20261020_add_user_session_version.sql` before restarting the new
backend. It adds a server-side session version for each account. Logging out
or changing a password then invalidates copied cookies and mobile session
headers immediately. Existing sessions are intentionally invalidated during
this rollout and users must sign in once again.
