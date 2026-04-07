# RFC 6238: Converting Time to TOTP Counter

## Core Formula

TOTP uses:

```text
T = floor((CurrentUnixTime - T0) / X)
```

- `CurrentUnixTime`: current UNIX time in seconds
- `T0`: epoch start (usually `0`)
- `X`: time-step size in seconds (usually `30`)

In most implementations:

```text
T = floor(current_unix_time / 30)
```

## Why it works

Time is split into fixed windows. With `X = 30`:

- `0-29` seconds -> same counter
- `30-59` seconds -> next counter
- `60-89` seconds -> next counter

OTP stays stable within a window and changes when the window changes.

## Important details

- use **seconds**, not milliseconds
- ensure integer flooring (`floor` or integer division)
- encode `T` as **8-byte big-endian** before HOTP

## Example

For `current_unix_time = 59`, `T0 = 0`, `X = 30`:

```text
T = floor(59 / 30) = 1
```

For `current_unix_time = 60`:

```text
T = floor(60 / 30) = 2
```

## Relationship to HOTP

TOTP is not a separate cryptographic primitive.  
It is HOTP where the counter comes from time:

```text
TOTP(K, time) = HOTP(K, time_counter)
```
