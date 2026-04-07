# RFC 4226: HOTP Basics

## Definition

HOTP stands for **HMAC-Based One-Time Password** and is defined in RFC 4226.

Formula:

```text
HOTP(K, C) = Truncate(HMAC-SHA1(K, C))
```

- `K`: shared secret key
- `C`: moving counter (8-byte big-endian input to HMAC)

## Standard Flow

1. prepare shared secret `K`
2. prepare counter `C`
3. compute `HS = HMAC-SHA1(K, C)`
4. apply dynamic truncation
5. modulo by `10^digits` (commonly `10^6`)
6. zero-pad to fixed length

## Dynamic Truncation

```text
offset = HS[19] & 0x0f
P = ((HS[offset] & 0x7f) << 24)
  | ((HS[offset + 1] & 0xff) << 16)
  | ((HS[offset + 2] & 0xff) << 8)
  |  (HS[offset + 3] & 0xff)
OTP = P mod 10^digits
```

The highest bit is cleared with `& 0x7f` to keep a positive 31-bit integer.

## Common Implementation Pitfalls

- using plain `SHA1` instead of `HMAC-SHA1`
- wrong counter encoding (must be 8-byte big-endian)
- incorrect truncation offset logic
- forgetting leading-zero padding

## HOTP and TOTP Relationship

TOTP (RFC 6238) is HOTP with a time-derived counter:

```text
TOTP = HOTP(K, floor(unix_time / time_step))
```
