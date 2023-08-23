from passlib.context import CryptContext

_pwd_context = CryptContext(
    schemes=[
        "bcrypt",
    ],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """Generate a hash of the passed password.

    Args:
        password (str): The plain password.

    Returns:
        str: A hashed pasword.
    """

    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """

    return _pwd_context.verify(plain_password, hashed_password)
