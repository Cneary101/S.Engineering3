import pytest
from Publications import Publication


@pytest.fixture
def publication():
    return Publication()


def test_create_publication(publication):
    assert publication.create_publication(1, 'Irish Times', 'Newspaper', 3.00, 10, 'Daily') is True
    assert publication.getName() == 'Irish Times'
    assert publication.getActive() is True

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