# 技術仕様書

## 1. テクノロジースタック

### 1.1 フロントエンド
| 項目 | 採用技術 | 説明 |
|---|---|---|
| 言語 | TypeScript | 型安全性を確保 |
| フレームワーク | React | UI構築 |
| ビルドツール | Vite | 開発サーバー・ビルド |
| ルーティング | React Router | ページ遷移・URLクエリパラメータ管理 |
| スタイリング | Tailwind CSS | 共通のデザインシステム（CLAUDE.md準拠） |
| サーバー状態管理 | TanStack Query (React Query) | API通信・キャッシュ・再取得 |
| HTTPクライアント | fetch（axiosは使用しない） | APIクライアント |
| フォーム | React Hook Form + Zod | 入力管理・バリデーション |
| パッケージ管理 | npm | 依存パッケージ管理 |
| Lint/Format | ESLint + Prettier | コード品質・整形 |
| テスト | Vitest + React Testing Library | 単体・コンポーネントテスト |

### 1.2 バックエンド
| 項目 | 採用技術 | 説明 |
|---|---|---|
| 言語 | Python | 3.12以上 |
| フレームワーク | FastAPI | REST API |
| ASGIサーバー | Uvicorn | アプリケーションサーバー |
| ORM | SQLAlchemy 2.0 | データベースアクセス |
| マイグレーション | Alembic | スキーマ管理 |
| バリデーション | Pydantic v2 | リクエスト/レスポンスのスキーマ定義 |
| 認証 | JWT（python-jose） + passlib（パスワードハッシュ, argon2） | ログイン・トークン発行 |
| パッケージ管理 | uv | 依存パッケージ管理・実行 |
| Lint/Format | Ruff | コード品質・整形 |
| テスト | pytest + httpx | 単体・APIテスト |

### 1.3 データベース
| 項目 | 採用技術 | 説明 |
|---|---|---|
| DB | SQLite | 個人利用規模のため軽量なファイルDBを採用 |

- 将来的にPostgreSQL等への移行が必要になった場合も、SQLAlchemy + Alembicによる抽象化により切り替えコストを抑える

## 2. 開発ツールと手法

### 2.1 開発環境
- 開発環境はDevContainer（`.devcontainer/`）上で構築し、環境差異を吸収する
- フロントエンド・バックエンドは別々のプロセスとして起動し、Viteの開発サーバーからFastAPIへAPIリクエストをプロキシする

### 2.2 ディレクトリ構成（概要）
```
/
├── backend/        # FastAPIアプリケーション
├── frontend/       # React + TypeScript + Viteアプリケーション
├── docs/           # 永続的ドキュメント
└── .steering/      # 作業単位のドキュメント
```
詳細は `docs/repository-structure.md` で定義する。

### 2.3 品質チェック
- フロントエンド: `npm run lint`（ESLint）、`npm run typecheck`（tsc）、`npm run test`（Vitest）
- バックエンド: `ruff check`、`ruff format --check`、`pytest`
- コード変更後は必ずリント・型チェック・テストを実施する（CLAUDE.md準拠）

## 3. 技術的制約と要件

- 認証はJWTによるトークンベース認証とし、APIはステートレスとする
- フロントエンドはAccess Tokenをブラウザの保存領域（localStorage想定）に保持し、APIリクエスト時に `Authorization: Bearer <token>` ヘッダーを付与する
- バックエンドAPIはすべて `/api` 配下に配置し、フロントエンドとの責務を明確に分離する
- 自分以外のユーザーのデータにアクセスできないよう、APIレベルで認可チェックを行う
- 入力バリデーションはフロントエンド（Zod）・バックエンド（Pydantic）の両方で行う（多層防御）
- SQLインジェクション対策としてSQLAlchemyのORM/クエリビルダ経由でのみDBアクセスを行う（生SQL文字列結合は行わない）
- XSS対策として、Reactのデフォルトのエスケープ処理に依存し、`dangerouslySetInnerHTML` は使用しない

## 4. パフォーマンス要件

- 個人利用規模（蔵書数: 〜数千件程度）を想定し、特別なキャッシュ層やスケーリング対応は行わない
- 一覧取得APIはページネーション（デフォルト20件/ページ）により、レスポンスサイズを抑える
- 検索・並び替えはDB側（SQLクエリ）で実施し、全件取得後にアプリケーション側でフィルタリングしない
