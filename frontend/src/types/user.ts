// ユーザー登録リクエスト
// backend: app/schemas/user.py UserCreate
export interface UserCreate {
  email: string;
  password: string;
}

// ユーザー情報レスポンス
// backend: app/schemas/user.py UserRead
export interface UserRead {
  id: number;
  email: string;
  createdAt: string; // ISO 8601 datetime string
}

// ログインリクエスト
// backend: app/schemas/auth.py LoginRequest
export interface LoginRequest {
  email: string;
  password: string;
}

// JWTトークンレスポンス
// backend: app/schemas/auth.py Token
export interface Token {
  accessToken: string;
  tokenType: string;
}
