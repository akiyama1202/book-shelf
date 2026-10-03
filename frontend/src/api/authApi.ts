import { apiClient } from "./client";
import type { LoginRequest, Token, UserCreate, UserRead } from "../types/user";

export async function register(data: UserCreate): Promise<UserRead> {
  return apiClient<UserRead>("/auth/register", { method: "POST", body: data });
}

export async function login(data: LoginRequest): Promise<Token> {
  return apiClient<Token>("/auth/login", { method: "POST", body: data });
}
