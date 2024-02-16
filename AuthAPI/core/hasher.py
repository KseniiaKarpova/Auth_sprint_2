from core.config import settings
from passlib import hash
from faker import Faker
import random as rd

fake = Faker()


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

    async def random_password(self):
        choices = [
            f"{fake.last_name()}{fake.first_name()}",
            rd.randint(-1000000000, 100000000)]
        random_password = rd.choice(choices)
        return await self.generate_word_hash(secret_word=random_password)
