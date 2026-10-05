# タスクリスト：DBエンジンのSQLiteからMySQLへの移行

- [x] 1. 依存パッケージ追加：`backend/pyproject.toml` に `pymysql` を追加し、`uv sync` で反映する
- [x] 2. 接続設定変更：`.env.example` と `app/core/config.py` のデフォルト `database_url` をMySQL接続文字列に変更する
- [x] 3. `app/db/session.py` のSQLite専用分岐・コメントを削除し、MySQL前提の実装に簡素化する
- [x] 4. モデル修正：`User.email`/`password_hash`、`Book.title`/`author`、`Tag.name` に明示的な `String` 長を設定する
- [x] 5. Alembicマイグレーション作り直し：既存の初期マイグレーションを削除し、MySQL向けに新規の初期マイグレーションを生成する
- [x] 6. Docker Compose変更：`.devcontainer/docker-compose.yml` に `mysql` サービスを追加し、`backend` サービスの `DATABASE_URL`／起動順序（ヘルスチェック）を設定する
- [x] 7. テスト設定変更：`backend/tests/conftest.py` をMySQL（テスト用DB）接続に変更する
- [x] 8. CI変更：`.github/workflows/backend-ci.yml` の `test` ジョブにMySQLサービスコンテナを追加し、テスト用`DATABASE_URL`を設定する
- [x] 9. クリーンアップ：`backend/book_shelf.db` を削除する
- [ ] 10. 動作確認：Docker Compose上でMySQLに接続しマイグレーション適用、`pytest` 実行、lint/型チェックを実施する
  - [x] lint（`ruff check` / `ruff format --check`）は実施済み・パス
  - [ ] Docker ComposeでのMySQL起動確認、Alembicマイグレーション適用、`pytest` 実行は本セッション環境にDockerが無いため未実施（ユーザー環境での確認が必要）
