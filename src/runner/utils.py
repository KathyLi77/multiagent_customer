"""
Utility helpers for running the router and initializing the environment.
"""

import os
import warnings

from dotenv import load_dotenv

from src.database_setup import DatabaseSetup
from src.config.settings import DB_PATH, OPENAI_API_KEY


def suppress_adk_warnings():
    """
    Suppress noisy experimental warnings from google-adk's A2A implementation.
    """
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message=".*EXPERIMENTAL.*",
    )


def init_env():
    """
    Initialize environment variables and suppress warnings.
    """
    load_dotenv()
    suppress_adk_warnings()

    # Make sure OPENAI_API_KEY is available for LiteLlm
    if OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def init_db_if_needed():
    """
    Initialize the SQLite DB using DatabaseSetup if it does not exist.
    """
    db = DatabaseSetup(DB_PATH)
    db.connect()
    db.create_tables()
    db.create_triggers()
    db.insert_sample_data()
    db.close()