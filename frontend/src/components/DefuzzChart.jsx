import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend
} from "recharts";

export default function DefuzzChart({
  title,
  x,
  low,
  medium,
  high,
  crispValue
}) {
  if (
    !Array.isArray(x) ||
    !Array.isArray(low) ||
    !Array.isArray(medium) ||
    !Array.isArray(high) ||
    typeof crispValue !== "number"
  ) {
    return null;
  }

  const data = x.map((val, i) => ({
    x: val,
    low: low[i],
    medium: medium[i],
    high: high[i]
  }));

  return (
    <div
  style={{
    width: "100%",
    height: 300,
    minHeight: 300,
    marginBottom: 24
  }}
>
      <strong style={{ display: "block", marginBottom: 8 }}>
        {title}
      </strong>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
  <XAxis
    dataKey="x"
    type="number"
    domain={[0, 300]}
    tick={{ fontSize: 11 }}
  />
  <YAxis domain={[0, 1]} />
  <Tooltip />
  <Legend />

  <Line dataKey="low" stroke="#22c55e" dot={false} />
  <Line dataKey="medium" stroke="#f59e0b" dot={false} />
  <Line dataKey="high" stroke="#ef4444" dot={false} />

  {/* DEFUZZIFIED CENTROID LINE */}
  <ReferenceLine
    x={crispValue}
    stroke="#3b82f6"
    strokeWidth={2}
    strokeDasharray="6 4"
    isFront
    label={{
      value: `Defuzzified = ${crispValue.toFixed(2)}`,
      position: "top",
      fill: "#3b82f6",
      fontSize: 12
    }}
  />
</LineChart>
      </ResponsiveContainer>
    </div>
  );
}