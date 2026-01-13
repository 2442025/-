"""
variables.py - 環境変数・設定値管理
=====================================================
【設計意図】
- 環境変数で本番/開発環境を切り替え
- セキュリティ情報（SECRET_KEY）を分離
- 料金設定などのビジネスロジック定数を一元管理

【クラウド対応】
- ローカル: SQLite（mobile_battery.db）
- 本番: PostgreSQL（Render/Railway/Supabase等）
=====================================================
"""

import os
from dotenv import load_dotenv

# .envファイルがあれば読み込む
load_dotenv()

# ============================================================
# データベース接続設定
# ============================================================
# 環境変数 DATABASE_URL が設定されていればそれを使用
# なければローカルのSQLiteを使用
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mobile_battery.db")

# PostgreSQL用に接続文字列を修正（Renderなど）
# postgres:// → postgresql:// の変換
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ============================================================
# JWT認証設定
# ============================================================
# 【重要】本番環境では必ず環境変数で設定すること
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me_in_production_123!")

# トークン有効期限（秒）
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))  # 1時間

# ============================================================
# Flask設定
# ============================================================
# セッション用シークレットキー（HTMLフォームのCSRF対策等）
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "flask_secret_key_change_me!")

# デバッグモード
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# ============================================================
# 料金設定（ビジネスロジック）
# ============================================================
# 1分あたりの利用料金（cents = 円）
PRICE_PER_MINUTE_CENTS = int(os.getenv("PRICE_PER_MINUTE_CENTS", "10"))

# レンタル開始に必要な最低残高（cents = 円）
RENTAL_DEPOSIT_CENTS = int(os.getenv("RENTAL_DEPOSIT_CENTS", "500"))

# 初回チャージボーナス（cents = 円）
INITIAL_BALANCE_CENTS = int(os.getenv("INITIAL_BALANCE_CENTS", "0"))

# ============================================================
# 設定内容の確認（デバッグ用）
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("現在の設定値")
    print("=" * 50)
    print(f"DATABASE_URL: {DATABASE_URL[:30]}...")
    print(f"JWT_SECRET_KEY: {'*' * len(JWT_SECRET_KEY)}")
    print(f"PRICE_PER_MINUTE_CENTS: {PRICE_PER_MINUTE_CENTS}円/分")
    print(f"RENTAL_DEPOSIT_CENTS: {RENTAL_DEPOSIT_CENTS}円")
    print(f"DEBUG_MODE: {DEBUG_MODE}")
