import { apiClient } from "./client";
import type { BookCreate, BookListParams, BookListResponse, BookRead, BookUpdate } from "../types/book";

export async function getBooks(params: BookListParams = {}): Promise<BookListResponse> {
  const query = new URLSearchParams();
  if (params.search) query.set("search", params.search);
  if (params.sortBy) query.set("sort_by", params.sortBy);
  if (params.sortOrder) query.set("sort_order", params.sortOrder);
  if (params.page != null) query.set("page", String(params.page));
  if (params.pageSize != null) query.set("page_size", String(params.pageSize));

  const qs = query.toString();
  return apiClient<BookListResponse>(`/books${qs ? `?${qs}` : ""}`);
}

export async function getBook(id: number): Promise<BookRead> {
  return apiClient<BookRead>(`/books/${id}`);
}

export async function createBook(data: BookCreate): Promise<BookRead> {
  return apiClient<BookRead>("/books", { method: "POST", body: data });
}

export async function updateBook(id: number, data: BookUpdate): Promise<BookRead> {
  return apiClient<BookRead>(`/books/${id}`, { method: "PUT", body: data });
}

export async function deleteBook(id: number): Promise<void> {
  return apiClient<void>(`/books/${id}`, { method: "DELETE" });
}
