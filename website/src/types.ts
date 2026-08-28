/**
 * The contract between the data pipeline and every UI component.
 *
 * scripts/build_data.py emits exactly these shapes into public/data/build/.
 * Change this file and the script together, never one alone.
 */

/**
 * One participant variant within a context - the original conversation, or a
 * rewritten "Modified" version of it. `id` matches the build/<id>.json
 * filename to fetch with loadContext.
 */
export interface ContextVariant {
  id: string;
  label: "Original" | "Modified";
  participant_id: string;
  turn_count: number;
  /** ISO timestamps bounding this variant's conversation. */
  start: string;
  end: string;
}

/**
 * One row of public/data/build/index.json - the context selection screen.
 * `context_id` is the base participant id ("11_1", "8", "22_1"); a context
 * with a modified rewrite carries both variants here rather than appearing
 * twice in the index.
 */
export interface ContextSummary {
  context_id: string;
  /** Scenario name from context_names.json. */
  name: string;
  variants: ContextVariant[];
}

export type SignalKind = "numeric" | "categorical";

export interface SignalMeta {
  key: SignalKey;
  label: string;
  /** "uS", "bpm", "degC", "g", "counts" - render on the Y axis. */
  unit: string;
  kind: SignalKind;
}

export type SignalKey =
  | "EDA"
  | "PR"
  | "SkinTemp"
  | "ACCEL"
  | "ACT_COUNT"
  | "ACT_CLASS";

/** A single plotted sample. `v` is null where the source held NaN. */
export interface Point {
  t: string;
  v: number | string | null;
}

/**
 * The window a turn's physiological summary describes, and what gets
 * highlighted on all five graphs.
 *
 * `source` records how it was derived: "summary" means the minutes were read
 * out of the summary text, "csv_row" means the summary had no readable
 * interval and the turn's own CSV row window was used instead.
 */
export interface Interval {
  start: string;
  end: string;
  minutes: number;
  source: "summary" | "csv_row";
}

export interface Turn {
  /** 1-based, matches the "Turn N" label in the UI. */
  turn: number;
  timestamp: string;
  participant_full_id: string;
  user_text: string;
  ai_text: string;
  strategy: string;
  physio_summary: string;
  stress_score: number | null;
  stress_level: string | null;
  interval: Interval | null;
}

export interface ContextData {
  /**
   * The five signals to chart: EDA, PR, SkinTemp, ACCEL, ACT_COUNT. Render one
   * graph per entry rather than hard-coding the list.
   */
  signals: SignalMeta[];
  /** [start, end] ISO timestamps - the shared X domain for all five charts. */
  domain: [string, string];
  /**
   * Keyed by signal. Also carries ACT_CLASS, which is categorical and is NOT
   * one of the five graphs - available for annotating a turn if wanted.
   */
  series: Record<SignalKey, Point[]>;
  turns: Turn[];
  /**
   * [turn, statedMinutes, expectedMinutes] where the summary's look-back does
   * not follow the 1, 2, 3 ... 6 scheme. Diagnostic only; the UI still uses
   * whatever the summary said.
   */
  interval_mismatches: [number, number, number][];
}
