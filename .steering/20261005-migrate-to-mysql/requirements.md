# 要求定義：DBエンジンのSQLiteからMySQLへの移行

## 背景・目的

現在、バックエンドのDBエンジンにはSQLite（ファイルDB）を採用しているが、個人利用規模を超えた**本番運用を見据え**、スケーラビリティと運用実績のあるMySQLへ移行する。

## 変更内容の概要

- 本番・開発・テストの全環境において、DBエンジンをSQLiteからMySQL 8.0へ変更する
- 開発環境はDocker Compose（`.devcontainer/docker-compose.yml`）にMySQLサービスを追加して用意する
- テスト（pytest）もMySQLに統一し、SQLite固有の方言差異に起因するバグを防ぐ
- 既存のAlembicマイグレーション（`26bb49e77b83_create_initial_tables.py`）はMySQL向けに作り直す（SQLite用DBファイルは本番投入前のためデータ移行は不要）

## 受け入れ条件

- [ ] バックエンドの接続設定（`DATABASE_URL`）がMySQL接続文字列になっている
- [ ] ローカル開発環境で `docker compose up` 相当の操作によりMySQLコンテナが起動し、バックエンドがMySQLに接続できる
- [ ] Alembicマイグレーションを実行し、MySQL上にスキーマが作成できる
- [ ] `pytest` がMySQL（テスト用DB/スキーマ）に対して実行され、既存テストがすべてパスする
- [ ] GitHub Actions（`backend-ci.yml`）のテストジョブでもMySQLサービスコンテナを使ってテストが実行される
- [ ] `docs/architecture.md` のDB記載がMySQLに更新されている（対応済み）
- [ ] 不要になったSQLite関連の記述・ファイル（`book_shelf.db`、SQLite専用の分岐コードなど）が整理されている

## 制約事項

- SQLAlchemy 2.0 + Alembicの構成は維持し、ORM/マイグレーションの仕組み自体は変更しない
- 認証・API仕様など、DB以外の機能・振る舞いに変更を加えない
- 既存のSQLiteデータ（`book_shelf.db`）の移行（データ移行バッチ等）は本要求の対象外とする（開発中のダミーデータのため）
