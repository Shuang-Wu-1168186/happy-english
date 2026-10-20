# Public opaque identifiers

Database IDs remain positive integers inside Python services and DAOs. Every
JSON API response exposes an authenticated opaque identifier instead:

```
hei1_<url-safe AES-SIV ciphertext>
```

The route boundary performs both directions of the conversion. It encrypts
fields named `id`, `*_id`, `*_ids`, `ids`, and the explicit audit-user fields
in JSON responses. Before FastAPI validates a request, the same route boundary
decrypts matching path parameters, query parameters, and JSON request fields.
Service and DAO interfaces therefore continue receiving integer IDs.

Internal UI deep links are covered as well. For example, a stored
`/learning-materials/1` link is returned as
`/learning-materials/hei1_...`; when an administrator saves that link back,
the boundary validates and restores its internal ID. Raw numeric IDs in those
supported links are rejected.

The token payload uses deterministic AES-SIV with a domain-separated key. A
given database ID has a stable token, which preserves React keys, URLs, saved
links, and equality checks. AES-SIV authentication rejects altered tokens;
plain numeric IDs are deliberately rejected with HTTP 422 at the API boundary.
The tokens hide values and prevent ID enumeration. Authorization remains the
responsibility of each endpoint and service.

## Client contract

Treat every ID received from the API as an opaque string. Web and Android
clients must retain the exact token in routes, request bodies, query strings,
state, and local storage; they must not use `Number`, `parseInt`, or any other
numeric conversion. New client integrations should model database references
as strings from the start.

## Configuration and rotation

`EXTERNAL_ID_SECRET` is optional. When absent, the application derives an
independent identifier-encryption key from `SECRET_KEY`, so existing secure
deployments work without a migration. Set a dedicated high-entropy
`EXTERNAL_ID_SECRET` when identifier-token rotation must be independent of
session signing.

During a key rotation, configure the new secret as `EXTERNAL_ID_SECRET` and
place the retiring secret in `EXTERNAL_ID_PREVIOUS_SECRETS`. Pydantic parses
that setting as a JSON string list, for example:

```env
EXTERNAL_ID_PREVIOUS_SECRETS=["retiring-secret"]
```

Keep retiring secrets until all issued URLs and persisted browser state using
their tokens have aged out. Never add a raw-integer fallback: it would restore
the enumeration surface this boundary removes.
