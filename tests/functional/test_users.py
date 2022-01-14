from app import create_app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200


def test_home_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405


def test_register_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/register" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/register')
        assert response.status_code == 200


# def test_register_page_post():
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the "/register" page is posted to (POST)
#     THEN check that a '405' status code is returned
#     """
#     flask_app = create_app()
#
#     with  flask_app.test_client() as test_client:
#         response = test_client.post('/register')
#         assert response.status_code == 405


def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/login" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200


def test_dashboard_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/dashboard" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/dashboard')
        assert response.status_code == 200


def test_admin_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/admin" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/admin')
        assert response.status_code == 200


def test_search_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/search" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with  flask_app.test_client() as test_client:
        response = test_client.get('/search')
        assert response.status_code == 200
