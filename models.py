"""
models.py - データベースモデル定義
=====================================================
【設計意図】
- 第3正規形を満たすテーブル設計
- 外部キーによるリレーション構築
- 正規化により冗長データを排除

【ER図構成】
User (1) ──< (N) Rental (N) >── (1) Battery (N) >── (1) Station

- User: ユーザー情報（認証・残高管理）
- Station: 貸出スタンド（拠点情報）
- Battery: バッテリー本体（在庫管理）
- Rental: 貸出履歴（トランザクション記録）
=====================================================
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, 
    DateTime, Float, Text, func
)
from sqlalchemy.orm import relationship, declarative_base

# ベースクラス（全モデルの親）
Base = declarative_base()


class User(Base):
    """
    ユーザーテーブル
    - 認証情報（email, password_hash）
    - 残高管理（balance_cents）
    - 作成日時（created_at）
    """
    __tablename__ = "users"
    
    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 認証情報
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # 残高（centsで管理することで小数点誤差を回避）
    balance_cents = Column(Integer, default=0, nullable=False)
    
    # タイムスタンプ（サーバー時刻で自動設定）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション定義（1対多: User -> Rental）
    rentals = relationship("Rental", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} balance={self.balance_cents}>"


class Station(Base):
    """
    スタンド（貸出拠点）テーブル
    - 名称・位置情報を管理
    - バッテリーの設置場所を表す
    """
    __tablename__ = "stations"
    
    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # スタンド情報
    name = Column(String(120), nullable=False)
    location = Column(String(255), nullable=True)  # 住所・説明
    
    # 緯度経度（地図表示用、オプション）
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    
    # リレーション定義（1対多: Station -> Battery）
    batteries = relationship("Battery", back_populates="station", lazy="dynamic")

    def __repr__(self):
        return f"<Station id={self.id} name={self.name}>"


class Battery(Base):
    """
    バッテリーテーブル
    - 個別のバッテリー情報を管理
    - 貸出可否・充電状態を追跡
    - 外部キーでStationと紐付け
    """
    __tablename__ = "batteries"
    
    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # バッテリー識別情報
    serial = Column(String(120), unique=True, nullable=False, index=True)
    
    # 所属スタンド（外部キー: stations.id）
    # nullable=True で「貸出中」も表現可能
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    
    # 状態管理
    available = Column(Boolean, default=True, nullable=False)  # 貸出可否
    battery_level = Column(Integer, default=100, nullable=False)  # 0-100%
    
    # 追加情報（メモ・備考）
    extra_info = Column(Text, nullable=True)
    
    # リレーション定義
    station = relationship("Station", back_populates="batteries")
    rentals = relationship("Rental", back_populates="battery", lazy="dynamic")

    def __repr__(self):
        return f"<Battery id={self.id} serial={self.serial} avail={self.available}>"


class Rental(Base):
    """
    貸出履歴テーブル（トランザクション記録）
    - 貸出・返却の履歴を時系列で管理
    - 外部キーでUser, Batteryと紐付け
    - 正規化: 料金は返却時に計算して記録
    """
    __tablename__ = "rentals"
    
    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 外部キー（ユーザー・バッテリー）
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=True, index=True)
    
    # 時刻管理
    start_at = Column(DateTime(timezone=True), server_default=func.now())
    end_at = Column(DateTime(timezone=True), nullable=True)
    
    # 状態管理（ongoing: 貸出中, returned: 返却済, cancelled: キャンセル）
    status = Column(String(30), default="ongoing", nullable=False, index=True)
    
    # 料金（返却時に計算）
    price_cents = Column(Integer, nullable=True)
    
    # リレーション定義
    user = relationship("User", back_populates="rentals")
    battery = relationship("Battery", back_populates="rentals")

    def __repr__(self):
        return f"<Rental id={self.id} user={self.user_id} status={self.status}>"
