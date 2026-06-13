# リポジトリ構造定義書

## 1. ルートディレクトリ構成

```
/
├── backend/            # FastAPIアプリケーション
├── frontend/           # React + TypeScript + Viteアプリケーション
├── docs/               # 永続的ドキュメント
├── .steering/          # 作業単位のドキュメント
├── .devcontainer/      # 開発コンテナ設定
├── CLAUDE.md
└── README.md
```

## 2. backend/ ディレクトリ構成

```
backend/
├── app/
│   ├── main.py             # FastAPIアプリケーションのエントリポイント
│   ├── api/
│   │   ├── deps.py         # 共通依存（認証ユーザー取得など）
│   │   └── routes/
│   │       ├── auth.py     # /api/auth/* のルーター
│   │       ├── books.py    # /api/books/* のルーター
│   │       └── tags.py     # /api/tags/* のルーター
│   ├── core/
│   │   ├── config.py       # 環境変数・設定値
│   │   └── security.py     # JWT発行・検証、パスワードハッシュ
│   ├── models/              # SQLAlchemyモデル（DBテーブル定義）
│   │   ├── user.py
│   │   ├── book.py
│   │   └── tag.py
│   ├── schemas/             # Pydanticスキーマ（リクエスト/レスポンス）
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── tag.py
│   ├── services/            # ビジネスロジック（CRUD処理）
│   │   ├── auth_service.py
│   │   ├── book_service.py
│   │   └── tag_service.py
│   └── db/
│       ├── base.py          # Declarative Base、モデル一括import
│       └── session.py       # DBセッション・エンジン定義
├── alembic/
│   ├── versions/            # マイグレーションファイル
│   └── env.py
├── tests/
│   ├── api/                  # APIエンドポイントのテスト
│   └── services/             # サービス層のテスト
├── alembic.ini
├── pyproject.toml
└── .env.example
```

### 配置ルール
- APIエンドポイント定義は `app/api/routes/` にリソース単位で配置する
- DBテーブル定義（SQLAlchemyモデル）は `app/models/`、リクエスト/レスポンス用のスキーマ（Pydantic）は `app/schemas/` に分離する
- ビジネスロジック（DB操作を含む）は `app/services/` に置き、ルーター（`routes/`）には薄いハンドラのみを記述する
- マイグレーションは Alembic で管理し、モデル変更時は必ずマイグレーションファイルを生成する
- テストは対象コードのディレクトリ構成に対応させ、`tests/` 配下に配置する

## 3. frontend/ ディレクトリ構成

```
frontend/
├── src/
│   ├── main.tsx              # エントリポイント
│   ├── App.tsx                # ルーティング定義
│   ├── pages/                 # 画面単位のコンポーネント
│   │   ├── LoginPage/
│   │   ├── RegisterPage/
│   │   ├── BookListPage/
│   │   ├── BookCreatePage/
│   │   ├── BookEditPage/
│   │   ├── BookDetailPage/
│   │   └── TagManagePage/
│   ├── components/            # 再利用可能なUIコンポーネント
│   │   ├── layout/
│   │   ├── book/
│   │   └── common/
│   ├── hooks/                 # カスタムフック
│   ├── api/                   # APIクライアント
│   ├── types/                 # 型定義
│   └── styles/                # グローバルスタイル（Tailwind設定含む）
├── public/                     # 静的ファイル
├── index.html
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── .env.example
```

### 配置ルール
- 画面単位のコンポーネントは `src/pages/` にページ名のディレクトリを作成し、その中にコンポーネント本体・テストを配置する
- 複数画面で再利用するUIパーツは `src/components/` に機能ドメイン別（`book/`, `layout/`, `common/`）に配置する
- API呼び出しは `src/api/` に集約し、コンポーネントから直接 `fetch` を呼び出さない
- 型定義（DTO等）は `src/types/` に配置し、`api/` と `components/` から共有する
- コンポーネントのテストファイルは対象コンポーネントと同じディレクトリに `*.test.tsx` として配置する

## 4. docs/ ディレクトリ構成

```
docs/
├── product-requirements.md
├── functional-design.md
├── architecture.md
├── repository-structure.md
├── development-guidelines.md
└── glossary.md
```

## 5. .steering/ ディレクトリ構成

```
.steering/
└── [YYYYMMDD]-[開発タイトル]/
    ├── requirements.md
    ├── design.md
    └── tasklist.md
```

- 命名規則・運用ルールは `CLAUDE.md` を参照する
