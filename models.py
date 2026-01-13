from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    DateTime, Float, Text, func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    balance_cents = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    rentals = relationship("Rental", back_populates="user", lazy="dynamic")
    charges = relationship("ChargeHistory", back_populates="user", lazy="dynamic")


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    location = Column(String(255), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    batteries = relationship("Battery", back_populates="station", lazy="dynamic")


class Battery(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial = Column(String(120), unique=True, nullable=False, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    available = Column(Boolean, default=True, nullable=False)
    battery_level = Column(Integer, default=100, nullable=False)
    extra_info = Column(Text, nullable=True)

    station = relationship("Station", back_populates="batteries")
    rentals = relationship("Rental", back_populates="battery", lazy="dynamic")


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False, index=True)

    start_at = Column(DateTime(timezone=True), server_default=func.now())
    end_at = Column(DateTime(timezone=True), nullable=True)

    # 状態管理（ongoing: 貸出中, returned: 返却済）
    status = Column(String(30), default="ongoing", nullable=False, index=True)

    price_cents = Column(Integer, nullable=True)

    user = relationship("User", back_populates="rentals")
    battery = relationship("Battery", back_populates="rentals")


class ChargeHistory(Base):
    __tablename__ = "charge_histories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="charges")
