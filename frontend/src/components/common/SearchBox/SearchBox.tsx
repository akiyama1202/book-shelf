interface Props {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function SearchBox({ value, onChange, placeholder = "検索..." }: Props) {
  return (
    <input
      type="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
    />
  );
}
