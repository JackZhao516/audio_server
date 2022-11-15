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


def get_all_audio_file_ids():
    """Get all the audio files."""
    try:
        with sqlite_db.atomic():
            audios = Audio.select()
            return [audio.file_id for audio in audios]
    except Audio.DoesNotExist:
        return None


def get_all_audio_file_names_and_durations(maxduration: int = None):
    """Get all the audio files with/without maxduration."""
    try:
        with sqlite_db.atomic():
            if not maxduration:
                audios = Audio.select().order_by(Audio.old_name.asc())
            else:
                audios = Audio.select().where(Audio.duration <= maxduration)\
                    .order_by(Audio.duration.desc())
            return [{'name': audio.old_name, 'duration': audio.duration}
                    for audio in audios]
    except Audio.DoesNotExist:
        return None


def update_audio_file(file_id: str, path: str, duration: int):
    """Update the audio file with the given id."""
    try:
        with sqlite_db.atomic():
            Audio.update(path=path, duration=duration,
                         updated_at=datetime.datetime.now())\
                .where(Audio.file_id == file_id).execute()
    except Audio.DoesNotExist:
        pass


def add_audio_file(file_id: str, name: str, path: str, duration: int):
    """Add a new audio file."""
    with sqlite_db.atomic():
        Audio.create(file_id=file_id, old_name=name, path=path,
                     duration=duration, created_at=datetime.datetime.now(),
                     updated_at=datetime.datetime.now())
