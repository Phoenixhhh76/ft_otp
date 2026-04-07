# `storage.py` Notes

## What this file does

`storage.py` is responsible for one thing: securely storing and loading the OTP secret key.

- `save_encrypted_key(secret, output_path)`: encrypts and writes the key to disk
- `load_encrypted_key(input_path)`: reads and decrypts the key from disk

Instead of implementing AES manually, it calls the system `openssl` command.

## Internal helpers

- `_prompt_password()`: securely asks for a password (no echo)
- `_run_openssl()`: executes `openssl enc` for encryption/decryption

## Important constants

```python
DEFAULT_KEY_FILE = "ft_otp.key"
OPENSSL_ALGORITHM = "aes-256-cbc"
PASSWORD_ENV_NAME = "FT_OTP_PASSWORD"
```

These define the default output file, algorithm, and password environment variable.

## OpenSSL command behavior

Encryption:

```bash
openssl enc -aes-256-cbc -pbkdf2 -salt -pass env:FT_OTP_PASSWORD
```

Decryption:

```bash
openssl enc -d -aes-256-cbc -pbkdf2 -salt -pass env:FT_OTP_PASSWORD
```

Key options:
- `-pbkdf2`: stronger password-based key derivation
- `-salt`: prevents deterministic output for same input
- `-pass env:...`: avoids exposing password directly in arguments

## Save flow

1. validate non-empty secret
2. prompt password twice for confirmation
3. encrypt secret through OpenSSL
4. write encrypted content and set file mode to `600`

`chmod 600` means only the owner can read/write the key file.

## Load flow

1. verify file exists
2. read encrypted bytes
3. reject empty file
4. prompt password
5. decrypt through OpenSSL
6. return raw secret bytes

## Design summary

`storage.py` focuses on practical key protection:
- no plaintext key storage
- password-protected encrypted file
- mature crypto implementation delegated to OpenSSL
- strict file permissions
- explicit error handling