const BASE_URL = "/api";
export const TOKEN_STORAGE_KEY = "accessToken";

// バックエンドAPIはsnake_caseでJSONを返すため、フロントエンドのcamelCase型定義に合わせて変換する
function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, char: string) => char.toUpperCase());
}

function convertKeysToCamelCase(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(convertKeysToCamelCase);
  }

  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([key, val]) => [
        snakeToCamel(key),
        convertKeysToCamelCase(val),
      ]),
    );
  }

  return value;
}

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
}

// <T> = ジェネリクス型。型を呼び出し時に指定できる。
// Promise<T> = 非同期処理の結果として返す型。
export async function apiClient<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {

  // 分割代入。methodが空の場合は"GET"を代入する。
  const { method = "GET", body } = options;

  // Record<Keyの型, Valueの型>
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  // ローカルストレージからJWTトークンを取得し、Authorizationヘッダーに追加する
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const fetchOptions: RequestInit = {
    method,
    headers,
  };

  if (body !== undefined) {
    fetchOptions.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${path}`, fetchOptions);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API error: ${response.status} ${response.statusText} - ${errorText}`,
    );
  }

  const json: unknown = await response.json();
  return convertKeysToCamelCase(json) as T;
}
