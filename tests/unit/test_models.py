from models import Users


def test_new_user():
    """
    GIVEN a user model
    WHEN a user is created
    THEN check the email, password, role and banned fields are defined correctly
    """
    user = Users('stocsustest@testemail.com', 'Password1234', 'user', False)
    assert user.email == 'stocsustest@testemail.com'
    assert user.password == 'Password1234'
    assert user.role == 'user'
    assert user.banned == False
