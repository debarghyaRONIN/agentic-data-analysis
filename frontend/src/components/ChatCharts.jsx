import ChatChart from "./ChatChart";

export default function ChatCharts({ data }) {
  if (!data) return null;

  return (
    <div style={{ marginTop: 12 }}>
      <ChatChart
        data={data.orderFlowTrend}
        dataKey="order_flow"
        title="📈 Order Flow Trend"
      />

      <ChatChart
        data={data.rollingMean}
        dataKey="rolling_mean"
        title="📊 Rolling Demand Average"
      />

     <ChatChart
  title="Customer Rating Trend"
  data={data.ratingTrend}
  dataKey="rating"
  yDomain={[3.5, 5]}
/>

<ChatChart
  title="Rating Volatility"
  data={data.volatilityTrend}
  dataKey="volatility"
  yDomain={[0, "auto"]}
/>
    </div>
  );
}