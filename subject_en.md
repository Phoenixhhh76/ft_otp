# `ft_otp` Subject Notes (English)

Source: `Cyber_D2_ft_otp_en.subject.pdf`

## Project Goal

Implement a TOTP-based one-time password tool with a CLI interface:

- `-g`: read a key file (minimum 64 hexadecimal characters) and securely store it as encrypted `ft_otp.key`
- `-k`: load the encrypted key file and print a newly generated OTP

The implementation must rely on HOTP logic (RFC 4226) and produce fixed 6-digit OTP output.

## Core Requirements

- executable name must be `ft_otp`
- program must use command-line arguments
- key format validation is mandatory
- key storage must be encrypted
- output must be a 6-digit one-time password
- direct use of a fully built TOTP library is not allowed

## Practical Interpretation

The project is effectively testing three things:

1. understanding OTP, HOTP, and TOTP relationship
2. implementing core logic (not just calling a one-line TOTP package)
3. secure key management with a usable CLI workflow

## HOTP vs TOTP

There is no contradiction between “use HOTP algorithm” and “build TOTP”:

- HOTP: `HMAC(secret, counter)`
- TOTP: HOTP where `counter = floor(current_unix_time / time_step)`

So TOTP is HOTP with a time-derived counter.

## Suggested Implementation Steps

1. build CLI structure (`-g`, `-k`, argument checks)
2. implement key-file reading and hex validation
3. encrypt and store key in `ft_otp.key`
4. implement decryption path
5. implement HOTP core (HMAC-SHA1 + truncation + zero-padding)
6. convert current time to TOTP counter
7. connect `-k` flow end-to-end and verify with `oathtool`

## Validation Tip

Use a reference tool such as `oathtool` to compare generated OTP values during testing and evaluation.
