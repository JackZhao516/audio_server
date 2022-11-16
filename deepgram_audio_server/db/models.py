"""database models."""
import datetime
from peewee import Model, SqliteDatabase, CharField, TimestampField, IntegerField

sqlite_db = SqliteDatabase('audio_sever.db',
                           pragmas={'journal_mode': 'wal',
                                    'cache_size': -1 * 32000,  # 32MB
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

    @staticmethod
    def get_audio_file_info_with_name(name: str):
        """Get the audio file with the given name."""
        try:
            with sqlite_db.atomic():
                audio = Audio.get(Audio.old_name == name)
                return {'file_id': audio.file_id, 'path': audio.path,
                        'name': audio.old_name, 'duration': audio.duration,
                        'created_at': audio.created_at,
                        'updated_at': audio.updated_at}
        except Audio.DoesNotExist:
            return None

    @staticmethod
    def get_all_audio_file_ids():
        """Get all the audio files."""
        try:
            with sqlite_db.atomic():
                audios = Audio.select()
                return [audio.file_id for audio in audios]
        except Audio.DoesNotExist:
            return None

    @staticmethod
    def get_all_audio_file_names_and_durations(maxduration: int = None):
        """Get all the audio files with/without maxduration."""
        try:
            with sqlite_db.atomic():
                if not maxduration:
                    audios = Audio.select().order_by(Audio.old_name.asc())
                else:
                    audios = Audio.select().where(Audio.duration <= maxduration) \
                        .order_by(Audio.duration.desc())
                return [{'name': audio.old_name, 'duration': audio.duration}
                        for audio in audios]
        except Audio.DoesNotExist:
            return None

    @staticmethod
    def update_audio_file(file_id: str, path: str, duration: int):
        """Update the audio file with the given id."""
        try:
            with sqlite_db.atomic():
                Audio.update(path=path, duration=duration,
                             updated_at=datetime.datetime.now()) \
                    .where(Audio.file_id == file_id).execute()
        except Audio.DoesNotExist:
            pass

    @staticmethod
    def add_audio_file(file_id: str, name: str, path: str, duration: int):
        """Add a new audio file."""
        with sqlite_db.atomic():
            Audio.create(file_id=file_id, old_name=name, path=path,
                         duration=duration, created_at=datetime.datetime.now(),
                         updated_at=datetime.datetime.now())