"""Project-specific exceptions for ft_otp."""


class FtOtpError(Exception):
    """Base error for user-facing failures."""


class ValidationError(FtOtpError):
    """Raised when input data is invalid."""


class StorageError(FtOtpError):
    """Raised when key storage cannot be used safely."""
