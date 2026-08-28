import { useEffect, useRef } from "react";
import type { Turn } from "../types";
import { formatClock, formatInterval } from "../lib/time";

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

export default function TurnList({ turns, selectedTurn, onSelect }: TurnListProps) {
  const itemRefs = useRef<Map<number, HTMLElement>>(new Map());

  // Keep the active turn in view as selection changes (e.g. via keyboard),
  // without stealing focus or scrolling on every render.
  useEffect(() => {
    if (selectedTurn === null) return;
    const el = itemRefs.current.get(selectedTurn);
    el?.scrollIntoView({ block: "nearest" });
  }, [selectedTurn]);

  if (turns.length === 0) {
    return (
      <section className="turns">
        <p className="status-message">No turns in this conversation.</p>
      </section>
    );
  }

  return (
    <section className="turns">
      {turns.map((turn) => {
        const isActive = turn.turn === selectedTurn;
        return (
          <article
            key={turn.turn}
            ref={(el) => {
              if (el) itemRefs.current.set(turn.turn, el);
              else itemRefs.current.delete(turn.turn);
            }}
            className={`turn-card${isActive ? " turn-card--active" : ""}`}
            role="button"
            tabIndex={0}
            aria-pressed={isActive}
            onClick={() => onSelect(turn.turn)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(turn.turn);
              }
            }}
          >
            <header className="turn-card-header">
              <span className="turn-card-number">Turn {turn.turn}</span>
              <span className="turn-card-speaker">{turn.participant_full_id}</span>
              <span className="turn-card-time">{formatClock(turn.timestamp)}</span>
            </header>

            <p className="turn-card-user">
              <span className="turn-card-label">User</span>
              {turn.user_text}
            </p>

            <p className="turn-card-strategy">
              <span className="turn-card-label">Strategy</span>
              {turn.strategy}
            </p>

            <p className="turn-card-ai">
              <span className="turn-card-label">AI</span>
              {turn.ai_text}
            </p>

            <p className="turn-card-physio">
              <span className="turn-card-label">Physio summary</span>
              {turn.physio_summary}
            </p>

            <footer className="turn-card-footer">
              {turn.interval && (
                <span className="turn-card-interval">
                  {formatInterval(turn.interval.start, turn.interval.end, turn.interval.minutes)}
                </span>
              )}
              {turn.stress_level && (
                <span className="turn-card-stress">
                  {turn.stress_level}
                  {turn.stress_score !== null ? ` (${turn.stress_score})` : ""}
                </span>
              )}
            </footer>
          </article>
        );
      })}
    </section>
  );
}
