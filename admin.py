"""
DB初期化用スクリプト:
python admin.py init_db
python admin.py add_station --name "Central" --lat 35.6 --lng 139.7
python admin.py list_stations
"""
import sys
import argparse
from db import engine, get_session
from models import Base, Station, Battery
import random, string

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized DB (tables created).")

def add_station(name, lat=None, lng=None, location=None):
    session = get_session()
    try:
        st = Station(name=name, lat=lat, lng=lng, location=location)
        session.add(st)
        session.commit()
        print("Added station:", st)
    except Exception as e:
        session.rollback()
        print("Failed:", e)
    finally:
        session.close()

def add_battery(serial, station_id=None, level=100):
    session = get_session()
    try:
        b = Battery(serial=serial, station_id=station_id, battery_level=level, available=True)
        session.add(b)
        session.commit()
        print("Added battery:", b)
    except Exception as e:
        session.rollback()
        print("Failed:", e)
    finally:
        session.close()

def list_stations():
    session = get_session()
    try:
        for s in session.query(Station).all():
            print(s)
    finally:
        session.close()

def parse_args(argv):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("init_db")
    p_as = sub.add_parser("add_station")
    p_as.add_argument("--name", required=True)
    p_as.add_argument("--lat", type=float)
    p_as.add_argument("--lng", type=float)
    p_as.add_argument("--location")
    p_ab = sub.add_parser("add_battery")
    p_ab.add_argument("--serial", required=True)
    p_ab.add_argument("--station", type=int)
    p_ab.add_argument("--level", type=int, default=100)
    sub.add_parser("list_stations")
    return parser.parse_args(argv)

def main(argv):
    args = parse_args(argv)
    if args.cmd == "init_db":
        init_db()
    elif args.cmd == "add_station":
        add_station(args.name, args.lat, args.lng, args.location)
    elif args.cmd == "add_battery":
        add_battery(args.serial, args.station, args.level)
    elif args.cmd == "list_stations":
        list_stations()
    else:
        print("Use: init_db / add_station / add_battery / list_stations")

if __name__ == "__main__":
    main(sys.argv[1:])
