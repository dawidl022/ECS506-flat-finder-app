from flask.testing import FlaskClient


def test_request_example(client: FlaskClient):
    response = client.get("/")
    assert b"Hello world!" in response.data
