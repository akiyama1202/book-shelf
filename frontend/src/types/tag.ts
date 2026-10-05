// backend: app/schemas/tag.py TagRead
export interface TagRead {
  id: number;
  name: string;
}

// backend: app/schemas/tag.py TagCreate (PUT も同スキーマを使用)
export interface TagCreate {
  name: string;
}
