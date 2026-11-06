import pytest
from Publication_Basic import Publication, PublicationManager


# Start each test with a fresh Publication object.
@pytest.fixture
def publication():
    return Publication()


def test_create_publication(publication):
    assert publication.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily') is True
    assert publication.getName() == 'Irish Times'
    assert publication.getActive() is True


# Try several invalid inputs using the same creation test.
@pytest.mark.parametrize('details', [
    (0, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily'),
    (1, '', 'Newspaper', 3.00, 10, 'Daily'),
    (1, 'Irish Times', '', 3.00, 10, 'Daily'),
    (1, 'Irish Times', 'Newspaper', -1, 10, 'Daily'),
    (1, 'Irish Times', 'Newspaper', 3.00, -1, 'Daily'),
    (1, 'Irish Times', 'Newspaper', 3.00, 10, ''),
])
def test_invalid_publication(publication, details):
    assert publication.create_publication(*details) is False
    assert publication.getPublicationId() is None


def test_setters(publication):
    publication.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily')
    publication.setName('Independent')
    publication.setPrice(3.50)
    publication.setActive(False)
    assert publication.getName() == 'Independent'
    assert publication.getPrice() == 3.50
    assert publication.getActive() is False


def test_low_stock(publication):
    publication.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 6, 'Daily')
    assert publication.verifyLowStock() is False
    publication.setQuantity(5)
    assert publication.verifyLowStock() is True


# Test the manager's create, read, update and delete operations.
@pytest.fixture
def manager():
    return PublicationManager()


def test_manager_create_and_read(manager):
    assert manager.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily') == 1
    assert manager.read_publication(1).getName() == 'Irish Times'
    assert len(manager.read_all_publications()) == 1


def test_manager_rejects_duplicate_and_invalid(manager):
    assert manager.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily') == 1
    assert manager.create_publication(1, 'Independent', 'Newspaper', 2.00, 5, 'Daily') is False
    assert manager.create_publication(0, 'Invalid', 'Newspaper', 2.00, 5, 'Daily') is False
    assert manager.read_publication(99) is None
    assert len(manager.read_all_publications()) == 1


def test_manager_update_valid_and_invalid(manager):
    manager.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily')
    assert manager.update_publication(1, 'Independent', 'Magazine', 4.00, 5, 'Weekly') is True
    publication = manager.read_publication(1)
    assert publication.getName() == 'Independent'
    assert publication.getPublicationType() == 'Magazine'
    assert publication.getPrice() == 4.00
    assert publication.getQuantity() == 5
    assert publication.getFrequency() == 'Weekly'
    assert manager.update_publication(1, '', 'Magazine', 4.00, 5, 'Weekly') is False
    assert manager.update_publication(1, 'Changed', 'Magazine', -1, 5, 'Weekly') is False
    assert publication.getName() == 'Independent'
    assert publication.getPrice() == 4.00
    assert manager.update_publication(99, 'X', 'Magazine', 4.00, 5, 'Weekly') is False


def test_manager_delete_deactivates_without_removing(manager):
    manager.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily')
    assert manager.delete_publication(1) is True
    assert manager.read_publication(1).getActive() is False
    assert manager.delete_publication(1) is False
    assert manager.delete_publication(99) is False
    assert 1 in manager.read_all_publications()
