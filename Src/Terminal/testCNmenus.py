"Tests the menu options for our three parts of the system."

from unittest.mock import patch
from Publication_Basic import PublicationManager
from Newsagent_Basic import NewsagentManager
from billing import BillManager
from my_menus import publication_menu, newsagent_menu, billing_menu


# Simulate inputs instead of typing into the terminal during tests.
def test_publication_terminal_create_update_delete():
    manager = PublicationManager()
    entries = [
        '1', '1', 'Irish Times', 'Newspaper', '3.50', '5', 'Daily',
        '3', '1', '3', '8', '4', '1', '5'
    ]
    with patch('builtins.input', side_effect=entries):
        publication_menu(manager)
    publication = manager.read_publication(1)
    assert publication.getName() == 'Irish Times'
    assert publication.getQuantity() == 8
    assert publication.getActive() is False


def test_publication_terminal_rejects_invalid_and_duplicate(capsys):
    manager = PublicationManager()
    entries = [
        '1', '1', '   ', 'Newspaper', '3', '5', 'Daily',
        '1', '1', 'Irish Times', 'Newspaper', '3', '5', 'Daily',
        '1', '1', 'Independent', 'Newspaper', '3', '5', 'Daily',
        '5'
    ]
    with patch('builtins.input', side_effect=entries):
        publication_menu(manager)
    assert len(manager.read_all_publications()) == 1
    assert manager.read_publication(1).getName() == 'Irish Times'
    assert 'Invalid details' in capsys.readouterr().out


def test_newsagent_terminal_create_and_update():
    manager = NewsagentManager()
    entries = ['1', '1', 'Main Street Newsagents', '3', '1', 'Athlone Newsagents', '5']
    with patch('builtins.input', side_effect=entries):
        newsagent_menu(manager)
    assert manager.read_newsagent(1).getName() == 'Athlone Newsagents'
    assert manager.read_newsagent(1).getActive() is True


def test_billing_terminal_charges_delivered_only():
    manager, deliveries = BillManager(), []
    entries = [
        '1', '1', '2026-11-01', '3.50', '2', 'y',
        '1', '1', '2026-11-02', '3.50', '1', 'n',
        '2', '1', '1', '2026-11', '6'
    ]
    with patch('builtins.input', side_effect=entries):
        billing_menu(manager, deliveries)
    assert manager.read_bill(1).getTotal() == 7.00
    assert len(deliveries) == 2


def test_publication_terminal_update_type_frequency_and_repeat_delete(capsys):
    manager = PublicationManager()
    entries = [
        '1', '1', 'Irish Times', 'Newspaper', '3.50', '5', 'Daily',
        '3', '1', '4', 'Magazine',
        '3', '1', '5', 'Weekly',
        '4', '1',
        '4', '1',
        '5'
    ]
    with patch('builtins.input', side_effect=entries):
        publication_menu(manager)
    publication = manager.read_publication(1)
    assert publication.getPublicationType() == 'Magazine'
    assert publication.getFrequency() == 'Weekly'
    assert publication.getActive() is False
    assert 'already inactive' in capsys.readouterr().out


def test_newsagent_terminal_prevents_repeat_delete(capsys):
    manager = NewsagentManager()
    entries = ['1', '1', 'Athlone Newsagents', '4', '1', '4', '1', '5']
    with patch('builtins.input', side_effect=entries):
        newsagent_menu(manager)
    assert manager.read_newsagent(1).getActive() is False
    assert 'already inactive' in capsys.readouterr().out


def test_billing_terminal_update_and_delete():
    manager, deliveries = BillManager(), []
    entries = [
        '1', '1', '2026-11-01', '3.50', '2', 'y',
        '2', '1', '1', '2026-11',
        '4', '1', '1', '2026-11',
        '5', '1', '6'
    ]
    with patch('builtins.input', side_effect=entries):
        billing_menu(manager, deliveries)
    assert manager.read_bill(1) is None
