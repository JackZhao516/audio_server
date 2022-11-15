""" deepgram_audio_server configuration"""
import pathlib

APPLICATION_ROOT = '/'

DEEPGRAM_SERVER_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = DEEPGRAM_SERVER_ROOT/'audios'
ALLOWED_EXTENSIONS = {'wav'}
MAX_CONTENT_LENGTH = 256 * 1024 * 1024  # 256MB
