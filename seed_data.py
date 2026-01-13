"""
サンプルデータ投入スクリプト
モバイルバッテリーシステム用
"""

import random
import string
from datetime import datetime, timedelta
from db import get_session, engine
from models import Base, User, Station, Battery, Rental
from auth import hash_password
from variables import RENTAL_DEPOSIT_CENTS, PRICE_PER_MINUTE_CENTS

def random_serial(n=8):
    """ランダムなシリアル番号を生成"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

def seed():
    """サンプルデータを投入"""
    print("=== データベース初期化 ===")
    
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    
    session = get_session()
    try:
        # 既存データがあれば削除
        session.query(Rental).delete()
        session.query(Battery).delete()
        session.query(Station).delete()
        session.query(User).delete()
        
        print("1. ユーザーを作成中...")
        # ユーザー作成
        users = [
            User(email="alice@example.com", password_hash=hash_password("password123"), balance_cents=5000),
            User(email="bob@example.com", password_hash=hash_password("password123"), balance_cents=2000),
            User(email="charlie@example.com", password_hash=hash_password("password123"), balance_cents=1000),
        ]
        session.add_all(users)
        session.flush()  # IDを取得
        
        print("2. スタンドを作成中...")
        # スタンド作成
        stations = [
            Station(name="東京駅前", location="東京都千代田区丸の内1丁目", lat=35.681236, lng=139.767125),
            Station(name="新宿駅西口", location="東京都新宿区新宿3丁目", lat=35.6896, lng=139.7005),
            Station(name="渋谷スクランブル", location="東京都渋谷区宇田川町", lat=35.6580, lng=139.7016),
            Station(name="池袋東口", location="東京都豊島区池袋1丁目", lat=35.7292, lng=139.7108),
            Station(name="上野駅前", location="東京都台東区上野7丁目", lat=35.7137, lng=139.7770),
        ]
        session.add_all(stations)
        session.flush()
        
        print("3. バッテリーを作成中...")
        # バッテリー作成（各スタンドに3台ずつ）
        batteries = []
        for station in stations:
            for i in range(3):
                battery = Battery(
                    serial=random_serial(),
                    station_id=station.id,
                    available=True,
                    battery_level=random.randint(60, 100),
                    extra_info=f"Station {station.name} Battery {i+1}"
                )
                batteries.append(battery)
        
        session.add_all(batteries)
        session.flush()
        
        print("4. 利用履歴を作成中...")
        # 利用履歴作成（過去1週間のデータ）
        now = datetime.now()
        
        # 過去の貸出記録
        for i in range(20):
            user = random.choice(users)
            battery = random.choice(batteries)
            
            # 貸出日時（1週間以内のランダムな時間）
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            start_time = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # 50%の確率で返却済みにする
            if random.random() < 0.5:
                # 返却日時（貸出から1〜120分後）
                rental_minutes = random.randint(1, 120)
                end_time = start_time + timedelta(minutes=rental_minutes)
                price = rental_minutes * PRICE_PER_MINUTE_CENTS
                
                # 残高チェック
                if user.balance_cents >= price:
                    rental = Rental(
                        user_id=user.id,
                        battery_id=battery.id,
                        start_at=start_time,
                        end_at=end_time,
                        price_cents=price,
                        status="returned"
                    )
                    user.balance_cents -= price
                    battery.available = True
                    session.add(rental)
            else:
                # 貸出中
                rental = Rental(
                    user_id=user.id,
                    battery_id=battery.id,
                    start_at=start_time,
                    status="ongoing"
                )
                battery.available = False
                session.add(rental)
        
        # チャージ履歴（バッテリーIDは任意の値を使用）
        print("5. チャージ履歴を作成中...")
        for user in users:
            for i in range(2):
                charge_amount = random.choice([1000, 2000, 5000])
                rental = Rental(
                    user_id=user.id,
                    battery_id=batteries[0].id,  # チャージ履歴には任意のバッテリーIDを使用
                    status="charged",
                    price_cents=-charge_amount  # 負の値でチャージを表現
                )
                user.balance_cents += charge_amount
                session.add(rental)
        
        session.commit()
        print("✅ サンプルデータの投入が完了しました！")
        
        # 作成されたデータの概要を表示
        print("\n=== データ概要 ===")
        print(f"ユーザー数: {len(users)}")
        print(f"スタンド数: {len(stations)}")
        print(f"バッテリー数: {len(batteries)}")
        print(f"利用履歴数: {session.query(Rental).count()}")
        
        print("\n=== ログイン情報 ===")
        for user in users:
            print(f"メール: {user.email} / パスワード: password123 / 残高: ¥{user.balance_cents}")
            
    except Exception as e:
        session.rollback()
        print(f"❌ データ投入に失敗しました: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
