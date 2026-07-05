import unittest
import sys
import os
from datetime import timedelta
from jose import jwt, JWTError

# Add the project root to sys.path to enable backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.auth.auth_handler import hash_password, verify_password, create_access_token
from backend.app.config.config import settings

class TestAuthHandler(unittest.TestCase):
    def test_password_hashing_and_verification(self):
        password = "my_super_secret_password"
        hashed = hash_password(password)
        
        # Hashed password should not be plain text
        self.assertNotEqual(password, hashed)
        # Should start with bcrypt signature
        self.assertTrue(hashed.startswith("$2b$") or hashed.startswith("$2a$"))
        
        # Verify correct password
        self.assertTrue(verify_password(password, hashed))
        
        # Verify incorrect password fails
        self.assertFalse(verify_password("wrong_password", hashed))

    def test_jwt_token_generation_and_decoding(self):
        username = "cricket_fan_123"
        token = create_access_token(subject=username)
        
        # Token must be a string and have 3 parts (header, payload, signature)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split(".")), 3)
        
        # Decode and verify contents
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        self.assertEqual(payload.get("sub"), username)
        self.assertIn("exp", payload)

    def test_jwt_token_expiration(self):
        # Generate token with negative expiration time (already expired)
        username = "expired_user"
        delta = timedelta(minutes=-5)
        token = create_access_token(subject=username, expires_delta=delta)
        
        # Trying to decode it should raise JWTError due to expiration
        with self.assertRaises(JWTError):
            jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

if __name__ == "__main__":
    unittest.main()
