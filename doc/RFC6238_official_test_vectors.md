# RFC 6238 Official Test-Vector Validation

## Official reference

- RFC 6238: [https://www.rfc-editor.org/rfc/rfc6238](https://www.rfc-editor.org/rfc/rfc6238)
- Relevant section: `Appendix B. Test Vectors`

Using official vectors is the most reliable way to verify:

1. time-to-counter conversion
2. HMAC-SHA1 computation
3. dynamic truncation
4. fixed-digit OTP formatting

## Common SHA1 test secret

ASCII secret:

```text
12345678901234567890
```

Hex form:

```text
3132333435363738393031323334353637383930
```

## RFC values are 8-digit by default

Appendix B publishes 8-digit reference outputs, for example:

| Unix time | TOTP (8 digits, SHA1) |
| --- | --- |
| 59 | 94287082 |
| 1111111109 | 07081804 |
| 1111111111 | 14050471 |
| 1234567890 | 89005924 |

## Why this project shows 6 digits

This `ft_otp` project requires 6-digit output.  
So the same core flow is used, but final modulo is `10^6` instead of `10^8`.

Expected 6-digit values for the same timestamps:

| Unix time | TOTP (6 digits, SHA1) |
| --- | --- |
| 59 | 287082 |
| 1111111109 | 081804 |
| 1111111111 | 050471 |
| 1234567890 | 005924 |

## Quick local verification

```bash
python3 -c "from otp_core import totp; s=bytes.fromhex('3132333435363738393031323334353637383930'); print(totp(s, timestamp=59))"
```

Expected output:

```text
287082
```

## Notes

- RFC vectors are for algorithm validation, not mandatory production keys.
- If `-g` requires `64+` hex chars, the RFC demo secret (40 hex chars) should only be used to validate math logic.
