import { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
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
  // ✅ Hooks always first
  const [chartType, setChartType] = useState("line");

  if (!Array.isArray(data) || data.length === 0) return null;

  const chartData = data.map((value, index) => ({
    index,
    [dataKey]: value,
    avg: data.reduce((a, b) => a + b, 0) / data.length
  }));

  const commonAxes = (
    <>
      <XAxis dataKey="index" tick={false} axisLine={false} />
      <YAxis domain={yDomain} axisLine={false} />
      <Tooltip />
    </>
  );

  const renderChart = () => {
    switch (chartType) {
      case "bar":
        return (
          <BarChart data={chartData}>
            {commonAxes}
            <Bar
              dataKey={dataKey}
              fill="#6366f1"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        );

      case "area":
        return (
          <AreaChart data={chartData}>
            {commonAxes}
            <Area
              type="monotone"
              dataKey={dataKey}
              stroke="#6366f1"
              fill="#6366f1"
              fillOpacity={0.25}
            />
          </AreaChart>
        );

      case "scatter":
        return (
          <ScatterChart>
            {commonAxes}
            <Scatter
              data={chartData}
              fill="#6366f1"
              line
              shape="circle"
            />
          </ScatterChart>
        );

      case "step":
        return (
          <LineChart data={chartData}>
            {commonAxes}
            <Line
              type="stepAfter"
              dataKey={dataKey}
              stroke="#6366f1"
              strokeWidth={2.5}
              dot={false}
            />
          </LineChart>
        );

      case "multi":
        return (
          <LineChart data={chartData}>
            {commonAxes}
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke="#6366f1"
              strokeWidth={2.5}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="avg"
              stroke="#22c55e"
              strokeDasharray="6 4"
              dot={false}
            />
          </LineChart>
        );

      default:
        return (
          <LineChart data={chartData}>
            {commonAxes}
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke="#6366f1"
              strokeWidth={2.5}
              dot={false}
            />
          </LineChart>
        );
    }
  };

  return (
    <div style={{
width: "100%",
height: 320,
minHeight: 320,
marginBottom: 24
}}>
      {/* Title + Dropdown */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 8
        }}
      >
        <strong>{title}</strong>

        <select
          value={chartType}
          onChange={(e) => setChartType(e.target.value)}
          style={{
            padding: "4px 8px",
            borderRadius: 6,
            border: "1px solid #444",
            background: "#0f172a",
            color: "#fff",
            fontSize: 12
          }}
        >
          <option value="line">Line</option>
          <option value="bar">Bar</option>
          <option value="area">Area</option>
          {/*<option value="scatter">Scatter</option>*/}
          <option value="step">Step</option>
          <option value="multi">Trend + Avg</option>
        </select>
      </div>

      <ResponsiveContainer width="100%" height="100%">
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
}