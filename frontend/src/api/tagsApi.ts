import { apiClient } from "./client";
import type { TagCreate, TagRead } from "../types/tag";

export async function getTags(): Promise<TagRead[]> {
  return apiClient<TagRead[]>("/tags");
}

export async function createTag(data: TagCreate): Promise<TagRead> {
  return apiClient<TagRead>("/tags", { method: "POST", body: data });
}

export async function updateTag(id: number, data: TagCreate): Promise<TagRead> {
  return apiClient<TagRead>(`/tags/${id}`, { method: "PUT", body: data });
}

export async function deleteTag(id: number): Promise<void> {
  return apiClient<void>(`/tags/${id}`, { method: "DELETE" });
}
