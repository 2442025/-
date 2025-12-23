"""
簡単なpytest テスト
- 残高不足でレンタルが拒否されること
- 単純な貸出→返却フロー（シーケンシャル）
SQLite のまま動かす想定
"""
import pytest
from db import engine, get_session
from models import Base, User, Station, Battery, Rental
from app import app
from auth import hash_password
import json

@pytest.fixture(scope="module")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    s = get_session()
    # seed minimal
    u1 = User(email="u1@example.com", password_hash=hash_password("pass"), balance_cents=500)
    u2 = User(email="u2@example.com", password_hash=hash_password("pass"), balance_cents=5000)
    s.add_all([u1, u2])
    s.commit()
    st = Station(name="S", lat=0.0, lng=0.0)
    s.add(st)
    s.commit()
    b = Battery(serial="SER1", station_id=st.id, available=True)
    s.add(b)
    s.commit()
    s.close()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def login_get_token(client, email, password="pass"):
    r = client.post("/login", json={"email": email, "password": password})
    data = r.get_json()
    return data.get("access_token")

def test_rent_insufficient_balance(client):
    token = login_get_token(client, "u1@example.com")
    # try rent battery id 1
    r = client.post("/rent", json={"battery_id": 1}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 400
    assert "insufficient balance" in r.get_json().get("error", "")

def test_rent_and_return_flow(client):
    token = login_get_token(client, "u2@example.com")
    r = client.post("/rent", json={"battery_id": 1}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    rent_id = r.get_json()["rental_id"]

    # return
    r2 = client.post("/return", json={"rental_id": rent_id}, headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    j = r2.get_json()
    assert "price_cents" in j
