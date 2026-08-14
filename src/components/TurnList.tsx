import type { Turn } from "../types";

/**
 * Left panel. Each turn shows turn number, speaker id, user message, AI
 * strategy, AI response and the physiological summary, per the brief.
 *
 * OWNER: task D.
 * Done when: the selected turn is visibly active, the panel scrolls
 * independently of the graphs, and clicking a turn calls onSelect.
 */
export interface TurnListProps {
  turns: Turn[];
  selectedTurn: number | null;
  onSelect: (turn: number) => void;
}

export default function TurnList(_props: TurnListProps) {
  return <section className="turns">{/* TODO(task D) */}</section>;
}
