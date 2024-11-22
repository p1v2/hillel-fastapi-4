from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,  # or 4096 for more security, but slower performance
    backend=default_backend()
)

# Serialize the private key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()  # Or use a password
)

# Save the private key to a file
with open("private_key.pem", "wb") as f:
    f.write(private_pem)

# Generate the public key from the private key
public_key = private_key.public_key()

# Serialize the public key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the public key to a file
with open("public_key.pem", "wb") as f:
    f.write(public_pem)

print("RSA keys generated and saved to 'private_key.pem' and 'public_key.pem'")
