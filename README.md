# book-shelf

本棚管理アプリケーション

## 🚀 Claude Code開発環境のセットアップ

このプロジェクトはDockerコンテナ内でClaude Codeを使用して開発できます。

### 前提条件

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### セットアップ手順

1. **環境変数の設定**

   `.env.example`をコピーして`.env`ファイルを作成します：
   ```bash
   cp .env.example .env
   ```

   `.env`ファイルを編集し、Anthropic API Keyを設定します：
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

   APIキーは[Anthropic Console](https://console.anthropic.com/settings/keys)から取得できます。

2. **Dev Containerで開く**

   VS Codeでこのプロジェクトを開き、コマンドパレット（`Cmd+Shift+P` / `Ctrl+Shift+P`）から：
   ```
   Dev Containers: Reopen in Container
   ```
   を選択します。

3. **Claude Codeの起動**

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