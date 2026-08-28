import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { loadContext } from "../lib/data";
import TurnList from "../components/TurnList";
import SignalChart from "../components/SignalChart";
import type { ContextData } from "../types";

/**
 * Screen 3: conversation on the left, five graphs on the right.
 *
 * Owns the one piece of shared state - which turn is selected - and passes the
 * selected turn's interval down to every chart so all five highlight the same
 * range.
 *
 * OWNER: task D (shell, state, layout). Charts come from task C, the turn list
 * from task D, data loading from task B.
 */
export default function ConversationView() {
  const { contextId, participantId } = useParams<{
    contextId: string;
    participantId: string;
  }>();

  const [data, setData] = useState<ContextData | null | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [selectedTurn, setSelectedTurn] = useState<number | null>(null);

  // The route names which variant to show - "8" or "8-modified". Loading the
  // context id instead would always render the original, so a context with both
  // variants showed the same conversation for either card.
  const variantId = participantId ?? contextId;

  useEffect(() => {
    if (!variantId) return;
    let cancelled = false;
    setData(undefined);
    setError(null);
    setSelectedTurn(null);
    loadContext(variantId)
      .then((ctx) => {
        if (cancelled) return;
        setData(ctx);
        setSelectedTurn(ctx.turns.length > 0 ? ctx.turns[0].turn : null);
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Could not load this conversation");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [variantId]);

  const selectedInterval = useMemo(() => {
    if (!data || selectedTurn === null) return null;
    return data.turns.find((t) => t.turn === selectedTurn)?.interval ?? null;
  }, [data, selectedTurn]);

  if (error) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message status-message--error">{error}</p>
      </main>
    );
  }

  if (data === undefined) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message">Loading conversation…</p>
      </main>
    );
  }

  if (data === null) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message status-message--error">
          No conversation found for "{contextId}".
        </p>
      </main>
    );
  }

  return (
    <main className="layout">
      <section className="conversation-panel">
        <header className="conversation-panel-header">
          <Link to={`/context/${contextId}`} className="back-link">
            ← Context
          </Link>
          <h1 className="conversation-title">
            {data.turns[0]?.participant_full_id || contextId}
            {participantId?.endsWith("-modified") && " (Modified)"}
          </h1>
          <p className="conversation-subtitle">{data.turns.length} turns</p>
        </header>
        <TurnList
          turns={data.turns}
          selectedTurn={selectedTurn}
          onSelect={setSelectedTurn}
        />
      </section>

      <section className="charts-panel">
        {data.signals.map((meta) => (
          <SignalChart
            key={meta.key}
            meta={meta}
            points={data.series[meta.key]}
            domain={data.domain}
            interval={selectedInterval}
          />
        ))}
      </section>
    </main>
  );
}
