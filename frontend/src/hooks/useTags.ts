import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createTag, deleteTag, getTags, updateTag } from "../api/tagsApi";
import type { TagCreate } from "../types/tag";

const TAGS_KEY = "tags";

export function useTagList() {
  return useQuery({
    queryKey: [TAGS_KEY],
    queryFn: getTags,
  });
}

export function useCreateTag() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TagCreate) => createTag(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TAGS_KEY] });
    },
  });
}

export function useUpdateTag() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TagCreate }) => updateTag(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TAGS_KEY] });
    },
  });
}

export function useDeleteTag() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteTag(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TAGS_KEY] });
    },
  });
}
