"""database utility functions."""
import datetime
from deepgram_audio_server.db.models import Audio, sqlite_db


def create_db():
    """Create the database and the table if they don't exist."""
    if not sqlite_db.table_exists(Audio):
        sqlite_db.create_tables([Audio])


def connect_db():
    """Connect to the database."""
    sqlite_db.connect()


def close_db():
    """Close the database."""
    sqlite_db.close()



