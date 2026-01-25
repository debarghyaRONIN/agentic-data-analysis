import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function ChatChart({
  data = [],
  dataKey,
  title,
  yDomain
}) {
  if (!Array.isArray(data) || data.length === 0) return null;

  const chartData = data.map((value, index) => ({
    index,
    [dataKey]: value
  }));

  return (
    <div style={{ width: "100%", height: 260, marginBottom: 20 }}>
      <strong style={{ display: "block", marginBottom: 8 }}>
        {title}
      </strong>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          {/* Cleaner X-axis */}
          <XAxis
            dataKey="index"
            tick={false}
            axisLine={false}
          />

          {/*  Controlled Y-axis range */}
          <YAxis
            domain={yDomain}
            tick={{ fontSize: 12 }}
            axisLine={false}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey={dataKey}
            stroke="#6366f1"
            strokeWidth={2.5}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}