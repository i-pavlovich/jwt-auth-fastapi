from typing import Any

from config import settings


def get_refresh_token_settings(
    refresh_token: str, expired: bool = False
) -> dict[str, Any]:
    """Get the settings for a refresh token coockie.

    Args:
        refresh_token (str): The refresh token value.
        expired (bool, optional): Indicates whether the refresh token has expired. Defaults to False.

    Returns:
        dict[str, Any]: A settings for the refresh token coockie.
    """

    cookie_settings = {
        "key": "refresh_token",
        "httponly": True,
        "secure": True,
    }

    if not expired:
        cookie_settings.update(
            {
                "value": refresh_token,
                "max_age": settings.REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
            }
        )

    return cookie_settings
