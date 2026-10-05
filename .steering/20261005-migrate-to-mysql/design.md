# 設計：DBエンジンのSQLiteからMySQLへの移行

## 1. 実装アプローチ

本番・開発・テストの全環境でMySQL 8.0を使用する。既存データは開発用ダミーデータのみのため、マイグレーションは作り直し（新規1本）とし、データ移行は行わない。

## 2. 変更するコンポーネント

### 2.1 依存パッケージ（`backend/pyproject.toml`）
- `pymysql` を依存関係に追加（SQLAlchemyのMySQL用DBAPIドライバ）

### 2.2 接続設定
- `backend/.env.example`
  - `DATABASE_URL=mysql+pymysql://book_shelf:book_shelf@mysql:3306/book_shelf` に変更
- `backend/app/core/config.py`
  - `database_url` のデフォルト値を上記MySQL接続文字列に変更
- `backend/app/db/session.py`
  - SQLite専用だった `connect_args`（`check_same_thread`）の分岐・コメントを削除し、MySQL前提のシンプルな `create_engine(settings.database_url)` にする

### 2.3 モデル定義（MySQL対応のためString長を明示）
MySQLはインデックス付きカラムに長さ指定のない`VARCHAR`/`TEXT`を使えないため、以下を明示的な長さ付き`String`に変更する。
- `app/models/user.py`：`email: String(255)`（unique index対象）、`password_hash: String(255)`
- `app/models/book.py`：`title: String(255)`、`author: String(255)`
- `app/models/tag.py`：`name: String(100)`（unique constraintの一部）

### 2.4 Alembicマイグレーション
- 既存の `alembic/versions/26bb49e77b83_create_initial_tables.py` を削除し、上記モデル変更を反映した新規の初期マイグレーションを作り直す（`alembic revision --autogenerate`）
- 併せて、SQLite方言依存だった `server_default=sa.text("(CURRENT_TIMESTAMP)")`（括弧付き）が `sa.text("CURRENT_TIMESTAMP")`（括弧なし、MySQL互換）として生成されることを確認する

### 2.5 開発環境（Docker Compose）
`.devcontainer/docker-compose.yml` に `mysql` サービスを追加する。
- イメージ：`mysql:8.0`
- 環境変数：`MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD`
- 永続化用のnamed volume（`mysql-data`）をマウント
- ヘルスチェックを設定し、`backend` サービスは `depends_on.mysql.condition: service_healthy` で起動順序を保証
- `backend` サービスの環境変数 `DATABASE_URL` をMySQLサービス名（`mysql`）をホストとする接続文字列に設定

### 2.6 テスト（`backend/tests/conftest.py`）
- SQLiteのin-memory（`sqlite://` + `StaticPool`）をやめ、MySQL（Docker Composeの`mysql`サービス、テスト用DB名 `book_shelf_test`）に接続する構成に変更
- テスト用の `DATABASE_URL`（例：環境変数 `TEST_DATABASE_URL`、未設定時はdocker-compose上の`mysql`ホストを既定値とする）を読み、`create_engine` する
- 各テストの `client` フィクスチャ内で `Base.metadata.create_all` → テスト実行 → `Base.metadata.drop_all` を行う方針は維持（テーブル単位の作り直しで、テスト間のデータ競合を防ぐ）
- `StaticPool`/`check_same_thread` はMySQLでは不要なため削除

### 2.7 CI（`.github/workflows/backend-ci.yml`）
- `test` ジョブに GitHub Actions の `services:` を使ってMySQLコンテナ（`mysql:8.0`）を追加し、ヘルスチェック付きで起動を待機する
- `TEST_DATABASE_URL`（または `DATABASE_URL`）環境変数をジョブに設定し、`pytest` 実行時にMySQLサービスコンテナへ接続する
- `lint` ジョブはDB接続が不要なため変更なし

### 2.8 クリーンアップ
- ルートの `backend/book_shelf.db`（開発用SQLiteファイル）を削除する
- `app/db/session.py` 内のSQLite関連コメントを、MySQL前提の説明に書き換える

## 3. データ構造の変更

- テーブル構造（`users` / `books` / `tags` / `book_tags`）自体は変更しない
- 変更は上記2.3のとおり、一部`String`カラムへの長さ指定の追加のみ

## 4. 影響範囲の分析

| 対象 | 影響 | 備考 |
|---|---|---|
| バックエンドAPIのロジック（services/routes） | なし | DBアクセスはすべてORM経由のため影響なし |
| フロントエンド | なし | API仕様・レスポンス形式に変更はない |
| 既存テストコード（test_auth.py等） | なし（想定） | DB接続方式のみ変更、アサーション対象は変わらない |
| 開発環境の起動手順 | あり | MySQLコンテナの起動が追加で必要（Docker Compose経由で自動化） |
| CI実行時間 | 若干増加 | MySQLサービスコンテナの起動待ちが発生 |
