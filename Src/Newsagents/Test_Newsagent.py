import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import Newsagents.Newsagent as newsagent
from models import Base, Newsagent as NewsagentRow


@pytest.fixture
def database(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'newsagent_test.db'}")
    Base.metadata.create_all(engine)
    monkeypatch.setattr(newsagent, "engine", engine)
    yield engine
    engine.dispose()


# Validation
@pytest.mark.parametrize("name", ["Main Street Newsagents", "N", "  Athlone  "])
def test_valid_name(name):
    assert newsagent.verify_name(name) is True


@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_invalid_name(name):
    assert newsagent.verify_name(name) is False


# Create and Read
@pytest.mark.parametrize("newsagent_id,name", [
    (0, "Newsagent"), (-1, "Newsagent"), (True, "Newsagent"),
    ("1", "Newsagent"), (1, ""), (1, "   "), (1, None)
])
def test_invalid_creation(database, newsagent_id, name):
    assert newsagent.create_newsagent(newsagent_id, name) is False
    assert newsagent.read_all_newsagents() == []


def test_create_read_and_list(database):
    assert newsagent.create_newsagent(1, "  Main Street  ") == 1
    assert newsagent.create_newsagent(2, "Athlone") == 2
    row = newsagent.read_newsagent(1)
    assert (row.id, row.name, row.is_active) == (1, "Main Street", True)
    assert [row.id for row in newsagent.read_all_newsagents()] == [1, 2]
    assert newsagent.read_newsagent(99) is None


def test_duplicate_id_rejected(database):
    assert newsagent.create_newsagent(1, "Original") == 1
    assert newsagent.create_newsagent(1, "Duplicate") is False
    assert newsagent.read_newsagent(1).name == "Original"
    assert len(newsagent.read_all_newsagents()) == 1


# Update
@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_invalid_update_keeps_name(database, name):
    newsagent.create_newsagent(1, "Original")
    assert newsagent.update_newsagent(1, name) is False
    assert newsagent.read_newsagent(1).name == "Original"


def test_update_and_missing_id(database):
    newsagent.create_newsagent(1, "Original")
    assert newsagent.update_newsagent(1, " Updated ") is True
    assert newsagent.read_newsagent(1).name == "Updated"
    assert newsagent.update_newsagent(99, "Other") is False


# Deactivate, but keep the record

def test_deactivate_and_repeat_delete(database):
    newsagent.create_newsagent(1, "Main Street")
    assert newsagent.delete_newsagent(1) is True
    row = newsagent.read_newsagent(1)
    assert row is not None and row.is_active is False
    assert newsagent.delete_newsagent(1) is False
    assert newsagent.delete_newsagent(99) is False
    assert len(newsagent.read_all_newsagents()) == 1


def test_record_is_saved_in_sql(database):
    newsagent.create_newsagent(1, "Main Street")
    with Session(database) as session:
        assert session.get(NewsagentRow, 1).name == "Main Street"
