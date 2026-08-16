import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { loadContextSummary } from "../lib/data";
import type { ContextSummary } from "../types";

/**
 * Screen 2: the participant(s) inside one context. Each context currently
 * holds exactly one participant, but the screen is built to list more if a
 * context ever gets multiple.
 *
 * OWNER: task B.
 * Done when: the single participant renders as a card from the context's
 * index entry and clicking it routes to
 * /context/:contextId/participant/:participantId.
 */
export default function ParticipantList() {
  const { contextId } = useParams<{ contextId: string }>();
  const [summary, setSummary] = useState<ContextSummary | null | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!contextId) return;
    let cancelled = false;
    setSummary(undefined);
    setError(null);
    loadContextSummary(contextId)
      .then((found) => {
        if (!cancelled) setSummary(found ?? null);
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Could not load this context");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [contextId]);

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

  if (summary === undefined) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message">Loading…</p>
      </main>
    );
  }

  if (summary === null) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message status-message--error">
          No context found for "{contextId}".
        </p>
      </main>
    );
  }

  return (
    <main className="page">
      <Link to="/" className="back-link">
        ← Context
      </Link>
      <h1 className="page-title">{summary.name || summary.participant_id}</h1>
      <div className="card-grid">
        <article
          className="context-card"
          role="button"
          tabIndex={0}
          onClick={() => navigate(`/context/${summary.context_id}/participant/${summary.participant_id}`)}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              navigate(`/context/${summary.context_id}/participant/${summary.participant_id}`);
            }
          }}
        >
          <span className="context-card-name">{summary.participant_id}</span>
        </article>
      </div>
    </main>
  );
}
