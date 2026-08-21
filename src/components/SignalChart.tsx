import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceArea,
} from "recharts";
import type { Interval, Point, SignalMeta } from "../types";
import { toMs, formatClock } from "../lib/time";

/** Small readings (0.006 g) need decimals that a pulse rate (101 bpm) does not. */
function formatValue(value: number): string {
  const magnitude = Math.abs(value);
  if (magnitude === 0) return "0";
  if (magnitude < 0.1) return value.toFixed(3);
  if (magnitude < 10) return value.toFixed(2);
  return value.toFixed(0);
}

export interface SignalChartProps {
  meta: SignalMeta;
  points: Point[];
  domain: [string, string];
  interval: Interval | null;
}

export default function SignalChart({ meta, points, domain, interval }: SignalChartProps) {
  // Convert ISO string timestamps to milliseconds (numbers) for Recharts
  const chartData = points.map((p) => ({
    t: toMs(p.t),
    v: typeof p.v === "number" ? p.v : null, // null stays null, NOT zero
  }));

  const xMin = toMs(domain[0]);
  const xMax = toMs(domain[1]);

  // A few participants have a channel that was never recorded - say so rather
  // than drawing an empty pair of axes.
  const hasData = chartData.some((d) => d.v !== null);

  return (
    <figure className="chart">
      <figcaption style={{ margin: "0 0 0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
        {meta.label} <span style={{ fontWeight: 400, color: "#5d6b73" }}>({meta.unit})</span>
      </figcaption>

      {!hasData ? (
        <p className="chart-empty">Not recorded for this conversation</p>
      ) : (
      <ResponsiveContainer width="100%" height={170}>
        <LineChart data={chartData} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#dfe4e7" />

          {/* X axis: shows time labels formatted as HH:MM */}
          <XAxis
            dataKey="t"
            type="number"
            scale="time"
            domain={[xMin, xMax]}
            tickFormatter={(ms: number) => formatClock(new Date(ms).toISOString())}
            tick={{ fontSize: 11 }}
            tickCount={6}
          />

          {/* Y axis: shows value + unit */}
          <YAxis
            tick={{ fontSize: 11 }}
            tickFormatter={formatValue}
            width={55}
            label={{ value: meta.unit, angle: -90, position: "insideLeft", fontSize: 11, fill: "#5d6b73" }}
          />

          {/* Hover tooltip: shows exact time and value */}
          <Tooltip
            labelFormatter={(ms: number) => formatClock(new Date(ms).toISOString())}
            formatter={(value) => [
              typeof value === "number" ? `${formatValue(value)} ${meta.unit}` : "not recorded",
              meta.label,
            ]}
          />

          {/* Translucent highlight band for selected turn's interval */}
          {interval && (
            <ReferenceArea
              x1={toMs(interval.start)}
              x2={toMs(interval.end)}
              fill="#0e6e75"
              fillOpacity={0.15}
              stroke="#0e6e75"
              strokeOpacity={0.4}
            />
          )}

          {/* The line: connectNulls={false} means null breaks the line (not zero) */}
          <Line
            type="monotone"
            dataKey="v"
            stroke="#0e6e75"
            strokeWidth={1.5}
            dot={{ r: 3, fill: "#0e6e75" }}  // dots needed for sparse data
            activeDot={{ r: 5 }}
            connectNulls={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
      )}
    </figure>
  );
}
