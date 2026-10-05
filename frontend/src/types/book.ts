import type { TagRead } from "./tag";

// backend: app/models/book.py BookStatus
export type BookStatus = "want_to_read" | "unread" | "reading" | "finished";

// backend: app/schemas/book.py BookCreate / BookUpdate
export interface BookCreate {
  title: string;
  author: string;
  status: BookStatus;
  rating: number | null;
  memo: string | null;
  tags: string[];
}

export type BookUpdate = BookCreate;

// backend: app/schemas/book.py BookRead
export interface BookRead {
  id: number;
  title: string;
  author: string;
  status: BookStatus;
  rating: number | null;
  memo: string | null;
  tags: TagRead[];
  createdAt: string;
  updatedAt: string;
}

// backend: app/schemas/book.py BookListResponse
export interface BookListResponse {
  items: BookRead[];
  total: number;
  page: number;
  pageSize: number;
}

export type SortBy = "title" | "author" | "created_at" | "rating";
export type SortOrder = "asc" | "desc";

export interface BookListParams {
  search?: string;
  sortBy?: SortBy;
  sortOrder?: SortOrder;
  page?: number;
  pageSize?: number;
}
