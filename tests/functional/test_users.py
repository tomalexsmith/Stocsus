def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is posted to (POST)
    THEN check that a '405' status code is returned
    """

    response = test_client.post('/')
    assert response.status_code == 405


def test_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/register" page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get('/register')
    assert response.status_code == 200


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/login" page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get('/login')
    assert response.status_code == 200


def test_dashboard_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/dashboard" page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get('/dashboard')
    assert response.status_code == 302


def test_admin_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/admin" page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get('/admin')
    assert response.status_code == 302


def test_search_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/search" page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get('/search')
    assert response.status_code == 302
