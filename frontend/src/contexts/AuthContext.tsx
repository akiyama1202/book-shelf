import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";
import { login as loginApi, register as registerApi } from "../api/authApi";
import { TOKEN_STORAGE_KEY } from "../api/client";
import type { LoginRequest, UserCreate } from "../types/user";

interface AuthContextValue {
  isAuthenticated: boolean;
  token: string | null;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: UserCreate) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem(TOKEN_STORAGE_KEY),
  );

  const isAuthenticated = token !== null;

  async function login(data: LoginRequest): Promise<void> {
    const result = await loginApi(data);
    localStorage.setItem(TOKEN_STORAGE_KEY, result.accessToken);
    setToken(result.accessToken);
  }

  async function register(data: UserCreate): Promise<void> {
    await registerApi(data);
    await login({ email: data.email, password: data.password });
  }

  function logout(): void {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
