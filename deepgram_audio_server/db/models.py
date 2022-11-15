"""database models."""
import datetime
from peewee import Model, SqliteDatabase, CharField, TimestampField, IntegerField

sqlite_db = SqliteDatabase('audio_sever.db',
                           pragmas={'journal_mode': 'wal',
                                    'cache_size': -1 * 64000,  # 64MB
                                    'synchronous': 0})


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = sqlite_db


class Audio(BaseModel):
    """Audio model that stores all the audio file information."""
    file_id = CharField(primary_key=True)
    old_name = CharField()
    path = CharField()
    duration = IntegerField()
    created_at = TimestampField(utc=True, default=datetime.datetime.now())
    updated_at = TimestampField(utc=True, default=datetime.datetime.now())
