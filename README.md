# book-shelf

本棚管理アプリケーション

## 📚 概要

読んだ本・読みたい本を個人で記録・管理するための、シンプルな書籍管理システムです。

- ユーザー登録・ログイン（JWT認証）
- 書籍の登録・編集・削除・詳細表示
- 書籍一覧（検索・並び替え・ページネーション）
- 読書ステータス（読みたい / 未読 / 読書中 / 読了）、評価（1〜5）、タグ、メモの管理
- タグの登録・編集・削除
- 各ユーザーのデータは他ユーザーから分離（自分専用の本棚）

技術スタックは `backend/`（FastAPI + SQLAlchemy + Alembic）と `frontend/`（React + Vite + TypeScript、実装予定）。詳細は `docs/` 配下の設計ドキュメントを参照してください。

## 🚀 Claude Code開発環境のセットアップ

このプロジェクトはDockerコンテナ内でClaude Codeを使用して開発できます。

### 前提条件

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### セットアップ手順

1. **Dev Containerで開く**

   VS Codeでこのプロジェクトを開き、コマンドパレット（`Cmd+Shift+P` / `Ctrl+Shift+P`）から：
   ```
   Dev Containers: Reopen in Container
   ```
   を選択します。

2. **Claude Codeの起動**

   コンテナ内のターミナルで：
   ```bash
   claude
   ```

### 環境の特徴

- **Amazon Linux 2023ベース**: AWS本番環境と同一のOS
- **Python 3**: FastAPI開発用
- **MariaDB開発ライブラリ**: MySQL互換データベース接続用
- **Claude Code**: AIペアプログラミング環境
- **永続的な設定**: Claude Codeの設定はボリュームマウントで保持されます

### トラブルシューティング

- コンテナのリビルドが必要な場合：`Dev Containers: Rebuild Container`
- Claude Codeの認証情報はコンテナ内の`~/.claude/`に保存されます

## バックエンド（`backend/`）

FastAPI + SQLAlchemy + Alembic構成。パッケージ管理は[uv](https://docs.astral.sh/uv/)を使用します。

### セットアップ

```bash
cd backend
uv sync
cp .env.example .env
uv run alembic upgrade head
```

### 開発サーバー起動

```bash
uv run uvicorn app.main:app --reload
```

### リント・フォーマット・テスト

```bash
uv run ruff check
uv run ruff format --check
uv run pytest
```