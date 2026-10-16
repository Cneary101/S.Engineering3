import pytest
from Newsagents import Newsagent


@pytest.fixture
def newsagent():
    return Newsagent()


def test_create_newsagent(newsagent):
    assert newsagent.create_newsagent(1, 'Main Street Newsagents') is True
    assert newsagent.getName() == 'Main Street Newsagents'
    assert newsagent.getActive() is True


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
