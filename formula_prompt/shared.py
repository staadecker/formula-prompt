MAX_ENTRY_ATTEMPTS = 3


class UserInputError(Exception):
    """Custom error type raised when the user repeatedly enters invalid values."""
    pass
