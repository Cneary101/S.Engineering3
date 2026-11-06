import pytest
from Newsagent_Basic import Newsagent, NewsagentManager


# Start each test with a fresh Newsagent object.
@pytest.fixture
def newsagent():
    return Newsagent()


def test_create_newsagent(newsagent):
    assert newsagent.create_newsagent(1, 'Main Street Newsagents') is True
    assert newsagent.getName() == 'Main Street Newsagents'
    assert newsagent.getActive() is True


# Check invalid IDs and blank names.
@pytest.mark.parametrize('newsagent_id, name', [
    (0, 'Main Street Newsagents'),
    (1, ''),
    (1, '   '),
])
def test_invalid_newsagent(newsagent, newsagent_id, name):
    assert newsagent.create_newsagent(newsagent_id, name) is False
    assert newsagent.getNewsagentId() is None


def test_setters(newsagent):
    newsagent.create_newsagent(1, 'Main Street Newsagents')
    newsagent.setName('Athlone Newsagents')
    newsagent.setActive(False)
    assert newsagent.getName() == 'Athlone Newsagents'
    assert newsagent.getActive() is False


# The manager follows the CRUD pattern 
@pytest.fixture
def manager():
    return NewsagentManager()


def test_manager_create_and_read(manager):
    assert manager.create_newsagent(1, 'Main Street Newsagents') == 1
    assert manager.read_newsagent(1).getName() == 'Main Street Newsagents'
    assert len(manager.read_all_newsagents()) == 1


def test_manager_invalid_and_duplicate(manager):
    assert manager.create_newsagent(1, 'Main Street Newsagents') == 1
    assert manager.create_newsagent(1, 'Duplicate') is False
    assert manager.create_newsagent(2, '   ') is False
    assert manager.read_newsagent(2) is None
    assert manager.read_newsagent(99) is None


def test_manager_update(manager):
    manager.create_newsagent(1, 'Main Street Newsagents')
    assert manager.update_newsagent(1, 'Athlone Newsagents') is True
    assert manager.update_newsagent(1, '   ') is False
    assert manager.update_newsagent(99, 'Different') is False
    assert manager.read_newsagent(1).getName() == 'Athlone Newsagents'


def test_manager_delete_keeps_inactive_record(manager):
    manager.create_newsagent(1, 'Main Street Newsagents')
    assert manager.delete_newsagent(1) is True
    assert manager.read_newsagent(1).getActive() is False
    assert manager.delete_newsagent(1) is False
    assert manager.delete_newsagent(99) is False
