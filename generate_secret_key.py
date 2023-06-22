import secrets

def generate_secret_key(length=32):
    # Generate a random string of specified length
    secret_key = secrets.token_hex(length//2)
    return secret_key

# Generate a secret key
secret_key = generate_secret_key()

# Print the generated secret key
print("Generated Secret Key:", secret_key)

