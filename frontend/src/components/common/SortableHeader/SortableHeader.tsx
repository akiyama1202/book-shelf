import type { SortOrder } from "../../../types/book";

interface Props {
  label: string;
  sortKey: string;
  currentSortBy: string;
  currentSortOrder: SortOrder;
  onSort: (key: string) => void;
}

export function SortableHeader({
  label,
  sortKey,
  currentSortBy,
  currentSortOrder,
  onSort,
}: Props) {
  const isActive = currentSortBy === sortKey;
  const arrow = isActive ? (currentSortOrder === "asc" ? " ↑" : " ↓") : "";

  return (
    <button
      type="button"
      onClick={() => onSort(sortKey)}
      className={`flex items-center gap-1 text-left text-sm font-medium ${
        isActive ? "text-blue-600" : "text-gray-700 hover:text-gray-900"
      }`}
    >
      {label}
      <span className="w-3 text-xs">{arrow}</span>
    </button>
  );
}
