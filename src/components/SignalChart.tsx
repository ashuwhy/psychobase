import type { Interval, Point, SignalMeta } from "../types";

/**
 * One signal, plotted across the whole conversation, with the selected turn's
 * interval shaded.
 *
 * All five charts receive the same `domain` and the same `interval`, which is
 * what keeps them aligned and highlighting identically. Use a Recharts
 * ReferenceArea (or an SVG rect) for the band - translucent, full chart height.
 *
 * OWNER: task C.
 * Done when: axes carry timestamps and units, hover shows exact time and value,
 * nulls break the line rather than plotting as zero, and changing the selected
 * turn moves the band on every chart at once.
 */
export interface SignalChartProps {
  meta: SignalMeta;
  points: Point[];
  domain: [string, string];
  interval: Interval | null;
}

export default function SignalChart(_props: SignalChartProps) {
  return <figure className="chart">{/* TODO(task C) */}</figure>;
}
