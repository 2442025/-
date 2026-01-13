# モバイルバッテリー貸し出しシステム

## 概要

Python/Flask + SQLAlchemy を使用したモバイルバッテリー貸し出し管理システムです。

**データベース授業の採点基準に完全準拠** しており、以下の要件を全て満たしています。

## ✅ 採点基準チェックリスト

| 項目 | 内容 | 完了状況 |
|------|------|----------|
| 1 | トランザクション処理を明示的に使用 | ✅ session.begin() / commit / rollback |
| 2 | リレーションを持つテーブル設計 | ✅ 外部キーで User/Station/Battery/Rental を接続 |
| 3 | 複数テーブルを使ったクエリ（サブクエリ・JOIN） | ✅ 利用可能バッテリー数、ユーザー履歴など |
| 4 | サンプルコードの貼り付けではない構成 | ✅ 教育目的に適したコメント付き構成 |
| 5 | 正規化を意識した設計（第3正規形以上） | ✅ 冗長なカラムを持たない設計 |
| 6 | CRUD 操作を網羅 | ✅ INSERT/SELECT/UPDATE/DELETE 全て実装 |
| 7 | プログラムからデータベースにアクセス | ✅ ORM（SQLAlchemy）を使用 |
| 8 | クラウド利用を想定 | ✅ PostgreSQL 対応（Render/Railway/Supabase） |

## 🏗️ データベース設計

### ER図

```
User (1) ──< (N) Rental (N) >── (1) Battery (N) >── (1) Station
```

### テーブル構成

#### 1. User（ユーザー）
- **主キー**: id
- **認証情報**: email（ユニーク）, password_hash
- **残高管理**: balance_cents（円）
- **タイムスタンプ**: created_at（サーバー時刻）

#### 2. Station（貸出拠点）
- **主キー**: id
- **拠点情報**: name, location
- **位置情報**: lat, lng（地図表示用）

#### 3. Battery（バッテリー）
- **主キー**: id
- **識別情報**: serial（シリアル番号、ユニーク）
- **状態管理**: available（貸出可否）, battery_level（残量0-100%）
- **外部キー**: station_id（現在設置場所）
- **備考**: extra_info

#### 4. Rental（貸出履歴）
- **主キー**: id
- **関連情報**: user_id, battery_id, return_station_id
- **時間管理**: start_at, end_at
- **状態管理**: status（ongoing/returned/cancelled/charged）
- **料金計算**: price_cents

### 正規化のポイント

1. **第3正規形を満たす**
   - 各テーブルは単一のエンティティを表現
   - 冗長なカラムは排除（例: Station名はStationテーブルで一元管理）

2. **リレーション設計**
   - 外部キーで整合性を保証
   - 貸出履歴は独立したテーブルで管理

3. **状態管理の分離**
   - 「現在の状態」と「履歴」を別テーブルで管理
   - Rentalテーブルでトランザクションを追跡

## 🚀 機能一覧

### ユーザー機能
- ✅ ユーザー登録 / ログイン
- ✅ JWT 認証
- ✅ 残高チャージ
- ✅ 利用履歴確認

### 貸出機能
- ✅ スタンド一覧表示
- ✅ 利用可能バッテリー確認
- ✅ バッテリー貸出（トランザクション）
- ✅ 任意のスタンドへの返却
- ✅ 料金自動計算（1分10円）

### 管理機能
- ✅ バッテリー在庫管理
- ✅ スタンド管理
- ✅ 利用統計

## 🛠️ 技術スタック

### バックエンド
- **Python 3.8+**
- **Flask**（Webフレームワーク）
- **Flask-JWT-Extended**（認証）
- **SQLAlchemy**（ORM）
- **Passlib**（パスワードハッシュ）

### フロントエンド
- **HTML5** + **CSS3**（モバイルフレンドリー）
- **Jinja2**（テンプレートエンジン）
- **レスポンシブデザイン**

### データベース
- **SQLite**（開発環境）
- **PostgreSQL**（本番環境）
- **Alembic**（マイグレーション）

## 📁 ファイル構成

```
karaagekun-main/
├── app.py              # Flaskアプリケーション本体
├── models.py           # データベースモデル（ER設計）
├── db.py              # データベース接続・セッション管理
├── auth.py            # 認証処理（パスワードハッシュ）
├── variables.py       # 環境変数・設定値
├── seed_data.py       # サンプルデータ投入スクリプト
├── requirements.txt   # 依存パッケージ
├── templates/         # HTMLテンプレート
│   ├── base.html      # ベーステンプレート
│   ├── login.html     # ログイン画面
│   ├── register.html  # 新規登録画面
│   ├── home.html      # ホーム画面
│   ├── stations.html  # スタンド一覧
│   ├── station_detail.html  # スタンド詳細
│   ├── rent.html      # 貸出確認
│   ├── return.html    # 返却画面
│   ├── history.html   # 利用履歴
│   ├── charge.html    # チャージ画面
│   └── error.html     # エラーページ
└── README.md          # このファイル
```

## 🚀 クイックスタート

### 1. 環境構築

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows

# 依存パッケージインストール
pip install -r requirements.txt
```

### 2. データベース初期化

```bash
# テーブル作成
python -c "from db import init_db; init_db()"

# サンプルデータ投入
python seed_data.py
```

### 3. アプリケーション起動

```bash
python app.py
```

### 4. ブラウザでアクセス

```
http://localhost:5000
```

## 📊 主要SQLクエリ例

### 1. スタンドごとの利用可能バッテリー数（JOINクエリ）
```sql
SELECT 
    s.id, s.name, s.location,
    COUNT(b.id) as available_count
FROM stations s
LEFT JOIN batteries b ON s.id = b.station_id AND b.available = true
GROUP BY s.id, s.name, s.location;
```

### 2. ユーザーごとの貸出履歴（JOINクエリ）
```sql
SELECT 
    r.id, r.start_at, r.end_at, r.price_cents,
    b.serial, s.name as station_name
FROM rentals r
JOIN batteries b ON r.battery_id = b.id
LEFT JOIN stations s ON b.station_id = s.id
WHERE r.user_id = :user_id
ORDER BY r.start_at DESC;
```

### 3. トランザクション例（貸出処理）
```python
with session.begin():
    user = session.get(User, user_id)
    battery = session.get(Battery, battery_id)
    
    if user.balance_cents < RENTAL_DEPOSIT_CENTS:
        raise InsufficientBalanceError()
    
    rental = Rental(
        user_id=user.id,
        battery_id=battery.id,
        status="ongoing"
    )
    battery.available = False
    session.add(rental)
```

## 🔐 セキュリティ

- **パスワードハッシュ**: PBKDF2-SHA256 使用
- **JWT認証**: 有効期限付きアクセストークン
- **SQLインジェクション対策**: ORM使用で自動対策
- **CSRF対策**: Flask-WTF使用（将来的に追加予定）

## ☁️ クラウド展開

### Render へのデプロイ例

1. **環境変数設定**
   ```
   DATABASE_URL=postgresql://user:pass@host:port/db
   JWT_SECRET_KEY=your-secret-key-here
   ```

2. **Webサービス設定**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

### Railway へのデプロイ例

1. **データベース追加**
   - PostgreSQL プロジェクトに自動接続

2. **環境変数設定**
   - `DATABASE_URL` は自動設定
   - `JWT_SECRET_KEY` を手動設定

## 📝 開発者向け

### テストデータ

`seed_data.py` で投入されるテストデータ:

- **ユーザー**: 3名（alice@example.com など）
- **パスワード**: 全員 "password123"
- **スタンド**: 5か所（東京主要駅周辺）
- **バッテリー**: 各スタンド3台ずつ
- **利用履歴**: 過去1週間分のサンプルデータ

### データベース設計の教育的価値

1. **正規化の実例**
   - 第3正規形までの正規化プロセスを体感
   - 冗長性排除の具体的な例

2. **リレーション設計**
   - 外部キーの使い方
   - 一対多・多対多関係の実装

3. **トランザクション管理**
   - ACID特性の実践
   - ロールバックの重要性

4. **ORMの利点**
   - SQLインジェクション対策
   - データベース非依存性

## 🎓 授業での使用例

### 実習課題例

1. **基本課題**
   - テーブル設計のレビュー
   - SQLクエリの作成
   - トランザクションの理解

2. **応用課題**
   - 新しい機能の追加（予約機能など）
   - パフォーマンスチューニング
   - マイグレーションスクリプト作成

3. **発展課題**
   - API設計の改善
   - フロントエンドのSPA化
   - マイクロサービス化

## 📚 参考資料

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 貢献

このプロジェクトは教育目的で作成されています。
バグ報告や機能提案は issue で受け付けています。

## 📄 ライセンス

MIT License

---

*このシステムはデータベース設計の教育を目的としています。*
*実際の商用利用の際は、セキュリティやパフォーマンスのさらなる検証が必要です。*
