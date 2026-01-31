type Column<T> = {
  key: keyof T;
  label: string;
  align?: "left" | "right";
  color?: (value: any) => string;
};

type Props<T> = {
  data: T[];
  columns: Column<T>[];
};

export default function DataTable<T extends Record<string, any>>({
  data,
  columns
}: Props<T>) {
  return (
    <div className="bg-slate-900 rounded-lg overflow-hidden border border-slate-800">
      <table className="w-full text-sm">
        <thead className="bg-slate-800 text-slate-300">
          <tr>
            {columns.map(col => (
              <th
                key={String(col.key)}
                className={`px-4 py-2 text-${col.align ?? "left"}`}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr
              key={i}
              className="border-t border-slate-800 hover:bg-slate-800/50"
            >
              {columns.map(col => {
                const value = row[col.key];
                const color = col.color ? col.color(value) : "text-white";

                return (
                  <td
                    key={String(col.key)}
                    className={`px-4 py-2 ${color} text-${col.align ?? "left"}`}
                  >
                    {typeof value === "number"
                      ? value.toFixed(3)
                      : value}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
