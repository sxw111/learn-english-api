def http_400_username_details(username: str) -> str:
    return f"User with username `{username}` arleady exist!"


def http_400_email_details(email: str) -> str:
    return f"User with email `{email}` arleady exist!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed!"


def http_404_id_details(id: int) -> str:
    return f"User with id `{id}` does not exist!"
