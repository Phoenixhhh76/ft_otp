"""Key storage helpers backed by OpenSSL encryption."""

from __future__ import annotations

import getpass
import os
from pathlib import Path
import subprocess

from errors import StorageError


DEFAULT_KEY_FILE = "ft_otp.key"
OPENSSL_ALGORITHM = "aes-256-cbc"
PASSWORD_ENV_NAME = "FT_OTP_PASSWORD"


def _prompt_password(confirm: bool = False) -> str:
    """Read an encryption password without echoing it on screen."""

    prompt = "Choose a password to protect ft_otp.key: " if confirm else "Enter the password for ft_otp.key: "
    password = getpass.getpass(prompt)
    if not password:
        raise StorageError("password cannot be empty.")

    if confirm:
        confirmation = getpass.getpass("Confirm the password: ")
        if password != confirmation:
            raise StorageError("passwords do not match.")

    return password


def _run_openssl(payload: bytes, password: str, decrypt: bool = False) -> bytes:
    """Encrypt or decrypt bytes using OpenSSL with PBKDF2-derived keys."""

    command = [
        "openssl",
        "enc",
        f"-{OPENSSL_ALGORITHM}",
        "-pbkdf2",
        "-salt",
        "-pass",
        f"env:{PASSWORD_ENV_NAME}",
    ]
    if decrypt:
        command.insert(2, "-d")

    env = os.environ.copy()
    env[PASSWORD_ENV_NAME] = password

    try:
        completed = subprocess.run(
            command,
            input=payload,
            capture_output=True,
            check=False,
            env=env,
        )
    except FileNotFoundError as exc:
        raise StorageError("openssl is required to encrypt and decrypt the key file.") from exc

    if completed.returncode != 0:
        action = "decrypt" if decrypt else "encrypt"
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        if decrypt:
            raise StorageError("could not decrypt the key file. Check the password and file contents.") from None
        raise StorageError(f"could not {action} the key file: {detail or 'openssl failed.'}") from None

    return completed.stdout


def save_encrypted_key(secret: bytes, output_path: str = DEFAULT_KEY_FILE) -> None:
    """Save the secret to an encrypted file."""

    if not secret:
        raise StorageError("secret cannot be empty.")

    password = _prompt_password(confirm=True)
    encrypted_secret = _run_openssl(secret, password=password, decrypt=False)
    output_file = Path(output_path)

    try:
        output_file.write_bytes(encrypted_secret)
        output_file.chmod(0o600)
    except OSError as exc:
        raise StorageError(f"could not write encrypted key file: {output_path}") from exc


def load_encrypted_key(input_path: str) -> bytes:
    """Load and decrypt the saved key file."""

    input_file = Path(input_path)
    if not input_file.exists():
        raise StorageError(f"key file not found: {input_path}")

    try:
        encrypted_secret = input_file.read_bytes()
    except OSError as exc:
        raise StorageError(f"could not read key file: {input_path}") from exc

    if not encrypted_secret:
        raise StorageError("key file is empty.")

    password = _prompt_password(confirm=False)
    return _run_openssl(encrypted_secret, password=password, decrypt=True)
