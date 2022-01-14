import os
import tempfile
import pytest
from flask import url_for
from flask_login import login_user
from app import create_app
from database.models import Users, Blacklist, Favourite, WatchList, init_db



def test_new_user(new_user):
    """
    GIVEN a user model
    WHEN a user is created
    THEN check the email, password, role and banned fields are defined correctly
    """
    assert new_user.email == 'stocsustest@testemail.com'
    assert new_user.password != '@Password1'
    assert new_user.role == 'user'
    assert new_user.banned == False


def test_blacklist(new_blacklist):
    """
    GIVEN a blacklist model
    WHEN a blacklist is created
    THEN check the supplier_name field is defined correctly
    """
    assert new_blacklist.supplier_name == 'Test Supplier'


def test_favourite(new_favourite):
    """
    GIVEN a favourite model
    WHEN a favourite model is created
    THEN check the supplier_name field is defined correctly
    """
    assert new_favourite.supplier_name == 'Test Supplier'


def test_watchlist(new_watchlist):
    """
    GIVEN a watchlist model
    WHEN a watchlist model is created
    THEN check the part_number field is defined correctly
    """
    assert new_watchlist.part_number == 'AT0603FRE0747KL'
