import os
from dotenv import load_dotenv

load_dotenv()


class Envs:
    def __init__(self) -> None:
        self.SECRET = os.getenv('SECRET')
    