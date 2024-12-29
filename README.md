# Digital Signature Generator and Verifier

A Python-based tool for generating and verifying digital signatures using RSA encryption.

## Project Overview

The main objective of this project is to ensure the integrity and authenticity of messages by using digital signatures. The project includes functionalities to:

- Generate cryptographic keys
- Sign messages
- Verify signed messages

## Prerequisites

- Python
- cryptography library

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/sign-verify.git
cd sign-verify
```

2. Install required dependencies:

```bash
pip install cryptography
```

## Usage

### Generating Keys

```python
from key_generator import generate_keys

# Generate public and private keys
generate_keys()
```

### Signing a Message

```python
from signer import sign_message

# Sign a message using your private key
message = "Hello, World!"
signature = sign_message(message)
```

### Verifying a Signature

```python
from verifier import verify_signature

# Verify the signature using the public key
is_valid = verify_signature(message, signature)
print(f"Signature is valid: {is_valid}")
```

## Features

- RSA key pair generation
- Message signing using private key
- Signature verification using public key
- Secure cryptographic implementation using the `cryptography` library

## Deployment

Try out the live demo: [Digital Signature Generator & Verifier](https://digital-signature-nine.vercel.app/)

## Security Notice

- Keep your private key secure and never share it
- Store keys in a safe location
- Use strong passwords for key protection

## Author

Yugal1107
