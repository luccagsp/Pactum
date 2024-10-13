import os
from dotenv import load_dotenv

load_dotenv()


class Envs:
    SECRET = os.getenv('SECRET')
    ROOT_URL = os.getenv('ROOT_URL')
    if not os.getenv('SECRET'):
        raise KeyError("Falta declarar variable en '.env': 'SECRET'")
    if not os.getenv('ROOT_URL'):
        raise KeyError("Falta declarar variable en '.env': 'ROOT_URL'")