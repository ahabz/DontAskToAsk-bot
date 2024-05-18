from dataclasses import dataclass
from functools import lru_cache
import os
from loguru import logger
from dotenv import load_dotenv

logger.add(
    "logs/main.log",
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
)


@dataclass
class Config:
    token: str

    @classmethod
    @lru_cache(maxsize=1)
    def from_env(cls) -> "Config":
        try:
            load_dotenv()  # Load environment variables from .env file
        except FileNotFoundError:
            logger.error("load_dotenv() failed, no .env file ")

        token = os.getenv("DISCORD_TOKEN", None)
        if token is None:
            logger.warning("Token is empty")
            return None

        logger.info("Discord token successfully retrieved.")

        return cls(token)

    @classmethod
    @lru_cache(maxsize=1)
    def from_env_SVM(cls) -> "Config":
        try:
            load_dotenv()  # Load environment variables from .env file
        except FileNotFoundError:
            logger.error("load_dotenv() failed, no .env file ")

        SVM_moedl_path = os.getenv("SVM_PATH", None)

        if SVM_moedl_path is None:
            logger.warning("model path is empty")
            return None
        return cls(SVM_moedl_path)

    @classmethod
    @lru_cache(maxsize=1)
    def from_env_TFIDF(cls) -> "Config":
        try:
            load_dotenv()  # Load environment variables from .env file
        except FileNotFoundError:
            logger.error("load_dotenv() failed, no .env file ")

        TFIDF_vec_path = os.getenv("TFIDF_PATH")

        if TFIDF_vec_path is None:
            logger.warning("vectorizer path is empty")
            return None
        return cls(TFIDF_vec_path)
