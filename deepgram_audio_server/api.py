"""flask api"""
import os
import uuid
from tinytag import TinyTag
from flask import request, jsonify, send_file
from deepgram_audio_server.db import *
import deepgram_audio_server


@deepgram_audio_server.app.route('/post', methods=['POST'])
def upload_audio():
    """
    Upload an audio file to the server.
    If the file already exists, it will be overwritten.
    """
    # check if the post request has the file part
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'error': 'No file part'}), 404

    uploaded = request.files['file']
    filename = uploaded.filename

    # check if the file format is correct
    if filename.split('.')[-1].lower() not in \
            deepgram_audio_server.app.config['ALLOWED_EXTENSIONS'] or \
            not TinyTag.is_supported(filename):
        return jsonify({'error': 'file invalid format'}), 404

    # check if the file already exists.
    # if so, update the file, else, add the file
    connect_db()
    file_info = get_audio_file_info_with_name(filename)

    if file_info is None:
        ids = get_all_audio_file_ids()
        file_id = str(uuid.uuid4().hex)
        while file_id in ids:
            file_id = str(uuid.uuid4().hex)
        filename_uuid = file_id + '.' + filename.split('.')[-1]
        file_path = os.path.join(
            deepgram_audio_server.app.config['UPLOAD_FOLDER'], filename_uuid)
        uploaded.save(file_path)
        add_audio_file(
            file_id, filename, file_path, TinyTag.get(file_path).duration)
        return_msg = "file uploaded"
    else:
        filename_uuid = file_info['file_id'] + '.' + filename.split('.')[-1]
        file_path = os.path.join(
            deepgram_audio_server.app.config['UPLOAD_FOLDER'], filename_uuid)
        os.remove(file_path)
        uploaded.save(file_path)
        update_audio_file(file_info['file_id'], file_path,
                          TinyTag.get(file_path).duration)
        return_msg = "file updated"

    close_db()
    return jsonify({'message': return_msg}), 201


@deepgram_audio_server.app.route('/info', methods=['GET'])
def get_audio_info():
    """Get the information of the audio file with the given name."""
    if 'name' not in request.args:
        return jsonify({'error': 'No file name'}), 404

    connect_db()
    file_info = get_audio_file_info_with_name(request.args['name'])
    close_db()
    if file_info is None:
        return jsonify({'error': 'file not found'}), 404
    else:
        file_info.pop('file_id')
        file_info.pop('path')
        return jsonify(file_info), 201


@deepgram_audio_server.app.route('/download', methods=['GET'])
def download_audio():
    """Download the information of the audio file with the given name."""
    if 'name' not in request.args:
        return jsonify({'error': 'No file name'}), 404

    connect_db()
    file_info = get_audio_file_info_with_name(request.args['name'])
    close_db()
    if file_info is None:
        return jsonify({'error': 'file not found'}), 404
    else:
        return send_file(
            file_info['path'], as_attachment=True,
            download_name=request.args['name']), 201


@deepgram_audio_server.app.route('/list', methods=['GET'])
def list_audio():
    """List all the audio files in the server with or without max duration."""
    connect_db()
    maxduration = request.args.get('maxduration', default=None, type=int)
    audio_list = get_all_audio_file_names_and_durations(maxduration)
    close_db()
    return jsonify({'list': audio_list}), 201
