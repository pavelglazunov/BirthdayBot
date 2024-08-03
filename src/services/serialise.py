def username(telegram_username: str) -> str:
    return "@" + telegram_username.replace("@", "")
