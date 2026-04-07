# ft_otp

`ft_otp` is a Python command-line implementation of a time-based one-time password generator built for the 42 Piscine Cybersecurity D2 project.

This public version keeps the core implementation and technical notes while removing sensitive key material. The project stores a hexadecimal secret in encrypted form and generates 6-digit OTPs using HOTP-based logic with a time-derived counter, following the RFC 4226 / RFC 6238 model required by the subject.

## Highlights

- Python CLI executable named `ft_otp`, matching the project specification
- secure key-file handling with OpenSSL-based encryption
- manual HOTP/TOTP core implementation instead of relying on a ready-made TOTP library
- input validation for hex key format and file handling
- verification workflow using `oathtool` and RFC 6238 reference vectors

## Tech Stack

- `Python 3`
- `OpenSSL`
- `argparse`, `hmac`, `hashlib`, and standard library file handling

## How It Works

The project exposes two CLI flows:

- `-g`: reads a key file containing at least 64 hexadecimal characters, validates it, and stores it as encrypted `ft_otp.key`
- `-k`: loads the encrypted key file, decrypts it, computes the current TOTP, and prints a 6-digit OTP

The implementation follows this logic:

1. convert current Unix time into a moving counter
2. apply HOTP with `HMAC-SHA1(secret, counter)`
3. use RFC 4226 dynamic truncation
4. format the result as a fixed 6-digit OTP

This is why the subject can require HOTP core logic while still asking for a TOTP generator: TOTP is HOTP with a time-based counter.

## Repository Structure

- `ft_otp`: executable Python CLI entry point
- `otp_core.py`: key validation, HOTP, and TOTP logic
- `storage.py`: encrypted key storage and retrieval using OpenSSL
- `errors.py`: project-specific exceptions
- `RFC4226_HOTP_basics.md`: summary of HOTP core flow
- `RFC6238_TOTP_time_to_counter.md`: explanation of time-to-counter conversion
- `RFC6238_official_test_vectors.md`: validation notes based on RFC reference vectors
- `storage_notes.md`: design notes for encrypted key handling
- `subject_en.md`: project subject summary in English

## Quick Start

### Requirements

- `python3`
- `openssl`

### Make the entry script executable

```bash
chmod +x ft_otp
```

### Prepare a valid key file

The key file must contain at least 64 hexadecimal characters.

Example:

```text
31323334353637383930313233343536373839303132333435363738393031323334
```

### Encrypt and store the key

```bash
./ft_otp -g key.hex
```

You will be prompted for a password and confirmation. On success, the encrypted file `ft_otp.key` is created.

### Generate a one-time password

```bash
./ft_otp -k ft_otp.key
```

You will be prompted for the decryption password, then the program prints a 6-digit OTP. The value changes every 30-second time window.

## Verification With `oathtool`

### macOS

```bash
brew update
brew install oath-toolkit
```

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install oathtool
```

### Compare outputs

If your test secret is stored in `key.hex`:

```bash
oathtool --totp "$(cat key.hex)"
```

Then compare it with:

```bash
./ft_otp -k ft_otp.key
```

The outputs should match if both commands are run within the same time window.

## Notes on Security and Scope

- this repository does not include real or previously used secrets
- generated key files such as `ft_otp.key` should never be committed
- demo keys used in documentation should only be test values
- this public repo focuses on the mandatory CLI and core algorithm flow

## Learning Outcomes

This project helped reinforce:

- the relationship between HOTP and TOTP
- RFC 4226 dynamic truncation and fixed-length OTP formatting
- secure handling of secret material in a CLI application
- practical validation of cryptographic logic against reference tools

## Initialize as a New Repository

```bash
cd D2_ft_otp_public
git init
```
# ft_otp
