import os


class DefaultConfig:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")
    WORK_DIR = os.getenv("WORK_DIR", "/home/app")

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 5000)

    # Flask general
    DEBUG = False
    TESTING = False
