from peewee import SqliteDatabase
from deepgram_audio_server.db import *


def init():
    """Initialize the database."""
    test_db = SqliteDatabase(':memory:')
    test_db.bind([Audio], bind_refs=False, bind_backrefs=False)
    if not test_db.table_exists(Audio):
        test_db.create_tables([Audio])


def test_basic_add_get_method():
    """Test the basic add and get method."""
    init()
    add_audio_file("1", "name1", "/some/path", 56)
    res = get_audio_file_info_with_name("name1")
    assert res["file_id"] == "1"
    assert res["path"] == "/some/path"
    assert res["name"] == "name1"
    assert res["duration"] == 56
    assert res["created_at"] is not None
    assert res["updated_at"] is not None


def test_basic_add_get_all_method():
    """Test the basic add and get all method."""
    init()
    add_audio_file("1", "name1", "/some/path", 56)
    add_audio_file("2", "name2", "/some/path/2", 17)
    res = get_all_audio_file_ids()
    assert res == ["1", "2"]


def test_basic_add_get_all_with_maxduration_method():
    """Test the basic add and get all with maxduration method."""
    init()
    add_audio_file("1", "name1", "/some/path", 56)
    add_audio_file("2", "name2", "/some/path/2", 17)
    res = get_all_audio_file_names_and_durations(20)
    assert res == [{'name': 'name2', 'duration': 17}]
    res = get_all_audio_file_names_and_durations(100)
    assert res == [{'name': 'name2', 'duration': 17}, {'name': 'name1', 'duration': 56}]
    res = get_all_audio_file_names_and_durations()
    assert res == [{'name': 'name1', 'duration': 56}, {'name': 'name2', 'duration': 17}]


def test_basic_add_update_method():
    """Test the basic add and update method."""
    init()
    add_audio_file("1", "name1", "/some/path", 56)
    update_audio_file("1", "/some/other/path", 17)
    res = get_audio_file_info_with_name("name1")
    assert res["file_id"] == "1"
    assert res["path"] == "/some/other/path"
    assert res["name"] == "name1"
    assert res["duration"] == 17
    assert res["updated_at"] is not None
