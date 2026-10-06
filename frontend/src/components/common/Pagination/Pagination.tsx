interface Props {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ page, pageSize, total, onPageChange }: Props) {
  const totalPages = Math.ceil(total / pageSize);

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between text-sm text-gray-600">
      <span>
        {(page - 1) * pageSize + 1}–{Math.min(page * pageSize, total)} 件 / 全 {total} 件
      </span>
      <div className="flex gap-1">
        <button
          type="button"
          onClick={() => onPageChange(page - 1)}
          disabled={page === 1}
          className="rounded px-3 py-1 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
        >
          前へ
        </button>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
          <button
            key={p}
            type="button"
            onClick={() => onPageChange(p)}
            className={`rounded px-3 py-1 ${
              p === page
                ? "bg-blue-600 text-white"
                : "hover:bg-gray-100"
            }`}
          >
            {p}
          </button>
        ))}
        <button
          type="button"
          onClick={() => onPageChange(page + 1)}
          disabled={page === totalPages}
          className="rounded px-3 py-1 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
        >
          次へ
        </button>
      </div>
    </div>
  );
}
