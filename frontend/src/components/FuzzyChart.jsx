import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function FuzzyChart({ title, x, ...memberships }) {

  if (!x) return null;

  // Convert to chart format
  const data = x.map((val, i) => {
    const point = { x: val };

    Object.keys(memberships).forEach(name => {
      point[name] = memberships[name][i];
    });

    return point;
  });

  const colors = [
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#6366f1",
    "#06b6d4"
  ];

  return (
    <div style={{ width: "100%", height: 260, marginBottom: 20 }}>
      <strong>{title}</strong>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="x" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />

          {Object.keys(memberships).map((name, i) => (
            <Line
              key={name}
              dataKey={name}
              stroke={colors[i % colors.length]}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
