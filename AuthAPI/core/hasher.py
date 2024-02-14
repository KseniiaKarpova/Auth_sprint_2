from core.config import settings
from passlib import hash


class DataHasher:
    def __init__(self) -> None:
        self.algorithm = settings.hasher.algorithm
        self.rounds = settings.hasher.rounds

    async def generate_word_hash(self, secret_word: str):
        hasher = self.get_hasher()
        return hasher.hash(secret=secret_word)

    def get_hasher(self):
        if self.algorithm == "sha256_crypt":
            hasher = hash.sha256_crypt
        elif self.algorithm == "pbkdf2_sha256":
            hasher = hash.pbkdf2_sha256
        else:
            ValueError("Unsupported hashing algorithm")
        if self.rounds:
            hasher.using(rounds=self.rounds)
        return hasher

    async def verify(self, secret_word: str, hashed_word):
        hasher = self.get_hasher()
        return hasher.verify(secret_word, hashed_word)

    def sync_generater(self, secret_word: str):
        hasher = self.get_hasher()
        return hasher.hash(secret=secret_word)
