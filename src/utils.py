import os
import logging


def createDirectory(dir: str) -> None:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f">>> {dir} is created !!!")
    except OSError:
        print(f"[ERROR] Creating {dir} is failed !!!")


def getLogger() -> logging.Logger:
    logger = logging.getLogger()
    return logger
