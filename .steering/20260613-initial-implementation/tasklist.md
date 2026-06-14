# 初回実装 タスクリスト

進捗状況は `[ ]` 未着手 / `[x]` 完了 で管理する。

## フェーズ1: バックエンド基盤・認証

- [x] `backend/` プロジェクト初期化（uv, pyproject.toml, FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, Ruff, pytest）
- [x] `core/config.py` 作成（環境変数: DB接続情報, JWTシークレット等）、`.env.example` 作成
- [x] `db/base.py`, `db/session.py` 作成
- [x] `models/user.py`, `models/book.py`, `models/tag.py` 作成（USERS, BOOKS, TAGS, BOOK_TAGS）
- [x] Alembic初期マイグレーション作成・適用
- [x] `core/security.py` 作成（パスワードハッシュ、JWT発行・検証）
- [x] `schemas/auth.py`, `schemas/user.py` 作成
- [x] `services/auth_service.py` 作成（ユーザー登録、認証）
- [x] `api/deps.py` 作成（`get_current_user` 依存関数）
- [x] `api/routes/auth.py` 作成（`POST /api/auth/register`, `POST /api/auth/login`）
- [x] `tests/api/test_auth.py` 作成（登録・ログイン・不正なパスワード等）
- [x] `ruff check` / `ruff format --check` / `pytest` 実行・成功確認

## フェーズ2: バックエンド 書籍・タグAPI

- [x] `schemas/book.py`, `schemas/tag.py` 作成
- [x] `services/tag_service.py` 作成（一覧、登録、リネーム、削除）
- [x] `api/routes/tags.py` 作成（`GET/POST /api/tags`, `PUT/DELETE /api/tags/{id}`）
- [x] `services/book_service.py` 作成（CRUD、検索・並び替え・ページネーション、タグ紐付け）
- [x] `api/routes/books.py` 作成（`GET/POST /api/books`, `GET/PUT/DELETE /api/books/{id}`）
- [x] 認可チェック（他ユーザーのデータへのアクセスは404）の実装
- [x] `tests/api/test_tags.py` 作成（CRUD、重複エラー、認可）
- [x] `tests/api/test_books.py` 作成（CRUD、検索、並び替え、ページネーション、認可）
- [x] `ruff check` / `ruff format --check` / `pytest` 実行・成功確認

## フェーズ3: フロントエンド基盤・認証画面

### 3.1 プロジェクト初期化

- [x] `frontend/` プロジェクト作成（Vite + React + TypeScriptテンプレート）
- [x] 不要なボイラープレート（サンプルコード・アセット）の削除・整理
- [x] Tailwind CSS インストール・設定（`tailwind.config`, `postcss.config`, グローバルCSS）
- [x] ESLint セットアップ（プロジェクトのルールに合わせて設定）
- [x] Prettier セットアップ
- [x] Vitest + React Testing Library セットアップ
- [x] Vite開発サーバーのプロキシ設定（`/api` → バックエンド）

### 3.2 ルーティング・データ取得の土台

- [ ] React Router インストール・最小限のルーティング定義（空のページでルートのみ確認）
- [ ] TanStack Query インストール・`QueryClientProvider` 設定

### 3.3 認証関連

- [ ] `types/user.ts` 作成（ユーザー・トークンの型定義）
- [ ] `api/client.ts` 作成（fetchラッパー、JWT付与）
- [ ] `api/authApi.ts` 作成（登録・ログインAPI呼び出し）
- [ ] `hooks/useAuth.ts` 作成（ログイン状態管理、トークン保存・読み込み）
- [ ] 未ログイン時に `LoginPage` へリダイレクトするルートガードの実装

### 3.4 画面

- [ ] `components/layout/Header` 作成（ナビゲーション・ログアウト）
- [ ] `pages/LoginPage` 作成
- [ ] `pages/RegisterPage` 作成
- [ ] `App.tsx` のルーティングを最終構成に更新（Header・ガードを組み込み）

### 3.5 品質チェック

- [ ] `npm run lint` / `npm run typecheck` / `npm run test` 実行・成功確認

## フェーズ4: フロントエンド 書籍・タグ画面

### 4.1 型・APIクライアント

- [ ] `types/book.ts`, `types/tag.ts` 作成
- [ ] `api/booksApi.ts` 作成（CRUD・検索・並び替え・ページネーション）
- [ ] `api/tagsApi.ts` 作成（CRUD）

### 4.2 データ取得フック

- [ ] `hooks/useBooks.ts` 作成（一覧取得・作成・更新・削除）
- [ ] `hooks/useTags.ts` 作成（一覧取得・作成・更新・削除）

### 4.3 共通コンポーネント

- [ ] `components/common/SearchBox` 作成
- [ ] `components/common/Pagination` 作成
- [ ] `components/common/SortableHeader` 作成

### 4.4 書籍関連コンポーネント

- [ ] `components/book/StatusBadge` 作成
- [ ] `components/book/RatingStars` 作成
- [ ] `components/book/TagInput` 作成
- [ ] `components/book/BookTable` 作成
- [ ] `components/book/BookForm` 作成

### 4.5 画面

- [ ] `pages/BookListPage` 作成（一覧・検索・並び替え・ページネーションを統合）
- [ ] `pages/BookCreatePage` 作成
- [ ] `pages/BookEditPage` 作成
- [ ] `pages/BookDetailPage` 作成
- [ ] `pages/TagManagePage` 作成（一覧・登録・編集・削除）

### 4.6 品質チェック

- [ ] `npm run lint` / `npm run typecheck` / `npm run test` 実行・成功確認

## フェーズ5: 結合確認

- [ ] バックエンド・フロントエンドを同時起動し、E2Eで一連の操作を確認
  - [ ] ユーザー登録・ログイン・ログアウト
  - [ ] 書籍の登録・編集・削除・詳細表示
  - [ ] タグの登録・編集・削除、書籍へのタグ付け
  - [ ] 検索・並び替え・ページネーション
  - [ ] 他ユーザーのデータにアクセスできないことの確認
- [ ] `docs/` の記載内容と実装に差異がないか最終確認

## 完了条件

- 全フェーズのチェックリストが完了している
- バックエンド・フロントエンドともにリント・型チェック・テストが成功する
- `docs/product-requirements.md` の受け入れ条件をすべて満たす
