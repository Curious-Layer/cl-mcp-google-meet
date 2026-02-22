from typing import TypedDict


class OAuthTokenData(TypedDict, total=False):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]
