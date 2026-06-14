# 初回実装 タスクリスト

進捗状況は `[ ]` 未着手 / `[x]` 完了 で管理する。

## フェーズ1: バックエンド基盤・認証

- [x] `backend/` プロジェクト初期化（uv, pyproject.toml, FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, Ruff, pytest）
- [x] `core/config.py` 作成（環境変数: DB接続情報, JWTシークレット等）、`.env.example` 作成
- [x] `db/base.py`, `db/session.py` 作成
- [x] `models/user.py`, `models/book.py`, `models/tag.py` 作成（USERS, BOOKS, TAGS, BOOK_TAGS）
- [x] Alembic初期マイグレーション作成・適用
- [ ] `core/security.py` 作成（パスワードハッシュ、JWT発行・検証）
- [ ] `schemas/auth.py`, `schemas/user.py` 作成
- [ ] `services/auth_service.py` 作成（ユーザー登録、認証）
- [ ] `api/deps.py` 作成（`get_current_user` 依存関数）
- [ ] `api/routes/auth.py` 作成（`POST /api/auth/register`, `POST /api/auth/login`）
- [ ] `tests/api/test_auth.py` 作成（登録・ログイン・不正なパスワード等）
- [ ] `ruff check` / `ruff format --check` / `pytest` 実行・成功確認

## フェーズ2: バックエンド 書籍・タグAPI

- [ ] `schemas/book.py`, `schemas/tag.py` 作成
- [ ] `services/tag_service.py` 作成（一覧、登録、リネーム、削除）
- [ ] `api/routes/tags.py` 作成（`GET/POST /api/tags`, `PUT/DELETE /api/tags/{id}`）
- [ ] `services/book_service.py` 作成（CRUD、検索・並び替え・ページネーション、タグ紐付け）
- [ ] `api/routes/books.py` 作成（`GET/POST /api/books`, `GET/PUT/DELETE /api/books/{id}`）
- [ ] 認可チェック（他ユーザーのデータへのアクセスは404）の実装
- [ ] `tests/api/test_tags.py` 作成（CRUD、重複エラー、認可）
- [ ] `tests/api/test_books.py` 作成（CRUD、検索、並び替え、ページネーション、認可）
- [ ] `ruff check` / `ruff format --check` / `pytest` 実行・成功確認

## フェーズ3: フロントエンド基盤・認証画面

- [ ] `frontend/` プロジェクト初期化（Vite + React + TypeScript）
- [ ] Tailwind CSS セットアップ
- [ ] ESLint, Prettier, Vitest, React Testing Library セットアップ
- [ ] React Router セットアップ、`App.tsx` にルーティング定義
- [ ] TanStack Query セットアップ
- [ ] `api/client.ts` 作成（JWT付与、`/api`へのプロキシ設定）
- [ ] `types/user.ts`, `api/authApi.ts` 作成
- [ ] `hooks/useAuth.ts` 作成（ログイン状態管理、未ログイン時リダイレクト）
- [ ] `components/layout/Header` 作成
- [ ] `pages/LoginPage` 作成
- [ ] `pages/RegisterPage` 作成
- [ ] `npm run lint` / `npm run typecheck` / `npm run test` 実行・成功確認

## フェーズ4: フロントエンド 書籍・タグ画面

- [ ] `types/book.ts`, `types/tag.ts`, `api/booksApi.ts`, `api/tagsApi.ts` 作成
- [ ] `hooks/useBooks.ts`, `hooks/useTags.ts` 作成
- [ ] `components/common/SearchBox`, `Pagination`, `SortableHeader` 作成
- [ ] `components/book/StatusBadge`, `RatingStars`, `TagInput` 作成
- [ ] `pages/BookListPage` 作成（一覧・検索・並び替え・ページネーション）
- [ ] `components/book/BookForm` 作成
- [ ] `pages/BookCreatePage` 作成
- [ ] `pages/BookEditPage` 作成
- [ ] `pages/BookDetailPage` 作成
- [ ] `pages/TagManagePage` 作成（一覧・登録・編集・削除）
- [ ] `components/book/BookTable` 作成
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
