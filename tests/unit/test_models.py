from database.models import Users, Blacklist, Favourite, WatchList


def test_new_user():
    """
    GIVEN a user model
    WHEN a user is created
    THEN check the email, password, role and banned fields are defined correctly
    """
    user = Users('stocsustest@testemail.com', '@Password1', 'user', False)
    assert user.email == 'stocsustest@testemail.com'
    assert user.password != '@Password1'
    assert user.role == 'user'
    assert user.banned == False


def test_blacklist():
    """
    GIVEN a blacklist model
    WHEN a blacklist is created
    THEN check the supplier_name field is defined correctly
    """
    blacklist = Blacklist('Test Supplier')
    assert blacklist.supplier_name == 'Test Supplier'


def test_favourite():
    """
    GIVEN a favourite model
    WHEN a favourite model is created
    THEN check the supplier_name field is defined correctly
    """
    favourite = Favourite('Test Supplier')
    assert favourite.supplier_name == 'Test Supplier'


def test_watchlist():
    """
    GIVEN a watchlist model
    WHEN a watchlist model is created
    THEN check the supplier_name field is defined correctly
    """
    watchlist = WatchList('Test Supplier')
    assert watchlist.part_number == 'Test Supplier'


