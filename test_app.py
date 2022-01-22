import pytest, json
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

def test_get_rates(client):
    response = client.get('/rates')
    assert response.status_code == 200

def test_put_rates(client):
    fakeRate = {
        "days": "mon,tues,thurs",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 1500
    }
    
    putResponse = client.put('/rates', data=json.dumps(fakeRate))
    assert putResponse.status_code == 200

    getResponse = client.get('/rates')
    assert len(json.loads(getResponse.data)) == 6

def test_get_price(client):
    response = client.get('/price', query_string="start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00")
    assert response.status_code == 200
    assert json.loads(response.data)['price'] == 1750

    response = client.get('/price', query_string="start=2015-07-04T15:00:00+00:00&end=2015-07-04T20:00:00+00:00")
    assert response.status_code == 200
    assert json.loads(response.data)['price'] == 2000

    response = client.get('/price', query_string="start=2015-07-04T07:00:00+05:00&end=2015-07-04T20:00:00+05:00")
    assert response.status_code == 503

