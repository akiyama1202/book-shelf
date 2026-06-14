# 初回実装 設計

## 1. 実装アプローチ

初回実装のため、新規にバックエンド・フロントエンドのプロジェクトを構築する。
`docs/architecture.md` および `docs/repository-structure.md` で定義した構成・技術スタックに従う。

実装は以下の順序で進める。依存関係上、バックエンドを先行させる。

1. バックエンド: プロジェクト初期化・DB・認証
2. バックエンド: 書籍・タグAPI
3. フロントエンド: プロジェクト初期化・認証画面
4. フロントエンド: 書籍・タグ画面

各フェーズの完了時にリント・型チェック・テストを実行し、品質を確認する。

## 2. 作成するコンポーネント・モジュール

### 2.1 バックエンド（`backend/`）

`docs/repository-structure.md` の構成に従い、以下を作成する。

| レイヤ | モジュール | 内容 |
|---|---|---|
| models | `user.py`, `book.py`, `tag.py` | SQLAlchemyモデル（USERS, BOOKS, TAGS, BOOK_TAGS） |
| schemas | `auth.py`, `user.py`, `book.py`, `tag.py` | Pydanticスキーマ（リクエスト/レスポンス） |
| services | `auth_service.py`, `book_service.py`, `tag_service.py` | ビジネスロジック（認証、CRUD、検索・並び替え・ページネーション） |
| api/routes | `auth.py`, `books.py`, `tags.py` | `/api/auth`, `/api/books`, `/api/tags` のルーター |
| core | `config.py`, `security.py` | 設定値、JWT発行・検証、パスワードハッシュ |
| db | `base.py`, `session.py` | DBエンジン・セッション、Declarative Base |
| alembic | 初期マイグレーション | USERS, BOOKS, TAGS, BOOK_TAGS の作成 |

認可の共通処理（`get_current_user` 依存関数）は `api/deps.py` に実装し、各ルーターで使用する。

### 2.2 フロントエンド（`frontend/`）

`docs/repository-structure.md` の構成に従い、以下を作成する。

| 種別 | モジュール | 内容 |
|---|---|---|
| pages | `LoginPage`, `RegisterPage`, `BookListPage`, `BookCreatePage`, `BookEditPage`, `BookDetailPage`, `TagManagePage` | 画面単位のコンポーネント |
| components/layout | `Header` | ナビゲーション・ログアウト |
| components/book | `BookTable`, `BookForm`, `StatusBadge`, `RatingStars`, `TagInput` | 書籍関連の再利用コンポーネント |
| components/common | `SearchBox`, `Pagination`, `SortableHeader` | 共通UIコンポーネント |
| hooks | `useAuth`, `useBooks`, `useTags` | 認証状態・書籍データ・タグデータ管理 |
| api | `client`, `authApi`, `booksApi`, `tagsApi` | APIクライアント（JWT付与） |
| types | `user.ts`, `book.ts`, `tag.ts` | 型定義 |

ルーティングは `App.tsx` で定義し、未ログイン時は `LoginPage` へリダイレクトするガードを設ける。

## 3. データ構造

`docs/functional-design.md` の「2. データモデル定義（ER図）」に定義したテーブル（USERS, BOOKS, TAGS, BOOK_TAGS）をAlembicの初期マイグレーションで作成する。
詳細なカラム定義・制約はそのドキュメントを正とする。

## 4. 影響範囲の分析

初回実装のため既存コードへの影響はないが、以下を新規に整備する。

- `backend/` `frontend/` の各プロジェクト初期設定（依存パッケージ、Lint/Format設定、テスト設定）
- `.env.example`（DB接続情報、JWTシークレット等のテンプレート）
- `.devcontainer/` の起動コマンド・ポート設定が、新規に追加するバックエンド/フロントエンドの起動方法と整合していることを確認する
