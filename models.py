from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, func, Numeric, Float, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    balance_cents = Column(Integer, default=0, nullable=False)  # 残高（cents）
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    rentals = relationship("Rental", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} balance={self.balance_cents}>"

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)

    batteries = relationship("Battery", back_populates="station")

    def __repr__(self):
        return f"<Station id={self.id} name={self.name}>"

class Battery(Base):
    __tablename__ = "batteries"
    id = Column(Integer, primary_key=True)
    serial = Column(String(120), unique=True, nullable=False, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    available = Column(Boolean, default=True, nullable=False)
    battery_level = Column(Integer, default=100, nullable=False)  # 0-100
    extra_info = Column(Text, nullable=True)

    station = relationship("Station", back_populates="batteries")
    rentals = relationship("Rental", back_populates="battery")

    def __repr__(self):
        return f"<Battery id={self.id} serial={self.serial} avail={self.available} level={self.battery_level}>"

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    start_at = Column(DateTime(timezone=True), server_default=func.now())
    end_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default="ongoing")  # ongoing, returned, cancelled
    price_cents = Column(Integer, nullable=True)  # 最終支払額（cents）

    user = relationship("User", back_populates="rentals")
    battery = relationship("Battery", back_populates="rentals")

    def __repr__(self):
        return f"<Rental id={self.id} user={self.user_id} battery={self.battery_id} status={self.status}>"
