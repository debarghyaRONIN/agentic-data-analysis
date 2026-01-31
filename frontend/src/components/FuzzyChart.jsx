import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function FuzzyChart({ title, x, low, medium, high }) {
  if (!x || !low || !medium || !high) return null;

  const data = x.map((val, i) => ({
    x: val,
    low: low[i],
    medium: medium[i],
    high: high[i]
  }));

  return (
    <div style={{
width: "100%",
height: 300,
minHeight: 300,
marginBottom: 24
}}>
      <strong style={{ display: "block", marginBottom: 8 }}>
        {title}
      </strong>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="x" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />

          <Line
            type="monotone"
            dataKey="low"
            stroke="#22c55e"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="medium"
            stroke="#f59e0b"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="high"
            stroke="#ef4444"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}