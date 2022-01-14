import pytest
from app import create_app
from database.models import Users, Blacklist, Favourite, WatchList


@pytest.fixture(scope='module')
def new_user():
    user = Users('stocsustest@testemail.com', '@Password1234', 'user', False)
    return user


@pytest.fixture(scope='module')
def new_blacklist():
    blacklist = Blacklist('Test Supplier')
    return blacklist


@pytest.fixture(scope='module')
def new_favourite():
    favourite = Favourite('Test Supplier')
    return favourite


@pytest.fixture(scope='module')
def new_watchlist():
    watchlist = WatchList('Test Supplier')
    return watchlist


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        yield testing_client
