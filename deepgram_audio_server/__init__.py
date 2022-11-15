""" Initialize the package. """
import flask

app = flask.Flask(__name__)
app.config.from_object('deepgram_audio_server.config')

import deepgram_audio_server.db
deepgram_audio_server.db.create_db()

import deepgram_audio_server.api
