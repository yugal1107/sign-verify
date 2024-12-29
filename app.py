from flask import Flask, render_template, request, send_file, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

app = Flask(__name__)

# Paths for key storage
PRIVATE_KEY_PATH = "keys/private_key.pem"
PUBLIC_KEY_PATH = "keys/public_key.pem"

# Generate RSA keys (once)
if not os.path.exists("keys"):
    os.makedirs("keys")

if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_PATH, "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )

    with open(PUBLIC_KEY_PATH, "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_keys():
    try:
        # Load private key
        with open(PRIVATE_KEY_PATH, "rb") as private_file:
            private_key = serialization.load_pem_private_key(private_file.read(), None)

        # Load public key
        with open(PUBLIC_KEY_PATH, "rb") as public_file:
            public_key = serialization.load_pem_public_key(public_file.read())

        return private_key, public_key
    except Exception as e:
        print(f"Error loading keys: {e}")
        raise e



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/public_key")
def public_key():
    try:
        with open(PUBLIC_KEY_PATH, "r") as public_file:
            public_key = public_file.read()
        return public_key
    except Exception as e:
        print(f"Error loading public key: {e}")
        return "Error loading public key", 500


@app.route("/sign", methods=["POST"])
def sign_document():
    try:
        message = request.form.get("message").encode()
        private_key, _ = load_keys()

        # Sign the message
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        # Save the signature to a file
        signature_path = "signature.sig"
        with open(signature_path, "wb") as sig_file:
            sig_file.write(signature)

        # Send the file as a response for download
        return send_file(signature_path, as_attachment=True)
    except Exception as e:
        print(f"Error in signing: {e}")
        return jsonify({"status": "error", "message": "Failed to sign the document."})


@app.route("/verify", methods=["POST"])
def verify_signature():
    message = request.form.get("message").encode()
    signature_path = request.files["signature"]
    signature = signature_path.read()
    public_key_pem = request.form.get("publicKey").encode()

    try:
        # Ensure the public key is correctly formatted
        public_key_pem = b"-----BEGIN PUBLIC KEY-----\n" + public_key_pem + b"\n-----END PUBLIC KEY-----\n"
        public_key = serialization.load_pem_public_key(public_key_pem)

        # Verify the signature
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return jsonify({"status": "success", "message": "Signature is valid."})
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return jsonify({"status": "error", "message": "Signature is invalid!"})


if __name__ == "__main__":
    app.run(debug=False)
