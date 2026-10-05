import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createBook, deleteBook, getBook, getBooks, updateBook } from "../api/booksApi";
import type { BookCreate, BookListParams, BookUpdate } from "../types/book";

const BOOKS_KEY = "books";

export function useBookList(params: BookListParams = {}) {
  return useQuery({
    queryKey: [BOOKS_KEY, params],
    queryFn: () => getBooks(params),
  });
}

export function useBook(id: number) {
  return useQuery({
    queryKey: [BOOKS_KEY, id],
    queryFn: () => getBook(id),
  });
}

export function useCreateBook() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BookCreate) => createBook(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BOOKS_KEY] });
    },
  });
}

export function useUpdateBook(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BookUpdate) => updateBook(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BOOKS_KEY] });
    },
  });
}

export function useDeleteBook() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteBook(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BOOKS_KEY] });
    },
  });
}
