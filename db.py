"""
db.py - データベース接続・セッション管理
=====================================================
【設計意図】
- SQLAlchemyのセッション管理を一元化
- ローカル（SQLite）と本番（PostgreSQL）の切り替え対応
- トランザクション管理の基盤を提供

【セッション利用方法】
session = get_session()
try:
    # データベース操作
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()
=====================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from variables import DATABASE_URL
from models import Base

# ============================================================
# エンジン作成
# - echo=True: 発行されるSQLをコンソールに表示（デバッグ用）
# - future=True: SQLAlchemy 2.0スタイルを使用
# ============================================================
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQLログ出力（授業で見せる用）
    future=True
)

# ============================================================
# セッションファクトリ
# - expire_on_commit=False: コミット後もオブジェクトにアクセス可能
# - autoflush=False: 明示的なflush/commitを要求
# ============================================================
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    future=True
)


def get_session():
    """
    セッションを取得する
    
    【使用例】
    session = get_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        session.commit()
    finally:
        session.close()
    """
    return SessionLocal()


@contextmanager
def get_session_context():
    """
    コンテキストマネージャーでセッションを管理
    
    【使用例】
    with get_session_context() as session:
        user = session.query(User).filter_by(email=email).first()
        # 自動的にcloseされる
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db():
    """
    データベースの初期化（テーブル作成）
    
    【注意】
    - 既存テーブルは削除されない（create_all）
    - 本番ではマイグレーションツール（Alembic）推奨
    """
    Base.metadata.create_all(bind=engine)
    print("✅ データベーステーブルを作成しました")


def drop_all_tables():
    """
    全テーブル削除（開発用）
    
    【警告】本番環境では使用しないこと
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ 全テーブルを削除しました")


# ============================================================
# スクリプトとして実行時: テーブル初期化
# ============================================================
if __name__ == "__main__":
    init_db()
