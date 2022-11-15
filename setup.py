"""
DeepgramAudioServer python package configuration.

"""

from setuptools import setup

setup(
    name='deepgram-audio-server',
    version='0.1.0',
    packages=['deepgram_audio_server'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'peewee',
        'tinytag',
    ],
    python_requires='>=3.6',
)
