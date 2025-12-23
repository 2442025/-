"""
サンプルデータ投入
python addrandomba.py
"""
import random, string
from db import engine, get_session
from models import Base, Station, Battery, User
from variables import RENTAL_DEPOSIT_CENTS

def random_serial(n=8):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

def seed():
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        # Stations
        stations = [
            ("Central Station", 35.681236, 139.767125, "Tokyo"),
            ("North Station", 43.06417, 141.34694, "Sapporo"),
            ("South Station", 34.693738, 135.502165, "Osaka"),
        ]
        for name, lat, lng, loc in stations:
            session.add(Station(name=name, lat=lat, lng=lng, location=loc))
        # Users
        users = [
            User(email="alice@example.com", password_hash="$2b$12$invalid", balance_cents=5000),  # パスワード上書きし直してください
            User(email="bob@example.com", password_hash="$2b$12$invalid", balance_cents=200),
        ]
        session.add_all(users)
        session.commit()

        sts = session.query(Station).all()
        for st in sts:
            for i in range(5):
                session.add(Battery(serial=random_serial(), station_id=st.id, available=True, battery_level=random.randint(40,100)))
        session.commit()
        print("Seed finished.")
    except Exception as e:
        session.rollback()
        print("Seed failed:", e)
    finally:
        session.close()

if __name__ == "__main__":
    seed()
